# main.py
import os
import argparse
import base64
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from colorama import Fore, Style, init

init(autoreset=True)

def derive_key(secret_phrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(secret_phrase.encode()))

def encrypt_file(file_path, fernet):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        enc_data = fernet.encrypt(data)
        with open(file_path + '.enc', 'wb') as f:
            f.write(enc_data)
        os.remove(file_path)
        print(f"{Fore.GREEN}[Encrypted]{Style.RESET_ALL} {file_path}")
    except Exception as e:
        print(f"{Fore.RED}[Error] {file_path}: {e}")

def decrypt_file(file_path, fernet):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        dec_data = fernet.decrypt(data)
        original = file_path.replace('.enc', '')
        with open(original, 'wb') as f:
            f.write(dec_data)
        os.remove(file_path)
        print(f"{Fore.CYAN}[Decrypted]{Style.RESET_ALL} {original}")
    except Exception as e:
        print(f"{Fore.RED}[Error] {file_path}: {e}")

def save_key_file(path, key, salt):
    with open(path, 'wb') as f:
        f.write(salt + b':' + key)
        

def load_key_file(path):
    with open(path, 'rb') as f:
        content = f.read()
        salt, key = content.split(b':')
    return salt, key

def process_directory(path, fernet, encrypt=True):
    for root, _, files in os.walk(path):
        for name in files:
            full_path = os.path.join(root, name)
            if name.endswith('.key'):
                continue
            if encrypt and not name.endswith('.enc'):
                encrypt_file(full_path, fernet)
            elif not encrypt and name.endswith('.enc'):
                decrypt_file(full_path, fernet)

def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt files in a directory.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--encrypt', help='Encrypt the directory', metavar='DIR')
    group.add_argument('--decrypt', help='Decrypt the directory', metavar='DIR')
    args = parser.parse_args()

    path = args.encrypt or args.decrypt
    if not os.path.isdir(path):
        print(Fore.RED + "❌ Error: Provided path is not a directory.")
        return

    key_file = os.path.join(path, ".key")
    encrypt_mode = bool(args.encrypt)

    if encrypt_mode:
        phrase = getpass.getpass(Fore.YELLOW + "🔐 Enter secret phrase to encrypt: ")
        salt = os.urandom(16)
        key = derive_key(phrase, salt)
        save_key_file(key_file, key, salt)
        fernet = Fernet(key)
        process_directory(path, fernet, encrypt=True)
        print(Fore.GREEN + f"\n✅ Encrypted. Key saved to: {key_file}")
    else:
        if not os.path.exists(key_file):
            print(Fore.RED + "❌ No .key file found in this directory.")
            return
        phrase = getpass.getpass(Fore.YELLOW + "🔑 Enter secret phrase to decrypt: ")
        salt, saved_key = load_key_file(key_file)
        try:
            derived_key = derive_key(phrase, salt)
            if derived_key != saved_key:
                raise ValueError("Invalid secret phrase.")
            fernet = Fernet(derived_key)
            process_directory(path, fernet, encrypt=False)
            print(Fore.CYAN + "\n✅ Decryption complete.")
        except Exception as e:
            print(Fore.RED + f"❌ Failed to decrypt: {e}")

if __name__ == "__main__":
    main()
