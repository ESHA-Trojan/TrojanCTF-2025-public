# Description
Following suspicious activity from one of our company's computers, we recorded its network traffic. Analyzing the resulting file, we noticed that it is communicating with a specific address, but the packets it sends are empty. Our suspicion is that it is trying to secretly send data to this address. Can you confirm this?

# Solution
This challenge provides us with a `pcap` file, a file that contains captured network traffic.  

Opening this file in a program that can analyze network traffic, such as `Wireshark`, we can see the following traffic:  

![alt text](Images/image1.png)  


If we try to follow one of the TCP streams of whatever packet, we will end up in an empty packet (no content inside). Looking further for whatever useful information, we are led to a dead end.

The description of the challenge refers to hidden information inside the traffic, and we also notice that the challenge is called `knock-knock`. Could the hidden info be in the port numbers (and thus the title `knock-knock` refering to the port) ?

Looking at the port numbers, we see all are in the range of printable ascii characters (while normally port numbers can go up to 65535).  


Just out of curiosity, we make the following python program that uses the `scapy` library to parce the port numbers of each packet. You could also just select and extract the port numbers to a list, and just use simple python:    
```py
from scapy.all import *

packets = rdpcap("knock-knock.pcap")

for p in packets:
    if p.haslayer(TCP):
	    dst_port = p[TCP].dport

	    # Converted to chr to get the ascii
	    print(chr(dst_port), end='') 
```

Running the following program, we get:
```sh
└─$ python solver.py 
https://pastebin.com/raw/LCLSmQ8F
```
We get back a pastebin url. Simply put, pastebins are public or private posts that contain data. They can be used by attackets and malicious actors to store payloads, leaked data and more.  

Visiting the pastebin, we get a base64 string:  

![alt text](Images/image2.png)  

Decoding from base64, we get the flag for this one:  

```sh
└─$ echo "VHJvamFue2gxZDFuZ18xbmYwXzFuX3AwMjdfbnVtYjMyNX0=" | base64 -d
Trojan{h1d1ng_1nf0_1n_p027_numb325}
```
