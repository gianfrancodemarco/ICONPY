from time import sleep

from lib.queries import FILM_QUERY, create_query
from lib.wikidataAPI import WikiDataAPI
from lib.csvutilities import writeCSV, readCSVtoObj


def main():
    # leggiamo il csv
    data = readCSVtoObj("data/dataset.csv", ["id", "title"])

    already_fetched = readCSVtoObj("data/dataset_with_uris.csv", ["id", "title", "uri"])
    last_fetched = already_fetched[len(already_fetched)-1]["id"]

    data = data[int(last_fetched):]

    #leggi da dataset with uris, trova l'ultimo id

    print(f'Total movies: {len(data)}')

    i = 1
    for movie in data:

        print(f'Getting movie {i / len(data)}')

        # query per recupare l'uri del film
        wikidataAPI = WikiDataAPI()

        query = create_query(FILM_QUERY, [movie['title']])
        results = wikidataAPI.do_query(query)

        if results is None or len(results) == 0:
            continue

        result_movie = results[0]

        writeCSV(
            'data/dataset_with_uris.csv',
            [[movie['id'], movie['title'], result_movie['movie']['value']]],
            mode='a'
        )


while True:
    try:
        main()
    except Exception as e:
        print(e)
        sleep(600)
