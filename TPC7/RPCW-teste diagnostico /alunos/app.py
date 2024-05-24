from flask import Flask, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)

# Configuração do endpoint SPARQL
SPARQL_ENDPOINT = "http://localhost:7200/repositories/novorep"

def sparql_get_query(query):
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setMethod('GET')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

@app.get('/alunos')
def get_alunos():
    if request.args.get('groupBy') == 'curso':
        return get_alunos_grouped_by_curso()
    
    elif request.args.get('groupBy') == 'projeto':
        return get_Projeto()
    
    elif request.args.get('groupBy') == 'recurso':
        return alunosRecurso()
    
    elif 'curso' in request.args:
        return get_curso(request.args.get('curso'))
    query = """
    PREFIX :  <http://rpcw.di.uminho.pt/2024/untitled-ontology-28/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?idAluno ?nome ?curso
    WHERE {
      ?aluno a :Aluno ;
              :Id ?idAluno ;
              :Nome ?nome ;
              :cursos ?curso .
    }
    ORDER BY ?nome
    """
    result = sparql_get_query(query)
    alunos = []
    for linha in result['results']['bindings']:
        aluno = {
            "idAluno": linha['idAluno']['value'],
            "nome": linha['nome']['value'],
            "curso": linha['curso']['value']
        }
        alunos.append(aluno)
    return jsonify(alunos), 200


@app.get('/alunos/<id>')
def get_aluno(id):
    query = f"""

PREFIX :  <http://rpcw.di.uminho.pt/2024/untitled-ontology-28/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

PREFIX ont: <http://rpcw.di.uminho.pt/2024/untitled-ontology-28/>
SELECT ?Nome ?cursos ?notaNormal ?notaEspecial ?notaRecurso ?notaProjeto ?TPCTipo ?notaTPC
WHERE {{
  ?aluno a ont:Aluno ;
         ont:Id "{id}" ;  # Substitua "A29920" pelo idAluno desejado
         ont:Nome ?Nome ;
         ont:cursos ?cursos .
  
  OPTIONAL {{
    ?exameNormal a ont:EpocaNormal ;
                 ont:NotaExame ?notaNormal .
    ?aluno ont:temExame ?exameNormal .
  }}
  
  OPTIONAL {{
    ?exameEspecial a ont:EpocaEspecial ;
                   ont:NotaExame ?notaEspecial .
    ?aluno ont:temExame ?exameEspecial .
  }}
  
  OPTIONAL {{
    ?exameRecurso a ont:EpocaRecurso ;
                  ont:NotaExame ?notaRecurso .
    ?aluno ont:temExame ?exameRecurso .
  }}
  
  OPTIONAL {{
    ?projeto a ont:Projeto ;
             ont:ProjetoNota ?notaProjeto .
    ?aluno ont:temProjeto ?projeto .
  }}
  
  ?tpc a ont:TPC ;
       ont:TPCtipo ?TPCTipo ;
       ont:TPCNota ?notaTPC .
  ?aluno ont:temTPC ?tpc .
}}

    """
    result = sparql_get_query(query)
    if not result['results']['bindings']:
        return jsonify({"erro": "Aluno inexistente"}), 404

    aluno_data = result['results']['bindings'][0]
    aluno_info = {
        "idAluno": id,
        "nome": aluno_data['Nome']['value'],
        "curso": aluno_data['cursos']['value']
    }
    
    if 'notaProjeto' in aluno_data:
        aluno_info["notaProjeto"] = aluno_data['notaProjeto']['value']
    
    tpcs = []
    for entry in result['results']['bindings']:
        if 'TPCTipo' in entry and 'notaTPC' in entry:
            tpcs.append({
                "tipo": entry['TPCTipo']['value'],
                "nota": entry['notaTPC']['value']
            })
    aluno_info["tpcs"] = tpcs

    exames = {}
    if 'notaNormal' in aluno_data:
        exames["EpocaNormal"] = aluno_data['notaNormal']['value']
    if 'notaEspecial' in aluno_data:
        exames["EpocaEspecial"] = aluno_data['notaEspecial']['value']
    if 'notaRecurso' in aluno_data:
        exames["EpocaRecurso"] = aluno_data['notaRecurso']['value']
    aluno_info["exames"] = exames

    return jsonify(aluno_info), 200



def get_curso(curso):
    query = f"""
PREFIX :  <http://rpcw.di.uminho.pt/2024/untitled-ontology-28/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX ont: <http://rpcw.di.uminho.pt/2024/untitled-ontology-28/>
    SELECT ?idAluno ?nome ?curso
    WHERE {{
      ?aluno a :Aluno ;
             :Id ?idAluno ;
             :Nome ?nome ;
             :cursos ?curso .
      FILTER (?curso = "{curso}")
    }}
    ORDER BY ?nome
    """
    result = sparql_get_query(query)
    alunos = []
    for linha in result['results']['bindings']:
        aluno = {
            "idAluno": linha['idAluno']['value'],
            "nome": linha['nome']['value'],
            "curso": linha['curso']['value']
        }
        alunos.append(aluno)
    return jsonify(alunos), 200




