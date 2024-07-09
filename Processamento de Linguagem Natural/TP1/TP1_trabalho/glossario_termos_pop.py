import re
import json

filename = r"data\glossario_termos_pop.txt"
with open(filename, 'r', encoding='utf-8') as f:
    texto = f.readlines() # Ler ficheiro linha a linha

texto_tratado = []
linha_temp = ''  # Variável para armazenar temporariamente linhas concatenadas

for linha in texto:
    linha = re.sub(r"\n", "", linha)  # Remover caracteres \n (quebra de linha) da linha
    linha = re.sub(r"\f", "", linha)  # Remover caracteres \f (quebra de página) da linha
    if "(pop)" in linha and " , " in linha:  # Se reconhecer o padrão de uma designação + descrição de completa
        if linha_temp:  # Se houver linhas concatenadas pendentes, adicioná-las primeiro
            texto_tratado.append(linha_temp)
            linha_temp=''

        else: 
            texto_tratado.append(linha)
        
    else:
        linha_temp += linha  # Concatenar linhas que não atendem às condições

# Adicionar a última linha concatenada, se houver
if linha_temp:
    texto_tratado.append(linha_temp)

dici={} 

for item in texto_tratado:
    item=item.split(r" , ")
    if len(item)==2:
        desc=re.search("\(pop\)", item[0])
        if desc:
            dici[item[1]]=item[0] # Caso a descrição (onde se encontra o pop) esteja em primeiro, o elemento seguinte é a designação
        else:
            dici[item[0]]=item[1] # Caso contrário a designação é o primeiro elemento e a descrição o segundo

dici = dict(sorted(dici.items())) # Ordenar por ordem alfabética o dicionário
#print(dici)
file_out=open("jsons\glossario_de_termos_medicos.json","w",encoding='utf-8')
json.dump(dici,file_out,indent=4,ensure_ascii=False) #guardar
file_out.close()