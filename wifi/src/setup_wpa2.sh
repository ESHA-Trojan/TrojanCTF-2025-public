#!/bin/bash
# Simple WPA2-PSK AP
IFACE=wlan0
IP_ADDR=10.0.0.1
NETMASK=24
SSID="Catnip_Cafe2"
PASSPHRASE="Password123"
CHANNEL=1

bash cleanup.sh

# generate hostapd conf
cat > hostapd-wpa2.conf <<EOC
interface=$IFACE
driver=nl80211
ssid=$SSID
hw_mode=g
channel=$CHANNEL
auth_algs=1
wpa=2
wpa_passphrase=$PASSPHRASE
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP CCMP
rsn_pairwise=CCMP
EOC

# network, NAT, DHCP
sudo ip link set $IFACE down
sudo ip addr flush dev $IFACE
sudo ip addr add $IP_ADDR/$NETMASK dev $IFACE
sudo ip link set $IFACE up
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -F
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo pkill dnsmasq || true
sudo dnsmasq --interface=$IFACE --bind-interfaces --dhcp-range=10.0.0.10,10.0.0.100,12h &

# start WPA2 AP
sudo pkill hostapd || true
sudo hostapd hostapd-wpa2.conf
