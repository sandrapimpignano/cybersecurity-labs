# 🛡️ Defensive Countermeasures — ARP Spoofing Mitigation

This document outlines defensive strategies and network‑level protections that can detect, prevent, or mitigate ARP spoofing attacks within a Layer‑2 environment.  
These countermeasures complement the threat model and provide a realistic view of how modern networks defend against ARP‑based Man‑in‑the‑Middle (MitM) attacks.

---

## 1. 🔐 Switch‑Level Protections (Enterprise‑Grade)

### **1.1 Dynamic ARP Inspection (DAI)**
DAI validates ARP packets against trusted bindings (DHCP snooping tables).  
It prevents attackers from injecting forged ARP replies.

**Effectiveness:**  
⭐⭐⭐⭐⭐ — Completely blocks ARP spoofing on managed switches.

---

### **1.2 DHCP Snooping**
DHCP Snooping builds a trusted IP–MAC–Port binding table.  
DAI uses this table to validate ARP traffic.

**Benefits:**
- Prevents rogue DHCP servers  
- Enables DAI to function correctly  

---

### **1.3 Port Security**
Limits the number of MAC addresses allowed on a switch port.

**Mitigation:**
- Prevents MAC flooding  
- Blocks unauthorized devices  
- Can shut down ports with suspicious activity  

---

## 2. 🧱 Host‑Level Protections

### **2.1 Static ARP Entries**
Manually binding IP–MAC pairs prevents ARP cache poisoning.

**Limitations:**
- Not scalable  
- Requires manual maintenance  
- Used mainly in high‑security or ICS environments  

---

### **2.2 ARP Cache Locking (OS‑Level Hardening)**
Some operating systems allow locking ARP entries or restricting unsolicited ARP replies.

**Examples:**
- Linux `arp -s` static entries  
- Windows `netsh interface ipv4 add neighbors`  

---

### **2.3 Local Firewall Rules**
Host firewalls can block unsolicited ARP replies or limit ARP rate.

**Tools:**
- `arptables` (Linux)  
- Windows Defender Firewall (limited ARP filtering)  

---

## 3. 🔍 Detection & Monitoring Tools

### **3.1 arpwatch**
Monitors ARP traffic and alerts when MAC–IP bindings change unexpectedly.

**Detects:**
- ARP spoofing  
- MAC address changes  
- Network anomalies  

---

### **3.2 IDS/IPS Systems**
Systems like Snort or Suricata can detect ARP poisoning signatures.

**Example rules:**
- ARP reply with mismatched MAC  
- High‑frequency ARP broadcasts  

---

### **3.3 Network Scanners & Baseline Tools**
Tools like `arp-scan` can be used to periodically verify network integrity.

**Usage:**
- Detect rogue hosts  
- Identify MAC inconsistencies  
- Validate gateway identity  

---

## 4. 🧬 Architectural Defenses

### **4.1 VLAN Segmentation**
Separating hosts into VLANs reduces the broadcast domain size.

**Benefits:**
- Limits ARP spoofing to a single VLAN  
- Reduces lateral movement  

---

### **4.2 Zero‑Trust Network Architecture**
Assumes no device is trusted by default.

**Mitigations:**
- Continuous verification  
- Micro‑segmentation  
- Identity‑based access  

---

### **4.3 Encrypted Protocols**
Even if ARP spoofing succeeds, encrypted traffic remains protected.

**Examples:**
- HTTPS  
- SSH  
- TLS‑based services  

**Note:**  
Metadata (DNS, SNI, IP headers) may still be visible.

---

## 5. 🧯 Operational Best Practices

### **5.1 Gateway MAC Verification**
Users or scripts can periodically verify the gateway MAC address.

### **5.2 Logging & Alerting**
Enable logging on switches, firewalls, and IDS systems.

### **5.3 Regular Network Audits**
Perform routine scans to detect anomalies in MAC/IP mappings.

---

## 6. ✔️ Summary

ARP spoofing is effective only in networks lacking Layer‑2 security controls.  
Modern defenses — especially Dynamic ARP Inspection, DHCP Snooping, and VLAN segmentation — can fully prevent or significantly limit the attack.

This document provides a comprehensive overview of defensive strategies that complement the ARP Spoofing laboratory and demonstrate how real‑world networks mitigate Layer‑2 threats.

