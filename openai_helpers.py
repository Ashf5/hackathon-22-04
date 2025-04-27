
from openai import OpenAI
from password_tools import get_openai


def get_common(data):
    api_key = get_openai()
    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                'role': 'developer',
                'content': """You will be passed data in an array of dictionaries. Each dictionary contains details about a movie, such as runtime, genre...... The list of movies was given by a group of friends that would like to watch a movie and want to know what they would all enjoy, so they all gave in a few of their favorite movies. Your job is to tell us the common denominators between them. It doesn't have to be shared by all the movies, just by a bunch of them. Examples would be 'the runtimes are generally short', 'their are a lot of horror movies', 'Many of these movies are set in the olden days'.... The output should be adult or not,  list of most common genres, if there is a common theme in when the release date was, write that. Average runtime, and 2 or 3 keywords from the overview if there seems to be a common theme. The output should be short. If runtime isn't specified, put down 100. Store your response only in PURE json. There should be NOTHING in the response that isn't in json format. in this format 
                'adult: bool
                genres: list 
                avg_runtime: int 
                bet_date_avg: list (start date and end date avg of when most movies were made) 
                keywords: list 
                summary: str '
                The genres attribute should be a list of lists of common genres that seem to often go together ordered by most common, date should be yyyy-mm-dd, if the begining of average date is within 2 years, set 5 years back"""
            },
            {
                'role': 'user',
                'content': str(data)
            }
        ]
    )

    return response.output_text
