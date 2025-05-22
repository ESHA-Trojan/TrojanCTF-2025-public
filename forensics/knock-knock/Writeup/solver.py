from scapy.all import *

packets = rdpcap("knock-knock.pcap")

for p in packets:
    if p.haslayer(TCP):
	    dst_port = p[TCP].dport

	    # Converted to chr to get the ascii
	    print(chr(dst_port), end='') 