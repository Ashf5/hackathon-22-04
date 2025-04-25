from password_tools import get_tmdb
import requests 
from urllib.parse import urlencode
import json

def get_movie_id(movie)->int:
    """
    This function takes in a movie string and returns the movie int, returns None if it can't be found
    """
    # get the tmdb password
    password = get_tmdb()
    if not password:
        return None
    params = {
        'query': movie
    }
    url = f"https://api.themoviedb.org/3/search/movie?{urlencode(params)}&include_adult=true&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {password}"
    }

    response = requests.get(url, headers=headers)
    try:
        return response.json()['results'][0]['id']
    except IndexError:
        print('Movie not found')
        return None
    except:
        print('Error getting movie')
        return None


def get_movie_details(movie_id)->dict:
    """
    Takes in a movie_id and returns some data in a dictionary to be passed on to be analyzed. If there's an issue it returns None.
    """

    password = get_tmdb()
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {password}"
    }

    response = requests.get(url, headers=headers)

    json_data = response.json()
    try:
        return {
            'name' : json_data['original_title'],
            'adult' : json_data['adult'],
            'budget' : json_data['budget'],
            'genres' : [genre['name'] for genre in json_data['genres']],
            'release' : json_data['release_date'],
            'runtime' : json_data['runtime'],
            'vote_average' : json_data['vote_count'],
            'overview': json_data['overview']
        }
    except KeyError:
        print("Movie not found")
        return None
    except:
        print("Error getting movie data")
        return None
    
def get_keyword_id(keyword):
    """
    Accepts a keyword and returns the id or none if the id wasn't found.
    """
    api_key = get_tmdb()
    url = f"https://api.themoviedb.org/3/search/keyword?query={keyword}&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(url, headers=headers)

    try:
        id = response.json()['results'][0]['id']
        return id 
    except (KeyError, IndexError):
        return None

def get_genre_ids(genres):
    """
    Accepts a list of genres and returns the ids in a list.
    """
    with open('genres.json', 'r') as f:
        genre_list = json.load(f) 
    
    genre_ids = []
    for genre in genres:
        try:
            id = genre_list[genre]
            genre_ids.append(id)
        except KeyError:
            continue 
    return genre_ids


    

def discover_movies(data):
    """
    Takes in the data given back from openai and searches for movies matching the description. It returns 5 movies from each group of genres.
    """
    # headers for the request
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {get_tmdb()}"
    }

    to_watch = []
    # Get all the keywords in and put in a string 
    keyword_string = ""
    for keyword in data['keywords']:
        id = get_keyword_id(keyword)
        if id:
            keyword_string += str(id)+'|'

    # Go through all the sets of genres and make a request with each
    for set_genres in data['genres']:
        genre_ids = get_genre_ids(set_genres)
        param = ""
        for genre in genre_ids:
            param += str(genre) + ","

        url = f"https://api.themoviedb.org/3/discover/movie?include_adult={data['adult']}&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_genres={param}&with_runtime.gte={data['avg_runtime'] - 20}&with_runtime.lte{data['avg_runtime'] + 20}&primary_release_date.gte={data['bet_date_avg'][0]}&with_keywords={keyword_string}"
        response = requests.get(url, headers=headers)

        to_watch.extend(get_clean_data(response.json(), to_watch))
    return to_watch



def get_clean_data(data, current_list):
    """
    returns a list of up to five movies, in a list of dictionaries
    """
    li_movies = []
    counter = 0
    for i in data['results']:
        movie_dict = {
            'title': i['original_title'],
            'overview': i['overview'],
            'release_date': i['release_date']

        }

        # make sure you don't get doubles
        if movie_dict in current_list:
            continue

        li_movies.append(movie_dict)
        counter += 1 
        if counter == 5:
            break 
    return li_movies


