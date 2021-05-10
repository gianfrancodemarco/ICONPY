import pickle

from lib.utils import clean_filename

WIKI_MOVIE_PROPS = ["instance_of", "cast_member", "title", "PORT_film_ID"]

class WikiMovie:

    def __init__(self, wiki_movie_response):
        self.wiki_movie_response = wiki_movie_response
        self.properties = []

    def build_full(self):
        payload = self.wiki_movie_response
        properties = {}

        for prop in payload:

            #prende solo un titolo; se c'è, quello in inglese
            if prop['propLabel']['value'] == 'title' and 'title' in properties:
                if prop['value']['type'] == 'literal' and 'xml:lang' in prop['value'] and prop['value']['xml:lang'] == 'en':
                    del properties['title']
                else:
                    continue

            prop_label = prop['propLabel']['value'].replace(" ", "_")

            if True:
            #if prop_label in WIKI_MOVIE_PROPS:

                prop_value = {"uri": prop['value']['value'], "value": prop['valueLabel']['value']}

                #se la proprietà è già stato inserito, crea una lista (se non lo è già) e appende il nuovo valore
                if prop_label in properties:
                    if isinstance(properties[prop_label], list):
                        values = properties[prop_label]
                    else:
                        values = [properties[prop_label]]
                    values.append(prop_value)

                    properties[prop_label] = values
                else:
                    properties[prop_label] = prop_value

        self.properties = properties

        return properties

    def set_prop(self, name, value):
        self.properties[name] = value

    def serialize(self):
        filename = self.properties["wiki_data_id"] + "_" + self.properties["title"]["value"]
        filename = clean_filename(filename)

        with open(f'data/serialized_movies/{filename}', 'wb') as f:
            pickle.dump(self, f)
