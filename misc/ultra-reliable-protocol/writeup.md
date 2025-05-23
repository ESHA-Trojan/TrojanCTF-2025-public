# Ultra Reliable Protocol
## Disclaimer
Unfortunately, something went wrong and the source code was not provided during the CTF. That made this challenge basically a big guess.
A number of people still solved it, but I hope this writeup can clarify a bit the idea behind it.

## writeup
This challenge was inspired by the course Verification of Security Protocols at the TU/e.
It is a small demo of the type confusion discussed in one of the first lectures.

The main idea is this: if a key is used for multiple messages, there must be a way to identify what the type of each message is.
If this is not the case, it might lead to a confusion between the messages, which could lead to the disclosure of secret information.

The protocol is supposed to be executed as follows:

1. Bob sends message 1 (Flag1, Nonce1) encrypted to Alice
2. Bob sends message 2 (Nonce2, Flag2) encrypted to Alice.
3. Alice responds with Nonce1 as an acknowledgement.
4. Alice responds with Nonce2 as an acknowledgement.

Since the flag pieces as well as the nonces are strings of equal length, Alice has no way of identifying which message is which, 
especially since no tags were used in the encryption (I assume this is the exact reason why tags are used here).
To solve the challenge, it suffices to let Alice receive the messages in the wrong order, because then the Flag pieces will be seen as the Nonces and will be 
returned to the solver.
