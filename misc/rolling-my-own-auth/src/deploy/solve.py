from pwn import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Cipher import ChaCha20

alice = remote("alice-chall.trojanc.tf",5000)
bob = remote("bob-chall.trojanc.tf", 5000)

alice.recvuntil(b'(e, n) = (')
alice_e = alice.recvuntil(b", ", drop=True)
alice_n = alice.recvuntil(b")\n", drop=True)

bob.recvuntil(b'(e, n) = (')
bob_e = bob.recvuntil(b", ", drop=True)
bob_n = bob.recvuntil(b")\n", drop=True)
bob_e = int(str(bob_e, 'ascii'))
bob_n = int(str(bob_n, 'ascii'))


pubkey_bob = RSA.construct((bob_n, bob_e)).publickey()

key = RSA.generate(3072)
pubkey = key.publickey()

alice.recvuntil(b'Choice: ')
alice.sendline(b'1')
alice.recvuntil(b'name: ')
alice.sendline(b'eve')
alice.recvuntil(b'exponent: ')
alice.sendline(bytes(str(pubkey.e), 'ascii'))
alice.recvuntil(b'key modulus n: ')
alice.sendline(bytes(str(pubkey.n), 'ascii'))
alice.recvuntil(b'Choice: ')

bob.recvuntil(b'Choice: ')
bob.sendline(b'1')
bob.recvuntil(b'name: ')
bob.sendline(b'eve')
bob.recvuntil(b'exponent: ')
bob.sendline(bytes(str(pubkey.e), 'ascii'))
bob.recvuntil(b'key modulus n: ')
bob.sendline(bytes(str(pubkey.n), 'ascii'))
bob.recvuntil(b'Choice: ')

alice.sendline(b'2')
alice.recvuntil(b'name: ')
alice.sendline(b'eve')
alice.recvuntil(b'message 1:\n')
message1 = alice.recvline(keepends=False)

bytes_c1 = base64.decodebytes(message1)

cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256, label=b'\x01')
plain1 = cipher.decrypt(bytes_c1)

cipher = PKCS1_OAEP.new(pubkey_bob, hashAlgo=SHA256, label=b'\x01')
cipher_1_bob = cipher.encrypt(plain1)

bob.sendline(b'2')
bob.recvuntil(b'message 1: ')
bob.sendline(base64.b64encode(cipher_1_bob))
bob.recvuntil(b'message 2:\n')
message2 = bob.recvline(keepends=False)

alice.recvuntil(b'message 2: ')
alice.sendline(message2)
alice.recvuntil(b'message 3:\n')
cipher3 = alice.recvline(keepends=False)

cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256, label=b'\x03')
plain3 = cipher.decrypt(base64.decodebytes(cipher3))
cipher = PKCS1_OAEP.new(pubkey_bob, hashAlgo=SHA256, label=b'\x03')
cipher_3_bob = cipher.encrypt(plain3)

bob.recvuntil(b'message 3: ')
bob.sendline(base64.b64encode(cipher_3_bob))

bob.recvuntil(b'flag: ')
encrypted_flag = base64.decodebytes(bob.recvline(keepends=False))
nonce = encrypted_flag[:8]
ciphertext = encrypted_flag[8:]
cipher = ChaCha20.new(key = plain1[:16] + plain3, nonce=nonce)
print(cipher.decrypt(ciphertext))

alice.close()
bob.close()
