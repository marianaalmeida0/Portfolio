
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
texto = re.sub(r'<outline>.*?</outline>', '', texto, flags=re.DOTALL) # re.DOTALL inclui \n no ponto (.)



texto = re.sub(r'^(.*?\b15\b.*?){3}', '', texto, flags=re.DOTALL)  # Remover todo o texto até ao terceiro 15 encontrado.

# Apenas existe um 107. Apagar tudo do 107 para a frente (ficar apenas com a primeira parte)
texto=re.sub(r'\b107\b.*','107',texto, flags=re.DOTALL)

# Dentro do texto, apagar paginacao e cabecalho  pag 15-107

texto=re.sub(r'<b>(?!ARC|AZT)[A-Z]{3}</b>',r'',texto) # ACI, VIU, etc.. #excluir ARC e AZT

texto=re.sub(r'\b[A-Z]\b',r'',texto)# carateres isolados sem significado (ex: A,B,C)

texto = re.sub(r'<b>.*?</b>\n<b>.*?</b>\n+[0-9]+' ,r'',texto)  #do primeiro <b> ate ao um numero  ( do n16 ao 107, por isso deixa-se o n 107)

texto = re.sub(r'\n\b([0-9]+)\b\n', r'', texto) # remove apenas a restante paginacao q nao esta incluida no padrao acima.

#Marca @ para resolver problema e destacar info
texto=re.sub(r'<b>',r'@',texto)
texto=re.sub(r'</b>',r'@',texto)

texto=re.sub(r'<i>(@.*?@)</i>',r'\1',texto,flags=re.DOTALL) # termos en ingles, remover italico


padrao= r"(@.*?)@\n*@(.*?@)"
while re.search(padrao, texto):
        texto = re.sub(padrao, r'\1\2',texto)

#cabecalhos q ficaram

texto=re.sub(r'@Adjuvante farmacêuticoAids pediátrica@',r'',texto)
texto=texto.replace('@Centrais FarmacêuticasCentro Nacional de Epidemiologia (Cenepi)@','') # nao funcionava com regex 
texto=re.sub(r'@Equivalência in vitroÉtica em pesquisa@',r'',texto)
texto=re.sub(r'@HemovigilânciaHepatite viral @',r'',texto)
texto=re.sub(r"(.*)\n(\s*Saúde)",r"\1\2",texto)
texto=re.sub(r"(.*)\n(\s*em Saúde)",r"\1\2",texto)


texto=re.sub(r'</i>\n(.*)\n',r'</i>\n\1\n£', texto) # Marca para descricao £
texto=re.sub(r'£(.*?)@',r'£\1#\n@', texto,flags=re.DOTALL) # Marca para descricao # no fim

padrao= r"(£.*?)\n*(.*?£)"
while re.search(padrao, texto):
        texto = re.sub(padrao, r'\1\2',texto)

texto=re.sub(r'@\n*(Ver.*)',r'@\n<i>Categoria:</i>\nVer descrição\n£\1\n#',texto)#Tratamento dos casos que diz VER

# casos particulares
texto=re.sub(r'£<i>','<i>',texto)




termos=re.findall(r'@(.*?)@.*?</i>(.*?)\£(.*?)#',texto,flags=re.DOTALL)
print(len(termos))

dic = {}

for t1, t2, t3 in termos:
    chave = t1.strip().replace('\n', '')
    categoria = t2.strip().replace('\n', '')
    descricao = t3.strip().replace('\n', '')

    # Verifica se a chave existe no dic
    if chave in dic:
        #Se a chave existe, insere na lista de dics
        if not isinstance(dic[chave], list):
            # se nao é ainda lista, converte em lista
            dic[chave] = [dic[chave]]
        dic[chave].append({"categoria": categoria, "descricao": descricao})
    else:
        # Se a chave nao existe, cria nova entrada sem lista
        dic[chave] = {"categoria": categoria, "descricao": descricao}



fo=open(r"testes\ministerio1.xml","w", encoding='utf-8')
fo.write(texto)
fo.close()

file_out=open("jsons\ministerio1.json","w",encoding='utf-8')
json.dump(dic,file_out,indent=4,ensure_ascii=False) #guardar
file_out.close()

