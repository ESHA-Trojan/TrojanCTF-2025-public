import hashlib
import struct
import os
import urllib.parse

# SHA-1 constants
SHA1_BLOCK_SIZE_BYTES = 64  # 512-bit blocks (64 bytes)
SHA1_DIGEST_SIZE_BYTES = 20  # 160-bit output (20 bytes)

def compute_padding(message_length_bytes):
    """
    Compute SHA-1 padding for a message of a given length (in bytes).
    """
    # SHA-1 padding: 0x80 followed by 0x00 until the last 8 bytes
    padding = b"\x80"  # Start with 0x80 byte

    # Add zeros until the total length is 56 bytes (448 bits) modulo 64 bytes
    padding += b"\x00" * ((56 - (message_length_bytes + 1) % SHA1_BLOCK_SIZE_BYTES) % SHA1_BLOCK_SIZE_BYTES)

    bit_length = message_length_bytes * 8
    padding += bit_length.to_bytes(8, byteorder='big')  # ✅ 8-byte big-endian

    return padding

def sha1_length_extension(original_hash, original_data, new_data, secret_key_length_bytes):
    """
    Perform a SHA-1 length extension attack.
    """

    # Step 1: Split the original hash into 5 × 32-bit words (big-endian)
    h = struct.unpack(">5I", original_hash)

    # Step 2: Compute the total length of the original input (secret + data + padding)
    original_data_length_bytes = len(original_data)

    # Step 3: 
    padding_original = compute_padding(secret_key_length_bytes + original_data_length_bytes)

    # Step 4: Initialize a SHA-1 object with the original hash as the internal state

    # Your original padding logic

    padding_new = compute_padding(secret_key_length_bytes + original_data_length_bytes + len(padding_original) + len(new_data))

    print("Original is multiple of 64 bytes: ", (secret_key_length_bytes + original_data_length_bytes + len(padding_original)) % 64)
    full_message_to_be_hashed = new_data + padding_new  # Preserved
    print("New is multiple of 64 bytes: ", (len(new_data) + len(padding_new)) % 64)
    
    new_hash = sha1(h, full_message_to_be_hashed)

    forged_message = original_data + padding_original + new_data

    # Step 6: Return the new hash and forged message
    return new_hash, forged_message

def sha1(h, full_message_to_be_hashed):

    # Initialize working variables from input hash
    a, b, c, d, e = h
    
    # Process full message in 64-byte blocks
    for block_start in range(0, len(full_message_to_be_hashed), 64):
        block = full_message_to_be_hashed[block_start:block_start+64]
        
        # Your original message schedule code
        w = list(struct.unpack('>16I', block)) + [0] * 64
        for i in range(16, 80):
            w[i] = _left_rotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1)
        
        # Your original compression logic
        for i in range(80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6
                
            temp = _left_rotate(a, 5) + f + e + k + w[i]
            temp &= 0xFFFFFFFF
            e = d
            d = c
            c = _left_rotate(b, 30)
            b = a
            a = temp
        
        # Update hash values
        h = (
            (h[0] + a) & 0xFFFFFFFF,
            (h[1] + b) & 0xFFFFFFFF,
            (h[2] + c) & 0xFFFFFFFF,
            (h[3] + d) & 0xFFFFFFFF,
            (h[4] + e) & 0xFFFFFFFF
        )
        a, b, c, d, e = h
    
    return struct.pack('>5I', *h)

def _left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

# Example usage
if __name__ == "__main__":
    # Original data and secret key
    # secret_key = b"whisking-crumpled-cartwheel-drew"  # 32 bytes
    original_data = b"user=guest&role=member"
    # input_to_hash = secret_key + original_data

    # Step 1: Compute original SHA-1 hash
    original_hash = bytes.fromhex("49fed001fe4c84a9468711fa33784a1b6b5d3588")
    print(f"Original SHA-1 hash: {original_hash.hex()}")

    # print(f"This implementation SHA-1 hash: {sha1([0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0], input_to_hash + compute_padding(len(input_to_hash))).hex()}")
    # print(f"Padding: ", compute_padding(len(input_to_hash)))

    # Step 2: Perform length extension attack
    new_data = b"&role=admin"
    # print(len(secret_key))
    new_hash, forged_message = sha1_length_extension(
        original_hash, original_data, new_data, 32
    )

    # Step 3: Output results
    if new_hash and forged_message:
        print(f"New SHA-1 hash: {new_hash.hex()}")
        print(f"Forged message (with padding): {forged_message}")

        # URL encode the string using urllib.parse.quote
        encoded_data = urllib.parse.quote(forged_message)

        print(f"URL Encoded data: {encoded_data}")
