import os
import pandas as pd
from influxdb import InfluxDBClient
import datetime
from unicodedata import normalize

base_path = 'E:\\ProgramFiles\\Backup'
last_ts_filepath = f'{base_path}\\last_log_timestamp.txt'
ffs_log_parser_log = f'{base_path}\\ffs_log_parser.log'
ffs_logs_location =f'{base_path}\\_LOGS'
influx_host = ""
influx_port = 8086
database = ""
username = ""
password = ""

def basic_logger(msg):
    with open(ffs_log_parser_log, "a", encoding='utf-8') as f:
        print(msg)
        f.write(str(msg)+"\n")


def check_last_ts(timestamp):
    ts = datetime.datetime.strptime(timestamp, '%Y. %m. %d. %H:%M:%S')
    try:
        with open(last_ts_filepath, 'r') as f:
            last_ts = f.read()
            last_ts = datetime.datetime.strptime(last_ts, '%Y. %m. %d. %H:%M:%S')
    except FileNotFoundError:
        with open(last_ts_filepath, 'w') as f:
            f.write(timestamp)
        basic_logger(f"{datetime.datetime.now()}: Új log!")
        return

    if ts <= last_ts:
        basic_logger(f"{datetime.datetime.now()}: Nincs új log!")
        exit()
    else:
        with open(last_ts_filepath, 'w') as f:
            f.write(timestamp)
        basic_logger(f"{datetime.datetime.now()}: Új log!")
        return

# loop through _LOGS folder and parse the latest log
def get_latest_log(log_dir):
    logs = [os.path.join(log_dir, log) for log in os.listdir(log_dir) if log.endswith(".html")]
    latest_log = max(logs, key=os.path.getctime)
    return latest_log

def normalize_string_to_int(string):
    return int(normalize('NFKC', string).replace(" ", "").replace(",", ""))

latest_file = get_latest_log(ffs_logs_location)
try:
    with open(latest_file, "r",encoding='utf-8') as f:
        txt = f.read()
        timestamp = txt.split("""BatchRun</span> &nbsp;<span style="white-space:nowrap">""")[1]
        timestamp = timestamp.split("</span></div>")[0]
        timestamp = timestamp.replace('&nbsp;', '')

    check_last_ts(timestamp)

    df = pd.read_html(latest_file)
    input_dict = df[0].to_dict()
    output_dict = {}
    for key, value in input_dict[0].items():
        output_dict[value] = input_dict[2][key]

    error_count = output_dict.get('Hiba:', "0")
    error_count = normalize_string_to_int(error_count)

    file_count, size = output_dict.get('Feldolgozott elemek száma:', "0 (0)").split(" (")
    file_count = normalize_string_to_int(file_count)

    size = size.replace(")", "")
    time_taken = output_dict.get('Összes időszükséglet:', "0:00:00")

    client = InfluxDBClient(host=influx_host,
                            port=influx_port,
                            ssl=True,
                            verify_ssl=False,
                            username=username,
                            password=password,
                            database=database)

    body = [
        {
            "measurement": "backup",
            "fields": {
                "file_count": file_count,
                "error_count": error_count,
                "size": size,
                "time_taken": time_taken,
                "timestamp": timestamp
            }
        }]
    client.write_points(body)
    print("Done!")
except Exception as e:
    basic_logger(e)


