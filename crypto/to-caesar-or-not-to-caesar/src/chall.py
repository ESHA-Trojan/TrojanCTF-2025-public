#! /usr/bin/python3

import re
import random

with open('./julius-caesar_TXT_FolgerShakespeare.txt') as original:
    orig_lines = original.readlines()

concatenaded = "".join(orig_lines)
allinone = "".join(concatenaded.split())
# allinone = re.sub(r'\s', '_', concatenaded)
allinone = re.sub(r'[^a-zA-Z]', '', allinone) 

# print(allinone)

# make sure the flag has length = 2 mod 3
flag = "trojanbigramfrequencyanalysisftw"

allinone += flag
allinone = allinone.lower()

alphabet = "abcdefghijklmnopqrstuvwxyz" 
ngrams = [a + b for a in alphabet for b in alphabet]

key = ngrams.copy()
random.shuffle(key)
print("Key shuffled")

n = 2
cyphertext = ""
keyMap = dict(zip(ngrams, key))
for ngram in [allinone[i:i+n].ljust(n, "_") for i in range(0, len(allinone), n)]:
    cyphertext += keyMap.get(ngram)

with open('./ciphertext.txt', 'w') as output:
    print(cyphertext, file=output)

cleartext = ""
keyDecMap = dict(zip(key, ngrams))
for ngram in [cyphertext[i:i+n].ljust(n, "_") for i in range(0, len(cyphertext), n)]:
    cleartext += keyDecMap.get(ngram)

with open('./caesar_reconstructed.txt', 'w') as output:
    print(cleartext, file=output)

