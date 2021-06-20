import requests

#bb0c5db9
class OMDBApi:
    def __init__(self):
        self.key = "96d93400"
        self.url = f"http://www.omdbapi.com/?i=<id>&apikey={self.key}"

    def get_movie(self, imdb_id):
        return requests.get(self.url.replace("<id>", imdb_id))

