import json
with open("alunos.json") as f:
    data = json.load(f)

s="""@prefix : <http://rpcw.di.uminho.pt/2024/teste/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/teste/> .

<http://rpcw.di.uminho.pt/2024/teste> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/teste#exame
:exame rdf:type owl:ObjectProperty ;
       rdfs:domain :Aluno ;
       rdfs:range :Exame .


###  http://rpcw.di.uminho.pt/2024/teste#tpc
:tpc rdf:type owl:ObjectProperty ;
     rdfs:domain :Aluno ;
     rdfs:range :TPC .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/teste#curso
:curso rdf:type owl:DatatypeProperty ;
       rdfs:domain :Aluno ;
       rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/teste#idAluno
:idAluno rdf:type owl:DatatypeProperty ;
         rdfs:domain :Aluno ;
         rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/teste#nome
:nome rdf:type owl:DatatypeProperty ;
      rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/teste#nota
:nota rdf:type owl:DatatypeProperty ;
      rdfs:domain :Exame ,
                  :TPC ;
      rdfs:range xsd:integer .


###  http://rpcw.di.uminho.pt/2024/teste#projeto
:projeto rdf:type owl:DatatypeProperty ;
         rdfs:domain :Aluno ;
         rdfs:range xsd:integer .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/teste#Aluno
:Aluno rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/teste#Exame
:Exame rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/teste#TPC
:TPC rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/teste#Especial
:Especial rdf:type owl:Class ;
          rdfs:subClassOf :Exame .


###  http://rpcw.di.uminho.pt/2024/teste#Normal
:Normal rdf:type owl:Class ;
        rdfs:subClassOf :Exame .


###  http://rpcw.di.uminho.pt/2024/teste#Recurso
:Recurso rdf:type owl:Class ;
         rdfs:subClassOf :Exame .

"""

for aluno in data['alunos']:
    id = aluno["idAluno"]
    nome =  aluno["nome"]
    curso = aluno["curso"]
    tpcs=set()
    for i in aluno["tpc"]:
        tpcId = id + "_" + i["tp"]
        tpcs.add(tpcId)
        s+=f"""
###  http://rpcw.di.uminho.pt/2024/teste#{tpcId}
:{tpcId} rdf:type :TPC ;
    :nome "{i["tp"]}";
    :nota {i["nota"]} .
"""
    projeto = aluno["projeto"]
    exames=set()
    for k,v in aluno["exames"].items():
        exameId = id + "_exame_" + k
        exames.add(exameId)
        s+=f"""
###  http://rpcw.di.uminho.pt/2024/teste#{exameId}
:{exameId} rdf:type :{k[0].upper()+k[1:]} ;
    :nota {v} .
"""
    s+=f"""
###  http://rpcw.di.uminho.pt/2024/teste#{id}
:{id} rdf:type :Aluno ;
    :projeto {projeto} ;
    :curso "{curso}" ;
    :nome "{nome}";
"""+"".join([f"    :tpc :{tpc};\n" for tpc in tpcs])+"".join([f"    :exame :{exame};\n" for exame in exames])+f":id \"{id}\" ."

with open("ontologia_alunos.ttl", "w") as file:
    file.write(s)