import re
import json

#####################################################
### Leitura do Ficheiro
#####################################################

f=open(r"data\ossos.xml","r",encoding='utf-8')
texto=f.read()

#####################################################
### Limpeza
#####################################################

texto=re.sub(r'<\??xml.*>',r'',texto)
texto = re.sub(r'</?page.*>',r'', texto)
texto = re.sub(r'</?text.*?>', r'', texto)
texto = re.sub(r'<fontspec.*/>', r'', texto) 
texto = re.sub(r'<image.*/>', r'', texto)
texto=re.sub(r'<!DOCTYPE.*?>',r'',texto)
texto=re.sub(r'<pdf2xml.*?>',r'',texto)

#####################################################
### Recolha dos textos Introdutórios
#####################################################

textoIntros=re.sub(r'^<b>GABARITO</b>.*',r'',texto, flags=re.DOTALL) # Eliminar texto à frente das imagens
textoIntros=re.findall(r'Introdução</b>(.*?)<b>', textoIntros, flags=re.DOTALL) # Recolha das introduções - Criação de uma lista utilizada posteriormente 



#####################################################
### Recolha do texto importante - Legendas
#####################################################


texto=re.sub(r'^.*<b>GABARITO</b>',r'',texto, flags=re.DOTALL) # Remover tudo até GABARITO inclusive
# Mais limpeza
texto = re.sub(r'<a.*?</a>', '', texto)# Retirar ancoras 
texto = re.sub(r'<b>\b[a-zA-ZÀ-ÖØ-öø-ÿ]{1,6}\b</b>', '', texto) # Retirar cabecalhos
texto=re.sub(r'\s*<b>\:*\s*\w*</b>','',texto) # Retirar cabecalhos que se tinham mantiveram
texto = re.sub(r'm\) Músculo Ilíaco.+', 'm) Músculo Ilíaco', texto, flags=re.DOTALL) # Remover a Bibliografia


#####################################################
### Tratamento de Casos Particulares
#####################################################



texto = re.sub(r'([0-9].)\s\n<b>', r'\n<b>\1', texto) # Colocar numeracao a negrito
texto = re.sub(r'([0-9].[0-9]*)\s\n<b>', r'<b>\1', texto) # Colocar numeracao a negrito (resolve 2.9;3; 3.1; 3.2)
texto=re.sub(r'(c\) Osso )<b>fíbula</b>',r'\1fíbula',texto) # Retirar de negrito a fíbula
texto=re.sub(r'n\) Dente \n<b>371.30 MANDÍBULA: VISTA CRANIAL </b>', r'n) Dente 37\n<b>1.30 MANDÍBULA: VISTA CRANIAL </b>', texto, flags=re.DOTALL)

texto = re.sub(r'(^[0-9]+\.[0-9]+\..*\n[A-Z]+)', r'<b>\1</b>', texto, flags=re.MULTILINE)  # Titulo passa para baixo 
texto=re.sub(r'(^[0-9]\.[0-9]\..*)',r'<b>\1</b>',texto,flags=re.MULTILINE)  # Titulo esta numa so linha (resolvem o resto)
texto = re.sub(r"\n+", r"\n", texto)  # Uniformizacao de espacos


#####################################################
### Marcações
#####################################################                                                                                              

# Marcação dos títulos 1. 2. 3. com @@@@@@@@@@@
texto=re.sub(r'</b>\n<b>([0-9])',r'</b>\n@@@@@@@@@@@@@@\n<b>\1',texto) # P ex: 1. Cranio @@@@@@@@@@@ 1.1 Cranio Vista...

# Marcação dos subtítulos com # no início e § no final
texto=re.sub(r'(<b>[0-9]*\.\s*[0-9]+.*?</b>)\s*\na\)',r'#\1§\na)',texto, flags=re.DOTALL) # P ex: #<b>1.1. CRÂNIO: VISTA ANTERIOR - I </b>§

### Tratamento de casos particulares
### Tentativa: (^#<b>.*?</b>)\s*\n@@@@@@@@@@@@@@\n(<b>.*?</b>§) para não ter de ser usado os casos particulares, mas nao deu
texto=re.sub(r'(#<b>1.25 E 1.26 NÃO POSSUEM GABARITO</b>)\n@@@@@@@@@@@@@@\n(<b>1.27 MANDÍBULA: VISTA ANTERIOR </b>§)', r'\1§\na)\n#\2', texto, flags=re.DOTALL)
texto=re.sub(r'(#<b>4.4 VÉRTEBRAS CERVICAIS ATÍPICAS: ÁXIS \(C2\)</b>)\n@@@@@@@@@@@@@@\n(<b>4.4.1 VISTA PÓSTERO-SUPERIOR</b>§)', r'\1§\na)\n#\2', texto, flags=re.DOTALL)
texto=re.sub(r'(#<b>4.5 VÉRTEBRAS CERVICAIS TÍPICAS: DE C3 A C6 </b>)\n@@@@@@@@@@@@@@\n(<b>4.5.1 VISTA SUPERIOR DE C3</b>§)', r'\1§\na)\n#\2', texto, flags=re.DOTALL)
texto=re.sub(r'(#<b>4.6 VÉRTEBRAS CERVICAIS ATÍPICAS: VÉRTEBRA PROEMINENTE )</b>\n<b>(\(C7\)</b>)\n@@@@@@@@@@@@@@\n(<b>4.6.1 VISTA SUPERIOR</b>)', r'\1\2§\na)\n#\3', texto, flags=re.DOTALL)

