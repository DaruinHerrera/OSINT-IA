from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options # Importar Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import logging
import random

# Setting logg
logging.basicConfig(filename='scraping.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
# Setting driver
def setting_driver(driver_path, user_agent=None):
    options = Options()
    options.add_argument("--headless=new")

    if user_agent:  # add the User-Agent
        options.add_argument(f"user-agent={user_agent}")
        logging.info(f"Usando User-Agent: {user_agent}")
    else:
        logging.warning("User-Agent no setting.")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_and_save(url, driver_path, output_file):
    # start browser
    user_agents_lista = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
        # ... more User-Agents
    ]
    user_agent_random = random.choice(user_agents_lista)

    driver = setting_driver(driver_path, user_agent_random)
    try:
        # move site
        driver.get(url)
        logging.info(f"Get to URL: {url}")
        
        # sleep
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
            )
        except TimeoutException:
            logging.error("Timeout to enter the article.")
            return

        # to save
        data = []
        articles = driver.find_elements(By.TAG_NAME, "article")
        logging.info(f"Found {len(articles)} articles.")
        
        for article in articles:
            try:
                # get data
                title = article.find_element(By.TAG_NAME, "h2").text
                date = article.find_element(By.CSS_SELECTOR, ".updated").text
                content = article.find_element(By.CSS_SELECTOR, ".entry-content").text
                link = article.find_element(By.TAG_NAME, "a").get_attribute("href")
                data.append([title, link, date, content])
                logging.info(f"Articles proccesed: {title}")
            except NoSuchElementException as e:
                logging.warning(f"Item not found in an article: {e}")
            except Exception as e:
                logging.error(f"Error processing an article: {e}")

        # scroll
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(3):  # Scroll 3 veces
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)

        # save data
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'link','date', 'content'])
            writer.writerows(data)
        logging.info(f"Save data in {output_file}")
        
    except Exception as e:
        logging.error(f"General error during scraping: {e}")
    finally:
        # close chromedriver
        driver.quit()

# values
url = "https://krebsonsecurity.com/"
driver_path = "drivers\\chromedriver-win64\\chromedriver.exe"
output_file = "./data/results.csv"

# run function
scrape_and_save(url, driver_path, output_file)
