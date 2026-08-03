# Truegle WiFi Auditor

A lightweight tool to discover devices on your local network and perform targeted scanning, designed for Android (Termux) security testing.

## Prerequisites

- Termux with `arp-scan` and `nmap` installed:
  ```bash
  pkg install arp-scan nmap

Usage

Run from the project root:

```bash
python harness/wifi_audit.py [options]
```

Options

Option Description
--ssid SSID Network name (required unless --manual-connect)
--password PASS Network password
--manual-connect Skip WiFi connection (use if already connected)
--target-ip IP Scan a specific IP address
--auto-target-motorola Automatically find and scan a Motorola device

Examples

1. Auto‑connect and scan for Motorola devices:

```bash
python harness/wifi_audit.py --ssid "PepeWiFi39" --password "19041986RA" --auto-target-motorola
```

2. Manual connect (already on WiFi) and target specific IP:

```bash
python harness/wifi_audit.py --manual-connect --target-ip 192.168.1.10
```

3. List all devices (no detailed scan):

```bash
python harness/wifi_audit.py --manual-connect
```

Output

· A list of active devices (IP, MAC, vendor) is printed.
· A full JSON report is saved to wifi_report.json.
· If a target is specified, a detailed nmap scan is performed.

Notes

· Use only on networks you own or have explicit permission to test.
· The script is for educational/defensive security research.
· The termux-wifi-connection feature may require additional setup.
