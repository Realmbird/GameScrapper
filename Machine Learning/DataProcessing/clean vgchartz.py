import json
import pandas as pd
import numpy as np
from datetime import datetime
import re

def clean_date(date_str):
    # Remove the suffix from the day part
    date_str = re.sub(r'(st|nd|rd|th)', '', date_str)
    # Parse the date using strptime and the known format
    try:
        date_obj = datetime.strptime(date_str, '%d %b %y')
        # Convert the date to the desired string format
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        # In case of parsing error, return None or the original string
        return None
    
# Function to convert sales data
def convert_sales_to_million(value):
    if 'm' in value:
        return float(value.replace('m', ''))
    elif value == 'N/A':
        return np.nan  # Using numpy's NaN for missing values
    else:
        return value  # Return as is if the pattern doesn't match

# Function to convert scores to integers or NaN
def convert_score_to_int(value):
    if value == 'N/A':
        return np.nan  # Representing missing or non-applicable scores with NaN
    else:
        try:
            return int(float(value))  # Convert to float first to handle decimal scores, then to int
        except ValueError:  # In case of unexpected format
            return np.nan

# Load JSON data
with open('vgchartz.json') as f:
    response_json = json.load(f)
cleaned_data = []
# Processing each game entry
for game in response_json:
    # Removing 'img' field
    del game['img']
    
    # Stripping whitespace
    for field in ['title', 'console', 'publisher', 'developer', 'vg_score', 'critic_score', 'user_score']:
        if game[field] is not None:
            game[field] = game[field].strip()
        
    for field in ['title', 'publisher', 'developer']:
        if game[field] is not None:
            game[field] = game[field].encode('ascii', 'ignore').decode('ascii')
    
    # Converting sales data
    for field in ['total_shipped', 'total_sales', 'na_sales', 'pal_sales', 'jp_sales', 'other_sales']:
        if game[field] is not None:
            game[field] = convert_sales_to_million(game[field])
    
    # Converting score fields
    for field in ['vg_score', 'critic_score', 'user_score']:
        if game[field] is not None:
            game[field] = convert_score_to_int(game[field])
    for date_field in ['release_date', 'last_update']:
        if game[date_field] is not None:
            game[date_field] = clean_date(game[date_field])
    if pd.notnull(game.get('total_shipped')) or pd.notnull(game.get('total_sales')) \
       or pd.notnull(game.get('na_sales')) or pd.notnull(game.get('pal_sales')) \
       or pd.notnull(game.get('jp_sales')) or pd.notnull(game.get('other_sales')):
        # At least one sales field has data, so keep the row
        cleaned_data.append(game)

# Save the cleaned data to a new JSON file
cleaned_filename = 'cleaned_vgchartz_sales.json'  # Prepend 'cleaned_' to the original filename
with open(cleaned_filename, 'w') as f:
    json.dump(cleaned_data, f, indent=4)  # Save with pretty-printing

print(f"Cleaned data saved to {cleaned_filename}")
