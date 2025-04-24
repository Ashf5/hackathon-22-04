def get_tmdb()->str:
    """
    Returns my tmdb api key. Must be edited to go to the file it's stored in on users device.
    """
    try:
        with open('/Users/fried/hackathon_passwords/tmdb.txt') as f:
            password = f.read()
    except FileNotFoundError:
        print("File not found")
        return None
    except:
        print('an error occured while getting your tmdb password')
        return None
    return password

def get_openai()->str:
    try:
        with open('/Users/fried/hackathon_passwords/openai.txt') as f:
            password = f.read()
    except FileNotFoundError:
        print("File not found")
        return None
    except:
        print('an error occured while getting your openai password')
        return None
    return password


def get_postgres()->str:
    try:
        with open('/Users/fried/hackathon_passwords/postgres.txt') as f:
            password = f.read()
    except FileNotFoundError:
        print("File not found")
        return None
    except:
        print('an error occured while getting your openai password')
        return None
    return password

