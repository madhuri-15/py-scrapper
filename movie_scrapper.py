"""
Python class to scrap animation movies from the imdb websites.
The scripts outputs list of movie title, year, rated, runtime, genre, rating, description and total votes.
"""


from base64 import encode
from textwrap import indent
import requests
import numpy as np
import pandas as pd
import json 
from bs4 import BeautifulSoup

# Python class to scrape animation Movies.
# webpage: www.imdb.com/movies

class imdb_movie_scrapper:
    
    # constructor for imdb_moive_scrapper class
    def __init__(self, url):
        self.url = url
        response = requests.get(self.url)
        texthtml = response.text
        self.soup = BeautifulSoup(texthtml, 'html.parser') # beautiful soup object.
        
    
    # Function to scraps movies to retrive movies titles,  year, rated, runtime, genre, rating, description and total votes.
    # Returns a list of dictionaries.
    def scrape(self):
        soup_object = self.soup
        movies = []
        
        for content in soup_object.findAll('div', attrs= {'class': 'lister-item-content'}):
            output = {}
            
            # movie title
            output['movie_title'] = content.find('h3').a.get_text()
            
            # movie year
            output['release_year'] = content.find('span', attrs={'class':'lister-item-year'}).get_text()
            
            # movie certificate
            certificate = content.find('span', attrs={'class':'certificate'})
            if certificate:
                output['rated'] = certificate.get_text()
            else:
                output['rated'] = certificate
            
            # movie runtime
            runtime = content.find('span', attrs={'class':'runtime'})
            if runtime:
                output['runtime'] = runtime.get_text()
            else:
                output['runtime']= runtime

            # movies genre
            genre = content.find('span', attrs={'class':'genre'})
            if genre:
                output['genre'] = genre.get_text().strip()
            else:
                output['genre'] = genre
        
            # movie ratings
            ratings = content.find('div', attrs={'class': 'ratings-imdb-rating'})
            if ratings:
                output['rating'] = ratings['data-value']
            else:
                output['rating'] = ratings
            
            # descriptions
            p_tags = content.findChildren('p')
        
            if p_tags[1]:
                output['description'] = p_tags[1].get_text().strip()
            else:
                output['description'] = p_tags[1]
        
            # total votes
            votes = content.find('p', attrs={'sort-num_votes-visible'})
            
            if votes:
                votes = votes.get_text().strip()
                
                if '|' in votes:
                    total_votes = votes.split('|')[0].strip()
                    output['total_votes'] = total_votes.split(':')[-1].strip()
                else:
                    output['total_votes'] = votes.split(':')[-1].strip()
            else:
                output['total_votes'] = votes
                
            movies.append(output)
        
        return movies
    
    

if __name__ == "__main__":

    movies = []
    
    for page in range(1, 312, 50):
        url = "https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=animation&sort=user_rating,desc&start=page&ref_=adv_nxt"
        
        obj = imdb_movie_scrapper(url)
        
        # return list of dictionaries.
        output = obj.scrape()
        movies = movies + output

    with open('animation_movies.json', 'a') as f:
        json_dumps = json.dumps(movies, indent=4, ensure_ascii=False)
        f.write(json_dumps)     
       
    
    
    
    
    