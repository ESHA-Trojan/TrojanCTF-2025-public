#!/usr/local/bin/python

from argparse import ArgumentParser
from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Cipher import ChaCha20

import secrets
import base64
import os

NONCE_LEN = 128 // 8
LABEL1 = b'\x01'
LABEL2 = b'\x02'
LABEL3 = b'\x03'
 
def encryptFlag(flag, nonceA, nonceB):
    cipher = ChaCha20.new(key=nonceA + nonceB)
    ciphertext = cipher.encrypt(bytes(flag, 'ascii'))
    # nonce is the first 8 bytes
    return base64.b64encode(cipher.nonce + ciphertext).decode()

def readKeyFile(filename):
    with open(filename, 'r') as pkFile:
        pkData = pkFile.read()
    return RSA.importKey(pkData)

def insertKey():
    name = input("Please input your name: ")

    if keys.get(name) != None:
        print(f"Hacker detected! The public key for {name} is already known")
        return
    e = input("Please input your public key exponent: ")

    n = input("Please input your public key modulus n: ")

    pubkey = RSA.construct((int(n), int(e))).publickey()

    keys[name] = pubkey
    return

def alice(skFilePath):
    privKey = readKeyFile(skFilePath)

    name = input("\nPlease input your name: ")

    if keys[name] is None:
        print(f"no key known for {name}")
        return
    
    pubkey = keys[name]
    nonce = secrets.token_bytes(NONCE_LEN)

    plain1 = nonce + bytes("Alice", 'ascii')
    cipher = PKCS1_OAEP.new(pubkey, hashAlgo=SHA256, label=LABEL1)
    ciphertext1 = cipher.encrypt(plain1)

    print(f"\nHere is message 1:\n{base64.b64encode(ciphertext1).decode()}\n")

    ciphertext2 = input("\nPlease input message 2: ")
    cipher = PKCS1_OAEP.new(privKey, hashAlgo=SHA256, label=LABEL2)
    plain2 = cipher.decrypt(base64.decodebytes(bytes(ciphertext2, 'ascii')))

    if plain2[:NONCE_LEN] != nonce:
        print("hacker detected!! The nonce in message 2 does not match the nonce I sent")
        return

    nonceBob = plain2[NONCE_LEN:]

    cipher = PKCS1_OAEP.new(pubkey, hashAlgo=SHA256, label=LABEL3)
    ciphertext3 = cipher.encrypt(nonceBob)
    
    print(f"\nHere is message 3:\n{base64.b64encode(ciphertext3).decode()}\n")
    print("\nSuccessfully completed the protocol!!\n\n")
    
    return

def bob(skFilePath):
    privKey = readKeyFile(skFilePath)

    ciphertext1 = input("\nPlease input message 1: ")
    cipher = PKCS1_OAEP.new(privKey, hashAlgo=SHA256, label=LABEL1)
    plain1 = cipher.decrypt(base64.decodebytes(bytes(ciphertext1, 'ascii')))

    nonceAlice = plain1[:NONCE_LEN]
    name = str(plain1[NONCE_LEN:], 'ascii')

    if keys.get(name) is None:
        print(f"failed to get public key for {name}")
        return

    pubkey = keys[name]
    nonce = secrets.token_bytes(NONCE_LEN)

    plain2 = nonceAlice + nonce
    cipher = PKCS1_OAEP.new(pubkey, hashAlgo=SHA256, label=LABEL2)
    ciphertext2 = cipher.encrypt(plain2)

    print(f"\nHere is message 2:\n{base64.b64encode(ciphertext2).decode()}\n")

    ciphertext3 = input("\nPlease input message 3: ")
    cipher = PKCS1_OAEP.new(privKey, hashAlgo=SHA256, label=LABEL3)
    plain3 = cipher.decrypt(base64.decodebytes(bytes(ciphertext3, 'ascii')))

    if nonce == plain3:
        if name == "Alice":
            print(f"\nWell done, Alice. Here is the flag: {encryptFlag(flag, nonceA=nonceAlice, nonceB=nonce)}\n\n")
        else:
            print("\nSucces, now do it as Alice!\n\n")
    return

flag = os.environ.get('FLAG', 'Trojan{TEMP}')  # Default flag if not set
role = os.environ.get('ROLE', 'None')

if role != 'Alice' and role != 'Bob':
    print(f"Unknown role: {role}")
    exit(1)

parser = ArgumentParser()

parser.add_argument("-pkalice",  dest="alicePubKeyFile", default=Path("./keys/alice_pem.pub"), type=Path, help="Specify location of Alice's public key file")
parser.add_argument("-pkbob",  dest="bobPubKeyFile", type=Path, default=Path("./keys/bob_pem.pub"), help="Specify location of Bob's public key file")
parser.add_argument("-skalice",  dest="alicePrivKeyFile", type=Path, default=Path("./keys/alice"), help="Specify location of Alice's secret/pivate key file")
parser.add_argument("-skbob",  dest="bobPrivKeyFile", type=Path, default=Path("./keys/bob"), help="Specify location of Bob's secret/private key file")

args = vars(parser.parse_args())

alicePKFileName= args['alicePubKeyFile']
bobPKFileName= args['bobPubKeyFile']
aliceSKFileName= args['alicePrivKeyFile']
bobSKFileName= args['bobPrivKeyFile']

pkAlice = readKeyFile(alicePKFileName)
pkBob = readKeyFile(bobPKFileName)

keys = {}
keys['Alice'] = pkAlice
keys['Bob'] = pkBob

pk = keys[role]
print(f"Hello, I am {role}, here is my public key: (e, n) = ({pk.publickey().e}, {pk.publickey().n})")

while True:
    print("Please choose either option:\n\t1) Import public key\n\t2) Start session\n\t3) exit\n\n")
    choice = input("Choice: ")

    match choice:
        case "1":
            insertKey()
        case "2":
            match role:
                case "Alice":
                    alice(aliceSKFileName)
                case "Bob":
                    bob(bobSKFileName)
                case _:
                    print(f"Unsupported role {role}")
        case "3":
            break
        case _:
            print("Invalid choice, try again")
