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
            if prop_label in WIKI_MOVIE_PROPS:

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


def serialize(objects):
    with open('data/wikimovieserialization', 'wb') as f:
        pickle.dump(len(objects), f)
        for obj in objects:
            pickle.dump(obj, f)


def deserialize():
    objects = []
    with open('data/wikimovieserialization', 'rb') as f:
        for _ in range(pickle.load(f)):
            objects.append(pickle.load(f))

    return objects
