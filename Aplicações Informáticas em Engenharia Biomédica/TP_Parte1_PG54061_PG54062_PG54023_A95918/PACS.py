import re
import os
import json
from datetime import datetime
"""
-ver pedidos pendentes
-realizar exames
-realizar relatorio
-cancelar pedido
"""
try:
    with open("AIDA.json", "r", encoding="utf-8") as file:
        ficheiros = json.load(file)
except Exception as e:
    ficheiros = {}
    

pasta = 'B1'

def processa_mensagem(mensagem):             # recebe string e devolve dicionario com informacao da mensagem
    
    campos = mensagem.split("\n")
    OBX = ""
    OBR = ""
    for campo in campos:
        campo = campo.strip()
        if campo.startswith("MSH"):
            MSH = campo
        elif campo.startswith("PID"):
            PID = campo
            PID = PID.split("|")
            pid = PID[3]
            nome = PID[5]
            data_nascimento = PID[7]
            genero = PID[8]
        elif campo.startswith("ORC"):
            ORC = campo
            ORC = ORC.split("|")
            ordercontrol = ORC[1]
            idpedido = ORC[2]
            status = ORC[5]
            data_transacao = ORC[9]
        elif campo.startswith("OBR"):
            OBR += "\n" + campo
            tipopedido = OBR.split("|")[4]
        elif campo.startswith("OBX"):
            OBX += "\n" + campo
    
    return {pid : {"Nome": nome,
                    "Data de nascimento": data_nascimento,
                    "Genero": genero,
                    "Pedidos": {
                idpedido: {"Tipo de pedido": tipopedido,
                            "Status": status,
                            "Data de transacao": data_transacao,
                            "Order Control": ordercontrol,
                            "OBR": OBR,
                            "OBX": OBX }
                                }
                    }
            }



def atualiza():
    for arquivo in os.listdir(pasta):
        if os.path.isfile(os.path.join(pasta, arquivo)) and os.path.join(pasta, arquivo).endswith(".dat"):
            with open(os.path.join(pasta, arquivo), 'r', encoding="utf-8") as f:
                mensagem = f.read()
                msg = processa_mensagem(mensagem)
                for paciente in msg:
                    if paciente not in ficheiros:                                                         # se paciente nao existe
                        ficheiros[paciente] = msg[paciente]
                    else:                                                                                 # se paciente existe
                        for idpedido in msg[paciente]["Pedidos"]:
                            ficheiros[paciente]["Pedidos"][idpedido] = msg[paciente]["Pedidos"][idpedido]                                                                                    # se pedido existe


        file_out=open("PACS.json","w",encoding='utf-8')
        json.dump(ficheiros,file_out,indent=4,ensure_ascii=False) 
        file_out.close()
    return ficheiros



def guardarpedido(dicionario):
    for paciente in dicionario:
        if paciente not in ficheiros:                                                         # se paciente nao existe
            ficheiros[paciente] = dicionario[paciente]
            print("Paciente adicionado com sucesso e pedido guardado!")
        else:                                                                                 # se paciente existe
            for idpedido in dicionario[paciente]["Pedidos"]:
                ficheiros[paciente]["Pedidos"][idpedido] = dicionario[paciente]["Pedidos"][idpedido]     
                print("Pedido guardado!")
    


def ver_pedidos_pendentes():
    pid = input("ID do paciente: ")
    if pid in ficheiros:
        print("A carregar pedidos pendentes de " + ficheiros[pid]["Nome"])
        for pedido in ficheiros[pid]["Pedidos"]:
            if ficheiros[pid]["Pedidos"][pedido]["Status"] != "CM" and  ficheiros[pid]["Pedidos"][pedido]["Status"] != "CA":
                print(ficheiros[pid]["Pedidos"][pedido])
        print("Carregamento terminado!")
    else:
        print("Paciente não encontrado!")
        
    
