#!/usr/bin/env python3
\"\"\"
Utility script to generate a secure encryption key for session storage.
\"\"\"

from cryptography.fernet import Fernet
import base64
import sys

def generate_encryption_key():
    \"\"\"Generate a new encryption key and print it in base64 format.\"\"\"
    key = Fernet.generate_key()
    encoded_key = base64.b64encode(key).decode()
    print(encoded_key)
    return encoded_key

if __name__ == \"__main__\":
    print(\"Session Encryption Key:\")
    generate_encryption_key()
    print(\"\\nAdd this key to your environment variables as SESSION_ENCRYPTION_KEY\")