#!/usr/bin/env python3
"""Tailscale setup helpers for the HashWatcher Gateway (Docker).

Provides functions to authenticate with a Tailscale auth key, enable subnet
routing, query connection status, and tear down the Tailscale session.

Inside the Docker container, tailscaled runs as root so no sudo is needed.
"""

import json
import os
import re
import subprocess
from typing import Any, Dict, List, Optional


def _run(cmd: List[str], timeout: int = 30) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        return subprocess.CompletedProcess(cmd, returncode=127, stdout="", stderr=f"{cmd[0]}: not found")


def is_installed() -> bool:
    result = _run(["which", "tailscale"])
    return result.returncode == 0


def _ensure_ip_forwarding() -> None:
    """Enable IPv4/IPv6 forwarding at runtime.

    Tries /usr/sbin/sysctl first (Debian slim), falls back to writing
    /proc directly. In Docker, forwarding is usually already set via
    sysctls in docker-compose.yml, so failures here are non-fatal.
    """
    sysctl = "/usr/sbin/sysctl" if os.path.exists("/usr/sbin/sysctl") else "sysctl"
    result = _run([sysctl, "-w", "net.ipv4.ip_forward=1"])
    if result.returncode != 0:
        try:
            with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
                f.write("1")
        except OSError:
            pass
    result = _run([sysctl, "-w", "net.ipv6.conf.all.forwarding=1"])
    if result.returncode != 0:
        try:
            with open("/proc/sys/net/ipv6/conf/all/forwarding", "w") as f:
                f.write("1")
        except OSError:
            pass


_VIRTUAL_IFACE_PREFIXES = (
    "docker", "br-", "veth", "virbr", "lxc", "flannel", "cni", "calico",
    "tailscale", "tun", "tap", "utun",
)


def _is_physical_iface(name: str) -> bool:
    return not name.startswith(_VIRTUAL_IFACE_PREFIXES) and name != "lo"


def _cidr_from_ip_line(line: str) -> Optional[str]:
    match = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+/\d+)", line)
    if not match:
        return None
    cidr = match.group(1)
    parts = cidr.split("/")
    ip_addr = parts[0]
    if _is_docker_internal_ip(ip_addr):
        return None
    prefix = int(parts[1])
    octets = ip_addr.split(".")
    if prefix <= 24:
        return f"{octets[0]}.{octets[1]}.{octets[2]}.0/24"
    return cidr


def _is_docker_internal_ip(ip: str) -> bool:
    """Return True if the IP belongs to a Docker/container-internal range."""
    if not ip:
        return True
    parts = ip.split(".")
    if len(parts) != 4:
        return True
    a, b = int(parts[0]), int(parts[1])
    if a == 127:
        return True
    if a == 172 and 16 <= b <= 31:
        return True
    if a == 10:
        return True
    return False


def _subnet_from_ip(ip: str) -> Optional[str]:
    """Derive a /24 subnet from a single IP address."""
    if not ip or _is_docker_internal_ip(ip):
        return None
    octets = ip.split(".")
    if len(octets) != 4:
        return None
    return f"{octets[0]}.{octets[1]}.{octets[2]}.0/24"


def _detect_host_lan_ip() -> Optional[str]:
    """Find the host's real LAN IP by reading the host's /proc/net/fib_trie.

    When running inside a Docker bridge container, the container's own
    interfaces only show Docker-internal IPs. If the host's /proc/net is
    mounted at /host_proc_net (read-only), we can parse fib_trie for
    LOCAL addresses that are on a real private LAN (192.168.x.x, etc.).
    """
    try:
        with open("/host_proc_net/fib_trie", "r") as f:
            content = f.read()
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("|-- "):
                ip = line[4:].strip()
                if not _is_docker_internal_ip(ip) and not ip.endswith(".0") and not ip.endswith(".255"):
                    return ip
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return None


def _detect_via_docker_gateway() -> Optional[str]:
    """Inside a Docker bridge container, the default gateway is the host.

    Read the gateway IP from /proc/net/route, then derive the host's real
    LAN subnet from it (the gateway is typically the host's LAN IP).
    """
    try:
        with open("/proc/net/route", "r") as f:
            for line in f:
                fields = line.strip().split()
                if len(fields) < 3 or fields[1] != "00000000":
                    continue
                gw_hex = fields[2]
                gw_bytes = bytes.fromhex(gw_hex)
                gw_ip = f"{gw_bytes[3]}.{gw_bytes[2]}.{gw_bytes[1]}.{gw_bytes[0]}"
                return _subnet_from_ip(gw_ip)
    except Exception:
        pass
    return None


