import os
import time
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

base_url = "https://www.thewhiskyexchange.com/"

def save_to_csv(data, filename):
    '''Function to Save Results into CSV File'''

    df = pd.DataFrame(data)
    df.to_csv(f"./Data/{filename}_whisky_result.csv", index=False)

def save_to_json(data, filename):
    '''Function to Save Results into JSON File'''

    with open(f"./Data/{filename}_whisky_result.json", 'w') as f:
        json.dump(data, f)



class Whisky_Scrapper:

    def __init__(self, code, country, npage):
        self.country = country
        self.npage = npage
        self.code = code
        os.makedirs(f"./Images/{self.country}", exist_ok=True)

    
    def scrape(self):
        USER_AGENT = "YOUR_USER_AGENT"
        HEADERS = ({'User-Agent':USER_AGENT, 'Accept-Language':'en-us, en;q=0.5'})

        PRODUCTS = []

        for page in range(1, self.npage+1):
            URL = base_url + f"c/{self.code}/{self.country}-whisky?pa={page}"
            response = requests.get(URL, headers=HEADERS)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                product_list = soup.find(attrs={'ul'}, class_='product-grid__list')

                product_details = {}
                i = 1
                for product in product_list:
                    product_details['country'] = self.country
                  
                    # Get ProductLink, ProductName, MetaInfo, Price, and PricePerLTR
                    product_details['product_link'] = base_url + product.find(attrs={'a'}, class_='product-card').get('href')

                    content = product.find(attrs={'div'}, class_="product-card__content").find_all('p')
                    product_name, meta = [tag.get_text() for tag in content]
                    product_details['product_name'], product_details['meta'] =  product_name, meta 

                    prices = product.find(attrs={'div'}, class_="product-card__data").find_all('p')
                    product_details['price'], product_details['unit_price'] = [tag.get_text() for tag in prices]

                    # Get Image URL
                    image_url = product.find(attrs={'div'}, class_="product-card__image-container").find('img').get('src')
                    image = requests.get(image_url)

                    # Save Image
                    with open(f"./Images/{self.country}/image_{code}_{i}.jpg", 'wb') as f:
                        f.write(image.content)
                    i += 1
                    PRODUCTS.append(product_details)


        # Save Results To CSV
        save_to_csv(PRODUCTS, self.country)

        # Save Results to JSON
        save_to_json(PRODUCTS, self.country)


        
if __name__ == "__main__":
  
    scrap = Whisky_Scrapper(code=code,
                            country=country,
                            npage=npage)
    scrap.scrape()
