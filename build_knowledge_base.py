import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
from data_utils import clean_text, extract_price_value, categorize_price_range, get_restaurant_files

def load_restaurant_data():
    """Load all restaurant data from CSV files"""
    files = get_restaurant_files()
    
    # Load main restaurant info
    restaurants_df = pd.read_csv(files['restaurants'])
    
    # Initialize knowledge base
    knowledge_base = []
    
    # Process each restaurant
    for _, restaurant in tqdm(restaurants_df.iterrows(), desc="Processing restaurants", total=len(restaurants_df)):
        restaurant_name = restaurant['Name']
        
        # Create restaurant entry
        restaurant_data = {
            "name": restaurant_name,
            "type": "restaurant",
            "basic_info": {
                "cuisine": restaurant.get('Cuisine', ''),
                "location": restaurant.get('Locality', ''),
                "price_range": restaurant.get('Price_Range', ''),
                "opening_hours": restaurant.get('Opening_Hours', ''),
                "phone": restaurant.get('Phone', ''),
                "rating": restaurant.get('Rating', ''),
                "rating_count": restaurant.get('Rating_Count', '')
            },
            "menu_items": [],
            "reviews": []
        }
        
        # Load menu data if available
        if restaurant_name in files['menus']:
            menu_df = pd.read_csv(files['menus'][restaurant_name])
            
            for _, item in menu_df.iterrows():
                if not pd.isna(item.get('Name')) and item.get('Name'):
                    # Process menu item
                    price_value = extract_price_value(item.get('Price', ''))
                    
                    menu_item = {
                        "name": item.get('Name', ''),
                        "description": item.get('Description', ''),
                        "category": item.get('Standard_Category', item.get('Category', '')),
                        "price": item.get('Price', ''),
                        "price_value": price_value,
                        "price_category": categorize_price_range(price_value),
                        "dietary_info": item.get('Dietary_Info', 'Unknown'),
                        "tags": item.get('Tags', ''),
                        "restaurant": restaurant_name
                    }
                    restaurant_data["menu_items"].append(menu_item)
        
        # Load review data if available
        if restaurant_name in files['reviews']:
            review_df = pd.read_csv(files['reviews'][restaurant_name])
            
            for _, review in review_df.iterrows():
                if not pd.isna(review.get('Description')) and review.get('Description'):
                    review_data = {
                        "author": review.get('Author', ''),
                        "rating": review.get('Rating', ''),
                        "text": clean_text(review.get('Description', '')),
                        "restaurant": restaurant_name
                    }
                    restaurant_data["reviews"].append(review_data)
        
        knowledge_base.append(restaurant_data)
    
    return knowledge_base

def create_restaurant_documents(knowledge_base):
    """Create document chunks for each restaurant and its menu items"""
    documents = []
    
    for restaurant in knowledge_base:
        # Create a document for restaurant info
        restaurant_info_doc = {
            "id": f"restaurant-{restaurant['name'].replace(' ', '-').lower()}",
            "content": f"Restaurant: {restaurant['name']}\n"
                      f"Cuisine: {restaurant['basic_info']['cuisine']}\n"
                      f"Location: {restaurant['basic_info']['location']}\n"
                      f"Price range: {restaurant['basic_info']['price_range']}\n"
                      f"Opening hours: {restaurant['basic_info']['opening_hours']}\n"
                      f"Rating: {restaurant['basic_info']['rating']} from {restaurant['basic_info']['rating_count']} reviews\n"
                      f"Phone: {restaurant['basic_info']['phone']}",
            "metadata": {
                "type": "restaurant_info",
                "restaurant": restaurant['name'],
                "cuisine": restaurant['basic_info']['cuisine'],
                "location": restaurant['basic_info']['location'],
                "price_range": restaurant['basic_info']['price_range']
            }
        }
        documents.append(restaurant_info_doc)
        
        # Create documents for menu categories
        menu_by_category = {}
        for item in restaurant['menu_items']:
            category = item['category']
            if category not in menu_by_category:
                menu_by_category[category] = []
            menu_by_category[category].append(item)
        
        # Create a document for each menu category
        for category, items in menu_by_category.items():
            if not category:
                category = "Uncategorized"
                
            items_text = "\n".join([
                f"- {item['name']}: {item['description']} Price: {item['price']}. " 
                f"Dietary info: {item['dietary_info']}. Tags: {item['tags']}"
                for item in items
            ])
            
            category_doc = {
                "id": f"menu-{restaurant['name']}-{category}".replace(' ', '-').lower(),
                "content": f"Restaurant: {restaurant['name']}\n"
                          f"Menu category: {category}\n"
                          f"Items:\n{items_text}",
                "metadata": {
                    "type": "menu_category",
                    "restaurant": restaurant['name'],
                    "category": category,
                    "item_count": len(items)
                }
            }
            documents.append(category_doc)
        
        # Create documents for individual menu items
        for item in restaurant['menu_items']:
            item_doc = {
                "id": f"menu-item-{restaurant['name']}-{item['name']}".replace(' ', '-').lower(),
                "content": f"Restaurant: {restaurant['name']}\n"
                          f"Menu item: {item['name']}\n"
                          f"Description: {item['description']}\n"
                          f"Category: {item['category']}\n"
                          f"Price: {item['price']}\n"
                          f"Dietary info: {item['dietary_info']}\n"
                          f"Tags: {item['tags']}",
                "metadata": {
                    "type": "menu_item",
                    "restaurant": restaurant['name'],
                    "name": item['name'],
                    "category": item['category'],
                    "price_value": item['price_value'],
                    "price_category": item['price_category'],
                    "dietary_info": item['dietary_info']
                }
            }
            documents.append(item_doc)
        
        # Create documents for reviews
        if restaurant['reviews']:
            reviews_text = "\n".join([
                f"- {review['author']} (Rating: {review['rating']}): {review['text']}"
                for review in restaurant['reviews'][:10]  # Limit to 10 reviews per document
            ])
            
            reviews_doc = {
                "id": f"reviews-{restaurant['name']}".replace(' ', '-').lower(),
                "content": f"Restaurant: {restaurant['name']}\n"
                          f"Reviews:\n{reviews_text}",
                "metadata": {
                    "type": "reviews",
                    "restaurant": restaurant['name'],
                    "review_count": len(restaurant['reviews'])
                }
            }
            documents.append(reviews_doc)
    
    return documents

def main():
    # Create directories if they don't exist
    os.makedirs('knowledge_base', exist_ok=True)
    
    print("Building knowledge base...")
    knowledge_base = load_restaurant_data()
    
    # Save complete knowledge base
    with open('knowledge_base/restaurant_data.json', 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
    
    # Create document chunks for RAG
    print("Creating document chunks for retrieval...")
    documents = create_restaurant_documents(knowledge_base)
    
    # Save documents
    with open('knowledge_base/documents.json', 'w', encoding='utf-8') as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    
    print(f"Knowledge base built successfully with {len(knowledge_base)} restaurants and {len(documents)} document chunks.")
    print("Files saved to knowledge_base/restaurant_data.json and knowledge_base/documents.json")

if __name__ == "__main__":
    main()
