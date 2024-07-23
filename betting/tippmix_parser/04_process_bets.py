import csv
import json

def process_api_response(api_response):
    markets_info = []
    for market in api_response['event']['markets']:
        market_name = market['marketName']
        count = 0
        if "nyer vagy mindkét" in market_name and ("Hazai" in market_name or "Vendég" in market_name):
            market_name = market_name.replace("csapat nyer","").replace("csapat szerez gólt","")
            for outcome in market['outcomes']:
                if outcome['outcomeNo'] in [1]:
                    market_name_yn = f"{market_name} - {outcome['outcomeName']}"
                    fixed_odds = outcome['fixedOdds']
                    markets_info.append((market_name_yn, fixed_odds,market['marketRealNo'],outcome['outcomeRealNo']))
            count += 1
            if count < 2:
                break
    if len(markets_info) > 0:
        return markets_info
    for market in api_response['event']['markets']:
        market_name = market['marketName']
        if "t visszaj" in market_name:
            for outcome in market['outcomes']:
                if outcome['outcomeNo'] in [1, 2]:
                    market_name_yn = f"{market_name} - {outcome['outcomeName']}"
                    fixed_odds = outcome['fixedOdds']
                    markets_info.append((market_name_yn, fixed_odds,market['marketRealNo'],outcome['outcomeRealNo']))
                    if len(markets_info) >= 2:
                        return markets_info
    return markets_info


def main(api_responses_file, output_file, odds_threshold):
    with open(api_responses_file, 'r') as json_file:
        api_responses = json.load(json_file)

    with open(output_file, mode='w', newline='') as file:
        fieldnames = ['Event ID', 'Event Name', 'Event Date', 'Picked Odds', 'Profit', 'Market ID', 'Picked Outcome ID',
                      'Home Odds', 'Draw Odds', 'Away Odds', 'Market 1 Name',
                      'Fixed Odds 1', 'Outcome ID 1', 'Market 2 Name', 'Fixed Odds 2', 'Outcome ID 2']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for api_response in api_responses:
            event_id = api_response['event']['eventId']
            event_name = api_response['event']['eventName']
            event_date = api_response['event']['eventDate']
            outcomes = api_response['event']['markets'][0]['outcomes']
            markets_info = process_api_response(api_response)

            if markets_info:
                row = {
                    'Event ID': event_id,
                    'Event Name': event_name,
                    'Event Date': event_date,
                    'Home Odds': outcomes[0]['fixedOdds'],
                    'Draw Odds': outcomes[1]['fixedOdds'],
                    'Away Odds': outcomes[2]['fixedOdds']
                }
                if row['Home Odds'] > odds_threshold and row['Away Odds'] > odds_threshold:
                    continue
                picked_odds = float('inf')
                picked_outcome_id = None
                market_id = None

                for i, (market_name, fixed_odds, market_id, outcome_id) in enumerate(markets_info[:2]):
                    row[f'Market {i + 1} Name'] = market_name
                    row[f'Fixed Odds {i + 1}'] = fixed_odds
                    row[f'Outcome ID {i + 1}'] = outcome_id
                    if fixed_odds < picked_odds:
                        picked_odds = fixed_odds
                        picked_outcome_id = outcome_id
                        market_id = market_id

                row['Picked Odds'] = picked_odds
                row['Market ID'] = market_id
                row['Picked Outcome ID'] = picked_outcome_id
                row['Profit'] = "=5000*(D2-1)"
                writer.writerow(row)

if __name__ == "__main__":
    api_responses_file = '03_api_responses.json'
    output_file = '04_bets.csv'
    odds_threshold = 1.5
    main(api_responses_file, output_file, odds_threshold)
