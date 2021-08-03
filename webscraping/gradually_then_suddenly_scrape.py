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
    driver.get("https://unchained-capital.com/blog/category/gradually-then-suddenly/")

    articles = driver.find_elements_by_xpath("//a[@href]")
    seen = set()
    for article in articles:
        if article.get_attribute("href") != "https://unchained-capital.com/blog/" and "/blog/" in article.get_attribute("href") and "/author/" not in article.get_attribute("href") and "/category/" not in article.get_attribute("href"):
            if article.get_attribute("href") not in seen:
                seen.add(article.get_attribute("href"))
    
    # Now go to the next page
    driver.find_element_by_xpath("//a[@class='next page-numbers']").click()
    articles = driver.find_elements_by_xpath("//a[@href]")
    for article in articles:
        if article.get_attribute("href") != "https://unchained-capital.com/blog/" and "/blog/" in article.get_attribute("href") and "/author/" not in article.get_attribute("href") and "/category/" not in article.get_attribute("href"):
            if article.get_attribute("href") not in seen:
                seen.add(article.get_attribute("href"))

    for item in seen:
        driver.get(item)
        driver.implicitly_wait(4)
        title = driver.find_element_by_xpath("//h1").text
        content = driver.find_elements_by_xpath("//p")

        for con in content:
            if con.text != "":
                j = {
                    "prompt": title,
                    "content": con.text
                }
                data.append(j)

with open('gradually_then_suddenly.json', 'w') as outfile:    
    for obj in data:
        json.dump(obj, outfile)
        outfile.write('\n')

