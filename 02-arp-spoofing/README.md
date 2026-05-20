# ⚡ ARP Spoofing Tool: Layer-2 MitM Simulation Utility

[![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org)
[![Scapy](https://img.shields.io/badge/Scapy-Layer2%20Packet%20Forge-yellow)](https://scapy.net)
[![Linux](https://img.shields.io/badge/OS-Linux-orange)](https://www.linux.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

### Man-in-the-Middle (MitM) Engine & Network Traffic Routing Simulator

A Python-based utility engineered for controlled Address Resolution Protocol (ARP) manipulation and traffic routing analysis within isolated laboratory environments. This module is part of the `cybersecurity-labs` project, providing an automated framework to simulate network-layer interception using Scapy and the Linux kernel networking stack.

---

## 🌐 Overview

ARP Spoofing (or ARP Cache Poisoning) is a critical technique used to analyze trust flaws within local area networks (LANs). By emitting forged ARP replies, this tool demonstrates how an unauthenticated attacker can position themselves between a target host and the local gateway, establishing a full Man-in-the-Middle (MitM) position.

This utility automates the entire attack lifecycle, ensuring smooth data link routing via kernel forwarding, automated target discovery validation, and atomic network state restoration upon termination.

---

## 📂 Repository Structure

```text
cybersecurity-labs/
└── 02-arp-spoofing/
    ├── arp_spoofing.py             --> 1. MITM Execution Engine (Python/Scapy)
    ├── THREAT_MODEL.md             --> 2. Attack Surface & STRIDE Analysis
    └── DEFENSIVE_COUNTERMEASURES.md --> 3. Network Hardening & Mitigations
```
* arp_spoofing.py: The core simulation engine used to execute the Layer-2 manipulation.
* THREAT_MODEL.md: Architectural security analysis mapping the attack vectors using the STRIDE methodology.
* DEFENSIVE_COUNTERMEASURES.md: Blue Team documentation covering industry-standard mitigations (DAI, DHCP Snooping, etc.).

---

## ✨ Key Features

* **Asynchronous Dual-Target Poisoning:** Utilizes high-frequency ARP response generation to simultaneously spoof both the victim host and the network gateway.
* **Kernel-Level IP Forwarding Automation:** Direct interaction with the Linux kernel networking stack (`/proc/sys/net/ipv4/ip_forward`) to dynamically enable traffic routing, leveraging native OS performance and preventing Denial of Service (DoS) conditions on the target.
* **Automated Graceful Clean-up (SIGINT Handler):** Intercepts `Ctrl+C` termination to execute an atomic network rollback, sending standard ARP packets to restore correct cache mappings instantly.
* **Dynamic Argument Parsing:** Built using Python's `argparse` core library, allowing granular command-line input for IPs, MACs, and injection intervals without hardcoded limits.

---

## 🛠️ Requirements

*   **Operating System:** Linux (Kali Linux or any distribution with root execution access).
*   **Python Version:** Python 3.7+
*   **Core Dependencies:** `scapy` library (for Layer-2 packet forging).
*   **Privileges:** Root access (`sudo`) is mandatory to modify network kernel parameters and craft raw socket frames.

> 💡 **Prerequisite Check:** Before initializing the engine, ensure the Scapy package is installed on your host system:
> ```bash
> sudo pip3 install scapy
> ```

> ⚠️ **Note:**  
> The tool performs strict MAC address validation.  
> All MACs must follow the format `aa:bb:cc:dd:ee:ff`.

---

## 🚀 Usage Guide

### 1. Clone the Repository
```bash
git clone https://github.com/sandrapimpignano/cybersecurity-labs.git
cd cybersecurity-labs/02-arp-spoofing
sudo chmod +x arp_spoofing.py
```
### 2. Execution Workflow
The deployment of a Man-in-the-Middle scenario requires a structured four-stage workflow: **Reconnaissance → Target Mapping → Exploitation → Interception**.

---

### Phase 1: Network Reconnaissance & Target Mapping

In a real-world scenario, the attacker does not have direct access to the victim's configuration. To extract the required operational parameters (IP and MAC addresses) from the local area network (LAN), we execute an active Layer-2 discovery scan using `arp-scan` from the Kali Linux host.

Run the following command to map the subnet:

```bash
sudo arp-scan --localnet
```
**Expected output:** 

```text
Interface: eth0, type: EN10MB, MAC: 00:11:22:33:44:58, IPv4: 192.168.142.154
Starting arp-scan 1.10.0 with 256 hosts (https://github.com/royhills/arp-scan)

192.168.142.1    00:50:56:c0:00:08    VMware, Inc. (Host Interface)
192.168.142.2    00:50:56:e6:8d:e3    VMware, Inc. (NAT Gateway / Router)
192.168.142.135  00:0c:29:a5:a5:35    VMware, Inc. (Lubuntu Target Victim)
192.168.142.254  00:50:56:f4:c5:5a    VMware, Inc. (DHCP Server - Ignored)


4 packets received by filter, 0 packets dropped by kernel
Ending arp-scan 1.10.0: 256 hosts scanned in 3.216 seconds (79.60 hosts/sec). 4 responded
```

#### Network Topology Matrix

Based on the reconnaissance phase, the extracted parameters required for the command-line interface are defined as follows:

| Parameter Flag | Role | Target IP Address | Target MAC Address |
| :--- | :--- | :--- | :--- |
| `-v` / `-vm` | **Victim Target** (Lubuntu) | `192.168.142.135` | `00:0c:29:a5:a5:35` |
| `-r` / `-rm` | **Network Gateway** (Router) | `192.168.142.2` | `00:50:56:e6:8d:e3` |
| `-am` | **Attacker Host** (Kali Linux) | `192.168.142.154` | `00:11:22:33:44:58` |

#### 🔍 Logical Topology Diagram

```bash
                         ┌──────────────────────────┐
                         │        Internet          │
                         └─────────────┬────────────┘
                                       │
                               [ VMware NAT ]
                                       │
                         ┌─────────────┴─────────────┐
                         │       Virtual LAN          │
                         └─────────────┬─────────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        │                              │                              │
   ┌──────────┐                 ┌──────────┐                 ┌──────────┐
   │  Router  │◄─────spoof──────│  Kali    │─────spoof──────►│  Victim  │
   │ (Gateway)│─────spoof──────►│ Attacker │◄────spoof───────│ (Host)   │
   └──────────┘                 └──────────┘                 └──────────┘
   192.168.142.2             192.168.142.154             192.168.142.135
   MAC: 00:50:56:e6:8d:e3    MAC: 00:11:22:33:44:58      MAC: 00:0c:29:a5:a5:35

                 ▲                     │                     ▲
                 │                     │                     │
                 └─────────────── MITM Traffic ─────────────┘
```



### Phase 2: Tool Execution & Exploitation

With the target parameters successfully mapped, initialize the spoofing engine by passing the arguments to `arp_spoofing.py`. The utility will automatically enable kernel-level IP forwarding to ensure seamless transit routing, preventing network drops for the target.

Run the script using the mapped topological variables:

```bash
sudo ./arp_spoofing.py -v 192.168.142.135 -vm 00:0c:29:a5:a5:35 -r 192.168.142.2 -rm 00:50:56:e6:8d:e3 -am 00:11:22:33:44:58
```
**Expected output:** 
```text
[*] Configuring Linux kernel network parameters...
[+] Network routing and packet forwarding: ENABLED

[*] Target Acquired: 192.168.142.135 (00:0c:29:a5:a5:35)
[*] Gateway Acquired: 192.168.142.2 (00:50:56:e6:8d:e3)
[*] Injecting persistent ARP updates into the segment...
[+] Poison packets broadcasted: 136
```

### Phase 3: Interception & Post-Attack Verification

To validate that the Man-in-the-Middle state has been fully achieved, execute the following operational checks across the lab infrastructure:

#### 1. Cache Poisoning Verification (On Lubuntu Target)
Open a terminal on the victim host (`192.168.142.135`) and check the kernel ARP table:

```bash
arp -n
```
**Analysis:** The gateway IP (`192.168.142.2`) will now point directly to the Attacker's hardware address (`00:11:22:33:44:58`) instead of the legitimate VMware router MAC address.

#### 2. Passive Traffic Analysis (CLI vs GUI Approaches)
To capture and inspect the diverted traffic stream flowing through your host interface, spawn a secondary terminal on Kali Linux. You can opt for either a lightweight command-line logging setup or a full graphical analysis session.

##### Option A: Command-Line Interception via `tshark`
Perfect for lightweight, terminal-only operational environments. Run the packet analyzer with a targeted display filter:

```bash
sudo tshark -i eth0 -Y "ip.addr == 192.168.142.135"
```
##### Option B: Graphical Analysis via `Wireshark`
Ideal for deep packet inspection and detailed traffic reconstruction. Launch the interface in the background:

```bash
sudo wireshark &
```
**Operational Step:** Inside Wireshark, select the `eth0` interface and apply the identical display filter in the top navigation bar: `ip.addr == 192.168.142.135`. Every DNS query, unencrypted HTTP payload, and transit frame originating from the Lubuntu target will surface inside the analytical matrix in real-time.

---

### Phase 4: Graceful Restoration ("Leaving Quietly")

An essential requirement for professional offensive tools is the ability to clear the operational footprint upon termination. When `Ctrl+C` is pressed, the custom SIGINT handler intercepts the break sequence, halts the injection loop, and executes an atomic recovery sequence.

#### Expected Output (Termination Phase):

```text
[+] Poison packets broadcasted: 136^C
[!] Execution halted via user interrupt.

[*] Initiating 'Leaving Quietly' protocol...
[*] Re-establishing correct MAC/IP bindings in target caches...
[+] Network state restored successfully. Mitigation verified.
[+] Session closed cleanly.
```

**Analysis:** The script broadcasts genuine, legitimate ARP frames containing the original MAC-to-IP mappings back to both the victim and the gateway. This instantly resolves the poisoning, allowing the local network caches to recover completely without requiring a network restart.

---

## 🧩 Troubleshooting

### 1. Invalid MAC Address Format
If you see:

```bash
[-] Invalid <label> MAC address format
```

**Fix:** Ensure all target MAC addresses strictly follow the hexadecimal, colon-separated standard format:

```bash
# Example of valid MAC address format:
aa:bb:cc:dd:ee:ff
```

### 2. Routing Configuration Errors
If you see:

```bash
[-] Failed to configure kernel routing.
```

Fix:
* Run with sudo
* Ensure no firewall blocks sysctl or iptables
### 3. Victim ARP Cache Not Updating
* Wait a few seconds
* Restart victim’s network interface
* Ensure spoofing loop is running (counter increasing)
### 4. Only Encrypted HTTPS Traffic Visible
This is expected.
The tool performs Layer‑2 MITM, not TLS decryption.
You will still see:
* DNS queries
* SNI
* HTTP
* Metadata

---

## 🔬 Learning Objectives & Core Concepts

Developing and testing this simulation utility allowed for the practical verification of critical networking and security principles:

*   **Data Link Layer Vulnerabilities (OSI Layer 2):** Direct analysis of the stateless nature of the Address Resolution Protocol (ARP). Since ARP lacks authentication mechanisms, systems accept unsolicited responses, making them inherently vulnerable to spoofing.
*   **Linux Routing Architecture:** Hands-on experience with internal kernel parameters (`/proc/sys/net/ipv4/ip_forward`), understanding how operating systems process, route, and forward transit network traffic.
*   **Packet Construction & Manipulation:** Utilizing Scapy to manually forge Ethernet and ARP headers, gaining familiarity with structural fields such as Operation Codes (`op=2` for ARP replies) and hardware/protocol address bindings.
*   **Network Resilience & Defenses:** Analyzing how structural mitigations, such as Static ARP configurations, Dynamic ARP Inspection (DAI) on managed switches, and monitoring tools like `arpwatch`, can detect or completely prevent these anomalies.

---

## ⚠️ Ethical Considerations & Disclaimer

> [!WARNING]
> **Educational and Laboratory Use Only:** This utility is engineered exclusively for controlled educational simulations, security academic research, and authorized penetration testing environments. 

Unauthorized deployment of ARP spoofing tools against production networks or systems without explicit, written administrative consent is strictly prohibited and constitutes a violation of cyber laws worldwide. The developer assumes absolutely no liability for any misuse, operational disruptions, or damage caused by the application of this educational framework.

---

## 📚 Additional Documentation
- [Threat Model](THREAT_MODEL.md)
- [Defensive Countermeasures](DEFENSIVE_COUNTERMEASURES.md)

---

## 📄 License

This repository is distributed under the **MIT License**. For detailed information regarding permissions and limitations, see the main `LICENSE` file at the root of the `cybersecurity-labs` workspace.