def detect_subnet(interface: str = "eth0") -> Optional[str]:
    """Auto-detect the local subnet CIDR, skipping Docker/virtual interfaces.

    Strategy:
    1. HOST_IP env var (set by Umbrel via DEVICE_HOST in docker-compose)
    2. Try well-known physical interface names (works with --network=host)
    3. Enumerate all interfaces, pick the first physical one with a private IP
    4. Docker gateway detection (works inside bridge-networked containers)
    5. Fall back to a UDP-socket heuristic
    """
    host_ip = os.getenv("HOST_IP", "").strip()
    if host_ip:
        cidr = _subnet_from_ip(host_ip)
        if cidr:
            return cidr

    for iface in [interface, "wlan0", "end0", "enp0s3", "enp0s25", "eno1"]:
        result = _run(["ip", "-4", "-o", "addr", "show", iface])
        if result.returncode == 0 and result.stdout.strip():
            cidr = _cidr_from_ip_line(result.stdout)
            if cidr:
                return cidr

    result = _run(["ip", "-4", "-o", "addr", "show"])
    if result.returncode == 0 and result.stdout.strip():
        for line in result.stdout.strip().splitlines():
            parts = line.split()
            if len(parts) < 2:
                continue
            iface_name = parts[1]
            if _is_physical_iface(iface_name):
                cidr = _cidr_from_ip_line(line)
                if cidr:
                    return cidr

    host_lan_ip = _detect_host_lan_ip()
    if host_lan_ip:
        cidr = _subnet_from_ip(host_lan_ip)
        if cidr:
            return cidr

    gw_subnet = _detect_via_docker_gateway()
    if gw_subnet:
        return gw_subnet

    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        cidr = _subnet_from_ip(ip)
        if cidr:
            return cidr
    except Exception:
        pass
    return None


def setup(auth_key: str, subnet_cidr: Optional[str] = None) -> Dict[str, Any]:
    """Authenticate Tailscale and enable subnet routing.

    Args:
        auth_key: A Tailscale auth key (tskey-auth-...).
        subnet_cidr: Optional subnet to advertise. Auto-detected if omitted.

    Returns:
        Dict with ok, ip, hostname, advertisedRoutes, and any error.
    """
    if not is_installed():
        return {"ok": False, "error": "tailscale is not installed"}

    auth_key = auth_key.strip()
    if not auth_key:
        return {"ok": False, "error": "authKey is required"}
    if not auth_key.startswith("tskey-"):
        return {"ok": False, "error": "authKey must start with 'tskey-'"}

    _ensure_ip_forwarding()

    resolved_cidr = (subnet_cidr or "").strip() or detect_subnet()
    if not resolved_cidr:
        return {"ok": False, "error": "Could not detect local subnet. Enter your LAN subnet in the \"Subnet (optional)\" field (e.g. 192.168.1.0/24 or 10.51.127.0/24) and try again."}

    ts_hostname = os.getenv("PI_HOSTNAME", "HashWatcherGateway")

    cmd = [
        "tailscale", "up",
        f"--authkey={auth_key}",
        f"--advertise-routes={resolved_cidr}",
        f"--hostname={ts_hostname}",
        "--accept-routes",
        "--reset",
    ]

    import threading
    proc_result: Dict[str, Any] = {}

    def _run_tailscale():
        r = _run(cmd, timeout=120)
        proc_result["returncode"] = r.returncode
        proc_result["stderr"] = r.stderr
        proc_result["stdout"] = r.stdout

    thread = threading.Thread(target=_run_tailscale, daemon=True)
    thread.start()
    thread.join(timeout=10)

    if not thread.is_alive() and proc_result.get("returncode", 0) != 0:
        stderr = (proc_result.get("stderr") or proc_result.get("stdout") or "").strip()
        return {"ok": False, "error": f"tailscale up failed: {stderr}"}

    import time
    for i in range(15):
        time.sleep(2 if i < 5 else 3)
        s = status()
        if s.get("authenticated") and s.get("ip"):
            return {"ok": True, "advertisedRoutes": [resolved_cidr], "ip": s["ip"], "hostname": s.get("hostname")}

    s = status()
    return {
        "ok": True,
        "advertisedRoutes": [resolved_cidr],
        "ip": s.get("ip"),
        "hostname": s.get("hostname") or ts_hostname,
        "note": "Tailscale connected but IP may still be propagating. The page will reload shortly.",
    }


