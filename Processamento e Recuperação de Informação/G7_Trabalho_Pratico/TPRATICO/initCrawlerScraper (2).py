# https://blog.streamlit.io/purehub-a-search-engine-for-your-university
# https://github.com/maladeep/Coventry-PureHub-Search-Engine

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time
import requests
import ujson
from webdriver_manager.chrome import ChromeDriverManager

def write_authors(list1, file_name):
     # Function to write authors' URLs to a file
    with open(file_name, 'w', encoding='utf-8') as f:
        for i in range(0, len(list1)):
            f.write(list1[i] + '\n')
def initCrawlerScraper(url_seed, max_profiles=500):
    
    SLEEP_SECONDS = 1
    #MAX_NR_SEARCHES = 20  #new
    print("inici")
    # Initialize driver for Chrome 
    webOpt = webdriver.ChromeOptions()
    webOpt.add_experimental_option('excludeSwitches', ['enable-logging'])
    webOpt.add_argument('--ignore-certificate-errors')
    webOpt.add_argument('--incognito')
    webOpt.headless = True

    service =Service(executable_path=r'/usr/bin/chromedriver') #new
    #options = webdriver.Chrome()
    #options.add_argument('--headless')
    #driver = webdriver.Chrome(ChromeDriverManager().install(), options=webOpt)
    driver = webdriver.Chrome(service=service, options=webOpt) #new
    print("gg")
    driver.get(url_seed)  # Start with the original link
   
    links = []  # Array with pureportal profiles URL
    pub_data = []  # To store publication information for each pureportal profile

    #nextLink = driver.find_element_by_css_selector(".nextLink").is_enabled()  # Check if the next page link is enabled
    from selenium.webdriver.common.by import By #new
    nextLink = driver.find_element(By.CSS_SELECTOR,".nextLink").is_enabled()  # Check if the next page link is enabled  #new


    link = '<a class="link person" href="https://pureportal.coventry.ac.uk/en/persons/amal-ahmad-khair" rel="Person"><span>Amal Ahmad Khair</span></a>'
    a=str(link)[str(link).find('https://pureportal.coventry.ac.uk/en/persons/'):]
    b=[str(link).find('https://pureportal.coventry.ac.uk/en/persons/')]
    url =  str(link)[str(link).find('https://pureportal.coventry.ac.uk/en/persons/'):].split('>')


    print("Crawler has begun...")
    while (nextLink):
        page = driver.page_source
        # XML parser to parse each URL
        bs = BeautifulSoup(page, "lxml")  # Parse the page source using BeautifulSoup. (Requires pip install lxml)
        # Extracting exact URL by spliting string into list
        for link in bs.findAll('a', class_='link person'):
            #url = str(link)[str(link).find('https://pureportal.coventry.ac.uk/en/persons/'):].split('>"')
            url = str(link)[str(link).find('https://pureportal.coventry.ac.uk/en/persons/'):].split('>') #new
            url = str(url[0]).split('"')
            links.append(url[0])
            
        # Click on Next button to visit next page
        try:
            # find_element (not find_elements) returns a single webElement, not a list.
            #if driver.find_element_by_css_selector(".nextLink"):
            if driver.find_element(By.CSS_SELECTOR,".nextLink"):  #new
                #element = driver.find_element_by_css_selector(".nextLink")
                element = driver.find_element(By.CSS_SELECTOR,".nextLink") #new
                #print("ELEMENTo", element.text) #new
                try:
                    driver.execute_script("arguments[0].click();", element)
                except:
                    print("EXCEPTION1") #new
                    break
            else:
                nextLink = False
        except NoSuchElementException:
            print("EXCEPTION2") #new
            break

        # Check if the maximum number of profiles is reached
        if len(links) >= max_profiles:
            print("ABOVE MAX_PROFILES") #new
            break
        
    #links = links[:MAX_NR_SEARCHES]      #new  limitar nr links pesquisados a 20
    print("Crawler has found ", len(links), " pureportal profiles")
    write_authors(links, 'Authors_URL.txt') # Write the authors' URLs to a file
    nr_links = len(links)
    print("Scraping publication data for ", nr_links, " pureportal profiles...")
    count = 0
    for link in links:
        count += 1; print("LINKS TO SCRAPPE", nr_links - count) #new
        # Visit each link to get data
        time.sleep(SLEEP_SECONDS)
        driver.get(link)
        try:
            #if driver.find_elements_by_css_selector(".portal_link.btn-primary.btn-large"):
            if driver.find_elements(By.CSS_SELECTOR,".portal_link.btn-primary.btn-large"): #new
                #element = driver.find_elements_by_css_selector(".portal_link.btn-primary.btn-large")
                element = driver.find_elements(By.CSS_SELECTOR,".portal_link.btn-primary.btn-large") #new
                for a in element:
                    #print ("ELEMENT", a.text) #new
                    if "research output".lower() in a.text.lower():
                        driver.execute_script("arguments[0].click();", a)
                        driver.get(driver.current_url)
                        print("CURRENT URL", driver.current_url) #new
                        # Get name of Author
                        #name = driver.find_element_by_css_selector("div[class='header person-details']>h1")
                        name = driver.find_element(By.CSS_SELECTOR,("div[class='header person-details']>h1")) #new
                        r = requests.get(driver.current_url)
                        # Parse all the data via BeautifulSoup
                        soup = BeautifulSoup(r.content, 'lxml')
                        #print(soup) #complete html page

                        # Extracting publication name, publication url, date and CU Authors
                        table = soup.find('ul', attrs={'class': 'list-results'})
                        if table != None:
                            for row in table.findAll('div', attrs={'class': 'result-container'}):
                                data = {}
                                #print("!!!!",row)
                                #print("!!!!!!!!",row.h3)
                                data['name'] = row.h3.a.text
                                print("NAME", row.h3.a.text)
                                data['pub_url'] = row.h3.a['href']
                                date = row.find("span", class_="date")
                                
                                rowitem = row.find_all(['div'])
                                span = row.find_all(['span'])                                
                                data['cu_author'] = name.text                                
                                data['date'] = date.text                                
                                print("Publication Name :", row.h3.a.text)
                                print("Publication URL :", row.h3.a['href'])
                                print("CU Author :", name.text)
                                print("Date :", date.text)
                                print("\\n")
                                pub_data.append(data)
            else:
                # Get name of Author
                #name = driver.find_element_by_css_selector("div[class='header person-details']>h1")
                name = driver.find_element(By.CSS_SELECTOR,"div[class='header person-details']>h1") #new
                r = requests.get(link)
                # Parse all the data via BeautifulSoup
                soup = BeautifulSoup(r.content, 'lxml')
                # Extracting publication name, publication URL, date and CU Authors
                table = soup.find('div', attrs={'class': 'relation-list relation-list-publications'})
                if table != None:
                    for row in table.findAll('div', attrs={'class': 'result-container'}):
                        data = {}
                        data["name"] = row.h3.a.text
                        data['pub_url'] = row.h3.a['href']
                        date = row.find("span", class_="date")
                        rowitem = row.find_all(['div'])
                        span = row.find_all(['span'])
                        data['cu_author'] = name.text
                        data['date'] = date.text
                        print("Publication Name :", row.h3.a.text)
                        print("Publication URL :", row.h3.a['href'])
                        print("CU Author :", name.text)
                        print("Date :", date.text)
                        print("\\n")
                        pub_data.append(data)
        except Exception:
            print("EXCEPTION3") #new
            continue

    print("Crawler has scrapped data for ", len(pub_data), " pureportal publications")
    driver.quit()
    # Writing all the scraped results in a file with JSON format
    with open('scraper_results.json', 'w') as f:
        ujson.dump(pub_data, f)

initCrawlerScraper('https://pureportal.coventry.ac.uk/en/organisations/coventry-university/persons/', max_profiles=500)