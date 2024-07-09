import re
import os
import json
from datetime import datetime
import random


try:
    with open("AIDA.json", "r", encoding="utf-8") as file:
        ficheiros = json.load(file)
except Exception as e:
    ficheiros = {}


pasta = 'A2'

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


        file_out=open("AIDA.json","w",encoding='utf-8')
        json.dump(ficheiros,file_out,indent=4,ensure_ascii=False) 
        file_out.close()
    return ficheiros


def guardarpedido(dicionario):  # guarda pedidos no dicionario
    for paciente in dicionario:
        if paciente not in ficheiros:                                                         # se paciente nao existe
            ficheiros[paciente] = dicionario[paciente]
            r = "Paciente adicionado com sucesso e pedido guardado!"
        else:                                                                                 # se paciente existe
            for idpedido in dicionario[paciente]["Pedidos"]:
                ficheiros[paciente]["Pedidos"][idpedido] = dicionario[paciente]["Pedidos"][idpedido]     
                r = "Pedido guardado!"
    return r
    


def fzrpedido():
    r = ""
    idpedido = random.randint(1,999999)
    pid = input("Patient ID: ")
    if pid in ficheiros:
        nome = ficheiros[pid]["Nome"]
        genero = ficheiros[pid]["Genero"]
        data_nascimento = ficheiros[pid]["Data de nascimento"]
    else:
        nome = input("Patient name (Format: LAST^FIRST^MIDDLE): ")
        data_nascimento = input("Date of birth (Format: YYYYMMDD): ")
        genero = input("Gender (M/F): ")
    
    obr = input("Observation request: ")
    exame = input("Tipo de exame: ")
    data_transacao = datetime.now()
    id_msg = data_transacao.strftime("%Y%m%d%H%M%S%f")[:-3]  # Timestamp format: YYYYMMDDHHMMSSmmm
    data_transacao = data_transacao.isoformat()
    
    hl7_message = ""
    hl7_message += f"""MSH|^~\&|AIDA|AIDA|PACS|PACS|{id_msg}||ORM^O01|{id_msg}5751000002533|P|2.5|||AL|	
                    PID|||{pid}||{nome}||{data_nascimento}|{genero}|||||||||||	
                    PV1||I|INT||||||||||||||||15002727|		
                    ORC|NW|{idpedido}|{idpedido}||||||{data_transacao}|	
                    OBR|01|{idpedido}|{idpedido}|{obr}||||||||||||||CR|{exame}||||||||^^^{data_transacao}^^	
                    0||||||"""

    output_filename = f"A1/{id_msg}.hl7"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(hl7_message)
        r = "Mensagem enviada para PACS com sucesso!"
    dicionario_auxiliar={}
    dicionario_auxiliar[pid] = {"Nome": nome,
                                "Data de nascimento": data_nascimento,
                                "Genero": genero,
                                "Pedidos": {idpedido: {"Tipo de pedido": exame,
                                                        "Status": "",
                                                        "Order Control": "NW",
                                                        "Data de transacao": data_transacao,
                                                        "OBR": obr,
                                                        "OBX": "" }
                                            }
                                }
                                        
    guardarpedido(dicionario_auxiliar)
    return r


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

            output_filename = f"A1/{idpedido}.hl7"
            f = open(output_filename, "w", encoding="utf-8")
            f.write(hl7_message)
            r = "Pedido cancelado e notificação enviada para PACS!"
            

        else:
            r = "Pedido não encontrado"
    else:
        r = "Paciente não encontrado!"
    return r

def verpedido():
    pid = input("Introduza o ID do paciente: ")
    idpedido = input("Introduza o ID do pedido: ")
    if pid in ficheiros:
        if idpedido in ficheiros[pid]["Pedidos"]:
            r = ficheiros[pid]["Pedidos"][idpedido]
        else: 
            r = "O pedido não foi encontrado!"
    else:
        r = "O paciente não foi encontrado!"



def listarpedidos():
    for paciente in ficheiros:
        print("Pedidos do paciente " + str(paciente))
        print(ficheiros[paciente])
    r = "Todos os pedidos foram listados"
















def menu(inp):
    if inp == "1":
        fzrpedido()
    elif inp == "2":
        cancelarpedido()
    elif inp == "3":
        verpedido()
    elif inp == "4":
        listarpedidos()
    elif inp == "5":
        atualiza()
    else:
        return "Escolha as opções corretas"


# ---------------------- INICIO DO PROGRAMA ------------------------


T=True

while T==True:
    st = input("Escolha o que quer fazer: \n"
                "1 - Fazer pedido \n"
                "2 - Cancelar o pedido \n"
                "3 - Ver pedido \n"
                "4 - Ver todos os pedidos\n"
                "5 - Atualizar\n"
                "x - Sair \n" )
    if st=="x":
        T=False
    else:
        print(menu(st))


# ---------------------- FIM DO PROGRAMA ------------------------
file = open("AIDA.json","w",encoding='utf-8')
atualiza()
json.dump(ficheiros, file, indent=4, ensure_ascii=False)
file.close()