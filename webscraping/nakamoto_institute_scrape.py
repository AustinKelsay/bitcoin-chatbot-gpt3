from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable

#This example requires Selenium WebDriver 3.13 or newer
parent_articles = []
child_articles = []

with webdriver.Firefox() as driver:
    wait = WebDriverWait(driver, 10)
    driver.get("https://nakamotoinstitute.org/literature/")

    articles = driver.find_elements_by_xpath("//a[@href]")
    for article in articles:
        if "/literature/" in article.get_attribute("href"):
            driver.get(article.get_attribute("href"))
            driver.implicitly_wait(2)
            children = driver.find_elements_by_xpath("//a[@href]")
            for child in children:
                if child.text == "HTML":
                    print("child " + child.get_attribute("href"))
                # if child.text == "HTML":
                #     child_articles.append(child.get_attribute("href"))
                #     break

