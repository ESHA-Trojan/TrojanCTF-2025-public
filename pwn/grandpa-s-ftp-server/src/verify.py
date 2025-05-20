from ftplib import FTP
import time
import sys

ftp = FTP()
ftp.connect('9.223.189.135', 30019)

username = 'gRamP5'
password = 'iS_C0ol'

start = time.time()
ftp.sendcmd(f'USER {username}')
ftp.sendcmd(f'PASS {password}')
delta = time.time() - start

expected_delta = 0.2 * (len(username) + len(password))

if delta < expected_delta:
    print('bad, finished too fast')
    sys.exit(1)

if delta > expected_delta + 0.5:
    print('bad, finished too slow')
    sys.exit(1)

print(f'good, {delta:.3f} ~= {expected_delta}')
