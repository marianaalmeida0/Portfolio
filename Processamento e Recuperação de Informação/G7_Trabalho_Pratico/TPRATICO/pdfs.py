from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import requests
import ujson
from webdriver_manager.chrome import ChromeDriverManager
from weasyprint import HTML

def initCrawlerScraper(url_seed, max_artigos=41):
    
    # Inicializar driver para o Chrome
    webOpt = webdriver.ChromeOptions()
    webOpt.add_experimental_option('excludeSwitches', ['enable-logging'])
    webOpt.add_argument('--ignore-certificate-errors')
    webOpt.add_argument('--incognito')
    webOpt.headless = True

    service = Service(executable_path=r'/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=webOpt)
    current_url=driver.get(url_seed)  # Começa com o link original

    links = []  # Lista para armazenar os links dos artigos
    from selenium.webdriver.common.by import By 
    r = requests.get(driver.current_url)
                # Parse all the data via BeautifulSoup
    bs = BeautifulSoup(r.content, 'lxml')


   # Analisa o código-fonte da página usando BeautifulSoup
        
        
    links_dic = bs.findAll('a', {'rel': 'ContributionToJournal'})
    #print(links_dic)
# Exibir os links encontrados
    for link in links_dic:
            print("URL do link:", link['href'])
            #print(link)
            links.append(link['href'])

    print(links)


    # Escrever os links dos artigos em um arquivo JSON
    with open('articles_links.json', 'w') as f:
        ujson.dump(links, f)
    html={}
    # Converter cada link de artigo para PDF
    for idx, article_link in enumerate(links):
        html_content = requests.get(article_link).text
        html_file_name = f'article_{idx}.html'
        pdf_file_name = f'article_{idx}.pdf'
        
        with open(html_file_name, 'w') as html_file:
            html_file.write(html_content)
            html[pdf_file_name]=html_content


        HTML(html_file_name).write_pdf(pdf_file_name)
        print(f'Converted {article_link} to PDF: {pdf_file_name}')

    with open('htmls.json', 'w') as fi:
        ujson.dump(html, fi)
    
    driver.quit()

initCrawlerScraper('https://pureportal.coventry.ac.uk/en/organisations/ihw-centre-for-intelligent-healthcare-cih/publications/', max_artigos=41)
