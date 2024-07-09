from datetime import timedelta

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from Adafruit_IO import Client

# Configurações do Adafruit IO
ADAFRUIT_IO_USERNAME = "Mariana123"
ADAFRUIT_IO_KEY = "aio_fTmo56xD4GlWZy22YJYB6LajaM9B"
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Autenticação com o Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
gc = gspread.authorize(credentials)

# ID da spreadsheet do Google Sheets
SPREADSHEET_ID = '1Q78WlSU6sA2FByCs9x8dwEmEWgrV5OFqGIpV6cpmEps'


# Função para buscar dados do Google Sheets e enviar para o Adafruit IO
def enviar_dados_para_adafruit():
    folhas = gc.open_by_key(SPREADSHEET_ID)
    folha = folhas.get_worksheet(1)  # Abrir a segunda folha (índice 1)
    dados = folha.get_all_values()

    valores_filtrados = []
    for linha in dados[1:]:  # Ignora a linha de cabeçalho
        steps = linha[8]
        if steps.isdigit():  # Verifica se é um número válido
            steps = int(steps)
            intervalo = linha[7]  # Coluna do intervalo
            # Converter o intervalo para um objeto timedelta
            horas, minutos, segundos = map(int, intervalo.split(':'))
            intervalo_delta = timedelta(hours=horas, minutes=minutos, seconds=segundos)
            # Verificar se o intervalo se é mais ou menos a duracao do treino 1h30
            if steps < 3000 and intervalo_delta <= timedelta(hours=1, minutes=30)and intervalo_delta >= timedelta(hours=1, minutes=27):
                valores_filtrados.append((intervalo_delta, steps))


    print("Valores de Steps menores que 3000 em um intervalo de 1h30:")
    for timestamp, steps in valores_filtrados:
        print(f"Timestamp: {timestamp}, Steps: {steps}")
        aio.send('passos', steps)
        print(f"Dados enviados para Adafruit IO: {steps}")


enviar_dados_para_adafruit()