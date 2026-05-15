# ⚡ MAC Spoofing Tool: Layer-2 Stealth Utility
### *Ethernet Identity Spoofer & Network Reconnaissance Tool*
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Kali-557C94?logo=kalilinux&logoColor=white)
![Network](https://img.shields.io/badge/L2-Spoofing-grey?logo=wireshark&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-333333)

*A Python-based tool for controlled MAC address reconfiguration in cybersecurity laboratory environments.*

This module is part of the **cybersecurity-labs** project and provides a minimal, reliable Python utility for modifying the **Media Access Control (MAC)** address of a Linux network interface using the `iproute2` networking suite.
It is designed for **training**, **research**, and **authorized security testing** scenarios.

---

## 🌐 Overview

MAC address manipulation is a foundational technique in network security. 
By altering the hardware identifier of a network interface, practitioners can analyze how networks identify and authorize devices.



This utility automates the MAC spoofing workflow while ensuring validation, safety, and post-operation verification.

---

## ✨ Key Features

### • Interface Lifecycle Management  
Safely transitions the target interface through the sequence **down → reconfigure → up**, ensuring consistent and error-free operation.

### • Strict MAC Address Validation  
Validates the MAC address format using a compliant regular expression: `XX:XX:XX:XX:XX:XX`.

### • Post-Change Integrity Verification  
Retrieves and compares the system-reported MAC address to confirm successful application.

### • Advanced Error Handling  
Gracefully manages insufficient privileges, missing `iproute2` utilities, and invalid interfaces.

---

## 🛠️ Requirements

- **Operating System:** Linux (Kali recommended)
- **Networking Tools:** `iproute2` (`ip` command)
- **Python:** 3.6+
- **Privileges:** root access (`sudo`)

> [!TIP]
> **Not sure about your interface name?**  
> Use the command `ip link show` or `nmcli device` to list all available network interfaces on your system before configuring the script.

---

## 🚀 Usage Guide

### 1. Clone the Repository
```bash
git clone https://github.com/sandrapimpignano/cybersecurity-labs.git
cd cybersecurity-labs/01-mac-change
```

### 2. Configure the Script
Edit the following constants inside `mac_change.py`:

```python
INTERFACE = "eth0"
NEW_MAC   = "00:11:22:33:44:58"
```

### 3. Execute the Utility

```bash
sudo python3 mac_change.py
```

### 💡 Expected Output
When running the script, you should see a clean execution flow like this:
```bash
[i] Current MAC of eth0: xx:xx:xx:xx:xx:xx
[+] Bringing network interface eth0 down…
[+] Setting new MAC 00:11:22:33:44:58 on eth0…
[+] Bringing network interface eth0 up…
[i] MAC reported by the system: 00:11:22:33:44:58
[✓] MAC address successfully changed.
```

### 4. Verify the MAC Address Manually (Optional)

```bash
ip link show eth0
```
**or:**
```bash
ifconfig eth0
```

---

## 🔬 Internal Workflow
The tool follows a deterministic five-stage process:

1. **Discovery**: Reads the current MAC address using `ip link show`.
2. **Interface Shutdown**: Temporarily disables the interface to allow hardware address modification.
3. **MAC Reassignment**: Applies the new MAC address using:
   `ip link set eth0 address 00:11:22:33:44:58`
4. **Interface Reactivation**: Restores operational state and network connectivity:
   `ip link set eth0 up`
5. **Verification**: Confirms that the system reports the updated MAC address.

---

## 🎓 Learning Objectives
This laboratory module reinforces key concepts in:

- OSI Model (Layer 2): Understanding how Data Link layer identifiers function.

- Linux Networking Stack: Transitioning from legacy net-tools (ifconfig) to the modern iproute2 suite.

- Python Subprocess Management: Safely executing system-level commands and handling output streams.

- Automation Logic: Implementing "State Check → Action → Verification" patterns in security tooling.

---

## ⚠️ Ethical & Security Considerations
MAC address manipulation must be performed exclusively in:

- Controlled laboratory environments
- Personal systems
- Authorized penetration testing scenarios

Unauthorized MAC spoofing on managed networks may violate organizational policies or legal frameworks.
This tool is provided strictly for educational and research purposes.

---

## 📄 License
This project is distributed under the MIT License, allowing academic and professional reuse.
