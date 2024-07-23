# Correcting the error by importing NumPy
import numpy as np
# First, let's read the CSV file to understand its structure and contents.
import pandas as pd

# Load the CSV file
file_path = 'salaries.csv'
salaries_df = pd.read_csv(file_path)

# Display the first few rows of the dataframe to understand its structure
salaries_df.head()

# First, we need to clean the data: split the columns, remove whitespaces and periods, and handle NaN values.

# Split the '2023' and '2024' columns into 'min' and 'max' for each year
salaries_df[['min_2023', 'max_2023']] = salaries_df['2023'].str.split(' - ', expand=True)
salaries_df[['min_2024', 'max_2024']] = salaries_df['2024'].str.split(' - ', expand=True)


# Remove periods from the numbers and convert them to integers
for col in ['min_2023', 'max_2023', 'min_2024', 'max_2024']:
    salaries_df[col] = salaries_df[col].str.replace('.', '').astype(float)


salaries_df['avg_2023'] = (salaries_df['min_2023'] + salaries_df['max_2023']) / 2
salaries_df['avg_2024'] = (salaries_df['min_2024'] + salaries_df['max_2024']) / 2


# Calculate the percentage change for min and max salaries from 2023 to 2024
salaries_df['min_change'] = ((salaries_df['min_2024'] / salaries_df['min_2023']) - 1) * 100
salaries_df['max_change'] = ((salaries_df['max_2024'] / salaries_df['max_2023']) - 1) * 100

# Calculate the percentage change in average salary from 2023 to 2024
salaries_df['avg_change'] = ((salaries_df['avg_2024'] / salaries_df['avg_2023']) - 1) * 100

# Replace infinities with NaN again, now that np is imported
salaries_df.replace([float('inf'), -float('inf')], np.nan, inplace=True)

# Fill NaN values with 0 for percentage changes, to handle cases with no changes or missing values correctly
salaries_df[['min_change', 'max_change','avg_change']] = salaries_df[['min_change', 'max_change','avg_change']].fillna(0)


# Display the dataframe with the calculated percentage changes for verification

salaries_df.to_csv('salaries_cleaned.csv', index=False)
print(salaries_df)
print(salaries_df)
