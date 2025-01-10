import fitz  # PyMuPDF
import re
import csv
import os
import subprocess  # Import subprocess module

# Regular expression pattern for finding URLs
url_pattern = r'\/URI \((.*)\)'

def run_netcat_command(url_cmd):
    """Runs the netcat command and returns the output"""
    try:
        print(f"Running netcat command: {url_cmd}")
        cmd_parts = url_cmd.split()
        # Run the netcat command and capture the output
        result = subprocess.run(cmd_parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        res = result.stdout + " " + result.stderr
        status = "Unknown"
        if "Error:" in res:
            status = "Error"
        if "lookup failed" in res:
            status = "Lookup failed"
        if "Operation timed out" in res:
            status = "Timeout"
        if ") open" in res:
            status = "Success"
        print(res)
        return status,res # return both stdout and stderr
    except Exception as e:
        print(f"Error running netcat command {url_cmd}: {e}")
        return "Error executing command"

def cleanup_urls(urls):
    new_urls = set()
    for url in urls:
        if "confluence." in url or "jira." in url:
            continue
        url = url.replace("http://", "").replace("https://", "")
        url = url.split("/")[0]
        if ".rds." in url:
            # url = f"nc -vzw1 {url} 3306"
            continue
        else:
            url = f"nc -vzw1 {url} 443"
        new_urls.add(url)
    return new_urls

def extract_urls_from_pdf(file_path):
    """Extracts URLs from a given PDF file"""
    urls = set()
    try:
        doc = fitz.open(file_path)
        for i in range(1, doc.xref_length()):
            refs = doc.xref_object(i)  # Pre-cache text
            # Extract text from each page and find URLs
            urls.update(re.findall(url_pattern, refs))
        doc.close()
        urls = cleanup_urls(urls)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return urls

def write_urls_to_csv(csv_file_path, file_netcat_pairs):
    """Writes file and netcat command outputs to a CSV file"""
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["filename", "url","status", "netcat_output"])  # Updated header
        for row in file_netcat_pairs:
            writer.writerow(row)

def process_files(directory):
    """Process each file in the directory to extract URLs, run netcat, and write to a CSV"""
    file_netcat_pairs = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.lower().endswith('.pdf'):
                full_path = os.path.join(root, file_name)
                urls = extract_urls_from_pdf(full_path)

                # Updated logic to run netcat and capture output
                netcat_pairs = []
                for url in urls:
                    status, netcat_output = run_netcat_command(url)
                    file_netcat_pairs.append([file_name, url, status, netcat_output])
                file_netcat_pairs.extend(netcat_pairs)

    return file_netcat_pairs

# --- Main Execution ---
if __name__ == '__main__':
    directory_path = "files"
    csv_file_path = 'extracted_urls_and_netcat_outputs.csv'

    file_netcat_pairs = process_files(directory_path)
    if file_netcat_pairs:
        write_urls_to_csv(csv_file_path, file_netcat_pairs)
        print(f"URLs and netcat command outputs have been extracted and saved to {csv_file_path}")
    else:
        print("No URLs found or no PDF files to process.")
