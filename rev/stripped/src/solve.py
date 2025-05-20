pass_encoded = [
    89, 120, 118, 114, 106, 120, 134, 96, 78, 121, 66, 111, 126, 73, 114, 124,
    86, 132, 91, 119, 124, 74, 136, 79, 124, 128, 128, 99, 108, 129, 151, 84,
    132, 154, 143, 91, 136, 118, 140, 154, 145, 171
]

flag = []
for index, value in enumerate(pass_encoded):
    # Reverse: pass[index] = ord(char) + (5 + index)
    original_char = value - (5 + index)
    flag.append(chr(original_char))

print("".join(flag))
