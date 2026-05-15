#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to change the MAC address of a network interface on Linux
using the 'ip' command (iproute2 package). Requires root privileges.

Instructions:
1) Set INTERFACE and NEW_MAC in the constants below.
2) Run with: sudo python3 mac_change.py
"""

import re
import subprocess
import sys

# === PARAMETERS TO CUSTOMIZE ================================================
INTERFACE = "eth0"                 # e.g. "eth0", "wlan0", "enp3s0", etc.
NEW_MAC   = "00:11:22:33:44:58"    # format XX:XX:XX:XX:XX:XX
# ============================================================================


def run(cmd):
    """
    Executes a system command and raises an exception if it fails.
    - cmd: list of strings (e.g. ["ip", "link", "set", "eth0", "down"])
    Uses check=True to raise CalledProcessError on failure.
    """
    subprocess.run(cmd, check=True)


def get_current_mac(iface):
    """
    Returns the current MAC address of interface 'iface'
    by reading the output of 'ip link show <iface>'.
    If not found, returns None.
    """
    out = subprocess.check_output(["ip", "link", "show", iface], text=True)
    m = re.search(r"link/ether\s+([0-9a-f:]{17})", out, re.IGNORECASE)
    if m:
        return m.group(1)
    return None


def is_valid_mac(addr):
    """
    Checks whether 'addr' is a valid MAC address in the format XX:XX:XX:XX:XX:XX
    composed of hexadecimal digits.
    """
    return re.fullmatch(r"[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}", addr) is not None


def main():
    iface = INTERFACE
    new_mac = NEW_MAC

    # 1) Input validation
    if not iface:
        print("[!] Interface not specified.")
        return 1
    if not is_valid_mac(new_mac):
        print("[!] Invalid MAC: {} (use format XX:XX:XX:XX:XX:XX).".format(new_mac))
        return 1

    try:
        # 2) Current MAC (before change)
        current_before = get_current_mac(iface)
        print("[i] Current MAC of {}: {}".format(iface, current_before))

        # 3) Bring interface down to allow MAC change
        print("[+] Bringing network interface {} down…".format(iface))
        run(["ip", "link", "set", iface, "down"])

        # 4) Set the new MAC
        print("[+] Setting new MAC {} on {}…".format(new_mac, iface))
        run(["ip", "link", "set", iface, "address", new_mac])

        # 5) Bring interface back up
        print("[+] Bringing network interface {} up…".format(iface))
        run(["ip", "link", "set", iface, "up"])

        # 6) Final verification
        current_after = get_current_mac(iface)
        print("[i] MAC reported by the system: {}".format(current_after))

        if current_after and current_after.lower() == new_mac.lower():
            print("[✓] MAC address successfully changed.")
            return 0
        else:
            print("[!] Warning: MAC does not match the requested value.")
            print("    Possible causes: NetworkManager, driver restrictions, or system policies.")
            return 2

    except subprocess.CalledProcessError as e:
        print("[!] System error while executing command: {}".format(e))
        return 3
    except FileNotFoundError:
        print("[!] 'ip' command not found. Install the 'iproute2' package.")
        return 4
    except Exception as e:
        print("[!] Unexpected error: {}".format(e))
        return 5


if __name__ == "__main__":
    sys.exit(main())
