import json

file_1=open('jsons\ministerio1.json','r', encoding='utf-8')
json1=json.load(file_1)

file_2=open('jsons\ministerio2.json','r', encoding='utf-8')
json2=json.load(file_2)

file_3=open('jsons\ministerio3.json','r', encoding='utf-8')
json3=json.load(file_3)

# Inicializar o JSON combinado
json_combinado = {}

# Iterar sobre as chaves do primeiro JSON
for chave, valor in json1.items():
    if isinstance(valor, list):
        # Se o valor é uma lista, itera sobre cada valor
        for item in valor:
            categoria = item.get("categoria", "sem info")
            descricao = item.get("descricao", "sem info") 

            descricao_categoria = json2.get(categoria, "sem info")
            descritores_categoria = json3.get(categoria, ["sem info"])

            info_combinada = {
                "Categoria": {
                    "nome": categoria,
                    "descrição categoria": descricao_categoria,
                    "descritores categoria": descritores_categoria
                },
                "Descrição": descricao  
            }

            json_combinado[chave] = info_combinada
    else:
        categoria = valor.get("categoria", "sem info")
        descricao = valor.get("descricao", "sem info")  

        descricao_categoria = json2.get(categoria, "sem info")
        descritores_categoria = json3.get(categoria, ["sem info"])

        info_combinada = {
            "Categoria": {
                "nome": categoria,
                "descrição categoria": descricao_categoria,
                "descritores categoria": descritores_categoria
            },
            "Descrição": descricao  
        }

        json_combinado[chave] = info_combinada



# Imprimir o JSON combinado
file_out = open("jsons\ministerio_junto.json", "w", encoding='utf-8')
json.dump(json_combinado, file_out, indent=4, ensure_ascii=False)  # guardar
file_out.close()