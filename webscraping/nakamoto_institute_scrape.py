from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

#This example requires Selenium WebDriver 3.13 or newer
with webdriver.Firefox() as driver:
    wait = WebDriverWait(driver, 10)
    driver.get("https://nakamotoinstitute.org/literature/")

    articles = driver.find_elements_by_xpath("//a[@href]")
    for article in articles:
        print(article.get_attribute("href"))
        #driver.find_element(By.NAME, "a").click()
    # first_result = wait.until(presence_of_element_located((By.CLASS_NAME, "col-sm-9")))
    # print(first_result)