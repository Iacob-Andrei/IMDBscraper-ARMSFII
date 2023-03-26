from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import json

def get_movies_info():
    url = 'https://www.imdb.com/chart/moviemeter'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    movies = soup.select('td.titleColumn')
    crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
    ratings = [a.attrs.get('data-value') for a in soup.select('td.posterColumn span[name=ir]')]
    links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
    
    list = []
    for index in range(0, len(movies)):
        movie_string = movies[index].get_text()
        movie_title = movie_string.split('\n')[1]
        year = re.search('\((.*?)\)', movie_string).group(1)
        
        data = {"place": index+1,
                "movie_title": movie_title,
                "rating": ratings[index],
                "year": year,
                "star_cast": crew[index],
                "link": "https://www.imdb.com" + links[index]
                }
        list.append(data)

    json_object = json.dumps(list)
    with open("data/backup/imdb_top_100_movies.json", "w") as outfile:
        outfile.write(json_object)

    return list


def get_tv_series_info():
    url = "https://www.imdb.com/chart/tvmeter/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    tvseries = soup.select('td.titleColumn')
    crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
    ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
    links = [b.attrs.get('href') for b in soup.select('td.titleColumn a')]
    
    list = []

    for index in range(0, len(tvseries)):
        tvseries_string = tvseries[index].get_text()
        tvseries_title = tvseries_string.split('\n')[1]
        year = tvseries_string.split('\n')[2].replace("(", "").replace(")", "")

        data = {"place": index+1,
                "tvseries_title": tvseries_title,
                "rating": ratings[index],
                "year": year,
                "star_cast": crew[index],
                "link": "https://www.imdb.com" + links[index]
                }
        list.append(data)

    json_object = json.dumps(list)
    with open("data/backup/imdb_top_100_tv_series.json", "w") as outfile:
        outfile.write(json_object)
    return list
