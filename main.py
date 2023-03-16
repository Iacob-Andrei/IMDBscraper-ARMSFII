import shows
import reviews
import json
import episodes

if __name__ == "__main__":
    # movies_list = shows.get_movies_info()  
    # tvseries_list = shows.get_tv_series_info()
    
    # with open('data/without-reviews/imdb_top_100_movies.json') as json_file:
    #     data = json.load(json_file)
    #     reviews.add_reviews_to_movies(data, "data/imdb_top_100_movies_with_reviews.json")
    
    with open('data/without-reviews/imdb_top_100_tv_series.json') as json_file:
        data = json.load(json_file)
        episodes.add_episodes_to_tv_series(data, "data/imdb_top_100_tv_series_with_episodes_reviews.json")