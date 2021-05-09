import _thread
import time

from lib.datasetcreator import get_uris, get_entities
from lib.wikidata.wikimovie import WikiMovie, deserialize, serialize

wikimovie = WikiMovie([{'prop': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/P905'},
                        'value': {'type': 'literal', 'value': '75078'},
                        'propLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'PORT film ID'},
                        'valueLabel': {'type': 'literal', 'value': '75078'}}])
wikimovie2 = WikiMovie([{'prop': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/P905'},
                         'value': {'type': 'literal', 'value': '75078'},
                         'propLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'PORT film ID'},
                         'valueLabel': {'type': 'literal', 'value': 'STO CAZZO'}}])

wikimovie.build()
wikimovie2.build()

serialize([wikimovie, wikimovie2])

movies = deserialize()
print(movies)