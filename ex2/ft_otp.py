import sys
import argparse
import base64
import os

#-g for store and encrypt the key
#-k for decrypt the key

def check_valid_hex_key(file_path):
    if not os.path.isfile(file_path):
        print("File does not exist.")
        return False

    with open(file_path, 'r') as f:
        content = f.read().strip()

    # Check if content is exactly 64 hex characters
    if re.fullmatch(r'[0-9a-fA-F]{64}', content):
        print("Valid 64-character hex key found.")
        return True
    else:
        print("Invalid key: Must be exactly 64 hexadecimal characters.")
        return False


def Encrypt(message):
    key = os.urandom(len(message))  # Generate a random key
    encrypted_bytes = bytes([a ^ b for a, b in zip(message.encode(), key)])
    
    # Encode both the encrypted message and key in base64 for safe printing
    encrypted_b64 = base64.b64encode(encrypted_bytes).decode()
    key_b64 = base64.b64encode(key).decode()

    print(f"Encrypted: {encrypted_b64}")
    print(f"Key: {key_b64}")


def Decrypt(key_and_encrypted):
    try:
        encrypted_b64, key_b64 = key_and_encrypted.split(',')
        encrypted_bytes = base64.b64decode(encrypted_b64)
        key = base64.b64decode(key_b64)

        decrypted_bytes = bytes([a ^ b for a, b in zip(encrypted_bytes, key)])
        print(f"Decrypted: {decrypted_bytes.decode()}")
    except Exception as e:
        print(f"Decryption failed: {e}")








def main():

    if len(sys.argv) < 2:
        print("Error")
        sys.exit(1)

    parser = argparse.ArgumentParser(description = "OTP KEY")
    parser.add_argument('-k', type=syr , help = "Decrypt the Key ")
    parser.adda_rgument('-g', type=str , help="Encryt the Key ")
    args = parser.parse_args()

    if args.g:
        Encryt(int key)

    elif args.k:
        chex
        Decrypt(int key)
        
    else   
        print("please include only g or k")
        sys.exit(1)
  

if __name__ == "__main__":
    main()
