import hashlib
import os

USERS = {
    "admin": "admin123",
    "user": "user123"
}

def generate_challenge():
    return os.urandom(16).hex()

def solve_challenge(challenge, secret):
    return hashlib.sha256((challenge + secret).encode()).hexdigest()  

def verify(username, challenge, response):
    if username not in USERS:
        return False
    
    expected = solve_challenge(challenge, USERS[username])
    return expected == response