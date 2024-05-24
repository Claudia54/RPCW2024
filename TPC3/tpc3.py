import json
import random

with open("tpc3.json") as f:
    bd = json.load(f)


prefixos = """
@prefix : <http://rpcw.di.uminho.pt/2024/untitled-ontology-28/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/untitled-ontology-28/> .

<http://rpcw.di.uminho.pt/2024/untitled-ontology-28> rdf:type owl:Ontology .
"""
# Prefixos para o arquivo TTL
ttl = prefixos

# Adicionar os alunos, projetos, TPCs e exames ao TTL
for aluno in bd["alunos"]:
    aluno_id = aluno['idAluno']
    aluno_nome = aluno['nome'].replace(" ", "_")
    aluno_curso = aluno['curso']
    
    # Criar a entrada do aluno
    registo_aluno = f"""
    ###  http://rpcw.di.uminho.pt/2024/untitled-ontology-28#{aluno_id}
    :{aluno_id} rdf:type owl:NamedIndividual ,
                :Aluno ;
        :Id "{aluno_id}" ;
        :Nome "{aluno_nome}" ;
        :matriculadoEm "{aluno_curso}" .
    """
    ttl += registo_aluno
    
    # Criar as entradas dos TPCs
    for idx, tpc in enumerate(aluno["tpc"]):
        tpc_id = f"TPC_{aluno_id}_{idx}"
        registo_tpc = f"""
        ###  http://rpcw.di.uminho.pt/2024/untitled-ontology-28#{tpc_id}
        :{tpc_id} rdf:type owl:NamedIndividual ,
                  :TPC ;
            :TPCtipo "{tpc['tp']}" ;
            :TPCNota {tpc['nota']} .
        :{aluno_id} :temTPC :{tpc_id} .
        """
        ttl += registo_tpc
    
    # Criar a entrada do projeto
    projeto_id = f"Projeto_{aluno_id}"
    registo_projeto = f"""
    ###  http://rpcw.di.uminho.pt/2024/untitled-ontology-28#{projeto_id}
    :{projeto_id} rdf:type owl:NamedIndividual ,
                  :Projeto ;
        :ProjetoNota {aluno['projeto']} .
    :{aluno_id} :temProjeto :{projeto_id} .
    """
    ttl += registo_projeto
    
    # Criar as entradas dos exames
    for tipo, nota in aluno["exames"].items():
        exame_id = f"Exame_{aluno_id}_{tipo}"
        registo_exame = f"""
        ###  http://rpcw.di.uminho.pt/2024/untitled-ontology-28#{exame_id}
        :{exame_id} rdf:type owl:NamedIndividual ,
                    :Exame ;
            :Exametipo "{tipo}" ;
            :Examenota {nota} .
        :{aluno_id} :temExame :{exame_id} .
        """
        ttl += registo_exame

# Escrever o TTL no arquivo de saída
with open('output.ttl', 'w') as output:
    output.write(ttl)