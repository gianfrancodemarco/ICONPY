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

ENTITY_QUERY = '''
SELECT ?prop ?value ?propLabel ?valueLabel{
  VALUES (?movie) {(wd:<1>)}

  ?movie ?p ?statement .
  ?statement ?ps ?value .
  
  ?prop wikibase:claim ?p.
  ?prop wikibase:statementProperty ?ps.

  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
ORDER BY ?wd ?statement ?value
'''


def create_query(query_text, values):
    i = 1
    for value in values:
        query_text = query_text.replace(f'<{i}>', f'{value}')
        i += 1

    params = {"query": query_text, "format": "json"}

    return params
