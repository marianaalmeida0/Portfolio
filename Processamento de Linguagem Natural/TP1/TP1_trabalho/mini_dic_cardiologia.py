import re
import json

f=open(r"data\08. MinidicionÃ¡rio de Cardiologista Autor Ricardo Silveira Mello.xml", "r",encoding='utf-8')

texto=f.read()




###########################################################
######################MARCAS###############################
###########################################################

#DESIGNCACAO EM INGLES-> font="7"-> £
#TRADUCAO EM PT->font="8"->&
#DESIGNACAO EM PROTUGUES->font="13"€
#TRADUCAO EM INGLES_> font="8"->&


texto = re.sub(r"\n{2,}", " ", texto)
texto = re.sub(r'<.+font=\"7\"><b>(.+?)</b.+', r"£\1\n", texto)  # DESIGNACAO EM INGLES
texto = re.sub(r'<.+font=\"13\"><b>(.+?)</b.+', r'€\1\n', texto)  # DESIGNACAO EM PORTUGUES

texto = re.sub(r".+font=\"8\">(.+)<.+", r"&\1\n", texto)  # TRADUCOES
texto = re.sub(r"<.+>", "", texto) # apaga tudo o resto 


texto = re.sub(r'^\s*', '', texto)# retirar espacos no inicio
texto = texto.lstrip('\n')# eliminacao de quebras de linha iniciais vazios
texto=re.sub(r'\s*\n+',r'\n',texto) # apagar espacos antes de quebras de linha
texto=re.sub(r'&\n',r'',texto) # linha com traducao em branco

# Loop para tratar casos com frases com mais de uma linha
marcas = ["£", "€", "&"]

for m in marcas:
    padrao= rf"{m}(.+?)[\n]+?{m}(.+?)"
    while re.search(padrao, texto):
        texto = re.sub(padrao, rf"{m}\1 \2", texto)

texto=re.sub(r'\–',r'',texto)# remocao dos '-'



en = re.findall(r'£(.+?)\n&(.+)', texto) # lista com designacoes em ingles e traducao pt
novos_en = [(e[0].strip().replace("\n",""), e[1].strip().replace("\n","")) for e in en]


pt=re.findall(r'€(.+?)\n&(.+)', texto) # lista com designacoes em pt e traducao em ingles
novos_pt = [(p[0].strip().replace("\n",""), p[1].strip().replace("\n","")) for p in pt]

print(len(novos_en)+len(novos_pt))

dic = {
    "en:pt": dict(en),
    "pt:en": dict(pt)
}

      
file_out=open("jsons\card.json","w",encoding='utf-8')
json.dump(dic,file_out,indent=4,ensure_ascii=False) #guardar
file_out.close()

fo=open("testes/mini_dic_card.xml","w", encoding='utf-8')
fo.write(texto)
fo.close()