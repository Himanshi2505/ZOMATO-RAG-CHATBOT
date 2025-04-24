import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh;'
                         ' Intel Mac OS X 10_15_4)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/83.0.4103.97 Safari/537.36'}


def get_info(url):
    """ Get Information about the restaurant from URL """
    
    global headers
    try:
        webpage = requests.get(url, headers=headers, timeout=3)
        html_text = BeautifulSoup(webpage.text, 'lxml')
        
        # Check if there are enough script tags
        script_tags = html_text.find_all('script', type='application/ld+json')
        if len(script_tags) <= 1:
            print(f"Warning: Not enough script tags found for {url}. Found only {len(script_tags)}.")
            # Return a tuple of None values with the correct length
            return (None,) * 18  # Assuming 18 fields based on the original function
        
        info = script_tags[1]
        info = json.loads(info.string)
        
        # Get values with default for potentially missing keys
        restaurant_type = info.get('@type', None)
        name = info.get('name', None)
        url_info = info.get('url', None)
        opening_hours = info.get('openingHours', None)
        
        # Address information
        address = info.get('address', {})
        street_address = address.get('streetAddress', None)
        address_locality = address.get('addressLocality', None)
        address_region = address.get('addressRegion', None)
        postal_code = address.get('postalCode', None)
        address_country = address.get('addressCountry', None)
        
        # Geo information
        geo = info.get('geo', {})
        latitude = geo.get('latitude', None)
        longitude = geo.get('longitude', None)
        
        telephone = info.get('telephone', None)
        price_range = info.get('priceRange', None)
        payment_accepted = info.get('paymentAccepted', None)
        image = info.get('image', None)
        serves_cuisine = info.get('servesCuisine', None)
        
        # Rating information
        aggregate_rating = info.get('aggregateRating', {})
        rating_value = aggregate_rating.get('ratingValue', None)
        rating_count = aggregate_rating.get('ratingCount', None)
        
        data = (
            restaurant_type, name, url_info, opening_hours,
            street_address, address_locality, address_region, postal_code, address_country,
            latitude, longitude, telephone, price_range, payment_accepted,
            image, serves_cuisine, rating_value, rating_count
        )
        return data
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        # Return None values for all fields
        return (None,) * 18  # Since there are 18 fields in the data tuple




def save_df(file_name, df):
    """ Save the dataframe """
    
    df.to_csv(file_name, index=False)
    

def get_restaurant_info(url_list, save=True, file_name="Restaurants.csv"):
    """ Get Restaurant Information from all urls passed """

    # Collecting the data
    data = []
    for url in url_list:
        data.append(get_info(url))
        
    # Creating the DataFrame
    columns = ['Type', 'Name', 'URL', 'Opening_Hours',
               'Street', 'Locality', 'Region', 'PostalCode', 'Country',
               'Latitude', 'Longitude', 'Phone',
               'Price_Range', 'Payment_Methods',
               'Image_URL', 'Cuisine', 'Rating', 'Rating_Count']
    info_df = pd.DataFrame(data, columns=columns)
    
    # Save the df
    if save:
        save_df(file_name, info_df)
        
    return info_df


if __name__ == "__main__":
    urls = ["https://www.zomato.com/bangalore/voosh-thalis-bowls-1-bellandur-bangalore",
            "https://www.zomato.com/bangalore/flying-kombucha-itpl-main-road-whitefield-bangalore",
            "https://www.zomato.com/bangalore/matteo-coffea-indiranagar"]
    get_restaurant_info(urls)