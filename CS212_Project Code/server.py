import socket
import threading

from rsa import generate_keys, rsa_decrypt, encrypt, decrypt
from auth import generate_challenge, verify
from commands import handle_command, stats

print("Starting server... wait for it to initialize...")

# RSA keys once TO have commonf key
public_key, private_key = generate_keys()

print("RSA Private Key:", private_key)
print("RSA Public Key:", public_key)

def handle_client(conn, addr):
    print(f"[+] Connected: {addr}")

    try:
        # Key Exchange to generate session's symmetric Key
        # asym -> sym key exchange using RSA
        
        conn.send(str(public_key).encode())

        encrypted_session_key = eval(conn.recv(1024).decode())
        session_key = rsa_decrypt(encrypted_session_key, private_key)
        print("RSA Encrypted Session Key:", encrypted_session_key)
        print("RSA Decrypted Session Key:", session_key)


        print(f"[*] Session key established: {session_key}")
        print("\t This should be stored in Server memory securely so that noone can get this key")

        # --- AUTH ( USER / ADMIN ) ---
        conn.send(b"Username: ")
        username = conn.recv(1024).decode()

        challenge = generate_challenge()
        conn.send(challenge.encode())

        response = conn.recv(1024).decode()

        if not verify(username, challenge, response):
            conn.send(encrypt("AUTH FAILED", session_key).__str__().encode())
            conn.close()
            return

        role = "admin" if username == "admin" else "user"

        msg = "AUTH SUCCESS\n\n" + handle_command("HELP", role)
        conn.send(str(encrypt(msg, session_key)).encode())

        stats["clients"] += 1



        while True:
            data = conn.recv(1024)
            if not data:
                break

            cmd = decrypt(eval(data.decode()), session_key)

            result = handle_command(cmd, role)
            conn.send(str(encrypt(result, session_key)).encode())

            if cmd.upper() == "EXIT":
                break

    except Exception as e:
        print("Error:", e)

    finally:
        print(f"[-] Disconnected: {addr}")
        conn.close()

server = socket.socket()
server.bind(("0.0.0.0", 5000))
server.listen()

print("[*] Server listening on port 5000...")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()