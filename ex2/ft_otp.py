import sys
import argparse
import base64
import os
import re

def is_hex_string(s):
    return re.fullmatch(r'[0-9a-fA-F]+', s) is not None


def encrypt(message):
    key = os.urandom(len(message))  # Random key of same length
    encrypted_bytes = bytes([a ^ b for a, b in zip(message.encode(), key)])#pair each byte of the message with the key and xor them
#convert the bytes to a string for printing
    encrypted_b64 = base64.b64encode(encrypted_bytes).decode()
    key_b64 = base64.b64encode(key).decode()

    print(f"Encrypted: {encrypted_b64}")
    print(f"Key: {key_b64}")
    

def decrypt(key_and_encrypted):
    try:
        encrypted_b64, key_b64 = key_and_encrypted.split(',')
        if is_hex_string(key_b64):  
            print("Key is in hexadecimal format!")
            key = bytes.fromhex(key_b64)
        else:
            key = base64.b64decode(key_b64)#string to bytes

        encrypted_bytes = base64.b64decode(encrypted_b64)

        decrypted_bytes = bytes([a ^ b for a, b in zip(encrypted_bytes, key)])
        print(f"Decrypted: {decrypted_bytes.decode()}")

    except Exception as e:
        print(f"Decryption failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="OTP Tools")
    parser.add_argument('-g', type=str, help="Encrypt the given message")
    parser.add_argument('-k', type=str, help="Decrypt a message")
    args = parser.parse_args()

    if args.g:
        encrypt(args.g)
    elif args.k:
        decrypt(args.k)
    else:
        print("Usage: -g 'message' to encrypt or -k 'encrypted,key' to decrypt")
        sys.exit(1)

if __name__ == "__main__":
    main()
