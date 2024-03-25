import pandas as pd
import json

# Load datasets
with open('cleaned_open_critic.json', 'r') as file:
    open_critic_data = json.load(file)
with open('cleaned_steampage.json', 'r') as file:
    steam_data = json.load(file)
with open('processed_vgchartz.json', 'r') as file:
    vgchartz_data = json.load(file)

# Convert to pandas DataFrames
df_open_critic = pd.DataFrame(open_critic_data)
df_steam = pd.DataFrame(steam_data)
df_vgchartz = pd.DataFrame(vgchartz_data)

# Standardize title/name columns for a consistent merge key
df_open_critic['title'] = df_open_critic['title'].str.lower()
df_steam['title'] = df_steam['name'].str.lower()  # Create a 'title' column in df_steam for merging
df_vgchartz['title'] = df_vgchartz['title'].str.lower()

# Drop the original 'name' column from Steam data as we now have a 'title' column
df_steam.drop('name', axis=1, inplace=True)

# Merge DataFrames on the 'title' column
df_merged = df_vgchartz.merge(df_open_critic, on='title', how='left') \
                       .merge(df_steam, on='title', how='left')

# Handling missing values, if necessary, e.g., fill with 0, mean or median
# This step depends on the specific requirements of your ML model
# df_merged.fillna(0, inplace=True)  # Example: fill missing values with 0

# Saving the merged DataFrame to a new JSON file for ML processing
df_merged.to_json('combined_dataset_with_null.json', orient='records', indent=4)

print("Combined dataset created and saved.")