import json
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable

knowledge_sources = ('https://nakamotoinstitute.org/literature/', 'https://nakamotoinstitute.org/research/', 'https://nakamotoinstitute.org/mempool/')
articles = []
blacklisted_urls = ['https://nakamotoinstitute.org/mempool/authors', 'https://nakamotoinstitute.org/mempool/series', 'https://nakamotoinstitute.org/mempool/feed/', 
'https://nakamotoinstitute.org/', 'https://satoshi.nakamotoinstitute.org/', 'https://nakamotoinstitute.org/mempool/']
data = []

driver = webdriver.Firefox()

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'lxml')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return [t.strip() for t in visible_texts if t.strip() != '']

with webdriver.Firefox() as driver:
    wait = WebDriverWait(driver, 10)
    for knowledge_source in knowledge_sources:
        driver.get(knowledge_source)
        if knowledge_source == 'https://nakamotoinstitute.org/mempool/':
            # Scrape is slightly different on this page
            anchors = driver.find_elements_by_xpath("//a[@href]")
            for link in anchors:
                # Avoid all pages that arent an article text page
                if link.get_attribute('href') in blacklisted_urls or 'https://nakamotoinstitute.org/mempool/series/' in link.get_attribute('href'):
                    pass
                elif 'https://nakamotoinstitute.org/mempool/' in link.get_attribute('href'):
                    articles.append(link.get_attribute('href'))
        else:
            # Get all articles that arent pdf's
            anchors = driver.find_elements_by_xpath("//a[@href]")
            for link in anchors:
                if link.text == "HTML":
                    articles.append(link.get_attribute('href'))

count = 0
for article in articles:
    with webdriver.Firefox() as driver:
        wait = WebDriverWait(driver, 5)
        driver.get(article)
        title = driver.find_element_by_xpath("//h1").text
        body = driver.find_elements_by_xpath("//p")
        completion = ''
        for paragraph in body:
            obj = {
                'link': article,
                'title': title,
                'text': paragraph.text
            }
            data.append(obj)
        driver.close()
        count += 1
        print(count)

# Output training data to json file
with open('nakamoto_institute_scrape.json', 'w') as outfile:
    for d in data:
        json.dump(d, outfile)
        outfile.write('\n')