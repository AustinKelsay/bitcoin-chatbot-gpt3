import json
from gpt3.generate_training_data import generate
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable

#This example requires Selenium WebDriver 3.13 or newer
parent_articles = []
child_articles = []
data =[]

def scrape():
    with webdriver.Firefox() as driver:
        wait = WebDriverWait(driver, 10)
        driver.get("https://github.com/bitcoinbook/bitcoinbook/blob/develop/book.asciidoc")

        # Get parent articles
        articles = driver.find_elements_by_xpath("//a[@href]")
        for article in articles:
            if ".asciidoc" in article.text and "appdx" not in article.text:
                parent_articles.append(article.get_attribute("href"))

        for article in parent_articles:
                driver.get(article)
                text = driver.find_elements_by_xpath("//p")
                # Get the name of the chapter which is index 1 in the list of h2 elements
                chapter = driver.find_elements_by_xpath("//h2")
                # Trigger bitcoin chatbot training data generation
                generate(text)
                for section in text:
                    j = {
                        "link": article,
                        "title": "Mastering bitcoin - " + chapter[1].text,
                        "text": section.text
                    }
                    data.append(j)


    with open('./datasets/knowledge_datasets/bitcoin_knowledge.json', 'a') as outfile:    
        for obj in data:
            json.dump(obj, outfile)
            outfile.write('\n')