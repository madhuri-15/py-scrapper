import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_link(product):
    return product.get('href')

def get_brand(product):
    brand = product.find(class_='ProductCard__brand').get_text().strip()
    return brand

def get_name(product):
    product_name = product.find(class_='ProductCard__product').get_text().strip()
    return product_name

def get_price(product):
    try:
        price = product.find(class_="ProductCard__price").get_text().strip()
        return price
    except:
        price = None
        return price

def get_reviews(product):
    try:
        product_rating, total_reviews = product.find(class_='ProductCard__rating').find('span').get_text().split(';')
        product_rating = product_rating.strip().split(' ')[0]
        total_reviews = total_reviews.strip().split(' ')[0]
        
        return product_rating, total_reviews
        
    except AttributeError:
        product_rating = None
        total_reviews = None
        return product_rating, total_reviews 
    

def get_products(product_type, product_cat, npages):

    # list of product dictionary
    products = []
    base_url = "https://www.ulta.com/shop/skin-care/"

    # Create a url to get the products list
    url = base_url + product_type + '/' + product_cat

    print(f"=== Getting {product_type} info ===")
    for page in range(1, npages+1):
        print(f"==== Getting data from Page {page} ====")
        
        re = requests.get(url+'?page={0}'.format(page))
        if re.status_code == 200:
            # soup object
            soup = BeautifulSoup(re.content, 'html.parser')
            container = soup.find(id='product-listing-wrapper')
            product_list = container.find(name='ul', class_='ProductListingResults__productList')
            product_cards = product_list.find_all(name='li', class_='ProductListingResults__productCard')

            for product_card in product_cards:
                product_dict = {}
                product = product_card.find('a')
                product_dict['product_link'] = get_link(product)

                # product content bs4 object
                product_content = product.find(class_="ProductCard__content")
                
                product_dict['product_name'] = get_name(product_content)
                product_dict['brand_name'] = get_brand(product_content)
                product_dict['price'] = get_price(product_content)
                product_dict['ratings'], product_dict['total_reviews'] = get_reviews(product_content)

                # Product type and category
                product_dict['product_type'] = product_type
                product_dict['product_cat'] = product_cat

                # Add product information into a dictionary.
                products.append(product_dict)
            
        else:
            status_code = re.status_code
            return f'Status Code:{status_code}'

        # Add time latency
        time.sleep(2)
        
    print("-------xxx-------")
    return pd.DataFrame(products)


if __name__ == "__main__":

    # Load the url dataframe
    url_df = pd.read_csv("url_to_scrape.csv")

    # Create an empty dataframe to store product information
    product_data = pd.DataFrame()

    for idx in range(len(url_df)):
    
        product_type = url_df.loc[idx, 'product_type']
        product_cat = url_df.loc[idx, 'product_cat']
        npages = url_df.loc[idx, 'npages']

        product_df = get_products(product_type, product_cat, npages)
        product_data = pd.concat([product_data, product_df])

    # Save the data into pandas dataframe
    product_data.reset_index(drop=True, inplace=True)
    product_data.to_csv("ulta_skincare_products.csv", index=False)
    