import pickle

from src.lib.utils.utils import clean_string

WIKI_MOVIE_PROPS = [
    "wiki_data_id", "title", "main_subject", "follows", "genre", "performer", "country_of_origin",
    "original_language_of_film_or_TV_show", "publication_date", "director", "screenwriter", "cast_member",
    "director_of_photography", "film_editor", "production_designer", "costume_designer", "composer", "producer",
    "production_company", "distributed_by", "narrative_location", "filming_location", "duration", "award_received",
    "nominated_for", "box_office", "cost", "collection", "imdb_id", "metascore", "imdbrating", "imdbvotes"
]


class WikiMovie:

    def __init__(self, wiki_movie_response):
        self.wiki_movie_response = wiki_movie_response
        self.props = []

    def build_full(self):
        payload = self.wiki_movie_response
        properties = {}

        for prop in payload:

            # prende solo un titolo; se c'è, quello in inglese
            if prop['propLabel']['value'] == 'title' and 'title' in properties:
                if prop['value']['type'] == 'literal' and 'xml:lang' in prop['value'] and prop['value'][
                    'xml:lang'] == 'en':
                    del properties['title']
                else:
                    continue

            prop_label = prop['propLabel']['value'].replace(" ", "_")

            prop_value = {"uri": prop['value']['value'], "value": prop['valueLabel']['value']}

            # se la proprietà è già stato inserita, crea una lista (se non lo è già) e appende il nuovo valore
            if prop_label in properties:
                if isinstance(properties[prop_label], list):
                    values = properties[prop_label]
                else:
                    values = [properties[prop_label]]
                values.append(prop_value)

                properties[prop_label] = values
            else:
                properties[prop_label] = prop_value

        self.props = properties

        return properties

    def build(self):
        new_props = {}
        for key in self.props:
            if key.lower() in WIKI_MOVIE_PROPS:
                new_props[key] = self.props[key]

        self.props = new_props

    def set_prop(self, name, value):
        self.props[name] = value

    def serialize(self):
        filename = self.props["wiki_data_id"] + "_" + self.props["title"]["value"]
        filename = clean_string(filename)

        with open(f'data/serialized_movies/{filename}', 'wb') as f:
            pickle.dump(self, f)

    def get_statements(self):
        statements = []
        statements += self.get_statement("main_subject")
        statements += self.get_statement("follows", "sequel_of")
        statements += self.get_statement("genre")
        statements += self.get_statement("performer", "performed")
        statements += self.get_statement("country_of_origin")
        statements += self.get_statement("original_language_of_film_or_TV_show", "original_language")
        statements += self.get_statement("publication_date")
        statements += self.get_statement("director", "directed")
        statements += self.get_statement("screenwriter", "screenwrited")
        statements += self.get_statement("cast_member", "acted")
        statements += self.get_statement("director_of_photography", "directed_photography")
        statements += self.get_statement("film_editor", "editor")
        statements += self.get_statement("production_designer")
        statements += self.get_statement("costume_designer")
        statements += self.get_statement("composer", "composed")
        statements += self.get_statement("produced", "produced")
        statements += self.get_statement("production_company")
        statements += self.get_statement("distributed_by")
        statements += self.get_statement("narrative_location")
        statements += self.get_statement("filming_location")
        statements += self.get_statement("duration")
        statements += self.get_statement("award_received")
        statements += self.get_statement("nominated_for")
        statements += self.get_statement("box_office")
        statements += self.get_statement("cost")
        statements += self.get_statement("collection")

        # statements = [bytes(statement, 'utf-8').decode('utf-8', 'ignore') for statement in statements]

        return statements

    def get_statement(self, key, label=None):

        if key not in self.props:
            return []

        if label is None:
            label = key

        title = self.props['title']['value'].replace('"', "'")
        value = self.props[key] if type(self.props[key]) == list else [self.props[key]]
        statements = []

        for statement in value:
            val = statement["value"].replace('"', "'")
            statements.append(f'{label}("{title}", "{val}")')

        return statements

    def get_csv_representation(self, delimiter=";"):

        csv_representation = []

        for key in WIKI_MOVIE_PROPS:
            if key in self.props:
                if type(self.props[key]) == list:
                    csv_representation.append(",".join(map(lambda x: x['value'], self.props[key])))
                else:
                    if 'value' in self.props[key]:
                        csv_representation.append(self.props[key]['value'])
                    else:
                        csv_representation.append(self.props[key])
            else:
                csv_representation.append("?")

        return csv_representation
