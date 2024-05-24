import json
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL

# Namespaces
ontology_ns = Namespace("http://rpcw.di.uminho.pt/2024/untitled-ontology-28/")
mapa_ns = Namespace("http://rpcw.di.uminho.pt/2024/mapa/")

# Criar o grafo
g = Graph()
g.bind("ont", ontology_ns)
g.bind("mapa", mapa_ns)

# Carregar os dados do arquivo JSON
with open("alunos.json") as f:
    data = json.load(f)

    for aluno in data["alunos"]:
        idAluno = aluno["idAluno"]
        nome = aluno["nome"]
        curso = aluno["curso"]
        projeto_nota = aluno["projeto"]

        # Adicionar aluno como indivíduo
        aluno_uri = URIRef(mapa_ns[idAluno])
        g.add((aluno_uri, RDF.type, OWL.NamedIndividual))
        g.add((aluno_uri, RDF.type, ontology_ns.Aluno))
        g.add((aluno_uri, ontology_ns.Id, Literal(idAluno)))
        g.add((aluno_uri, ontology_ns.Nome, Literal(nome)))
        g.add((aluno_uri, ontology_ns.cursos, Literal(curso)))

        # Adicionar projeto
        projeto_uri = URIRef(f"{aluno_uri}/projeto")
        g.add((projeto_uri, RDF.type, OWL.NamedIndividual))
        g.add((projeto_uri, RDF.type, ontology_ns.Projeto))
        g.add((projeto_uri, ontology_ns.ProjetoNota, Literal(projeto_nota)))
        g.add((aluno_uri, ontology_ns.temProjeto, projeto_uri))

        # Adicionar TPCs
        for tpc in aluno["tpc"]:
            tp = tpc["tp"]
            nota = tpc["nota"]
            tpc_uri = URIRef(f"{aluno_uri}/tpc{tp}")
            g.add((tpc_uri, RDF.type, OWL.NamedIndividual))
            g.add((tpc_uri, RDF.type, ontology_ns.TPC))
            g.add((tpc_uri, ontology_ns.TPCtipo, Literal(tp)))
            g.add((tpc_uri, ontology_ns.TPCNota, Literal(nota)))
            g.add((aluno_uri, ontology_ns.temTPC, tpc_uri))

        # Adicionar exames
        if "exames" in aluno:
            for tipo, nota in aluno["exames"].items():
                exame_uri = URIRef(f"{aluno_uri}/exame{tipo}")
                g.add((exame_uri, RDF.type, OWL.NamedIndividual))
                if tipo == "normal":
                    g.add((exame_uri, RDF.type, ontology_ns.EpocaNormal))
                elif tipo == "recurso":
                    g.add((exame_uri, RDF.type, ontology_ns.EpocaRecurso))
                elif tipo == "especial":
                    g.add((exame_uri, RDF.type, ontology_ns.EpocaEspecial))
                    
                g.add((exame_uri, ontology_ns.NotaExame, Literal(nota)))
                g.add((aluno_uri, ontology_ns.temExame, exame_uri))

# Serializar e salvar o grafo RDF no formato TTL
g.serialize(destination='alunosNew.ttl', format='turtle')

print("Arquivo TTL gerado com sucesso.")
