from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json
import time

url = "{show}reviews?sort=totalVotes&dir=desc&ratingFilter=0"

def get_reviews(id: str, max_reviews: int): 
    
    driver = webdriver.Chrome()
    driver.get(url.format(show=id)) 

    count = 25
    while True:
        try:
            if count >= max_reviews:
                break
            load_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ipl-load-more__button']")))
            load_more_button.click()
            count += 15
        except:
            break

    reviews = driver.find_elements("css selector", ".lister-item-content")
    big_box = driver.find_elements("css selector", ".lister-item")
    
    reviews_list = list()
    
    for index, review in enumerate(reviews):
        review_dict = dict()
        review_dict['text'] = review.find_element("css selector", ".content .text").text
        review_dict['title'] = review.find_element("css selector", ".title").text
        
        try:    
            review_dict['rating'] = review.find_element("css selector",".rating-other-user-rating span:first-of-type").text
        except NoSuchElementException:
            review_dict['rating'] = None
        
        try:
            upvote = review.find_element("css selector", ".content .actions").text.split(" ")
            review_dict['upvote'] = upvote[0]
            review_dict['total-vote'] = upvote[3]
        except NoSuchElementException:
            button = big_box[index].find_element("css selector", ".ipl-expander")
            button.click()
            
            upvote = review.find_element("css selector", ".content .actions").text.split(" ")
            review_dict['upvote'] = upvote[0]
            review_dict['total-vote'] = upvote[3]

        reviews_list.append(review_dict)

    driver.quit()
    return reviews_list


def add_reviews_to_movies(shows: [], path: str):
    for index, movie in enumerate(shows):
        users_reviews = get_reviews(movie['link'], 50)
        movie['users_reviews'] = users_reviews
    
    json_object = json.dumps(shows)
    with open(path, "w", encoding="utf-8") as outfile:
        outfile.write(json_object)