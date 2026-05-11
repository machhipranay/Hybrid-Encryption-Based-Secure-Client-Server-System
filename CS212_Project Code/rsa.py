import random
from math import gcd

def generate_prime():
    primes = [
      10007, 10009, 10037, 10039, 10061,
      10067, 10069, 10079, 10091, 10093,
      10099, 10103, 10111, 10133, 10139,
      10141, 10151, 10159, 10163, 10169
    ]
    return random.choice(primes)  

def mod_inverse(e, phi):
    for d in range(1, phi):
        if (e * d) % phi == 1:
            return d

def generate_keys():
    a = generate_prime()
    b = a
    while( b == a):
        b = generate_prime()

    p = max(a, b)
    q = min(a, b)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 3
    while gcd(e, phi) != 1:
        e += 2

    d = mod_inverse(e, phi)

    return (e, n), (d, n)  # public / priv key


def rsa_encrypt(msg, pub_key):
    e, n = pub_key
    return [pow(ord(c), e, n) for c in msg]

def rsa_decrypt(encrypted_msg, priv_key):
    d, n = priv_key
    return ''.join(chr(pow(c, d, n)) for c in encrypted_msg)

def generate_keystream(key, length):
    seed = sum(ord(c) for c in key)
    stream = []

    for i in range(length):
        seed = (seed * 1103515245 + 12345) % (2**31)
        stream.append(seed % 256)

    return stream

def encrypt(msg, key):
    keystream = generate_keystream(key, len(msg))
    
    cipher = []
    for i, ch in enumerate(msg):
        val = (ord(ch) ^ keystream[i])
        val = (val + keystream[i]) % 256
        cipher.append(val)

    return cipher

def decrypt(cipher, key):
    keystream = generate_keystream(key, len(cipher))
    
    msg = ""
    for i, val in enumerate(cipher):
        val = (val - keystream[i]) % 256
        val = val ^ keystream[i]
        msg += chr(val)

    return msg

def analysis_accuracy_of_symmetric_key(key):
    import random

    res = f"Testing symmetric key encryption-decryption accuracy with key: {key}\n\n"

    cnt = 0
    total = 0

    while total != 100:
        msg = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ ") for _ in range(random.randint(1, 50)))
        total += 1

        cipher = encrypt(msg, key)
        decrypted_msg = decrypt(cipher, key)

        if msg == decrypted_msg:
            res += f"{msg} -> {decrypted_msg} ✓\n"
            cnt += 1
        else:
            res += f"{msg} -> {decrypted_msg} ✗\n"

    res += '\n'
    res += "-------------------------------------------------------------------\n"
    res += f"Tested: {total} | Correct: {cnt} | Accuracy: {cnt/total:.2%}\n"
    res += f"Accuracy: {cnt}/{total} = {cnt/total:.2%}\n"
    res += "-------------------------------------------------------------------\n"

    return res

if( __name__ == "__main__" ):
  print(analysis_accuracy_of_symmetric_key("mysecret123"))

# public_key, private_key = generate_keys()
# session_key = "mysecret123"
# encrypted_key = rsa_encrypt(session_key, public_key)
# decrypted_key = rsa_decrypt(encrypted_key, private_key)

# msg = ""
# while( msg != "EXIT" ):
#     msg = input("Message (EXIT to quit): ")
#     cipher = encrypt(msg, session_key)
#     print("Cipher:", cipher)

#     decrypted_msg = decrypt(cipher, decrypted_key)
#     print("Decrypted:", decrypted_msg)

#     print()