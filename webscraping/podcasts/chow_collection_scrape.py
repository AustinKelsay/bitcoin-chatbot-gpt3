import json
import time
from gpt3.generate_training_data import generate
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located, presence_of_element_located, element_to_be_clickable

# articles that arent podcast transcripts
article_blacklist = ["A Private Collector’s Guide to Art Collecting", "An introduction to /r/privatestudyrooms", 
'Step-by-step: Documenting Anthony Gunin’s creation of The Most Holy Theotokos “Glykophilousa” icon', "Legacy",
"Thoughts on Art Collecting", "Christ Pantocrator mosaic by Yury Yarin"]
article_links = []
data = []

def scrape():
    with webdriver.Firefox() as driver:
        wait = WebDriverWait(driver, 10)
        driver.get("https://chowcollection.medium.com")
        # Wait for show more button
        try:
            while driver.find_element_by_xpath("// button[contains(text(),'Show more')]"):
                driver.find_element_by_xpath("// button[contains(text(),'Show more')]").click()
                time.sleep(10)
        except:
            wait.until(presence_of_all_elements_located((By.XPATH, "//a[@class='eh bw']")))
            articles = driver.find_elements_by_xpath("//a[@class='eh bw']")
            for article in articles:
                article_links.append(article.get_attribute("href"))

            for link in article_links:
                    driver.get(link)
                    # Waiting for footer to render which means all of the text has rendered
                    wait.until(presence_of_all_elements_located((By.XPATH, "//p")))
                    text = driver.find_elements_by_xpath("//p")
                    title = driver.find_element_by_xpath("//h1")
                    podcast_link = driver.find_element_by_xpath("//a[contains(text(), 'http')]")
                    print(podcast_link.get_attribute("href"))
                    if title.text not in article_blacklist:
                        # Trigger bitcoin chatbot training data generation
                        generate(text)
                        for section in text:
                            try:
                                j = {
                                    "link": podcast_link.get_attribute("href"),
                                    "title": title.text,
                                    "text": section.text
                                }
                                data.append(j)
                            except:
                                print("Error")

    with open('./datasets/knowledge_datasets/bitcoin_knowledge.json', 'w') as outfile:
        for obj in data:
            json.dump(obj, outfile)
            outfile.write('\n')