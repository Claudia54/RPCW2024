import json
import random

with open("tpc3.json") as f:
    bd = json.load(f)

ttl = ""

cidades = bd["cidades"]
ligacoes = bd["ligacoes"]

for cidade in cidades: 
    registo= f"""     ###  http://rpcw.di.uminho.pt/2024/mapa#{cidade['id']}
                                :{cidade['id']} rdf:type owl:NamedIndividual ,
                                            :Cidade ;
                                    :distrito "{cidade['distrito'].replace(" ", "_")}" ;
                                    :id "{cidade['id']}" ;
                                    :nome "{cidade['nome'].replace(" ", "_")}" ;
                                    :populacao {cidade['população']} .
                """ 
    ttl+=registo

for ligacao in bd['ligacoes']:
    registo = f""" ###  http://rpcw.di.uminho.pt/2024/mapa#{ligacao['id']}
                                :{ligacao['id']} rdf:type owl:NamedIndividual ,
                                            :Ligacao ;
                                    :destino :{ligacao['destino']} ;
                                    :origem :{ligacao['origem']} ;
                                    :distancia {ligacao['distância']} ;
                                    :idLig "{ligacao['id']}" .
"""
    ttl += registo

with open('output.ttl', 'w') as output:
    output.write(ttl)
