
pwd = "Trojan{TAk3_m7_hAnD_c0m3_baCK_t0_th3_Land}"

print('int pass[] = {', end='')
for i in range(5, 5 + len(pwd) - 1):
    print(ord(pwd[i - 5]) + i, end=', ')

print(f'{ord(pwd[-1]) + 5 + len(pwd) - 1}}};')
