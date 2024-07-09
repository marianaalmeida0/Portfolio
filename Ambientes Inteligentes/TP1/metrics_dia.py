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
    folha = folhas.sheet1
    dados = folha.get_all_values()

    # Loop pelos dados e enviar para o Adafruit IO
    for linha in dados[1:]:  # Ignora o cabeçalho
        valor = linha[1]  # passos
        aio.send('passos', valor)
        print(f"Dados enviados para Adafruit IO: {valor}")
enviar_dados_para_adafruit()