def status() -> Dict[str, Any]:
    """Return current Tailscale connection status including key expiry."""
    from datetime import datetime, timezone

    info: Dict[str, Any] = {
        "installed": is_installed(),
        "running": False,
        "authenticated": False,
        "ip": None,
        "hostname": None,
        "advertisedRoutes": [],
        "online": False,
        "keyExpiry": None,
        "keyExpired": False,
        "keyExpiringSoon": False,
    }

    if not info["installed"]:
        return info

    result = _run(["tailscale", "status", "--json"])
    if result.returncode != 0:
        return info

    try:
        data = json.loads(result.stdout)
    except (json.JSONDecodeError, ValueError):
        return info

    backend_state = data.get("BackendState", "")
    info["running"] = backend_state != "Stopped"
    info["authenticated"] = backend_state == "Running"
    info["online"] = backend_state == "Running"

    self_node = data.get("Self", {})
    tailscale_ips = self_node.get("TailscaleIPs", [])
    if tailscale_ips:
        info["ip"] = tailscale_ips[0]
    info["hostname"] = self_node.get("HostName")

    key_expiry_raw = self_node.get("KeyExpiry")
    if key_expiry_raw:
        info["keyExpiry"] = key_expiry_raw
        try:
            expiry_str = key_expiry_raw.replace("Z", "+00:00")
            expiry_dt = datetime.fromisoformat(expiry_str)
            now = datetime.now(timezone.utc)
            info["keyExpired"] = expiry_dt <= now
            seven_days = 7 * 24 * 3600
            info["keyExpiringSoon"] = (not info["keyExpired"]
                                       and (expiry_dt - now).total_seconds() < seven_days)
        except (ValueError, TypeError):
            pass

    prefs = _get_prefs()
    if prefs:
        info["advertisedRoutes"] = prefs.get("AdvertiseRoutes", []) or []

    allowed_ips = self_node.get("AllowedIPs", [])
    advertised = info["advertisedRoutes"]
    if advertised and info["authenticated"]:
        approved = [r for r in advertised if r in allowed_ips]
        info["routesApproved"] = len(approved) == len(advertised)
        info["routesPending"] = len(approved) < len(advertised)
    else:
        info["routesApproved"] = False
        info["routesPending"] = False

    return info


def down() -> Dict[str, Any]:
    """Turn Tailscale off (stays authenticated; can turn back on without re-auth)."""
    if not is_installed():
        return {"ok": False, "error": "tailscale is not installed"}
    r = _run(["tailscale", "down"], timeout=15)
    if r.returncode != 0:
        stderr = (r.stderr or r.stdout or "").strip()
        if "not connected" in stderr.lower() or "not running" in stderr.lower():
            return {"ok": True, "note": "Already off"}
        return {"ok": False, "error": stderr or "tailscale down failed"}
    return {"ok": True, "note": "Tailscale turned off. You can turn it back on anytime."}


def up() -> Dict[str, Any]:
    """Turn Tailscale back on using existing auth (no auth key needed).

    Always re-detects the local subnet so that stale Docker-bridge routes
    (e.g. 172.17.0.0/24) are replaced with the real LAN subnet.
    """
    if not is_installed():
        return {"ok": False, "error": "tailscale is not installed"}
    ts_hostname = os.getenv("PI_HOSTNAME", "HashWatcherGateway")

    fresh_subnet = detect_subnet()
    if fresh_subnet:
        routes_str = fresh_subnet
    else:
        prefs = _get_prefs()
        routes = prefs.get("AdvertiseRoutes", []) or []
        routes_str = ",".join(routes) if routes else ""

    _ensure_ip_forwarding()
    cmd = ["tailscale", "up", f"--hostname={ts_hostname}", "--accept-routes"]
    if routes_str:
        cmd.append(f"--advertise-routes={routes_str}")
    r = _run(cmd, timeout=60)
    if r.returncode != 0:
        stderr = (r.stderr or r.stdout or "").strip()
        return {"ok": False, "error": stderr or "tailscale up failed"}
    s = status()
    return {"ok": True, "ip": s.get("ip"), "hostname": s.get("hostname"), "advertisedRoutes": [routes_str] if routes_str else []}


def logout() -> Dict[str, Any]:
    """Disconnect and deauthorize Tailscale on this gateway (requires re-auth to turn back on)."""
    if not is_installed():
        return {"ok": False, "error": "tailscale is not installed"}

    _run(["tailscale", "down"])
    result = _run(["tailscale", "logout"], timeout=15)
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        if "not logged in" not in stderr.lower():
            return {"ok": False, "error": f"tailscale logout failed: {stderr}"}

    return {"ok": True}


def _status_fields() -> Dict[str, Any]:
    """Extract ip and hostname from tailscale status --json."""
    result = _run(["tailscale", "status", "--json"])
    if result.returncode != 0:
        return {}
    try:
        data = json.loads(result.stdout)
    except (json.JSONDecodeError, ValueError):
        return {}

    self_node = data.get("Self", {})
    tailscale_ips = self_node.get("TailscaleIPs", [])
    return {
        "ip": tailscale_ips[0] if tailscale_ips else None,
        "hostname": self_node.get("HostName"),
    }


def _get_prefs() -> Optional[Dict[str, Any]]:
    """Read tailscale debug prefs for advertised routes."""
    result = _run(["tailscale", "debug", "prefs"])
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except (json.JSONDecodeError, ValueError):
        return None
