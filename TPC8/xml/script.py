from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, OWL
import xml.etree.ElementTree as ET
from collections import defaultdict


g = Graph()
g.parse("familia-base.ttl")

familia = Namespace("http://rpcw.di.uminho.pt/2024/familia/")

tree = ET.parse('biblia.xml')
root = tree.getroot()


def pessoaF():
    return {"nome": "", "sexo": "", "filhos": set()}

def familiaF():
    return {"pais": set(), "filhos": set()}


pessoas = defaultdict(pessoaF)
familias = defaultdict(familiaF)


for child in root:
    if child.tag == 'person':
        person_id = child.find('id').text
        
        pessoas[person_id]["nome"] = pessoas[person_id]["nome"] or child.find('namegiven').text
        pessoas[person_id]["sexo"] = pessoas[person_id]["sexo"] or child.find('sex').text
        
        for familyasspouse in child.findall('familyasspouse'):
            familias[familyasspouse.get('ref')]['pais'].add(person_id)
        
        for familyaschild in child.findall('familyaschild'):
            familias[familyaschild.get('ref')]['filhos'].add(person_id)
        
        for parent in child.findall('parent'):
            parent_id = parent.get('ref')
            pessoas[parent_id]["nome"] = pessoas[parent_id]["nome"] or parent.text
            pessoas[parent_id]["filhos"].add(person_id)
            
        for children in child.findall('child'):
            child_id = children.get('ref')
            pessoas[child_id]["nome"] = pessoas[child_id]["nome"] or children.text
            pessoas[person_id]["filhos"].add(child_id)


for family in familias.values():
    family['filhos'].difference_update(family['pais'])


for k, p in pessoas.items():
    person_uri = URIRef(f"{familia}{k}")
    g.add((person_uri, RDF.type, OWL.NamedIndividual))
    g.add((person_uri, RDF.type, familia.Pessoa))
    g.add((person_uri, familia.nome, Literal(p['nome'])))
    
    for c in p['filhos']:
        child_uri = URIRef(f"{familia}{c}")
        g.add((child_uri, RDF.type, OWL.NamedIndividual))
        g.add((child_uri, RDF.type, familia.Pessoa))
        g.add((child_uri, familia.nome, Literal(pessoas[c]['nome'])))
        
        if p['sexo'] == 'M':
            g.add((child_uri, familia.temPai, person_uri))
        else:
            g.add((child_uri, familia.temMae, person_uri))


with open("biblia.ttl", "w") as f:
    f.write(g.serialize())

    