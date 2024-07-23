import pandas as pd

def process_file(file_path):

    filename = file_path.split('.')[0].split('/')[-1]
    df = pd.read_csv(file_path)
    # Find matches where stronger team (based on odds) didn't score a goal
    matches_no_goal = []

    for index, row in df.iterrows():
        # Home team is stronger
        if row['B365H'] < row['B365A'] and row['FTHG'] == 0:
            matches_no_goal.append(row)
        # Away team is stronger
        elif row['B365A'] < row['B365H'] and row['FTAG'] == 0:
            matches_no_goal.append(row)

    # Convert the matches_no_goal list to a DataFrame for better readability
    matches_no_goal_df = pd.DataFrame(matches_no_goal)

    home_min = df['B365H'].min()
    away_min = df['B365A'].min()
    outlier_count = matches_no_goal_df.shape[0]
    outlier_percent = (outlier_count / df.shape[0]) * 100

    with open("total_stats.csv","a") as f:
            f.write(f"{filename},{home_min},{away_min},{outlier_count},{outlier_percent}\n")

    matches_no_goal_df.to_csv(f'{filename}_no_goal.csv', index=False)

import os
for root, dirs, files in os.walk("leagues"):
    for file in files:
        if file.endswith(".csv"):
            process_file(os.path.join(root, file))
