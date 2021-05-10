import pickle

WIKI_MOVIE_PROPS = ["instance_of", "cast_member", "title", "PORT_film_ID"]

class WikiMovie:

    def __init__(self, wiki_movie_response):
        self.wiki_movie_response = wiki_movie_response
        self.props = []

    def build(self):
        payload = self.wiki_movie_response
        props = {}

        for prop in payload:
            prop_label = prop['propLabel']['value'].replace(" ", "_")

            if True:
            #if prop_label in WIKI_MOVIE_PROPS:

                prop_value = {"uri": prop['value']['value'], "value": prop['valueLabel']['value']}

                if prop_label in props:
                    if isinstance(props[prop_label], list):
                        values = props[prop_label]
                    else:
                        values = [props[prop_label]]
                    values.append(prop_value)

                    props[prop_label] = values
                else:
                    props[prop_label] = prop_value

        self.props = props

        return props

    def set_prop(self, name, value):
        self.props[name] = value

    def serialize(self):
        filename = self.props["wiki_data_id"] + "_" + self.props["title"]["value"]

        with open(f'data/movie_serialized/{filename}', 'wb') as f:
            pickle.dump(self, f)
