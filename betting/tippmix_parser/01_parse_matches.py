import time
import random

import requests
import json

url = 'https://api.tippmix.hu/tippmix/search'
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


def fetch_data(page):
	payload = {
		'fieldValue': '',
		'sportId': 1,
		'competitionGroupId': 0,
		'competitionId': 0,
		'competitionType': '',
		'type': 1,
		'date': '0001-01-01T00:00:00.000Z',
		'hitsPerPage': 20,
		'page': page,
		'minOdds': None,
		'maxOdds': None
	}
	time.sleep(random.uniform(0.2, 2))
	response = requests.post(url, headers=headers, json=payload)
	return response.json()


# Main function to retrieve all pages
def fetch_all_pages():
	page = 1
	all_data = []

	while True:
		data = fetch_data(page)
		events = data.get('data', {}).get('events', [])

		if not events:
			break

		all_data.extend(events)
		page += 1

	return all_data


# Retrieve all data
all_events = fetch_all_pages()

# Optionally, write the results to a JSON file
with open('01_all_events.json', 'w') as f:
	json.dump(all_events, f, indent=2)

# You can print some parts of the data
for event in all_events:
	print(f"Event ID: {event['eventId']}, Event Name: {event['eventName']}")

