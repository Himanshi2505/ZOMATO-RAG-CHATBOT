import pandas as pd
import os

# --- Enhancement Functions ---

def infer_dietary_info(item_name, tags=""):
    item_lower = str(item_name).lower() if not pd.isna(item_name) else ""
    tags_lower = str(tags).lower() if not pd.isna(tags) else ""
    
    if "vegan" in tags_lower:
        return "Vegan"
    elif "vegetarian" in tags_lower:
        return "Vegetarian"
        
    non_veg_terms = ["chicken", "mutton", "fish", "pork", "prawn", "egg", "lamb", "beef", "shrimp"]
    veg_terms = ["paneer", "tofu", "veg", "vegetable", "mushroom", "dal", "cheese"]
    
    if any(term in item_lower for term in non_veg_terms):
        return "Non-Vegetarian"
    if any(term in item_lower for term in veg_terms):
        return "Vegetarian"
    
    return "Unknown"

def generate_description(item_name, category, cuisine="", price=""):
    # Handle NaN or None values
    if pd.isna(item_name) or not item_name:
        return ""
    
    # Convert inputs to strings, handling NaN values
    item_name_str = str(item_name) if not pd.isna(item_name) else ""
    category_str = str(category) if not pd.isna(category) else ""
    price_str = str(price) if not pd.isna(price) else ""
    
    desc = f"{item_name_str} is a"
    
    # Check item name for keywords
    if "chicken" in item_name_str.lower():
        desc += " delicious chicken dish"
    elif "paneer" in item_name_str.lower():
        desc += " classic Indian vegetarian dish"
    # Check category AFTER converting to string
    elif "pasta" in category_str.lower():
        desc += " pasta preparation"
    elif "dessert" in category_str.lower():
        desc += " sweet dessert"
    else:
        desc += f" {category_str.lower()} item"
    
    # Add price if available and not NaN
    if price_str and price_str != "nan":
        desc += f" priced at {price_str}"
    
    desc += "."
    return desc

def normalize_category(category):
    if pd.isna(category):
        return "Uncategorized"
        
    category_str = str(category).strip().lower()
    
    mapping = {
        "starters": "Appetizers",
        "appetizers": "Appetizers",
        "main course": "Main Courses",
        "mains": "Main Courses",
        "pasta": "Pasta & Pizza",
        "pizza": "Pasta & Pizza",
        "desserts": "Desserts",
        "drinks (beverages)": "Beverages",
        "beverages": "Beverages",
        "breads": "Breads",
        "rice & noodles": "Rice & Noodles",
        "snacks": "Snacks",
        "salads": "Salads",
    }
    
    for key in mapping:
        if key in category_str:
            return mapping[key]
            
    return category_str.capitalize()

# --- Enhance All Menus ---

menu_dir = "Menu"
enhanced_dir = "Enhanced_Menu"
os.makedirs(enhanced_dir, exist_ok=True)

print("Starting menu enhancement process...")

for menu_file in os.listdir(menu_dir):
    if not menu_file.endswith(".csv"):
        continue
        
    print(f"Processing {menu_file}...")
    menu_path = os.path.join(menu_dir, menu_file)
    
    try:
        menu_df = pd.read_csv(menu_path)
        
        # Check if dataframe has required columns
        if 'Name' not in menu_df.columns:
            print(f"Warning: {menu_file} missing 'Name' column, skipping...")
            continue
            
        # Add Tags column if not exists
        if 'Tags' not in menu_df.columns:
            menu_df['Tags'] = ""
            
        # Add dietary information
        menu_df["Dietary_Info"] = menu_df.apply(
            lambda row: infer_dietary_info(row.get("Name"), row.get("Tags", "")), 
            axis=1
        )
        
        # Generate descriptions where missing
        menu_df["Description"] = menu_df.apply(
            lambda row: row.get("Description") if pd.notna(row.get("Description")) and str(row.get("Description")).strip()
            else generate_description(row.get("Name"), row.get("Category"), price=row.get("Price")), 
            axis=1
        )
        
        # Normalize categories
        if 'Category' in menu_df.columns:
            menu_df["Standard_Category"] = menu_df["Category"].apply(normalize_category)
        else:
            menu_df["Standard_Category"] = "Uncategorized"
            
        # Save enhanced menu
        menu_df.to_csv(os.path.join(enhanced_dir, menu_file), index=False)
        print(f"Successfully enhanced {menu_file}")
        
    except Exception as e:
        print(f"Error processing {menu_file}: {e}")

print("All menu files processed.")
