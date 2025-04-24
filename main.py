from info_scraper import get_restaurant_info
from review_scraper import get_reviews
from menu_scraper import get_menu


def scrape_all_data(url_list):
    """Scrapes all data from the urls passed """

    get_restaurant_info(url_list=url_list, file_name="Restaurants.csv")
    for url in url_list:
        get_reviews(url=url, max_reviews=50, sort="popular", save=True)
        get_menu(url)


if __name__ == '__main__':
    urls = ["https://www.zomato.com/ncr/cabo-deli-1-sainik-farms-new-delhi",
            "https://www.zomato.com/bangalore/matteo-coffea-indiranagar" ,
            "https://www.zomato.com/bangalore/los-cavos-indiranagar-bangalore",
            "https://www.zomato.com/ncr/call-chotu-all-day-diner-1-kailash-colony-new-delhi",
            "https://www.zomato.com/bangalore/jamming-goat-3-0-indiranagar-bangalore",
            "https://www.zomato.com/bangalore/toit-indiranagar",
            "https://www.zomato.com/bangalore/kopitiam-lah-indiranagar-bangalore",
            "https://www.zomato.com/bangalore/native-bar-and-indian-kitchen-indiranagar-bangalore",
]
    scrape_all_data(urls)