@app.get('/alunos/tpc')
def get_alunos_tpc():
    query = """
    PREFIX ont: <http://rpcw.di.uminho.pt/2024/untitled-ontology-28/>
    SELECT ?idAluno ?nome ?curso (COUNT(?tpc) AS ?numTPCs)
    WHERE {
      ?aluno a ont:Aluno ;
             ont:Id ?idAluno ;
             ont:Nome ?nome ;
             ont:cursos ?curso .
      OPTIONAL { ?aluno ont:temTPC ?tpc }
    }
    GROUP BY ?idAluno ?nome ?curso
    ORDER BY ?nome
    """
    result = sparql_get_query(query)
    alunos = []
    for linha in result['results']['bindings']:
        aluno = {
            "idAluno": linha['idAluno']['value'],
            "nome": linha['nome']['value'],
            "curso": linha['curso']['value'],
            "numTPCs": linha['numTPCs']['value']
        }
        alunos.append(aluno)
    return jsonify(alunos), 200


def get_alunos_grouped_by_curso():
        query = """
        PREFIX ont: <http://rpcw.di.uminho.pt/2024/untitled-ontology-28/>
        SELECT ?curso (COUNT(?aluno) AS ?numAlunos)
        WHERE {
          ?aluno a ont:Aluno ;
                 ont:cursos ?curso .
        }
        GROUP BY ?curso
        ORDER BY ?curso
        """
        result = sparql_get_query(query)
        cursos = []
        for linha in result['results']['bindings']:
            curso = {
                "curso": linha['curso']['value'],
                "numAlunos": linha['numAlunos']['value']
            }
            cursos.append(curso)
        return jsonify(cursos), 200
    

def get_Projeto():
        query = """
        PREFIX ont: <http://rpcw.di.uminho.pt/2024/untitled-ontology-28/>
        SELECT ?notaProjeto (COUNT(?aluno) AS ?totalAlunos)
        WHERE {
          ?aluno a ont:Aluno ;
                 ont:temProjeto ?projeto .
          ?projeto ont:ProjetoNota ?notaProjeto .
        }
        GROUP BY ?notaProjeto
        ORDER BY ?notaProjeto
        """
        result = sparql_get_query(query)
        projetos = []
        for linha in result['results']['bindings']:
            projeto = {
                "notaProjeto": linha['notaProjeto']['value'],
                "totalAlunos": linha['totalAlunos']['value']
            }
            projetos.append(projeto)
        return jsonify(projetos), 200

def alunosRecurso():
        query = """
        PREFIX :  <http://rpcw.di.uminho.pt/2024/untitled-ontology-28/>
    SELECT ?idAluno ?nome ?curso ?nota
    WHERE {
        ?aluno a :Aluno ;
         :temExame ?recursoExame ;
         :Nome ?nome ;
         :cursos ?curso ;
         :Id ?idAluno .
    ?recursoExame a :EpocaRecurso;
       :NotaExame ?nota
    
}
ORDER BY ?nome
        """
        result = sparql_get_query(query)
        alunos = []
        for linha in result['results']['bindings']:
            aluno = {
                "idAluno": linha['idAluno']['value'],
                "nome": linha['nome']['value'],
                "curso": linha['curso']['value'],
                "recurso": linha['nota']['value']
            }
            alunos.append(aluno)
        return jsonify(alunos), 200
    


@app.get('/alunos/avaliados')
def get_alunos_avaliados():
    query = """
    PREFIX ont: <http://rpcw.di.uminho.pt/2024/untitled-ontology-28/>
    SELECT ?idAluno ?nome ?curso ?notaProjeto ?notaExame ?notaTPC
    WHERE {
      ?aluno a ont:Aluno ;
             ont:Id ?idAluno ;
             ont:Nome ?nome ;
             ont:cursos ?curso ;
             ont:temProjeto ?projeto .
      ?projeto ont:ProjetoNota ?notaProjeto .
      
      OPTIONAL {
        ?aluno ont:temExame ?exame .
        ?exame ont:NotaExame ?notaExame .
      }
      
      OPTIONAL {
        ?aluno ont:temTPC ?tpc .
        ?tpc ont:TPCNota ?notaTPC .
      }
    }
    ORDER BY ?nome
    """
    
    result = sparql_get_query(query)
    alunos_dict = {}

    for linha in result['results']['bindings']:
        idAluno = linha['idAluno']['value']
        nome = linha['nome']['value']
        curso = linha['curso']['value']
        notaProjeto = float(linha['notaProjeto']['value'])
        notaExame = float(linha.get('notaExame', {'value': 0})['value'])
        notaTPC = float(linha.get('notaTPC', {'value': 0})['value'])
        
        if idAluno not in alunos_dict:
            alunos_dict[idAluno] = {
                "idAluno": idAluno,
                "nome": nome,
                "curso": curso,
                "notaProjeto": notaProjeto,
                "notasExame": [],
                "totalTPC": 0
            }
        
        alunos_dict[idAluno]["notasExame"].append(notaExame)
        alunos_dict[idAluno]["totalTPC"] += notaTPC

    alunos_avaliados = []

    for aluno in alunos_dict.values():
        notaFinal = "R"
        if aluno["notaProjeto"] >= 10:
            maxNotaExame = max(aluno["notasExame"], default=0)
            if maxNotaExame >= 10:
                notaFinalCalc = aluno["totalTPC"] + 0.4 * aluno["notaProjeto"] + 0.4 * maxNotaExame
                if notaFinalCalc >= 10:
                    notaFinal = round(notaFinalCalc, 2)

        alunos_avaliados.append({
            "idAluno": aluno["idAluno"],
            "nome": aluno["nome"],
            "curso": aluno["curso"],
            "notaFinal": notaFinal
        })


    return jsonify(alunos_avaliados), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Use uma porta diferente se 5000 estiver em uso



