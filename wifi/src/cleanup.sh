#!/bin/bash
# cleanup.sh — tear down any old AP state

IFACE=wlan0

# stop any old daemons
sudo pkill hostapd dnsmasq 2>/dev/null

# disable NAT & forwarding
sudo sysctl -w net.ipv4.ip_forward=0
sudo iptables -t nat -F

# reset the radio
sudo rfkill unblock wifi
sudo iw reg set US           # or your country code
sudo ip link set $IFACE down
sudo ip addr flush dev $IFACE
