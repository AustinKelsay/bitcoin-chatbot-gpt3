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
data =[]

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
                # Avoid all pages that arent an article
                if link.get_attribute('href') in blacklisted_urls:
                    pass
                elif 'https://nakamotoinstitute.org/mempool/' in link.get_attribute('href'):
                    articles.append(link.get_attribute('href'))
        else:
            # Get all articles that arent pdf's
            anchors = driver.find_elements_by_xpath("//a[@href]")
            for link in anchors:
                if link.text in ["txt", "HTML"]:
                    articles.append(link.get_attribute('href'))

for article in articles:
    try:
        driver = webdriver.Firefox()
        driver.get(article)
        html = driver.page_source
        article_text = text_from_html(html)
        # Iterate through list of strings
        for text in article_text:
            obj = {
                'link': article,
                'text': text
            }
            data.append(obj)
        driver.close()
    except:
        print("ERROR")
        print('\n')
        print(article)

# Output training data to json file
with open('nakamoto_institute_scrape.json', 'w') as outfile:
    for d in data:
        json.dump(d, outfile)
        outfile.write('\n')