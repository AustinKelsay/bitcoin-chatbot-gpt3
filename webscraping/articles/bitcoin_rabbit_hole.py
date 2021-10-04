import json
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable

url = 'https://bitcoinrabbithole.org/writings/'
articles = []
titles = []
blacklist = ["Bitcoin", "The Bullish Case For Bitcoin", "The Bitcoin Standard",
"Cryptocurrency Technologies Book", "Blockchain Control Flow", "Mastering Bitcoin", "Bitcoin Optech 2018 Year in Review Special", "Grokking Bitcoin",
"The Book Of Satoshi", "The Sovereign Individual", "The Sovereign Individual", "James' Liberty File Collection Index", "What Is Austrian Economics?",
"Theory Of Money And Credit", "What Has Government Done To Our Money?", "Denationalisation Of Money", "The Case Against The Fed", 
"Has The Fed Been A Failure?", "Deflationary Spiral Bogey", "Why Debates Over Inflation Are Pointless", "The Ethics Of Money Production",]
    
driver = webdriver.Firefox()
driver.get(url)

for a in driver.find_elements_by_xpath('//a[contains(text(), "Link")]'):
    articles.append(a.get_attribute('href'))

for a in driver.find_elements_by_xpath('//h4'):
    titles.append(a.text)

driver.close()

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

for idx, article in enumerate(articles):
    try:
        if titles[idx] not in blacklist:
            driver = webdriver.Firefox()
            driver.get(article)
            html = driver.page_source
            article_text = text_from_html(html)
            # Iterate through all of the article text creating an object with the correct title for each text section
            with open('bitcoin_rabbit_hole.json', 'w') as outfile:    
                for text in article_text:
                    obj = {
                        'prompt': titles[idx],
                        'text': text
                    }
                    json.dump(obj, outfile)
                    outfile.write('\n')
            driver.close()
    except:
        print('Error')
        print()
        print(article)
