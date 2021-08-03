from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable

#This example requires Selenium WebDriver 3.13 or newer
parent_articles = []
child_articles = []
data =[]

with webdriver.Firefox() as driver:
    wait = WebDriverWait(driver, 10)
    driver.get("https://nakamotoinstitute.org/literature/")

    # Get parent articles
    articles = driver.find_elements_by_xpath("//a[@href]")
    for article in articles:
        if "/literature/" in article.get_attribute("href"):
            parent_articles.append(article.get_attribute("href"))

    # Get child articles
    for article in parent_articles:
        driver.get(article)
        articles = driver.find_elements_by_xpath("//a[@href]")
        for article in articles:
            if article.text == 'HTML':
                child_articles.append(article.get_attribute("href"))

    # Iterate through child articles and get content
    for article in child_articles:
        driver.get(article)

        section_header = driver.find_elements_by_xpath("//h2")
        section = driver.find_elements_by_xpath("//p")

        completion = ''
        for sec in section:
            completion += sec.text


        obj = {
            'prompt': driver.find_element_by_xpath("//h1").text,
            'completion': completion
        }
        data.append(obj)

for d in data:
    print(d)
    print("\n")