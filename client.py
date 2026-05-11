import socket
import random
import string

from rsa import rsa_encrypt, encrypt, decrypt

client = socket.socket()
client.connect(("127.0.0.1", 5000))

# --- RECEIVE PUBLIC KEY ---
public_key = eval(client.recv(4096).decode())

# --- GENERATE RANDOM SESSION KEY ---
session_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(10, 20)))

# --- SEND ENCRYPTED SESSION KEY ---
encrypted_key = rsa_encrypt(session_key, public_key)
client.send(str(encrypted_key).encode())

print("Public Key : ", public_key)

print("Session Key : ", session_key)
print("RSA Encrypted Session Key : ", encrypted_key)


print("[*] Session key established")

# --- AUTH ---
print(client.recv(1024).decode(), end="")
username = input()
client.send(username.encode())

challenge = client.recv(1024).decode()

password = input("Password: ")

from auth import solve_challenge
response = solve_challenge(challenge, password)
client.send(response.encode())

auth_status = decrypt(eval(client.recv(4096).decode()), session_key)
print(auth_status)

if "FAILED" in auth_status:
    client.close()
    exit()


while True:
    cmd = input(">> ")

    client.send(str(encrypt(cmd, session_key)).encode())

    response = client.recv(65536)
    data = response.decode()

    try:
        parsed = eval(data)
    except:
        print("Server sent invalid/incomplete data:")
        print(data)
        continue

    print("Server:", decrypt(parsed, session_key))
    
    if cmd.upper() == "EXIT":
        break

client.close()