flag = "THM{thisisafakeflag}"
encoded_hex = "PASTE_HEX_HERE"

# Convertemos de hex para bytes XORed
xored = bytes.fromhex(encoded_hex)

# Vamos testar todas as combinações de 5 caracteres (letras e números)
import itertools
import string

charset = string.ascii_letters + string.digits

for candidate in itertools.product(charset, repeat=5):
    key = ''.join(candidate)
    decrypted = ""
    for i in range(len(flag)):
        decrypted += chr(xored[i] ^ ord(key[i % len(key)]))
    if decrypted == flag:
        print("[+] Found key:", key)
        break
