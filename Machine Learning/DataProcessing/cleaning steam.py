import json
import pandas as pd
import numpy as np
from datetime import datetime
import re



# Load JSON data
with open('steampage.json') as f:
    response_json = json.load(f)


cleaned_data = []

for game in response_json:
    # Renaming columns by adding 'steam_' prefix
    game = {('steam_' + k if k in ['total_positive', 'total_negative', 'total_reviews', 'review_score', 'review_score_desc'] else k): v for k, v in game.items()}
    
    # Removing Unicode characters like ™ (trademark)
    game['name'] = game['name'].encode('ascii', 'ignore').decode('ascii')
    del game["steam_review_score_desc"]
    cleaned_data.append(game)

# Save the cleaned data to a new JSON file
cleaned_filename = 'cleaned_steampage.json'  # Prepend 'cleaned_' to the original filename
with open(cleaned_filename, 'w') as f:
    json.dump(cleaned_data, f, indent=4)  # Save with pretty-printing

print(f"Cleaned data saved to {cleaned_filename}")