# Marcação dos sub-subtitulos  p ex: 4.4.1
texto=re.sub(r'#?(<b>[0-9]\.[0-9]\.[0-9].*?</b>)§?', r'&\1£', texto) # P ex: &<b>4.4.1 VISTA PÓSTERO-SUPERIOR</b>£

#####################################################
### Marcação/Separação das duas Secções
#####################################################

# Marcação com £ no início e final dos títulos principais
texto=re.sub(r'(<b>SISTEMA MUSCULAR</b>)\n@@@@@@@@@@@@@@',r'££££££££££\1££££££££££',texto)
texto=re.sub(r'(<b>SISTEMA ESQUELÉTICO E ARTICULAR</b>)\n@@@@@@@@@@@@@@',r'££££££££££\1££££££££££',texto)

# Separação em dois textos principais
padroes=re.findall(r'££££££££££<b>(.+?)££££££££££<b>(.+)', texto, flags=re.DOTALL)
texto_1=padroes[0][0]
texto_2=padroes[0][1]

### Mais Tratamento 
texto_1=re.sub(r"<b>(.*)</b>\n<b>(.*)</b>", r"<b>\1\2</b>", texto_1) #Colocar os títulos numa linha só
texto_2=re.sub(r"<b>(.*)</b>\n<b>(.*)</b>", r"<b>\1\2</b>", texto_2) #Colocar os títulos numa linha só
texto_2=re.sub(r"<b>(.*)\n(.*)</b>", r"<b>\1\2</b>", texto_2) #Colocar os títulos numa linha só


#####################################################
### Estrutura de Dados 
#####################################################

#Existe o SISTEMA ESQUETICO E ARTICULAR e o SISTEMA MUSCULAR
# Dic= {"SISTEMA ESQUELETICO E ARTICULAR" : {"CRANIO" : {"Cranio lateral" : {"a":....., "b":} , "Introdução" : "...."}}, 
#                                            "COLUNAVERTEBRAL" :{"Vertebras Cervicais" : {"a":..., "b":....}, 
#                                                               "VertebrasAtipicas" : { "VistaAnterior" : {"a":..., "b":...}},
#                                                                "Introdução" : "....."}
#                                           },
#       "SISTEMA MUSCULAR" : {...}
#      }
# 

dic={}


#########################################################################################
######################## SECCÃO 1: SISTEMA ESQUELÉTICO E ARTICULAR ######################
#########################################################################################


seccao1=re.findall(r"^(.+?)</b>£{10}", texto_1, flags=re.DOTALL) # Recolha do título SISTEMA ESQUELÉTICO E ARTICULAR
dic[seccao1[0]]=""

titulos=re.findall(r"<b>(.*)?</b>\s*\n@@@@@@@@@@@@@@", texto_1) # Recolha dos títulos (Crânio, Membro Superior, ...)


dic[str(seccao1[0])] = dict.fromkeys(titulos) # Criação das chaves no dicionário para cada título desta secção

