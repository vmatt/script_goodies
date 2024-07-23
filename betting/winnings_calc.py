import os
import pandas as pd


def process_file(df, bet_amount, odds_threshold):
    # Initialize balances and counters
    starting_balance = 0
    ending_balance = 0
    total_matches = 0
    lost_matches = 0

    # Loop over each match in the DataFrame
    for index, row in df.iterrows():
        bet_home = row['B365H'] < row['B365A']
        stronger_team_odds = row['B365H'] if bet_home else row['B365A']

        # Check if the stronger team's odds are under the provided threshold
        if stronger_team_odds < odds_threshold:
            total_matches += 1

            # Determine if the bet is won or lost
            win_condition = (bet_home and row['FTR'] == 'H') or (not bet_home and row['FTR'] == 'A') or (
                row['FTHG'] > 0 and row['FTAG'] > 0)

            if win_condition:
                profit = bet_amount * (stronger_team_odds - 1)
                ending_balance += bet_amount + profit
            else:
                ending_balance -= bet_amount
                lost_matches += 1

            # Update the starting balance dynamically to ensure enough funds
            if ending_balance < 0:
                starting_balance += -ending_balance
                ending_balance = 0

    lost_percent = (lost_matches / total_matches) * 100 if total_matches > 0 else 0
    total_staked_money = bet_amount * total_matches  # Total invested money
    profit = ending_balance - total_staked_money  # Profit calculation
    avg_profit_per_game = (profit / total_matches) if total_matches > 0 else 0  # Adjusted for division by zero

    return starting_balance, total_staked_money, ending_balance, profit, total_matches, avg_profit_per_game, lost_matches, lost_percent


def main():
    bet_amount = 100000  # Amount bet on each match in HUF
    odds_range = [1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]  # Define the range of odds to test

    # Create or clear the stats file
    with open("total_stats.csv", "w") as f:
        f.write("League,StartingBalance,TotalStakedMoney,EndingBalance,Profit,TotalMatches,ProfitPerGame,LostMatches,LostPercent,OptimalOdds\n")

    results = []

    # Walk through the "leagues" directory
    for root, _, files in os.walk("leagues"):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                best_avg_profit = float('-inf')  # Initialize with minus infinity to find the maximum
                optimal_odds = 0
                best_stats = None

                for odds_threshold in odds_range:
                    stats = process_file(df, bet_amount, odds_threshold)

                    # Update if the new average profit per game is better
                    if stats[5] > best_avg_profit:
                        best_avg_profit = stats[5]
                        optimal_odds = odds_threshold
                        best_stats = stats

                filename = file_path.split('.')[0].split('/')[-1]
                results.append((filename,) + best_stats + (optimal_odds,))

    # Write all results to the stats file at once
    with open("total_stats.csv", "a") as f:
        for result in results:
            f.write(",".join(map(str, result)) + "\n")


if __name__ == "__main__":
    main()
