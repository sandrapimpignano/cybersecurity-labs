# 🛡️ Threat Model — ARP Spoofing Laboratory

This document defines the threat model for the ARP Spoofing simulation environment.  
It outlines the adversary profile, capabilities, constraints, targeted assets, and the expected attack flow within the controlled laboratory network.

---

## 1. 🎯 Objective of the Attack

The goal of the simulated adversary is to:

- Intercept network traffic between a victim host and the default gateway  
- Manipulate ARP cache entries to position themselves as a Man‑in‑the‑Middle (MitM)  
- Observe, analyze, or forward traffic without disrupting network availability  

This aligns with the behavior described in the main README:

> “By emitting forged ARP replies, this tool demonstrates how an unauthenticated attacker can position themselves between a target host and the local gateway…”  

---

## 2. 👤 Adversary Profile

**Type:** Internal network attacker  
**Location:** Same Layer‑2 broadcast domain as the victim  
**Access Level:**  
- Full access to the local LAN  
- Ability to send raw Ethernet frames  
- Root privileges on the attacking machine  

**Motivation:**  
- Traffic interception  
- Credential harvesting (unencrypted protocols)  
- Network reconnaissance  
- Lateral movement preparation  

---

## 3. 🧰 Adversary Capabilities

The attacker is capable of:

- Sending forged ARP replies at high frequency  
- Spoofing both victim and gateway simultaneously  
- Enabling IP forwarding to maintain network stability  
- Capturing traffic using tools such as `tshark` or `Wireshark`  
- Restoring network state to avoid detection  

These capabilities reflect the tool’s features:

> “Utilizes high‑frequency ARP response generation to simultaneously spoof both the victim host and the network gateway.”  
> “Direct interaction with the Linux kernel networking stack to enable traffic routing.”  

---

## 4. 🔒 Adversary Limitations

The attacker **cannot**:

- Break TLS encryption  
- Intercept traffic outside the local broadcast domain  
- Modify switch‑level security controls (e.g., DAI, port security)  
- Spoof MAC addresses that fail validation (tool enforces strict format)  

Additionally:

- HTTPS payloads remain encrypted  
- ARP spoofing is ineffective on networks with static ARP entries  
- Managed switches may block or alert on ARP anomalies  

---

## 5. 🏗️ Target Environment

### **Network Components**

| Role | IP Address | MAC Address |
|------|------------|-------------|
| Gateway Router | 192.168.142.2 | 00:50:56:e6:8d:e3 |
| Victim Host (Lubuntu) | 192.168.142.135 | 00:0c:29:a5:a5:35 |
| Attacker (Kali Linux) | 192.168.142.154 | 00:11:22:33:44:58 |

These values are derived from the reconnaissance phase:

> “192.168.142.135  00:0c:29:a5:a5:35 — Lubuntu Target Victim”  

---

## 6. 🧩 Attack Surface

The attacker exploits the following weaknesses:

### **ARP Protocol Weaknesses**
- Stateless  
- No authentication  
- Accepts unsolicited replies  
- Overwrites valid entries without validation  

### **Layer‑2 Broadcast Domain Exposure**
- All ARP frames are visible to all hosts  
- No segmentation or VLAN isolation  

### **Lack of Switch‑Level Protections**
- No Dynamic ARP Inspection (DAI)  
- No port security  
- No MAC binding policies  

---

## 7. 🔥 Attack Flow (STRIDE‑Aligned)

### **1. Spoofing**
The attacker forges ARP replies to impersonate the gateway and victim.

### **2. Tampering**
The ARP cache of both hosts is modified.

### **3. Information Disclosure**
Traffic is routed through the attacker’s machine.

### **4. Denial of Service (Avoided)**
The tool enables IP forwarding to prevent accidental DoS.

### **5. Elevation of Privilege**
Logically achieved at the network level by intercepting transit traffic designated only for the default gateway

---

## 8. 📉 Impact Assessment

### **Confidentiality**
- High impact  
- Attacker can view unencrypted traffic (DNS, HTTP, metadata)

### **Integrity**
- Medium impact  
- Attacker could alter packets before forwarding (not implemented in this tool)

### **Availability**
- Low impact  
- IP forwarding prevents service disruption

---

## 9. 🧹 Post‑Attack Recovery

The tool includes a built‑in SIGINT handler:

> “Re‑establishing correct MAC/IP bindings in target caches… Network state restored successfully.”

This ensures:

- ARP tables are restored  
- No persistent poisoning  
- Clean exit from the environment  

---

## 10. ✔️ Summary

This threat model defines a realistic internal attacker capable of performing ARP spoofing to achieve MitM positioning within a controlled laboratory environment.  
The simulation demonstrates the inherent insecurity of ARP and highlights the importance of Layer‑2 defenses in modern networks.