# Retirar o texto entre os títulos 1. Cranio  - 2. Membro Superior (É necessário fora do ciclo ir buscar o último texto desde 4. Torso para a frente)
for j in range (len(titulos)-1): 

    exp=fr"<b>{titulos[j]}</b>\n@@@@@@@@@@@@@@(.*)\s*<b>{titulos[j+1]}" # Expressão de Procura entre títulos
    textoaux=re.findall(exp, texto_1, flags=re.DOTALL)
    textoaux[0]=str(textoaux[0])+"#" # Acrescenta-se para o texto à frente do último subtítulo também poder ser encontrado com a mesma expressão

    subtitulos=re.findall(r"#<b>(.*)</b>?§", textoaux[0]) # Recolha dos subtítulos: (NÃO SE PODE USAR O DOTALL)

    dic[str(seccao1[0])][titulos[j]]=dict.fromkeys(subtitulos) # Criação das chaves a dos subtítulos
    dic[str(seccao1[0])][titulos[j]]["Introdução: "]=textoIntros[j].replace("\n", "").replace("\t", "") # Criação do par "Introdução"-> Texto Introdução

    # Retirar o texto entre os subtítulos 1.1 e 1.2 p.ex
    for i in range (len(subtitulos)-1):
        exp=fr"#<b>{subtitulos[i]}</b>§\n(.*)\n?#<b>{subtitulos[i+1]}" # Expressão de Procura entre subtítulos 
        textoaux2=re.findall(exp, textoaux[0], flags=re.DOTALL)

        textoaux2[0]=str(textoaux2[0])+"\n" # Acrescenta-se para o texto do último par ( a), ...; b), ...) poder ser dividido com a mesma expressão
        textoaux3=re.findall(r'(\w)\)(.+)?\n', textoaux2[0])
        
        dicvista = {t[0]: t[1] for t in textoaux3} # Dicionário Auxiliar: {"a": ...., "b": ...., ....}
        dic[str(seccao1[0])][titulos[j]][subtitulos[i]]=dicvista
    
    # Tratamento do último subtítulo p.ex 1.32 (não dá para tratar dentro do for por causa de list index out of range- dava se fizessemos um if e no último índice do ciclo (penúltimo da lista)  tratassemos o último subtítulo)
    
    exp=fr"#<b>{subtitulos[len(subtitulos)-1]}</b>§\n(.*)" # Expressão de Procura do último subtítulo
    textoaux2=re.findall(exp, textoaux[0], flags=re.DOTALL)
    textoaux2[0]=str(textoaux2[0])+"\n"
    textoaux3=re.findall(r'(\w)\)(.+)?\n', textoaux2[0])    
    dicvista = {t[0]: t[1] for t in textoaux3}
    dic[str(seccao1[0])][titulos[j]][subtitulos[len(subtitulos)-1]]=dicvista



# Retirar o texto do ultimo titulo - título 4. Torso
expfinal=f"<b>{titulos[len(titulos)-1]}</b>\n@@@@@@@@@@@@@@(.*)"

# Tratamento de títulos para uma linha só
textoauxfinal=re.findall(expfinal, texto_1, flags=re.DOTALL)
subtitulos=re.findall(r"#<b>(.*)</b>?§", textoauxfinal[0])
dic[str(seccao1[0])][titulos[len(titulos)-1]]=dict.fromkeys(subtitulos)
dic[str(seccao1[0])][titulos[j+1]]["Introdução: "]=textoIntros[j+1].replace("\n", "").replace("\t", "")


### Ler os textos ente subtitulos p ex entre 4.1 4.2:
for i in range (len(subtitulos)-1):
        expp = f"{re.escape(subtitulos[i])}(.*?){re.escape(subtitulos[i+1])}|$"

        # Encontrar o texto entre os subtítulos
        textoaux22 = re.findall(expp, textoauxfinal[0], flags=re.DOTALL)
        
        # Teste se há sub-subtítulos
        testesubsub=re.findall(r"&<b>(.*)</b>£", textoaux22[0])
        
        if not testesubsub: # Se não, tratar como um subtítulo normal e retirar os pares ( a), ...; b), ...)
            textoaux22[0]=str(textoaux22[0])+"\n"
            textoaux3=re.findall(r'(\w)\)(.+)?\n', textoaux22[0])
            dicvista = {t[0]: t[1] for t in textoaux3}
            dic[str(seccao1[0])][titulos[len(titulos)-1]][subtitulos[i]]=dicvista
        else: # Se sim, retirar os seus sub-subtítulos e posteriormente os pares ( a), ...; b), ...)
             dic3 = {}
             textoaux22=str(textoaux22[0])+"\n"+"&"
             print("uuu",textoaux22)
             textos=re.findall(r'£(.*?)&',textoaux22,flags=re.DOTALL) 
             for subtexto in textos:
                ind=textos.index(subtexto)        
                textoaux3=re.findall(r'(\w)\)(.+)?\n', textos[ind])
                dicvista = {t[0]: t[1] for t in textoaux3}
                dic3[testesubsub[ind]]=dicvista
             dic[str(seccao1[0])][titulos[len(titulos)-1]][subtitulos[i]]=dic3
             

             
### Tratamento do último subtítulo 4. 26

exp=f"#<b>{subtitulos[len(subtitulos)-1]}</b>§\n(.*)" 
textoaux2=re.findall(exp, textoauxfinal[0], flags=re.DOTALL)
textoaux2[0]=str(textoaux2[0])+"\n"
textoaux3=re.findall(r'(\w)\)(.+)?\n', textoaux2[0])    
dicvista = {t[0]: t[1] for t in textoaux3}
dic[str(seccao1[0])][titulos[len(titulos)-1]][subtitulos[len(subtitulos)-1]]=dicvista



