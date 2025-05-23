# Rolling my own auth
This challenge was also inspired by the course Verification of Security Protocols.
Specifically, this challenge was an implementation of the Needham Schroeder protocol.
The description contained a hint for this, there is a quote from Roger Needham about security protocols:
"they are three line programs that people still manage to get wrong"

The protocol goes as follows:

A -> B: {N_a, A}K_pb
B -> A: {N_b, N_a}K_pa
A -> B: {N_b}K_pb

The protocol was shown to be vulnerable to a MitM attack by Gavin Lowe.
The main issue with the protocol lies in the fact that Bob does not include its identity in the 2nd message.
This allows you to trick Bob into thinking he is communicating with Alice, while Alice thinks she is communicating with someone else. 
This does require Alice to start a session to you first, but this is not a problem for the challenge, you can start any number of instances of the protocol.
See the solve script for an actual implementation of the attack, but here is a high level overview:

1. Register as a new user with Alice
2. Let Alice start a session with you, decrypt her message 1
3. Start a session with Bob, telling him you are alice, re-encrypt message 1 from alice and forward it to bob
4. Forward Bob's response to Alice, Alice thinks it is from you as Bob's name is not included in this message.
5. Alice encrypts N_b with your key, so decrypt that and forward it back again to Bob.
6. Use both Nonces to generate the shared symmetric key and decrypt the flag!