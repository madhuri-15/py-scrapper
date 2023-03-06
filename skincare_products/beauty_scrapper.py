# Importing libraries
import requests
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np


# Function to extract link of the product.
def get_links(soup):
    
    # find all products
    products = soup.find_all('a', attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}) 
        
    product_links = []
    for product in products:
        product_links.append('https://www.amazon.in' + product.get('href'))
    
    return product_links
  
  
# Function to extract name of the product.
def get_title(soup):
    
    try:
        # find the product title
        title = soup.find('span', attrs={'id':'productTitle'})
        title_val = title.text.strip()
    
    except AttributeError:
        title_val = None
    
    return title_val


# Function to extract rating of the product.
def get_ratings(soup):
    
    try:
        # find the product ratings of the product out of 5.
        rating = soup.find('span', attrs={'class':'a-icon-alt'})
        rating = rating.text.strip()
    
    except AttributeError:
        rating = None
    
    return rating


# Function to extract total rating of the product.
def get_total_ratings(soup):
    
    try:
        # find the products total ratings by users.
        totalrating = soup.find('span', attrs={'id':'acrCustomerReviewText'})
        totalrating = totalrating.text.strip()
    
    except AttributeError:
        totalrating = None
    
    return totalrating


# Function to extract price of the product
def get_price(soup):
    
    try:
        # find the price of the product.
        price = soup.find('span', attrs={'class':'a-offscreen'})
        price = price.text.strip()
    
    except AttributeError:
        price = None
    
    return price



if __name__ == '__main__':

    amazon_skincare_product_dfs = []
    TOTAL_PAGES = 200
    
    for i in range(1, TOTAL_PAGES):

        # Set URL & HEADERS for the requests.
        URL = "https://www.amazon.in/s?i=beauty&rh=n%3A1374407031&fs=true&qid=1678085064&ref=sr_pg_{}".format(i)

        USER_AGENT = "YOUR_USER_AGENT"
        HEADERS = ({'User-Agent':USER_AGENT, 'Accept-Language': 'en-us', 'en;q=0.5'})

        # HTTP request
        response = requests.get(URL, headers=HEADERS)

        if response.status_code == 200:

            # Get the HTML content in byte format.
            content = response.content

            # Create a Soup Object
            soup = BeautifulSoup(content, 'html.parser')

            # Get the product info
            product_links = get_links(soup)

            products = {'name':[], 'price':[], 'ratings':[], 'total_ratings':[]}

            for url in product_links:
                # HTTP request
                response = requests.get(url, headers=HEADERS)
                soup = BeautifulSoup(response.content, 'html.parser')

                # get product info
                products['name'].append(get_title(soup))
                products['price'].append(get_price(soup)) 
                products['ratings'].append(get_ratings(soup))
                products['total_ratings'].append(get_total_ratings(soup))

            skincare_df = pd.DataFrame.from_dict(products)
            amazon_beauty_product_dfs.append(skincare_df)            
        else:
            pass


    data = pd.concat(amazon_beauty_products_dfs, ignore_index=True)

    # Drop products with no information
    data = data.dropna(how='all')

    # Save the dataframe into csv file
    data.to_csv("SkinCare_products.csv")
