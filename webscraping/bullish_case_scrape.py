import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable

#This example requires Selenium WebDriver 3.13 or newer
data =[]

with webdriver.Firefox() as driver:
    wait = WebDriverWait(driver, 2)
    driver.get("https://vijayboyapati.medium.com/the-bullish-case-for-bitcoin-6ecc8bdecc1")
    content = driver.find_elements_by_xpath("//p")

    for c in content:
        try:
            j = {
                "prompt": "The Bullish Case for Bitcoin",
                "completion": c.text
            }
            data.append(j)
        except:
            pass

with open('bullish_case.json', 'w') as outfile:    
    for obj in data:
        json.dump(obj, outfile)
        outfile.write('\n')

