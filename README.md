# HashWatcher Gateway for Umbrel

<p align="center">
  <img src="hashwatcher-gateway/icon.png" alt="HashWatcher Gateway" width="128">
</p>

<p align="center">
  <strong>Monitor your ASIC mining rigs from anywhere in the world.</strong><br>
  Built-in Tailscale. No port forwarding. No dynamic DNS.
</p>

<p align="center">
  <a href="https://www.HashWatcher.app">Download the App</a> &nbsp;·&nbsp;
  <a href="https://x.com/HashWatcher">Follow on X</a> &nbsp;·&nbsp;
  <a href="mailto:info@engineeredessentials.com?subject=Umbrel%20App%20Support">Support</a>
</p>

---

## What Is This?

HashWatcher Gateway turns your Umbrel into a secure remote bridge for monitoring ASIC mining rigs — BitAxe, Canaan, NerdQAxe, and more. It includes a built-in Tailscale VPN so you can access your miners (and your entire Umbrel) from anywhere without opening ports on your router.

Pair it with the free **HashWatcher app** for iOS, macOS, and Android to get real-time dashboards, alerts, and full control of your miners from your phone.

---

## Install
Watch this video first: https://www.twitch.tv/videos/2714786107?t=0h0m34s

Join our Discord https://discord.gg/Xu66PvpAm

1. Open your Umbrel dashboard
2. Go to **App Store** → **Community App Stores**
3. Add this repository:
   ```
   https://github.com/gpena208777/hashwatcherhub
   ```
4. Find **HashWatcher Gateway** and click **Install**
5. Click the app icon to open the gateway dashboard

---

## Setup (5 minutes)

After installing, the gateway dashboard walks you through everything:

Prefer a video how-to? Watch this 

 ```
https://www.twitch.tv/videos/2714786107?t=0h0m33s

   ```


### Step 1 — Download the HashWatcher App

