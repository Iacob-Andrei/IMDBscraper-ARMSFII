import re
import json
import reviews
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_episodes_tvshow(id: str, max_reviews: int):
    driver = webdriver.Chrome()
    driver.get(id + "episodes")
    
    num_seasons = len(driver.find_elements(By.XPATH, "//select[@id='bySeason']/option"))
    
    tvshow_seasons = dict()
    for season in range(1, num_seasons+1):
        url_season = id + "episodes?season=" + str(season)
        driver.get(url_season)

        episode_links = driver.find_elements(By.XPATH, "//div[@class='info']/strong/a")
        all_ratings = driver.find_elements("css selector", " .ipl-rating-star__rating")
        ratings = list()
        
        for rating in all_ratings:
            if bool(re.search(r'\d', rating.text)):
                ratings.append(rating.text)
        
        if len(ratings) == 0:
            break
        
        season_list = list()
        for index, link in enumerate(episode_links):
            if index >= len(ratings):
                break
            episode = dict()
            episode['number'] = index + 1
            episode['link'] = link.get_attribute("href").split("?")[0]
            episode['title'] = link.text
            episode['rating'] = ratings[index]
            episode['reviews'] = reviews.get_reviews(episode['link'], max_reviews)
            
            season_list.append(episode)
        tvshow_seasons[season] = season_list
    
    driver.quit()
    return tvshow_seasons

def add_episodes_to_tv_series(tvseries:[], path: str):
    for index, series in enumerate(tvseries):
        episodes = get_episodes_tvshow(series['link'], 20)
        series['seasons'] = episodes
    
        json_object = json.dumps(series)
        with open(path, "a", encoding="utf-8") as outfile:
            outfile.write(json_object)
            outfile.write(",\n")