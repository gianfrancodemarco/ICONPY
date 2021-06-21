import requests


# bb0c5db9
KEY = "96d93400"
URL = f"http://www.omdbapi.com/?i=<id>&apikey={KEY}"

def get_movie(imdb_id):
    return requests.get(URL.replace("<id>", imdb_id))
