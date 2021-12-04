import json
from gpt3.generate_training_data import generate
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable

knowledge_sources = ('https://nakamotoinstitute.org/literature/', 'https://nakamotoinstitute.org/research/', 'https://nakamotoinstitute.org/mempool/')
blacklisted_urls = ['https://nakamotoinstitute.org/mempool/authors', 'https://nakamotoinstitute.org/mempool/series', 'https://nakamotoinstitute.org/mempool/feed/', 
'https://nakamotoinstitute.org/', 'https://satoshi.nakamotoinstitute.org/', 'https://nakamotoinstitute.org/mempool/']
articles = []
data = []

def scrape():
    # Get all the article links from the three knowledge sources
    driver = webdriver.Firefox()
    with webdriver.Firefox() as driver:
        for knowledge_source in knowledge_sources:
            driver.get(knowledge_source)
            # Scrape is slightly different on mempool page
            if knowledge_source == 'https://nakamotoinstitute.org/mempool/':
                anchors = driver.find_elements_by_xpath("//a[@href]")
                for link in anchors:
                    # Avoid blacklisted urls and links to the series pages
                    if link.get_attribute('href') in blacklisted_urls or 'https://nakamotoinstitute.org/mempool/series/' in link.get_attribute('href'):
                        pass
                    elif 'https://nakamotoinstitute.org/mempool/' in link.get_attribute('href'):
                        articles.append(link.get_attribute('href'))
            else:
                # Get all articles that are hosted as HTML pages
                anchors = driver.find_elements_by_xpath("//a[@href]")
                for link in anchors:
                    if link.text == "HTML":
                        articles.append(link.get_attribute('href'))

    # Get all of the article text and title from the article links
    count = 0
    for article in articles:
        with webdriver.Firefox() as driver:
            driver.get(article)
            title = driver.find_element_by_xpath("//h1").text
            body = driver.find_elements_by_xpath("//p")
            # Trigger bitcoin chatbot training data generation
            generate(body)
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
    with open('./datasets/knowledge_datasets/bitcoin_knowledge.json', 'a') as outfile:
        for d in data:
            json.dump(d, outfile)
            outfile.write('\n')