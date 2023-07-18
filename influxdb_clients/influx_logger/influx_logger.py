#!/volume1/Admin/venv/bin/python
import os
import re

from influxdb import InfluxDBClient
import datetime

backup_log_path = 'synology_backup_list.txt'
log_parser_log = 'synology_influx.log'
influx_host = ""
influx_port = 8086
database = ""
username = ""
password = ""
# if backup_log_path does not exist, create it
if not os.path.exists(backup_log_path):
    with open(backup_log_path, 'w') as f:
        f.write("")
def basic_logger(msg):
    with open(log_parser_log, "a", encoding='utf-8') as f:
        print(msg)
        f.write(f"{datetime.datetime.now()}: {str(msg)}+\n")


def get_file_full_path(log_dir):
    files = []
    for log in os.listdir(log_dir):
        if not log.startswith('.'):
            print(log)
            files.append(os.path.join(log_dir, log))
    return files
def get_latest_log(log_dir):
    logs = get_file_full_path(log_dir)
    latest_log = max(logs)
    return latest_log

def get_path_filename(filename):
    return os.path.normpath(os.path.dirname(os.path.realpath(__file__))) + '/' + filename


try:
    re_backup_folder_path = re.compile(r'\/volume1\/(\w+)\/')
    log_file_path = get_path_filename('../synoscheduler')
    rsync_file_cnt = 0

    client = InfluxDBClient(host=influx_host,
                            port=influx_port,
                            ssl=True,
                            verify_ssl=False,
                            username=username,
                            password=password,
                            database=database)

    for script_log_folder in get_file_full_path(log_file_path):
        latest_log = get_latest_log(f"{script_log_folder}")
        if latest_log in open(backup_log_path).read():
            basic_logger(f"{latest_log} already processed")
            continue

        with open(backup_log_path, 'a') as f:
            f.write(latest_log+"\n")
        with open(f"{latest_log}/script.log", 'r', encoding='utf-8') as f:
            backup_name = re_backup_folder_path.findall(f.read())
        if backup_name:
            backup_name = backup_name[0]
            if backup_name == 'Admin':
                continue
            with open(f'{latest_log}/output.log', 'r', encoding='utf-8') as f:
                rsync_file_cnt = len(f.readlines())

            body = [
                {
                    "measurement": "backup",
                    "tags": {
                        "backup_name": backup_name
                    },
                    "fields": {
                        "file_count": rsync_file_cnt
                    }
                }]
            client.write_points(body)
    print("Done!")
except Exception as e:
    basic_logger(e)


