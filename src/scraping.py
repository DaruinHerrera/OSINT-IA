import requests
from bs4 import BeautifulSoup

url = "https://krebsonsecurity.com/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')

    for article in articles:
        title = article.find('h2').text
        link = article.find('a')['href']
        print(f"Título: {title}, Enlace: {link}")
else:
    print(f"Error al acceder al sitio: {response.status_code}")
