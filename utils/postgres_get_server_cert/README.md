# PostgreSQL Server Certificate Extractor

A utility script to fetch and save SSL certificates from PostgreSQL servers.

## Features
- Connects to PostgreSQL servers using their hostname/IP and port
- Retrieves SSL certificates in PEM format
- Supports TLS protocol versions
- Handles connection timeouts and SSL errors

## Requirements
```bash
pip install pycrypto
```

## Usage
```bash
python postgres_get_server_cert.py [database_url]
```

Example:
```bash
python postgres_get_server_cert.py postgres.example.com:5432
```
