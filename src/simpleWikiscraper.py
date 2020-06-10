# Aim: scrape Wikipedia webpage

from bs4 import BeautifulSoup
import requests

# specify webpage to scrape and
# get source code from webpage
url = "https://en.wikipedia.org/wiki/Category:Films_about_viral_outbreaks"
response = requests.get(url)

# convert source code to readable object
page = BeautifulSoup(response.text, 'html.parser')

# find film titles
films = page.find('div', class_ = 'mw-category')
list_of_titles = films.findAll('li')
for title in list_of_titles:
    print(title.text) # show film titles

