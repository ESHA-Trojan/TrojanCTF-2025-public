from flask import Flask, request, abort
import hashlib
import sys
from urllib.parse import unquote_to_bytes


app = Flask(__name__)

# Secret key used for MAC computation (32 bytes)
SECRET_KEY = b"whisking-crumpled-cartwheel-drew"  # 32 bytes

# Original data that the server expects
ORIGINAL_DATA = b"user=guest&role=member"

# The flag to be revealed when the challenge is solved
FLAG = "Trojan{length_extension_with_padding_success133333333333333}"

@app.route("/verify")
def verify():
    """
    Endpoint to verify the provided data and MAC.
    """
    # Get the 'data' and 'mac' parameters from the URL
    data = request.args.get("data")
    received_mac = request.args.get("mac")

    
    # Check if both 'data' and 'mac' are provided
    if not data or not received_mac:
        abort(400, "Missing 'data' or 'mac' parameter")

    # Debug: Print the received data and MAC
    print(f"[DEBUG] Received data: {unquote_to_bytes(data)}")
    print(f"[DEBUG] Received MAC: {received_mac}")
    sys.stdout.flush()

    # Compute the expected MAC: SHA1(secret_key + data)
    expected_mac = hashlib.sha1(SECRET_KEY + unquote_to_bytes(data)).hexdigest()

    # Debug: Print the computed MAC
    print(f"[DEBUG] Computed MAC: {expected_mac}")
    sys.stdout.flush()

    # Check if the received MAC matches the computed MAC
    if received_mac != expected_mac:
        print("[DEBUG] MAC mismatch! Invalid request.")
        sys.stdout.flush()
        abort(403, f"Invalid MAC \n"
                f"Received data: {unquote_to_bytes(data)}\n"
                f"Received MAC: {received_mac}\n"
                f"Expected MAC: {expected_mac[len(expected_mac) // 2 :] + '*' * (len(expected_mac) // 2)}")

    # Check if the data is different from the original
    if data == ORIGINAL_DATA.decode():
        print("[DEBUG] Data matches original! No flag for you.")
        sys.stdout.flush()
        abort(403, "Data matches original")

    # If both checks pass, return the flag
    print("[DEBUG] Valid request! Flag revealed.")
    sys.stdout.flush()
    return f"Flag: {FLAG}"

if __name__ == "__main__":
    # Run the Flask server on all available IPs and port 5000
    app.run(host="0.0.0.0", port=5000)