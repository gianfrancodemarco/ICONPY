import _thread
import time

from lib.datasetcreator import get_uris, get_entities
from lib.queries import create_query, ENTITY_QUERY
from lib.wikidata import wikidataAPI
from lib.wikidata.wikidataAPI import WikiDataAPI
from lib.wikidata.wikimovie import WikiMovie

#get_entities(resume_id=38)

wikiAPI = WikiDataAPI()

#77
query = create_query(ENTITY_QUERY, ['Q25188'])
results = wikiAPI.do_query(query)

wiki_movie = WikiMovie(results)
wiki_movie.build()
wiki_movie.set_prop("wiki_data_id", 'Q25188')
wiki_movie.serialize()
