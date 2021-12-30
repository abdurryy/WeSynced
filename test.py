import requests
from bs4 import BeautifulSoup

r = requests.get('https://s2dfree.de/MczozMjoiNjIxOXx8ODUuMjI2LjE4MS4yMDZ8fDE2NDA4NzM5NzAiOw.html')

soup = BeautifulSoup(r.text, 'html.parser')

print(soap.prettify())