# A secção 2 segue o mesmo raciocínio explicado mais detalhadamente acima

#########################################################################################
######################## SECCÃO 2: SISTEMA MUSCULAR #####################################
#########################################################################################

seccao2=re.findall(r"^(.+?)</b>£{10}", texto_2, flags=re.DOTALL)
dic[seccao2[0]]=""

titulos=re.findall(r"<b>(.*)?</b>\s*\n@@@@@@@@@@@@@@", texto_2)


### Criação das chaves no dicionário para cada título desta secção
dic[seccao2[0]] = dict.fromkeys(titulos)

### Tratamento dos títulos 1 a 3
for j in range (len(titulos)-1):
    exp=f"<b>{titulos[j]}</b>\n@@@@@@@@@@@@@@(.*)\s*<b>{titulos[j+1]}" 
    
    textoaux=re.findall(exp, texto_2, flags=re.DOTALL)
    
    textoaux[0]=str(textoaux[0])+"#"

    subtitulos=re.findall(r"#<b>(.*)</b>?§", textoaux[0])

    dic[str(seccao2[0])][titulos[j]]=dict.fromkeys(subtitulos) 
    dic[str(seccao2[0])][titulos[j]]["Introdução: "]=textoIntros[j+4].replace("\n", "").replace("\t", "")

    ### Trata de todos menos o ultimo subtitulo
    for i in range (len(subtitulos)-1):
        exp=f"#<b>{subtitulos[i]}</b>§\n(.*)\n?#<b>{subtitulos[i+1]}" 
        textoaux2=re.findall(exp, textoaux[0], flags=re.DOTALL)
        textoaux2[0]=str(textoaux2[0])+"\n"
        textoaux3=re.findall(r'(\w)\)(.+)?\n', textoaux2[0])
        dicvista = {t[0]: t[1] for t in textoaux3}
        dic[str(seccao2[0])][titulos[j]][subtitulos[i]]=dicvista
    
    ### Tratamento do último subtítulo 
    exp=f"#<b>{subtitulos[len(subtitulos)-1]}</b>§\n(.*)"
    textoaux2=re.findall(exp, textoaux[0], flags=re.DOTALL)
    textoaux2[0]=str(textoaux2[0])+"\n"
    textoaux3=re.findall(r'(\w)\)(.+)?\n', textoaux2[0])    
    dicvista = {t[0]: t[1] for t in textoaux3}
    dic[str(seccao2[0])][titulos[j]][subtitulos[len(subtitulos)-1]]=dicvista


### Retirar o texto do ultimo titulo 4
expfinal=f"<b>{titulos[len(titulos)-1]}</b>\n@@@@@@@@@@@@@@(.*)"

### Tratamento de títulos para uma linha só:
textoauxfinal=re.findall(expfinal, texto_2, flags=re.DOTALL)
subtitulos=re.findall(r"#<b>(.*)</b>?§", textoauxfinal[0])


dic[str(seccao2[0])][titulos[len(titulos)-1]]=dict.fromkeys(subtitulos)
dic[str(seccao2[0])][titulos[j+1]]["Introdução: "]=textoIntros[j+5].replace("\n", "").replace("\t", "")

### Tratamento dos subtítulos 4:
for i in range (len(subtitulos)-1):
        exp=f"#<b>{subtitulos[i]}</b>§\n(.*)\n?#<b>{subtitulos[i+1]}" 
        textoaux2=re.findall(exp, textoauxfinal[0], flags=re.DOTALL)
        textoaux2[0]=str(textoaux2[0])+"\n"
        textoaux3=re.findall(r'(\w)\)(.+)?\n', textoaux2[0])
        dicvista = {t[0]: t[1] for t in textoaux3}
        dic[str(seccao2[0])][titulos[len(titulos)-1]][subtitulos[i]]=dicvista
    
### Tratamento do último subtítulo 4.11 
exp=f"#<b>{subtitulos[len(subtitulos)-1]}</b>§\n(.*)"
textoaux2=re.findall(exp, textoauxfinal[0], flags=re.DOTALL)
textoaux2[0]=str(textoaux2[0])+"\n"
textoaux3=re.findall(r'(\w)\)(.+)?\n', textoaux2[0])    
dicvista = {t[0]: t[1] for t in textoaux3}
dic[str(seccao2[0])][titulos[len(titulos)-1]][subtitulos[len(subtitulos)-1]]=dicvista


#####################################################
### Guardar a estrutura de Dados em JSON
#####################################################

filejson=open("jsons\DicOssos.json", "w", encoding='utf-8')
json.dump(dic, filejson, indent=4, ensure_ascii=False)

