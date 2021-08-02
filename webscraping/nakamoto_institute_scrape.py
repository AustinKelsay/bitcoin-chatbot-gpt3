from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

#This example requires Selenium WebDriver 3.13 or newer
parent_articles = []
child_articles = []

with webdriver.Firefox() as driver:
    wait = WebDriverWait(driver, 10)
    driver.get("https://nakamotoinstitute.org/literature/")

    articles = driver.find_elements_by_xpath("//a[@href]")
    for article in articles:
        if "/literature/" in article.get_attribute("href"):
            article.click()
            wait.until(presence_of_element_located((By.XPATH, "//a[@href]")))
            children = driver.find_elements_by_xpath("//a[@href]")
            for child in children:
                if child.text == "HTML":
                    child_articles.append(child.get_attribute("href"))
                    break

print(child_articles)