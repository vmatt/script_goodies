import csv
import subprocess
from datetime import datetime


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


def write_urls_to_csv(csv_file_path, file_netcat_pairs):
    """Writes file and netcat command outputs to a CSV file"""
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Last ran:", datetime.now()])
        writer.writerow(["host_type", "url","status", "netcat_output"])
        for row in file_netcat_pairs:
            writer.writerow(row)

def process_csv(directory):
    """Process each file in the directory to extract URLs, run netcat, and write to a CSV"""
    netcat_pairs = []

    with open("access_check.csv") as f:
        reader = csv.reader(f)
        # skip timestamp and header
        next(reader)
        next(reader)
        for row in reader:
            host_type = row[0]
            url = row[1]
            status, netcat_output = run_netcat_command(url)
            netcat_pairs.append([host_type,url, status, netcat_output])
    return netcat_pairs

# --- Main Execution ---
if __name__ == '__main__':
    csv_file_path = 'access_check.csv'

    file_netcat_pairs = process_csv("access_check.csv")
    if file_netcat_pairs:
        write_urls_to_csv(csv_file_path, file_netcat_pairs)
        print(f"URLs and netcat command outputs have been saved to {csv_file_path}")
    else:
        print("No URLs found to process.")
