import base64

plain = "The person of interest is Leopold Lizard. FLAG{l1z4rd_c1ph3r}"
shift = 3

caesar = ""
for c in plain:
    if c.isupper():
        caesar += chr((ord(c) - 65 + shift) % 26 + 65)
    elif c.islower():
        caesar += chr((ord(c) - 97 + shift) % 26 + 97)
    else:
        caesar += c

encoded = base64.b64encode(caesar.encode()).decode()
print(encoded)