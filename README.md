# 🔐 File Encryption & Generation Tool

A powerful utility for **generating structured file trees** with customizable content and **encrypting/decrypting** them securely using a passphrase-based symmetric encryption method.

---

## 🚀 Overview

This project provides a complete solution for:

1. **File Generation** – Create text and binary files with randomized content in a structured folder hierarchy.
2. **File Encryption/Decryption** – Secure your files using encryption based on a passphrase-derived key (Fernet encryption).

---

## ✨ Features

### 📁 File Generation
- Generate **text and binary files** with customizable extensions.
- Control over:
  - Subfolders per level
  - Folder depth
  - Number of files per folder
- Randomized content:
  - Text files: ASCII content
  - Binary files: Random bytes

### 🔒 File Encryption
- Uses **Fernet symmetric encryption** (`cryptography` package).
- Secret phrases are securely converted into encryption keys.
- Saves the key to a `.key` file (one per encrypted directory).

### 🔓 File Decryption
- Decrypts files using the same secret phrase.
- Fully restores the original file content.

---

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Aminiow/FileEncryption.git
   cd FileEncryption
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧪 Usage Guide

### ✅ File Generation

Run the generator:

```bash
python App/helper.py
```

You'll be prompted for:
- Base directory path
- Number of subfolders per level
- Folder depth
- Number of files per folder
- Text file extensions (e.g., `.txt`, `.log`)
- Binary file extensions (e.g., `.bin`, `.dat`)
- Size and ratio of binary files

---

### 🔐 Encrypt Files

To encrypt all files in a directory recursively:

```bash
python App/main.py --encrypt <directory_path>
```

- You'll be asked to input a secret phrase.
- A `.key` file will be saved in the root of the target directory.

---

### 🔓 Decrypt Files

To decrypt previously encrypted files:

```bash
python App/main.py --decrypt <directory_path>
```

- Enter the same secret phrase used during encryption.
- Files will be restored to their original contents.

---

## 📁 Project Structure

```
FileEncryption/
├── App/
│   ├── helper.py        # File generator script
│   ├── main.py          # Encrypt/decrypt script
│   ├── requirements.txt # Dependencies
│   └── Files/           # (Optional) folder to store generated files
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚠️ Notes

- ⚠️ This tool is **not meant for high-security data** protection.
- The `.key` file must be preserved for successful decryption.
- The encryption is based on a **passphrase**, not biometric or hardware-level security.

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**.  
See the [LICENSE](LICENSE) file for full details.

---

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome!  
Feel free to open an [issue](https://github.com/Aminiow/FileEncryption/issues) or submit a pull request.

---

## 🙏 Acknowledgments

- Powered by the excellent [`cryptography`](https://cryptography.io/) Python library.
- Inspired by the need for structured test data and secure offline encryption tools.

---

📂 **GitHub Repository:** [Aminiow/FileEncryption](https://github.com/Aminiow/FileEncryption)
