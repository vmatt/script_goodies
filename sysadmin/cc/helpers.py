import os
import subprocess

def generate_ssl_key():
    key_path = "server.key"
    cert_path = "server.crt"

    # Check if key file already exists
    if os.path.isfile(key_path):
        print("SSL key file already exists.")
        return

    print("Generating new SSL key file...")
    subprocess.run(["openssl", "genrsa", "-out", key_path, "2048"])

    print("Generating new SSL certificate...")
    subprocess.run(["openssl", "req", "-new", "-x509", "-key", key_path, "-out", cert_path, "-days", "365", "-subj", "/CN=localhost"])
    print("SSL key and certificate generated successfully.")
