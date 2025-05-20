flag = 'Trojan{M0nkey_speAk_Monk3y_do_monKey_d0nT}'

flag_bytes = bytes(flag, 'utf-8')
flag_bits = ''.join([bin(byte)[2:].zfill(8) for byte in flag_bytes])

flag_bits_monkey = ' '.join(['oo oo' if bit == '0' else 'aa aa' for bit in flag_bits])

print(flag_bits_monkey)
