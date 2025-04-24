import re
import unicodedata
import pandas as pd
import os
import json

def clean_text(text):
    """Clean and normalize text for better processing."""
    if pd.isna(text) or not text:
        return ""
    
    # Convert to string if not already
    text = str(text)
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove special characters except for common punctuation
    text = re.sub(r'[^\w\s.,;?!-]', '', text)
    
    return text

def extract_price_value(price_str):
    """Extract numeric price value from price string."""
    if pd.isna(price_str) or not price_str:
        return None
    
    # Extract numbers from the price string (e.g., "Rs 795" -> 795)
    match = re.search(r'Rs\s*(\d+(?:\.\d+)?)', price_str)
    if match:
        return float(match.group(1))
    return None

def categorize_price_range(price):
    """Categorize price into ranges for easier comparison."""
    if price is None:
        return "Unknown"
    
    if price <= 200:
        return "Budget"
    elif price <= 500:
        return "Moderate"
    elif price <= 800:
        return "Premium"
    else:
        return "Luxury"

def get_restaurant_files():
    """Get all restaurant data files from the different directories."""
    files = {
        'restaurants': 'Restaurants.csv',
        'menus': {},
        'reviews': {}
    }
    
    # Get restaurant names from Restaurants.csv
    if os.path.exists('Restaurants.csv'):
        restaurants_df = pd.read_csv('Restaurants.csv')
        restaurant_names = restaurants_df['Name'].tolist()
        
        # Find menu files for each restaurant
        if os.path.exists('Enhanced_Menu'):
            for filename in os.listdir('Enhanced_Menu'):
                if filename.endswith('.csv'):
                    for name in restaurant_names:
                        if name in filename:
                            files['menus'][name] = os.path.join('Enhanced_Menu', filename)
        
        # Find review files for each restaurant
        if os.path.exists('Reviews'):
            for filename in os.listdir('Reviews'):
                if filename.endswith('.csv'):
                    for name in restaurant_names:
                        if name.replace(' ', '_') in filename:
                            files['reviews'][name] = os.path.join('Reviews', filename)
    
    return files
