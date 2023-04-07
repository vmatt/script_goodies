import pandas as pd

# Read the CSV file
df = pd.read_csv("toilet_paper.csv")

# Define the diminishing factor
diminishing_factor = 0.5  # adjust this value as needed

def comfort(n):
    n = float(n)
    return 2.5 + (0.5 * (1 - 0.5**(n-3))) if n > 2 else n

df['comfort'] = df['num_layers'].apply(comfort)

# Calculate the price per sheet
df['price_per_sheet'] = df['pack_cost'] / (df['rolls_per_pack'] * df['sheets_per_roll'] * df['comfort'])

# Identify the toilet paper pack with the best price/sheet ratio
best_pack = df.loc[df['price_per_sheet'].idxmin()]
print(df)

# Print the results
print("The best toilet paper pack is:")
print("Rolls per pack:", best_pack['rolls_per_pack'])
print("Sheets per roll:", best_pack['sheets_per_roll'])
print("Number of layers:", best_pack['num_layers'])
print("pack cost:", best_pack['pack_cost'])
print("Price per sheet:", best_pack['price_per_sheet'])
