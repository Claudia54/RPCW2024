import json

f= open("plantas.json")
bd=json.load(f)
f.close()


ttl=""

for planta in bd:
   registo = f"""
    <http://rpcw.di.uminho.pt/2024/plantas#{planta["Id"]} rdf:type owl:NamedIndividual ,
                        :Planta ;
                :temLocalizacao :r_{planta["Código de rua"]} ;
                :id "{planta["Id"]}"^^xsd:int ;
                :num_registo "{planta["Número de Registo"]}"^^xsd:int ;
                :especie "{planta["Espécie"]}" ;
                :nome_cient "{planta["Nome Científico"]}" ;
                :origem "{planta["Origem"]}" ;
                :data_planta "{planta["Data de Plantação"]}" ;
                :estado "{planta["Estado"]}" ;
                :caldeira "{planta["Caldeira"]}" ;
                :tutor "{planta["Tutor"]}" ;
                :implantacao "{planta["Implantação"]}" ;
                :gestor "{planta["Gestor"]}" ;
                :num_inter "{planta["Número de intervenções"]}"^^xsd:int";
                :data_atual "{planta["Data de actualização"]}" .
                

<http://rpcw.di.uminho.pt/2024/plantas#:r_{planta["Código de rua"]} rdf:type owl:NamedIndividual ;
            :cod_rua "{planta["Código de rua"]}"^^xsd:int ;
            :freguesia "{planta["Freguesia"]}" ;
            :local "{planta["Local"]}" ;
            :rua "{planta["Rua"]}".
    """                                        
   ttl += registo

print(ttl)