def realizacao_exame():
    idpedido = input("ID do pedido: ")
    pid = input("Patient ID: ")
    if pid in ficheiros:
        nome = ficheiros[pid]["Nome"]
        genero = ficheiros[pid]["Genero"]
        data_nascimento = ficheiros[pid]["Data de nascimento"]
        if idpedido in ficheiros[pid]["Pedidos"]:
            exame = ficheiros[pid]["Pedidos"][idpedido]["Tipo de pedido"]
        else:
            exame = input("Tipo de exame: ")
    else:
        nome = input("Patient name (Format: LAST^FIRST^MIDDLE): ")
        data_nascimento = input("Date of birth (Format: YYYYMMDD): ")
        genero = input("Gender (M/F): ")
        exame = input("Tipo de exame: ")
    obr = input("Observation request: ")
    data_transacao = datetime.now()
    id_msg = data_transacao.strftime("%Y%m%d%H%M%S%f")[:-3]  # Timestamp format: YYYYMMDDHHMMSSmmm
    data_transacao = data_transacao.isoformat()
    hl7_message = f"""MSH|^~\&|PACS|PACS|AIDA|AIDA|{id_msg}||ORM^O01|{id_msg}5751000002533|P|2.5|||AL|	
                    PID|||{pid}||{nome}||{data_nascimento}|{genero}|||||||||||	
                    PV1||I|INT||||||||||||||||15002727|		
                    ORC|SC|{idpedido}|{idpedido}||CM||||{data_transacao}|	
                    OBR|01|{idpedido}|{idpedido}|{obr}||||||||||||||CR|{exame}||||||||^^^{data_transacao}^^	
                    0||||||"""
    
    output_filename = f"B2/{id_msg}.hl7"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(hl7_message)
        print("Mensagem enviada para AIDA com sucesso!")
    dicionario_auxiliar={}
    dicionario_auxiliar[pid] = {"Nome": nome, 
                                "Genero": genero, 
                                "Data de nascimento": data_nascimento,
                                "Pedidos": {idpedido: {"Tipo de pedido": exame,
                                                        "Status": "CM",
                                                        "Order Control": "SC",
                                                        "Data de transacao": data_transacao,
                                                        "OBR": obr,
                                                        "OBX": "" }
                                            } }
    guardarpedido(dicionario_auxiliar)
    
    print(f"A mensagem HL7 de realização de exame foi escrita no arquivo: {output_filename}")


def realizacao_relatorio():
    idpedido = input("ID do pedido: ")
    pid = input("Patient ID: ")
    if pid in ficheiros:
        nome = ficheiros[pid]["Nome"]
        genero = ficheiros[pid]["Genero"]
        data_nascimento = ficheiros[pid]["Data de nascimento"]
        if idpedido in ficheiros[pid]["Pedidos"]:
            exame = ficheiros[pid]["Pedidos"][idpedido]["Tipo de pedido"]
            obr = ficheiros[pid]["Pedidos"][idpedido]["OBR"]
        else:
            exame = input("Tipo de exame: ")
            obr = input("Observation Request: ")
    else:
        nome = input("Patient name (Format: LAST^FIRST^MIDDLE): ")
        data_nascimento = input("Date of birth (Format: YYYYMMDD): ")
        genero = input("Gender (M/F): ")
        exame = input("Tipo de exame: ")
        obr = input("Observation Request: ")
    relatorio = input("Escreva o relatorio: ")
    data_transacao = datetime.now()
    id_msg = data_transacao.strftime("%Y%m%d%H%M%S%f")[:-3]  # Timestamp format: YYYYMMDDHHMMSSmmm
    data_transacao = data_transacao.isoformat()
    obx = f"OBX|1|PDF_BASE64|||{relatorio}|||||||||20150603012318"
    hl7_message = f"""MSH|^~\&|PACS|PACS|AIDA|AIDA|{id_msg}||ORM^O01|{id_msg}5751000002533|P|2.5|||AL|	
                    PID|||{pid}||{nome}||{data_nascimento}|{genero}|||||||||||	
                    PV1||I|INT||||||||||||||||15002727|		
                    ORC|RE|{idpedido}|{idpedido}||CM||||{data_transacao}|	
                    OBR|01|{idpedido}|{idpedido}|{obr}||||||||||||||CR|{exame}||||||||^^^{data_transacao}^^	
                    OBX|1|PDF_BASE64|||{relatorio}|||||||||20150603012318"""
    
    output_filename = f"B2/{id_msg}.hl7"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(hl7_message)
        print("Mensagem enviada para AIDA com sucesso!")
    dicionario_auxiliar={}
    dicionario_auxiliar[pid] = {"Nome": nome, 
                                "Genero": genero, 
                                "Data de nascimento": data_nascimento,
                                "Pedidos": {idpedido: {"Tipo de pedido": exame,
                                                        "Status": "CM",
                                                        "Order Control": "RE",
                                                        "Data de transacao": data_transacao,
                                                        "OBR": obr,
                                                        "OBX": obx }
                                            } }
    guardarpedido(dicionario_auxiliar)
    
    print(f"A mensagem HL7 de realização de exame foi escrita no arquivo: {output_filename}")


