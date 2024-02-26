import json

f = open('musica.json', 'r')
data = json.load(f)
f.close()



alunos = data['alunos']
cursos = data['cursos']
instrumentos = data['instrumentos']

ttl =""

    
for aluno in alunos : 
    print(aluno)
    registo = f"""
###  http://rpcw.di.uminho.pt/2024/musica#{aluno['id']}
:{aluno['id']} rdf:type owl:NamedIndividual ,
    :Aluno ;
    :temCurso :{aluno['curso']} ;
    :temInstrumento :{aluno['instrumento']} ;
    :idAluno "{aluno['id']}" ;
    :nomeAluno "{aluno['nome']}" ;
    :dataNasc "{aluno['dataNasc']}" ;
    :anoCurso "{aluno['anoCurso']}".           
    """
    ttl += registo 

for curso in cursos: 
    registo = f"""
###  http://rpcw.di.uminho.pt/2024/musica#{curso['id']}
:{curso['id']} rdf:type owl:NamedIndividual ,
    :Curso ;
    :CursotemInst :{curso['instrumento']['id']};
    :duracao "{curso['duracao']}" ;
    :idCurso "{curso['id']}";
    :designacao "{curso['designacao']}" .
    """
    ttl += registo 

for instrumento in instrumentos:
    registo = f"""
###  http://rpcw.di.uminho.pt/2024/musica#{instrumento['id']}
:{instrumento['id']} rdf:type owl:NamedIndividual ,
    :Instrumento ;
    :idIntrumento "{instrumento['id']}" ;
    :nomeInst "{instrumento['#text']}" .
    """
    ttl += registo

output = open("musicaElem.ttl", "w")
output.write(ttl)