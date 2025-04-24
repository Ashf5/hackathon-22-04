from password_tools import get_tmdb
import requests 
from urllib.parse import urlencode

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
    





if __name__ == "__main__":
    print(get_movie_details(671))