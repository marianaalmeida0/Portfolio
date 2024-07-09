import re
import json
f=open(r"data\glossario_ministerio_saude.xml", "r",encoding='utf-8')

texto=f.read()

#Limpeza
texto=re.sub(r'<\??xml.*>',r'',texto)
texto = re.sub(r'</?page.*>',r'', texto)
texto = re.sub(r'</?text.*?>', r'', texto)
texto = re.sub(r'<fontspec.*/>', r'', texto) # limpar todas
texto = re.sub(r'<image.*/>', r'', texto)
texto=re.sub(r'<!DOCTYPE.*?>',r'',texto)
texto=re.sub(r'<pdf2xml.*?>',r'',texto)
texto = re.sub(r'<outline>.*?</outline>', r'', texto, flags=re.DOTALL) # re.DOTALL inclui \n no ponto (.)

texto = re.sub(r'^(.*?\b107\b.*?){2}', r'', texto, flags=re.DOTALL)  # Remover todo o texto até ao segundo 107 encontrado.
texto=re.sub(r'\b113\b.*','113',texto, flags=re.DOTALL) # remove apos a pag 113
texto = re.sub(r'\n\b([0-9]+)\b\n', r'', texto) # remove paginacao

texto=re.sub(r'(.*?)(<b>Acidentes e Violência</b>)',r'\2',texto, flags=re.DOTALL) # remove todo o texto ate Acidentes e Violência

#Cabecalho caso-pontual

texto=re.sub(r'<b>.*?</b>\n<b>.*?</b>',r'',texto) # juntar 

texto=re.sub(r'<b>',r'\n@',texto) # marca delimitadora
texto=re.sub(r'</b>',r'§',texto) # marca delimitadora
texto=re.sub(r'(.*?)113',r'@',texto) # para apanhar a ultima designacao e apagar o 113

#afinacao
texto = re.sub(r'@Demograﬁ a§', r'@Demograﬁa§', texto)
texto=re.sub(r'<i>|</i>',r'',texto)


# Findall
termos = re.findall(r'@(.*?)§', texto) # lista de categorias
termos2 = re.findall(r'§(.*?)@', texto,flags=re.DOTALL) # lista de descricao das categorias
'''

dic = {}
for i in range(len(termos)):
    chave = termos[i].strip().replace("\n",'')
    valor = termos2[i].strip().replace("\n",'')
    dic[chave] = valor
'''
dic = {termos[i].strip().replace("\n", ''): termos2[i].strip().replace("\n", '') for i in range(len(termos))}

print(len(termos))
fo=open(r"testes\ministerio2.xml","w", encoding='utf-8')
fo.write(texto)
fo.close()

file_out=open("jsons\ministerio2.json","w",encoding='utf-8')
json.dump(dic,file_out,indent=4,ensure_ascii=False) #guardar
file_out.close()
