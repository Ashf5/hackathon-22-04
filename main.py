from tmdb_helpers import get_movie_id, get_movie_details, discover_movies
from postgres_helpers import insert_data, get_movie_ids
from openai_helpers import get_common
import json



def get_user_input():
    """
    Asks user for a username and movie and returns the two
    """
    username = input("Enter the username: ")
    movie = input("Enter a favorite movie: ")
    return username, movie 

def insert_database(username, movie):
    """
    Accepts as arguments a username and movie. Calls the function to get the movie id and inputs both into database.
    """
    movie_id = get_movie_id(movie)
    # Check to make sure the movie was found 
    if not movie_id:
        print("couldn't find the movie")
        return None 
    insert_data(movie_id, username)


def get_movies(movies):
    """
    Accepts a list of movie id's and returns a list of dictionaries with their details.
    """
    movie_details = []
    for movie in movies:
        deets = get_movie_details(movie)
        if deets:
            movie_details.append(deets)
            

    return movie_details
    

if __name__ == "__main__":
    while True:
        answer = input("1: Add movie\n2: Find us some movie\n3: quit ")
        if answer == '1':
            user_input = get_user_input()
            insert_database(*user_input)
            continue 
        elif answer == '2':
            print('Thinking....')
            ids = get_movie_ids()
            deets = get_movies(ids)
            data = get_common(deets)
            data = json.loads(data)
            to_watch = discover_movies(data)
            print(data['summary'])
            for movie in to_watch:
                print(f"Title: {movie['title']}")
                print(f"Overview: {movie['overview']}")
                print(f"Release Date: {movie['release_date']}")
                print('\n')
            break 
        else:
            break 
            
            
            