import json
import pandas as pd
import numpy as np
from datetime import datetime
import re

# Function to clean the publisher field
def clean_publisher(publisher):
    return publisher.replace(",", "").strip()

# Function to convert review scores to a float
def convert_review_to_float(review):
    try:
        if '/' in review:
            score, out_of = review.split('/')
            return float(score.strip()) / float(out_of.strip()) * 10  # Normalize to a 10-point scale
        elif review == "Recommended" or review == "Essential":
            return 10  # Assuming 'Recommended' or 'Essential' is a perfect score
        else:
            return float(review)  # Assume the score is already on a 10-point scale
    except ValueError:
        return None  # If conversion fails, return None

# Function to calculate average review score
def calculate_average_review(reviews):
    scores = [convert_review_to_float(score) for score in reviews.values() if convert_review_to_float(score) is not None]
    return sum(scores) / len(scores) if scores else None



# Load JSON data
with open('OpenCritic.json') as f:
    response_json = json.load(f)
cleaned_data = []
# Processing each game entry
for game in response_json:
    for field in ['title', 'publisher']:
        if game[field] is not None:
            game[field] = game[field].encode('ascii', 'ignore').decode('ascii')
    # Clean publisher
    game['publisher'] = clean_publisher(game['publisher'])
    # Convert platform list to count
    game['platform_count'] = len(game['platform'])
    del game['platform']  # Remove the original platform list
    # Convert date to datetime format
    game['date'] = datetime.strptime(game['date'], '%Y-%m-%d').strftime('%Y-%m-%d')
    # Calculate average review score
    game['average_review'] = calculate_average_review(game['reviews'])
    del game['reviews']  # Remove the original reviews dictionary

    cleaned_data.append(game)

# Save the cleaned data to a new JSON file
with open('cleaned_open_critic2.json', 'w') as outfile:
    json.dump(cleaned_data, outfile, indent=4)

print(f"Cleaned data saved to 'cleaned_reviews.json'")
