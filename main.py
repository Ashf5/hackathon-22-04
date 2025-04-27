from tmdb_helpers import get_movie_id, get_movie_details, discover_movies
from postgres_helpers import insert_data, get_movie_ids, delete_movies
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
    # use a set so we don't have to request the same movie twice
    movie_set = set(movies)
    for movie in movie_set:
        deets = get_movie_details(movie)
        if deets:
            # append the amount of times the movie was nominated by users
            for i in range(movies.count(movie)):
                movie_details.append(deets)
            

    return movie_details
    

if __name__ == "__main__":
    while True:
        answer = input("1: Add movie\n2: Find us some movie\n3: Delete all movies\n4: quit ")
        if answer == '1':
            user_input = get_user_input()
            insert_database(*user_input)
            continue 
        elif answer == '2':
            ids = get_movie_ids()

            # verify that there are movies available
            if len(ids) == 0:
                print("No movies were provided, please add movies")
                continue

            print('Thinking....')
            deets = get_movies(ids)
            data = get_common(deets)
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                print("Error with output from openai, please update or try again.")
                continue
            to_watch = discover_movies(data)
            print(f"\n{data['summary']}\n")
            for movie in to_watch:
                print(f"Title: {movie['title']}")
                print(f"Overview: {movie['overview']}")
                print(f"Release Date: {movie['release_date']}")
                print('\n')
            break 
        elif answer == '3':
            delete_movies()
        else:
            break 
            
            
            