import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable

url = 'https://bitcoinrabbithole.org/writings/'
articles = []
titles = []
articles_text = []
    
driver = webdriver.Firefox()
driver.get(url)

for a in driver.find_elements_by_xpath('//a[contains(text(), "Link")]'):
    articles.append(a.get_attribute('href'))

for a in driver.find_elements_by_xpath('//h4'):
    titles.append(a.text)

for a in articles:
    driver.get(a)
    text = ''
    for p in driver.find_elements_by_xpath('//p'):
        text += p.text
    articles_text.append(text)

driver.close()

for text in articles_text:
    print(text)