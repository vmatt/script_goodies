import json
# Structure to store extracted information
extracted_data = []
data = json.load(open('01_all_events.json'))
for event in data:
	event_id = event["eventId"]
	event_name = event["eventName"]
	event_date = event["eventDate"]

	# Assuming there's only one market with outcomes
	try:
		market_outcomes = event["markets"][0]["outcomes"]
	except:
		continue

	home_odds = next(outcome["fixedOdds"] for outcome in market_outcomes if outcome["outcomeNo"] == 1)
	draw_odds = next(outcome["fixedOdds"] for outcome in market_outcomes if outcome["outcomeNo"] == 2)
	away_odds = next(outcome["fixedOdds"] for outcome in market_outcomes if outcome["outcomeNo"] == 3)

	extracted_data.append([event_id, event_name, event_date, home_odds, draw_odds, away_odds])

# Create a spreadsheet (CSV format)
import csv

with open('event_odds.csv', mode='w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(["Event ID", "Event Name", "Event Date", "Home Odds", "Draw Odds", "Away Odds"])
	writer.writerows(extracted_data)

print("Data extraction complete. The spreadsheet 'event_odds.csv' has been created.")
