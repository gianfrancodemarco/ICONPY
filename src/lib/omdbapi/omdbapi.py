import requests

#bb0c5db9
#2c6308fb
class OMDBApi:
    def __init__(self):
        self.key = "37a11503"
        self.url = f"http://www.omdbapi.com/?i=<id>&apikey={self.key}"

    def get_movie(self, imdb_id):
        return requests.get(self.url.replace("<id>", imdb_id))