Get the free companion app at [HashWatcher.app](https://www.HashWatcher.app). Available for iOS, macOS, and Android.

### Step 2 — Get a Tailscale Auth Key

Go to [login.tailscale.com/admin/settings/keys](https://login.tailscale.com/admin/settings/keys) and generate an auth key. If you don't have a Tailscale account, [sign up free](https://tailscale.com) first.

### Step 3 — Enter Your Auth Key

Paste the auth key into the gateway's setup page. The gateway connects to your Tailscale network automatically.

### Step 4 — Approve Subnet Routes

Go to the [Tailscale Machines page](https://login.tailscale.com/admin/machines), find **HashWatcherGateway**, click **…** → **Edit route settings**, and approve your local subnet (e.g. `192.168.1.0/24`).
  Troubleshooting: If Tailscale shows as connected but your miners or local devices are not reachable remotely, confirm that the subnet listed in the Umbrel app matches your router’s local gateway network. For example, if your router is 170.100.1.1, the subnet should typically be 170.100.1.0/24. If the subnet in the gateway configuration does not match your actual LAN range, remote access will not work even though Tailscale appears connected.

### Step 5 — Install Tailscale on Your Phone

Download [Tailscale](https://tailscale.com/download) on your phone and sign in with the same account. Your phone and the gateway are now on the same private network.

### Step 6 — Disable Key Expiry (Recommended)

On the [Tailscale Machines page](https://login.tailscale.com/admin/machines), find **HashWatcherGateway**, click **…**, and toggle **Disable key expiry**. This keeps the gateway connected permanently with no maintenance.

### Step 7 — Open HashWatcher 
That's all. There is no need to change or edit any of the devices IP address in your inventory. 

**Done.** Open the HashWatcher app and your miners are accessible from anywhere.

---

## Features

**Mining Monitoring**
- Automatic discovery of miners on your local network
- Real-time polling of hashrate, temperature, power, and efficiency
- Proxy requests to individual miners through the gateway
- Web dashboard with system stats (CPU, memory, disk, temperature)

**Built-in Tailscale**
- Tailscale runs inside the app — no separate Tailscale installation needed
- Completely isolated from any Tailscale you already have on your Umbrel
- Secure encrypted tunnel with no port forwarding or dynamic DNS
- Key expiry monitoring with alerts in the dashboard and the HashWatcher app

**Full Umbrel Remote Access**
- Since the gateway advertises your local subnet, you also get remote access to all your other Umbrel apps — Home Assistant, Immich, Bitcoin Node, and everything else on your dashboard

---

## Supported Miners

- **BitAxe** — all variants (Supra, Ultra, Gamma, Hex, etc.)
- **NerdQAxe / NerdAxe**
- **Canaan Avalon**
- Any miner with an HTTP API on your local network

---

## FAQ

<details>
<summary><strong>I already have Tailscale on my Umbrel. Will this conflict?</strong></summary>

No. The gateway runs its own isolated Tailscale instance inside the Docker container with a separate state file and network namespace. Your existing Tailscale is untouched. You'll see two devices in your Tailscale admin — your Umbrel and the HashWatcher Gateway.
</details>

<details>
<summary><strong>Do I need to open any ports on my router?</strong></summary>

No. Tailscale creates an encrypted peer-to-peer tunnel. No port forwarding or dynamic DNS needed.
</details>

<details>
<summary><strong>What happens if I uninstall and reinstall?</strong></summary>

You'll need to re-enter your Tailscale auth key and re-approve subnet routes. Miner pairing data is stored in a persistent volume and may be preserved depending on how Umbrel handles the uninstall.
</details>

<details>
<summary><strong>Can I access my other Umbrel apps remotely too?</strong></summary>

Yes. The gateway advertises your local subnet through Tailscale, giving you remote access to everything on your network.
</details>

<details>
<summary><strong>Is this free?</strong></summary>

The gateway app is free. The HashWatcher companion app is free to download with optional premium features. Tailscale is free for personal use (up to 100 devices).
</details>

---
# HashWatcher Gateway for Umbrel

Monitor your ASIC mining rigs (BitAxe, Canaan, and more) from anywhere in the world. The HashWatcher Gateway turns your Umbrel into a secure remote bridge with built-in Tailscale — no port forwarding, no dynamic DNS, no separate VPN setup.

Pair it with the free [HashWatcher app](https://www.HashWatcher.app) for iOS, macOS, and Android.

Follow us on [X/Twitter](https://x.com/HashWatcher).

---

## Install on Umbrel

### From the Community App Store

1. Open your Umbrel dashboard (usually `http://umbrel.local`)
2. Go to **App Store** and search for **HashWatcher Gateway**, or add the community store repo:
   ```
   https://github.com/gpena208777/hashwatcherhub
   ```
3. Click **Install**
4. Once installed, click the app icon to open the gateway dashboard

### First-Time Setup

After installing, the gateway dashboard walks you through everything:

1. **Download the HashWatcher app** at [HashWatcher.app](https://www.HashWatcher.app)
2. **Get a Tailscale auth key** from [login.tailscale.com/admin/settings/keys](https://login.tailscale.com/admin/settings/keys) (free account)
3. **Enter the auth key** in the gateway's setup page
4. **Approve subnet routes** in the [Tailscale Machines page](https://login.tailscale.com/admin/machines) — find `HashWatcherGateway`, click **...** > **Edit route settings**, and approve your local subnet
5. **Install Tailscale on your phone** from [tailscale.com/download](https://tailscale.com/download) and sign in with the same account
6. **Disable key expiry** (recommended) so the gateway stays connected permanently

That's it. Your miners are now accessible from anywhere through the HashWatcher app.

---

## What It Does

- **Miner polling** — periodically fetches hashrate, temperature, power, and efficiency from your local miners
- **Miner discovery** — scans your local subnet to find miners automatically
- **Web dashboard** — status page with Tailscale controls and guided setup at port 8787
- **REST API** — JSON API for the HashWatcher app on port 8787
- **Miner proxy** — proxies HTTP requests to individual miners through the gateway
- **Built-in Tailscale** — the gateway runs its own Tailscale instance inside the Docker container, completely isolated from any Tailscale you may already have on your Umbrel
- **Key expiry monitoring** — warns you in the dashboard (and via push notification in the app) when your Tailscale key is about to expire

---

## Frequently Asked Questions

### I already have Tailscale installed on my Umbrel. Will this conflict?

No. The gateway runs its own isolated Tailscale instance inside the Docker container with a separate state file, socket, and network namespace. Your existing Tailscale setup is completely untouched. You'll just see two devices in your Tailscale admin — your Umbrel and the HashWatcher Gateway.

### What miners are supported?

Any miner with an HTTP API, including:
- **BitAxe** (all variants: Supra, Ultra, Gamma, Hex, etc.)
- **NerdQAxe / NerdAxe**
- **Canaan Avalon** (via CGMiner TCP protocol)
- **Any miner** reachable via HTTP on your local network

### Do I need to open any ports on my router?

No. Tailscale creates an encrypted tunnel — no port forwarding or dynamic DNS needed.

### What happens if I uninstall and reinstall?

Your Tailscale state is stored in a persistent volume (`/data`). If you uninstall and reinstall, you'll need to re-enter your auth key and re-approve subnet routes in the Tailscale admin console.

### Can I access my other Umbrel apps remotely too?

Yes. Since the gateway advertises your local subnet through Tailscale, you get remote access to everything on your network — Umbrel dashboard, Home Assistant, Bitcoin Node, and any other local services.

---

## Inspecting the Source Code

We believe in transparency. The gateway runs as a Docker image; you can inspect exactly what's inside.

### Quick inspection (without running)

```bash
# Pull the image
docker pull hashwatcher/hashwatcher-gateway:latest

# List files in the container
docker run --rm hashwatcher/hashwatcher-gateway:latest ls -la /app

# View the main agent source
docker run --rm hashwatcher/hashwatcher-gateway:latest cat /app/hub_agent.py

# View Tailscale setup code
docker run --rm hashwatcher/hashwatcher-gateway:latest cat /app/tailscale_setup.py
```

### Copy source out for full review

```bash
# Create a temp container and copy the app directory
docker create --name hw-inspect hashwatcher/hashwatcher-gateway:latest
docker cp hw-inspect:/app ./hashwatcher-gateway-source
docker rm hw-inspect

# Browse ./hashwatcher-gateway-source — hub_agent.py, tailscale_setup.py, entrypoint.sh, etc.
```

### Inspect a running instance (Umbrel)

If the app is already running on your Umbrel:

```bash
# Find the container name (e.g. umbrel-app-store_hashwatcher-gateway_web_1)
docker ps | grep hashwatcher

# Exec into it and explore
docker exec -it <container_name> sh
# Then: ls /app, cat /app/hub_agent.py, etc.
```

The gateway is built on Tailscale for security — we don't rely on obscurity. You're welcome to audit the code.

---


---





## Links

- **HashWatcher App** — [HashWatcher.app](https://www.HashWatcher.app)
- **Follow on X** — [@HashWatcher](https://x.com/HashWatcher)
- **Support** — [info@engineeredessentials.com](mailto:info@engineeredessentials.com?subject=Umbrel%20App%20Support)
- **Developer** — [Engineered Essentials](https://hashwatcher.app)
