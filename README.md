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

### Step 1 — Download the HashWatcher App

Get the free companion app at [HashWatcher.app](https://www.HashWatcher.app). Available for iOS, macOS, and Android.

### Step 2 — Get a Tailscale Auth Key

Go to [login.tailscale.com/admin/settings/keys](https://login.tailscale.com/admin/settings/keys) and generate an auth key. If you don't have a Tailscale account, [sign up free](https://tailscale.com) first.

### Step 3 — Enter Your Auth Key

Paste the auth key into the gateway's setup page. The gateway connects to your Tailscale network automatically.

### Step 4 — Approve Subnet Routes

Go to the [Tailscale Machines page](https://login.tailscale.com/admin/machines), find **HashWatcherGateway**, click **…** → **Edit route settings**, and approve your local subnet (e.g. `192.168.1.0/24`).

### Step 5 — Install Tailscale on Your Phone

Download [Tailscale](https://tailscale.com/download) on your phone and sign in with the same account. Your phone and the gateway are now on the same private network.

### Step 6 — Disable Key Expiry (Recommended)

On the [Tailscale Machines page](https://login.tailscale.com/admin/machines), find **HashWatcherGateway**, click **…**, and toggle **Disable key expiry**. This keeps the gateway connected permanently with no maintenance.

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

## Links

- **HashWatcher App** — [HashWatcher.app](https://www.HashWatcher.app)
- **Follow on X** — [@HashWatcher](https://x.com/HashWatcher)
- **Support** — [info@engineeredessentials.com](mailto:info@engineeredessentials.com?subject=Umbrel%20App%20Support)
- **Developer** — [Engineered Essentials](https://hashwatcher.app)
