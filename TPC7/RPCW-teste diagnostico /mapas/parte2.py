import requests

# SPARQL endpoint URL
sparql_endpoint = "http://localhost:7200/repositories/Mapas2"

# SPARQL CONSTRUCT query
sparql_query = """
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa/>

CONSTRUCT {
  :ligacao a :Ligação;
            :origem ?ori;
            :destino ?des.
}
WHERE {
  ?ori a :Cidade.
  ?lig a :Ligação.
  ?lig :origem ?ori.
  ?lig (:destino/^:origem)* ?ligações.
  ?ligações :destino ?des.
}
"""

# Sending the SPARQL CONSTRUCT query to GraphDB
response = requests.post(sparql_endpoint, data={'update': sparql_query})

if response.status_code == 200:
    print("Query executed successfully.")
else:
    print("Failed to execute the query.")

# Extracting the resulting triples
triples = response.text

# Now, let's insert the obtained triples back into the ontology
insert_query = """
INSERT DATA {
  %s
}
""" % triples

# Sending the INSERT query to GraphDB
insert_response = requests.post(sparql_endpoint, data={'update': insert_query})

if insert_response.status_code == 200:
    print("Triples inserted successfully.")
else:
    print("Failed to insert the triples.")
