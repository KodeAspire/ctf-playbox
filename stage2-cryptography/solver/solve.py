import base64

with open("../challenge/encoded_message.txt") as f:
    data = f.read().strip()

decoded = base64.b64decode(data).decode()

for shift in range(26):
    out = ""
    for c in decoded:
        if c.isupper():
            out += chr((ord(c) - 65 - shift) % 26 + 65)
        elif c.islower():
            out += chr((ord(c) - 97 - shift) % 26 + 97)
        else:
            out += c

    if "FLAG{" in out:
        print(f"Shift {shift}: {out}")