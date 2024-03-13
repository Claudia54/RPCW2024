from flask import Flask, render_template, url_for
import requests
from datetime import datetime

app = Flask(__name__)
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%d %H:%M:%S')


endpoint = "http://localhost:7200/repositories/tab-period"

@app.route('/')

def index():
    return render_template('index.html', data = {"data": data_iso_formatada})

@app.route('/elements')
def elements():
    sparql_query = """
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select * where { 
	?s a tp:Element;
    tp:name ?nome;
    tp:symbol ?simb;
    tp:atomicNumber ?n .
    ?grupo a tp:Group .
    ?grupo tp:element ?s . 
}order by ?n
"""

    response = requests.get(endpoint, params={"query": sparql_query},
        headers = {'Accept': 'application/sparql-results+json'}
    )
    if response.status_code == 200:
        data = response.json()["results"]["bindings"]
        return render_template('elements.html', data=data)
    else:
        return render_template('empty.html', data=data_iso_formatada)

@app.route('/groups')
def groups():
    sparql_query = """
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select * where {
        ?s a tp:Group.
        optional {?s tp:name ?nome. }
        optional {?s tp:number ?n . }
    }order by ?n
"""
    payload = {"query": sparql_query}
    response = requests.get(endpoint, params=payload,
        headers = {'Accept': 'application/sparql-results+json'}
    )
    if response.status_code == 200:
        data = response.json()["results"]["bindings"]
        return render_template('groups.html', data=data)
    else:
        return render_template('empty.html', data=data_iso_formatada)

@app.route('/elements/<int:na>')
def element(na):
    sparql_query = f"""
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select * where {{ 
	?s a tp:Element ;
    tp:name ?nome;
    tp:symbol ?simb;
    tp:atomicWeight ?pa;
    tp:block ?bloco; 
    tp:casRegistryID ?rid;
    tp:classification ?class;
    tp:color ?cor;
    tp:group ?grupo;
    tp:period ?periodo;
    tp:standardState ?estado;
    tp:atomicNumber {na} .
    ?s tp:atomicNumber ?na . 
}}
"""
    response = requests.get(endpoint, params= {"query": sparql_query},
        headers = {'Accept': 'application/sparql-results+json'}
    )
    if response.status_code == 200:
        data = response.json()["results"]["bindings"]
        return render_template('element.html', data=data[0])
    else:
        return render_template('empty.html', data=data_iso_formatada)
    
@app.route('/groups/<string:na>')
def group(na):
    sparql_query = f"""
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select * where {{
        optional {{ tp:{na} tp:name ?nome. }}
        optional {{ tp:{na} tp:number ?n . }}
        tp:{na} tp:element ?element .
        ?element tp:name ?nomeElem .
        ?element tp:symbol ?simb .
        ?element tp:atomicNumber ?na .
        ?element tp:group ?id .
    }}
"""
    payload = {"query": sparql_query}

    response = requests.get(endpoint, params=payload, headers = {'Accept': 'application/sparql-results+json'})
    if response.status_code == 200:
        data = response.json()["results"]["bindings"]
        print(data)
        return render_template('group.html', data=data)
    else:
        return render_template('empty.html', data=data_iso_formatada)
    
if __name__ == '__main__':
    app.run(debug=True)