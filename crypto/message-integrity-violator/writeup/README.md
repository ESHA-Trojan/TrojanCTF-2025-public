How to Solve (Hidden from Players)

•	Append the padding to the payload \
•	(optionally) Append new data (e.g., &role=admin) to the original payload. \
•	Compute the new MAC using the length extension attack. \
•	URL-encode the extended payload and submit it. 

To get the new MAC:
1)	Let payload = guest&role=member;
2)	Let input_to_hash = secret_key + guest&role=member
3)	Let payload_new = user=guest&role=member + padding(input_to_hash) + &role=admin
4)	MAC(payload_new) = compression_function(IV = MAC(payload), message = &role=admin + padding(payload_new))

Use solution.py to get the new url-encoded data field and the corresponding MAC.
