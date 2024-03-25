import json
import pandas as pd
import numpy as np

# Assuming the JSON data is in a file called 'cleaned_vgchartz.json'
with open('cleaned_vgchartz_sales.json', 'r') as file:
    data = json.load(file)

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(data)

# Function to sum sales while ignoring NaNs
def sum_sales(series):
    return series.dropna().sum()

# Function to average scores while ignoring NaNs
def average_scores(series):
    valid_scores = series.dropna()
    return valid_scores.mean() if not valid_scores.empty else None



# Aggregate data by title
aggregated_data = df.groupby('title').agg({
    'console': 'count',  # Count the number of consoles for each title
    'publisher': 'first',
    'developer': 'first',
    'vg_score': average_scores,
    'critic_score': average_scores,
    'user_score': average_scores,
    'total_sales': sum_sales,
    'na_sales': sum_sales,
    'pal_sales': sum_sales,
    'jp_sales': sum_sales,
    'other_sales': sum_sales,
    'release_date': 'first',  # You may want to handle date fields more appropriately
    'last_update': 'first',
    'genre': 'first'
}).reset_index()

# Rename the 'console' column to 'num_consoles'
aggregated_data.rename(columns={'console': 'num_consoles'}, inplace=True)



# Save the cleaned, aggregated data to a new JSON file
with open('cleaned_aggregated_vgchartz.json', 'w') as file:
    json.dump(aggregated_data.to_dict(orient='records'), file, indent=4, sort_keys=True)  # Indent by 4 spaces

print("Aggregated data saved to 'cleaned_aggregated_vgchartz.json'.")

