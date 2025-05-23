# Author Writeup
The idea for the challenge was as follows: I wanted to make a challenge that had to be solved using cryptanalysis.
However, a simple charachter for character substitution cipher was a bit too simple, as there are numerous automatic tools to break those online.
Therefor, I made a simple bigram substitution cipher. I checked the frequencies for the most occuring bigrams matched their substitutions for English text and so
I thought this should be a doable exercise: find the most common bigrams in the ciphertext, swap them for the most common bigrams in English text, try to find some words that are almost complete, find new substitutions, repeat.

Clearly, I should have tested the full process of decryption myself at least once to get the full flag, because this is not as easy as I thought...