from pwn import *

conn = remote("urp-chall.trojanc.tf", 5000)

conn.recvuntil(b"Message 1 is ")
message1 = conn.recvline(keepends=False)
conn.recvuntil(b"Message 2 is ")
message2 = conn.recvline(keepends=False)
conn.recvuntil(b"message 1: ")
conn.sendline(message2)
conn.recvuntil(b"Ack message 1 ")
flag_end = conn.recvuntil(b'}')
conn.recvuntil(b"message 2: ")
conn.sendline(message1)
conn.recvuntil(b"Ack message 2 ")
flag_start = conn.recvuntil(b',', drop=True)

print(flag_start + flag_end)

conn.close()