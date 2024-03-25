import json
import numpy as np
import pandas as pd

# Load the JSON data from the file
with open('cleaned_aggregated_vgchartz.json', 'r') as file:
    data = json.load(file)

# Iterate through each record and replace 'NaN' with None for specified fields
for record in data:
    for field in ['user_score', 'vg_score', 'critic_score']:
        # Check if the field exists in the record and if its value is NaN
        if field in record and pd.isna(record[field]):
            record[field] = None  # Replace NaN with None

# Save the modified data back to a new JSON file
with open('processed_vgchartz.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Processed data saved to 'processed_vgchartz.json'.")
