import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time
import requests
import ujson
with open('scraper_results.json', 'r') as file:
    # Carregue os dados JSON do arquivo
    data = json.load(file)

# Lista para armazenar as URLs das publicações
publication_urls = []

# Iterar sobre cada dicionário no JSON e extrair a URL da publicação
for item in data:
    publication_urls.append(item['pub_url'])

SLEEP_SECONDS = 1
print("Iniciando o crawler...")

# Inicializando o driver para Chrome
webOpt = webdriver.ChromeOptions()
webOpt.add_experimental_option('excludeSwitches', ['enable-logging'])
webOpt.add_argument('--ignore-certificate-errors')
webOpt.add_argument('--incognito')
webOpt.headless = True

service = Service(executable_path=r'/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=webOpt)
print("Conectado ao navegador")

 # Comece com o link original
# Imprimir a lista de URLs das publicações
#print(publication_urls)

abstracts=[]

for link in publication_urls:
    time.sleep(SLEEP_SECONDS)
    driver.get(link)
    r = requests.get(driver.current_url)
                # Parse all the data via BeautifulSoup
    soup = BeautifulSoup(r.content, 'lxml')
    abstract= soup.find_all( "div", class_="textblock")
    if abstract != []:
        abstracts.append(abstract[0].get_text())
    else:
        abstracts.append("No Abstract") #### PARA OS LINKS FICARAM COM OS ABSTRACTS CERTOS
   
with open('pub_abstracts.json', 'w') as f:
    ujson.dump(abstracts, f)
#print(abstract[0].get_text())