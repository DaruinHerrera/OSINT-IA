from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def scrape_and_save(url, driver_path, output_file):
    # Iniciar el navegador
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    
    try:
        # Navegar al sitio web
        driver.get(url)

        # Esperar hasta que los artículos estén presentes
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )

        # Lista para almacenar los datos extraídos
        data = []

        # Extraer todos los artículos de la página
        articles = driver.find_elements(By.TAG_NAME, "article")
        for article in articles:
            try:
                # Extraer título y enlace de cada artículo
                title = article.find_element(By.TAG_NAME, "h2").text
                link = article.find_element(By.TAG_NAME, "a").get_attribute("href")
                data.append([title, link])
            except Exception as e:
                print(f"Error al procesar un artículo: {e}")

        # Simular un scroll para cargar más contenido si es necesario
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(3):  # Scroll 3 veces
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)

        # Guardar los datos en un archivo CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Título', 'Enlace'])
            writer.writerows(data)
        
        print(f"Datos guardados en {output_file}")

    finally:
        # Cerrar el navegador
        driver.quit()

# Parámetros de entrada
url = "https://krebsonsecurity.com/"  # Reemplaza con el sitio web deseado
driver_path = "D:\\Development\\drivers\\chromedriver-win64\\chromedriver.exe"  # Ruta al ejecutable de ChromeDriver
output_file = "resultados.csv"  # Nombre del archivo de salida

# Ejecutar la función
scrape_and_save(url, driver_path, output_file)