def cancelarpedido():
    pid = input("Introduza o ID do paciente: ")
    idpedido = input("Introduza o ID do pedido que pretende cancelar: ")
    data_transacao = datetime.now()
    id_msg = data_transacao.strftime("%Y%m%d%H%M%S%f")[:-3]
    data_transacao = data_transacao.isoformat()
    if pid in ficheiros.keys():
        if idpedido in ficheiros[pid]["Pedidos"]:
            ficheiros[pid]["Pedidos"][idpedido]["Status"] ="CA"
            ficheiros[pid]["Pedidos"][idpedido]["Data de transacao"] = data_transacao
            ficheiros[pid]["Pedidos"][idpedido]["Order Control"] ="CA"
            hl7_message = ""
            hl7_message += f"""MSH|^~\&|AIDA|AIDA|PACS|PACS|{id_msg}||ORM^O01|{id_msg}5751000002533|P|2.5|||AL|	
                    PID|||{pid}||{ficheiros[pid]["Nome"]}||{ficheiros[pid]["Data de nascimento"]}|{ficheiros[pid]["Genero"]}|||||||||||	
                    PV1||I|INT||||||||||||||||15002727|		
                    ORC|CA|{idpedido}|{idpedido}||CA||||{data_transacao}|	
                    {ficheiros[pid]["Pedidos"][idpedido]["OBR"]}"""

            output_filename = f"B2/{idpedido}.hl7"
            f = open(output_filename, "w", encoding="utf-8")
            f.write(hl7_message)
            print("Pedido cancelado e notificação enviada para AIDA!")

        else:
            print("Pedido não encontrado")
    else:
        print("Paciente não encontrado!")


def listarpedidos():
    for paciente in ficheiros:
        print("Pedidos do paciente " + str(paciente))
        print(ficheiros[paciente])
    print("Todos os pedidos foram listados")















def menu(inp):
    if inp == "1":
        ver_pedidos_pendentes()
    elif inp == "2":
        realizacao_exame()
    elif inp == "3":
        realizacao_relatorio()
    elif inp == "4":
        cancelarpedido()
    elif inp == "5":
        listarpedidos()
    elif inp == "6":
        atualiza()
    else:
        return "Escolha as opções corretas"


# ---------------------- INICIO DO PROGRAMA ------------------------


file = open("PACS.json","a",encoding='utf-8')
json.dump(ficheiros, file, indent=4, ensure_ascii=False)

T=True

while T==True:
    st = input("Digite o tipo de pedido que pretende: \n"
                "1 - Ver pedido pendentes\n"
                "2 - Realizacao Exame\n"
                "3 - Realizacao Relatorio\n"
                "4 - Cancelar Pedido\n"   
                "5 - Listar pedidos\n" 
                "6 - Atualizar\n"     
                "x - Sair \n" )
    if st=="x":
        T=False
    else:
        print(menu(st))
        
        
# ---------------------- FIM DO PROGRAMA ------------------------

atualiza()
json.dump(ficheiros, file, indent=4, ensure_ascii=False)
