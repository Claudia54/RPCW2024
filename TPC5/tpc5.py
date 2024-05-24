import json, requests


sparql_endpoint = "http://dbpedia.org/sparql"

sparql_query = """
PREFIX schema: <http://schema.org/>
SELECT DISTINCT ?movie  ?name ?title ?director ?duration ?writer ?composer WHERE {
  ?movie a schema:Movie ;
  dbp:name ?name;
  dbo:director ?director ;
 dbo:musicComposer ?composer ;
 dbo:runtime ?duration ;
 dbo:writer ?writer;
FILTER (LANG(?name) = 'en') .
} LIMIT 1000
"""


headers = {
    "Accept": "application/sparql-results+json"
}


params = {
    "query": sparql_query,
    "format": "json"
}


response = requests.get(sparql_endpoint, params=params, headers=headers)

dic_movie = {}
json_movies = []
# Check if the request was successful
if response.status_code == 200:
    results = response.json()

    for result in results["results"]["bindings"]:
        movie = result['movie']['value']
        if movie not in dic_movie:
            dic_movie[movie] = {
                "name": [],
                "director": [],
                "writer": [],
                "duration":[],
                "composer": [],
                "uri": movie
            }
        dic_movie[movie]["director"].append(result['director']['value'])
        dic_movie[movie]["writer"].append(result['writer']['value'])
        dic_movie[movie]["name"].append(result['name']['value'])
        dic_movie[movie]["duration"].append(result['duration']['value'])
        dic_movie[movie]["composer"].append(result['composer']['value'])


    for dic_movie in dic_movie.values():
        dic_movie["director"] = list(set(dic_movie["director"]))
        dic_movie["writer"] = list(set(dic_movie["writer"]))
        dic_movie["name"] = list(set(dic_movie["name"]))
        dic_movie[movie]["duration"].append(result['duration']['value'])
        dic_movie["composer"] = list(set(dic_movie["composer"]))
        json_movies.append({
            "name": dic_movie["name"],
            "director": dic_movie["director"],
            "writer": dic_movie["writer"],
            "composer": dic_movie["composer"],
            "duration": dic_movie["duration"],
            "uri": dic_movie["uri"]
        })
        
    f = open("movie.json", "w", encoding='utf-8')
    json.dump(json_movies, f, indent=4)
    f.close()

else:
    print("Error:", response.status_code)