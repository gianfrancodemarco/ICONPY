FILM_QUERY = '''
SELECT DISTINCT ?movie ?title ?language
WHERE{
  ?movie wdt:P31 wd:Q11424.
  ?movie rdfs:label ?title.
  ?movie wdt:P364 ?language.
  FILTER(STRSTARTS(?title, "<1>")).
  FILTER((LANG(?title)) = "en").
}
'''


def create_query(query_text, values):

    i = 1
    for value in values:
        query_text = query_text.replace(f'<{i}>', f'{value}')
        i += 1

    params = {"query": query_text, "format": "json"}

    return params
