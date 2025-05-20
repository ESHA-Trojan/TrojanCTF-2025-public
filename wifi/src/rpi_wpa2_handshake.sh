#!/bin/bash
#
# rpi_wpa2_handshake.sh
#
# Continuously cycles connection attempts between two WPA2 networks
# to generate handshakes for capture.
#
# Usage:
#   1. Copy this script to your Raspberry Pi (e.g. /usr/local/bin/rpi_wpa2_handshake.sh)
#   2. chmod +x /usr/local/bin/rpi_wpa2_handshake.sh
#   3. Run with sudo: sudo /usr/local/bin/rpi_wpa2_handshake.sh

# --- Configuration ---
INTERFACE="wlan0"              # Your WiFi interface
WPA_CONF="/tmp/wpa2_cycle.conf"

SSID1="Catnip_Cafe"
PSK1="Password123"

SSID2="RainbowCat"
PSK2="Clawtastic1"

# Time to wait after each connection attempt (seconds)
WAIT_TIME=20

# --- Functions ---
generate_wpa_conf() {
    local ssid="$1"
    local psk="$2"
    cat > "$WPA_CONF" <<EOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="$ssid"
    psk="$psk"
    key_mgmt=WPA-PSK
}
EOF
}

cleanup() {
    echo "[*] Cleaning up: stopping wpa_supplicant..."
    killall wpa_supplicant 2>/dev/null
    exit 0
}

# Trap SIGINT/SIGTERM to clean up
trap cleanup SIGINT SIGTERM

# --- Main Loop ---
echo "[*] Starting WPA2 handshake trigger loop..."
while true; do
    echo "[*] Attempting connection to $SSID1 ..."
    generate_wpa_conf "$SSID1" "$PSK1"
    killall wpa_supplicant 2>/dev/null
    wpa_supplicant -B -i "$INTERFACE" -c "$WPA_CONF"
    sleep "$WAIT_TIME"

    echo "[*] Attempting connection to $SSID2 ..."
    generate_wpa_conf "$SSID2" "$PSK2"
    killall wpa_supplicant 2>/dev/null
    wpa_supplicant -B -i "$INTERFACE" -c "$WPA_CONF"
    sleep "$WAIT_TIME"
done
