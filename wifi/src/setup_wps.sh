#!/bin/bash
# setup_wps.sh — WPS AP on wlan0

# 0) Clean up any old AP or DHCP state
./cleanup.sh

# 1) Variables
IFACE=wlan0
IP_ADDR=10.0.1.1
NETMASK=24
SSID=MouseTrap01
CHANNEL=1
PIN=12345670

# 2) Generate hostapd-wps.conf
cat > hostapd-wps.conf <<EOF2
interface=$IFACE
driver=nl80211
ssid=$SSID
hw_mode=g
channel=$CHANNEL
macaddr_acl=0
ignore_broadcast_ssid=0

# WPA2 encryption (needed for the 4‐way handshake)
wpa=2
wpa_key_mgmt=WPA-PSK WPA-EAP
rsn_pairwise=CCMP
wpa_passphrase=wPSM30wM3ow_1337!

# Internal Registrar mode for WPS
eap_server=1
wps_state=1
ap_setup_locked=0
ap_pin=$PIN

# Advertise PIN mode via these methods (no device_password_id needed)
config_methods=label display push_button keypad

# Device‐info so hostapd emits the WPS IE in the beacon
uuid=01234567-89ab-cdef-0123-456789abcdef
device_name=$SSID
manufacturer=CTF
model_name=Pi_WPS
model_number=1
serial_number=0001
device_type=6-0050F204-1
EOF2

# 3) Network / NAT / DHCP
sudo ip link set $IFACE down
sudo ip addr flush dev $IFACE
sudo ip addr add $IP_ADDR/$NETMASK dev $IFACE
sudo ip link set $IFACE up

sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -F
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

sudo pkill dnsmasq 2>/dev/null
sudo dnsmasq --no-daemon --interface=$IFACE --bind-interfaces \
  --dhcp-range=10.0.1.10,10.0.1.100,12h &

# 4) Start hostapd
sudo pkill hostapd 2>/dev/null
sudo hostapd hostapd-wps.conf
