from time import sleep

from lib.queries import FILM_QUERY, create_query, ENTITY_QUERY
from lib.utils import all_files_in_path
from lib.wikidata.wikidataAPI import WikiDataAPI
from lib.wikidata.wikimovie import WikiMovie
from lib.csvutilities import writeCSV, readCSVtoObj
import webbrowser
import collections

#data_ids = [movie['uri'].split('/')[-1] for movie in data]
#dataset = []
#for movie in data:
#    dataset_ids = [movie['id'] for movie in dataset]
#    if movie['id'] not in dataset_ids:
#        dataset.append(movie)
#print(dataset)

#dataset = [[movie["id"], movie["title"], movie["uri"]] for movie in dataset]
#writeCSV('data/dataset_with_uris.csv', dataset, mode='w')


#files = [_.split('_')[0] for _ in all_files_in_path('data/serialized_movies')]
#print(len(files))
#print(len(set(files)))
#print([item for item, count in collections.Counter(data).items() if count > 1])
#print(len([item for item, count in collections.Counter(data).items() if count > 1]))
#asd = [idx for idx in files if idx not in [_['uri'].split('/')[-1] for _ in data]]
#print([_['uri'].split('/')[-1] for _ in data])
#print(files)
#print(len(asd))


#lunghezza di dataset_with_uris originale: 4124
#doppioni in dataset_with_uris originale: 246
#distinct = 3979

#data = readCSVtoObj("data/_old_dataset_with_uris.csv", ["id", "title", "uri"])
#data = [el for el in data]
#print(len(data))
#print(len(set([_['uri'].split('/')[-1] for _ in data])))

#new_dataset_with_movies = []
#for movie in data:
#    new_dataset_with_movies_uris = [_['uri'].split('/')[-1] for _ in new_dataset_with_movies]
#    if movie['uri'].split('/')[-1] not in new_dataset_with_movies_uris:
#        new_dataset_with_movies.append(movie)


#writeCSV("data/dataset_with_uris.csv", rows=[[count, _['title'], _['uri']] for count, _ in enumerate(new_dataset_with_movies)])