from password_tools import get_postgres 
import psycopg2

def get_connection()->tuple:
    """
    Returns a connection and cursor object.
    """
    DB_NAME = "Hackathon1_database"
    USER = "postgres" 
    PASSWORD = get_postgres()
    HOST = "localhost"

    connection = psycopg2.connect(host=HOST, user=USER, password=PASSWORD, dbname=DB_NAME )
    cursor = connection.cursor()
    return connection, cursor


def insert_data(movie, username):
    """
    INSERTS movie username into database, if doesn't exist yet
    """
   
    connection, cursor = get_connection()
    # Get user id Or create new user if doesn't exist
    query_for_user = f"""SELECT user_id FROM users WHERE user_name = '{username}'"""
    cursor.execute(query_for_user)
    try:
        user_id = cursor.fetchall()[0][0]
    except IndexError:
        create_user_query = f"""INSERT INTO users (user_name) VALUES ('{username}')"""
        cursor.execute(create_user_query)
        connection.commit()
        cursor.execute(query_for_user)
        user_id = cursor.fetchall()[0][0]

    
    # Insert the movie and user data 
    movie_query = f"""INSERT INTO movies (movie_id) VALUES ('{movie}') ON CONFLICT(movie_id) DO NOTHING"""
    cursor.execute(movie_query)
    connection.commit()
    data_query = f"""INSERT INTO user_movies (movie_id, user_id) VALUES ('{movie}', '{user_id}') ON CONFLICT(movie_id, user_id) DO NOTHING"""
    cursor.execute(data_query)
    connection.commit()
    print("Success!")

def get_movie_ids():
    """
    Returns a list of all the movie id's
    """
    connection, cursor = get_connection()
    cursor.execute("SELECT movie_id FROM movies")
    data = cursor.fetchall()
    ids = [i[0] for i in data]
    return ids

