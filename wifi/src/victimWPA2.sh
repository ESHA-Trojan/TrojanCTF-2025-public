#!/bin/bash
# handshake_reconnect.sh
# This script continuously connects and disconnects to two WPA2 networks to generate handshakes for CTF exercises.

# Configuration
SSID1="Catnip_Cafe"
PASS1="Password123"
SSID2="RainbowCat"
PASS2="Clawtastic1"
SSID3="Catnip_Cafe2"
PASS3="Password123"
INTERFACE="wlan0"  # Change if your Wi-Fi interface is different

# Timings (in seconds)
CONNECT_WAIT=5    # Time to stay connected for handshake capture
DISCONNECT_WAIT=2 # Time between disconnections and next connection

# Ensure Wi-Fi is enabled
nmcli radio wifi on

# Infinite loop to alternate connections
while true; do
  for i in 1 2 3; do
    if [ "$i" -eq 1 ]; then
      SSID="$SSID1"; PASS="$PASS1"
    elif [ "$i" -eq 2 ] ; then
      SSID="$SSID2"; PASS="$PASS2"
    else
      SSID="$SSID3" ; PASS="$PASS3"
    fi

    echo "[+] Connecting to $SSID..."
    nmcli device wifi connect "$SSID" password "$PASS" ifname "$INTERFACE"

    echo "[+] Waiting $CONNECT_WAIT seconds to capture handshake..."
    sleep "$CONNECT_WAIT"

    echo "[+] Disconnecting from $SSID..."
    nmcli connection down id "$SSID"

    # Optional: remove the saved connection profile to force fresh negotiation
    # nmcli connection delete id "$SSID"

    echo "[+] Waiting $DISCONNECT_WAIT seconds before next attempt..."
    sleep "$DISCONNECT_WAIT"
  done
done
