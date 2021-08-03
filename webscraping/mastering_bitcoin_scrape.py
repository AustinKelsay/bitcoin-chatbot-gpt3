import json
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
    driver.get("https://github.com/bitcoinbook/bitcoinbook/blob/develop/book.asciidoc")