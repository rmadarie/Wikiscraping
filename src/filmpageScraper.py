# Aim: collect source code from wiki film pages

from bs4 import BeautifulSoup
import requests
import time

# specify start url and get source code from start url
url = "https://en.wikipedia.org/wiki/Category:Films_about_viral_outbreaks"
response = requests.get(url)

# convert source code to readable format
page = BeautifulSoup(response.text, 'html.parser')

# lists of url endings and full urls of movie pages
initiallist = []
urllist = []

# extract and list url endings
films = page.find('div', class_ = 'mw-category')
for tag in films.findAll('a'):
    href = tag.attrs.get("href")
    initiallist.append(href)

# list full urls
for item in initiallist:
    fullurl = "https://en.wikipedia.org" + item
    urllist.append(fullurl)

# get source code from each url listed. We'll parse the source code later.
for url in urllist:
    try:
        response = requests.get(url) # get source code
        time.sleep(1) # pause 1 second to be gentle to the website
        source = response.text
        endofurl = url.rpartition("/")[-1] # set name of to-be-file
        filetitle = endofurl.replace(":", "_") # windows doesn't do : in filenames
        with open(filetitle + ".html", 'w', encoding='utf-8') as sourcecode:
            sourcecode.write(source) # write source code to file
    except Exception as e: # show errors
        print(url)
        print(e)

print(urllist)
