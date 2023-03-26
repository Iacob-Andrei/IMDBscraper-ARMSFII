import shows
import reviews
import json
import episodes
import processtext

def movies():
    # data = shows.get_movies_info()  
    # reviews.add_reviews_to_movies(data, "data/backup/imdb_top_100_movies_with_reviews.json")
    
    with open('data/backup/imdb_top_100_movies_with_reviews.json') as json_file:
        data = json.load(json_file)
    processtext.process_movies(data)

def tvshows():
    # data = shows.get_tv_series_info()
    # episodes.add_episodes_to_tv_series(data, "data/backup/imdb_top_100_tv_series_with_episodes_reviews.json")
    
    with open('data/backup/imdb_top_100_tv_series_with_episodes_reviews.json') as json_file:
        data = json.load(json_file)
    processtext.process_tvshows(data)


if __name__ == "__main__":
    movies()
    # tvshows()