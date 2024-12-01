from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def scrape_and_save(url, driver_path, output_file):
    # start browser
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    
    try:
        # move site
        driver.get(url)

        # sleep
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )

        # to save
        data = []

        # get articles to web site
        articles = driver.find_elements(By.TAG_NAME, "article")
        for article in articles:
            try:
                # get data
                title = article.find_element(By.TAG_NAME, "h2").text
                date = article.find_element(By.CSS_SELECTOR, ".updated").text
                comments = article.find_element(By.CSS_SELECTOR, ".link-comments").text
                link = article.find_element(By.TAG_NAME, "a").get_attribute("href")
                data.append([title, link, date, comments])
            except Exception as e:
                print(f"Error to process page: {e}")

        # scroll
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(3):  # Scroll 3 veces
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)

        # save data
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Título', 'Enlace','date', 'comments'])
            writer.writerows(data)
        
        print(f"Datos guardados en {output_file}")

    finally:
        # close chromedriver
        driver.quit()

# values
url = "https://krebsonsecurity.com/"
driver_path = "D:\\Development\\drivers\\chromedriver-win64\\chromedriver.exe"
output_file = "./data/resultados.csv"

# run function
scrape_and_save(url, driver_path, output_file)
