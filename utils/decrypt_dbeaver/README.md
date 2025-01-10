# DBeaver Password Decryptor

A utility to decrypt stored credentials from DBeaver's credentials-config.json file.

## Features
- Supports multiple DBeaver installation paths
- Decrypts AES encrypted credentials
- Outputs in formatted JSON
- Cross-platform support (Windows, Linux, macOS)

## Requirements
```bash
pip install pycryptodome
```

## Usage
```bash
python decrypt_dbeaver.py [path_to_credentials_config.json]
```

If no path is provided, the script will check common default locations.
