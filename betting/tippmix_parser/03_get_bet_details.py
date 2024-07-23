import csv
import random
import time
import requests
import json
from tqdm import tqdm

def call_api(event_id):
    time.sleep(random.uniform(0.2, 2))
    url = f'https://api.tippmix.hu/v2/tippmix/event/{event_id}/ungrouped?compatibility=v1'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.tippmix.hu',
        'Pragma': 'no-cache',
        'Referer': 'https://www.tippmix.hu/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def main(input_file):
    filtered_events = []
    with open(input_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            filtered_events.append(row)

    api_responses = []
    with tqdm(total=len(filtered_events)) as pbar:
        for event in filtered_events:
            event_id = event['Event ID']
            pbar.set_description(event['Event Name'])
            pbar.update(1)
            api_response = call_api(event_id)
            api_responses.append(api_response)

    with open('03_api_responses.json', 'w') as json_file:
        json.dump(api_responses, json_file, indent=4)

if __name__ == "__main__":
    input_file = '02_event_odds.csv'
    main(input_file)
