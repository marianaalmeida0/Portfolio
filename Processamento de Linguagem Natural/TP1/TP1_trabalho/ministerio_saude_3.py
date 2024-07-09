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
texto=re.sub(r'.*pesas de capital para o exercício ﬁ nanceiro.\n','',texto,flags=re.DOTALL) # remove tudo antes da expressao, inclusive
texto=re.sub(r'125\n<b>Categoria de Administração e </b>.*','',texto, flags=re.DOTALL) # remove tudo após

texto=re.sub(r"[0-9]+\n",r'',texto) # remover paginacao
texto=re.sub(r'<i>|</i>',r'',texto)
texto=re.sub(r'<b>Descritores organizados </b>\n<b>por categorias</b>',r'',texto)
texto = re.sub(r"\n+", r"\n", texto) #uniformizar espacos

termos=re.findall(r'<b>(.*?)</b>\n(.*?)(?=\n<b>|$)',texto,flags=re.DOTALL) # lista de tuplos das categorias e dos descritores

dic = {chave.strip(): valor.strip().split('\n') for chave, valor in termos} # dicionario cujos valor é uma lista

fo=open(r"testes\ministerio3.xml","w", encoding='utf-8')
fo.write(texto)
fo.close()

file_out=open("jsons\ministerio3.json","w",encoding='utf-8')
json.dump(dic,file_out,indent=4,ensure_ascii=False) #guardar
file_out.close()
