from bs4 import BeautifulSoup
import os
import csv

folder = "C:\\path\\to\\files" # provide path to folder with source codes
csvfilename = "wikifilms_database.csv"

colNames = ['title', 'directors', 'releasedate']
csvDatabase = [colNames]

def cleanDirectors(directors):
    if len(directors) == 1:
        return directors[0]
    elif len(directors) > 1:
        director_concat = ""
        for person in directors:
            director_concat = director_concat + person + "; "
        director_concat = director_concat[:-2]
        return director_concat
    else:
        directors = ""
        return directors

# note: releasedate still looks messy, you'll have to make it prettier afterwards..
def cleanReleasedates(releasedate):
    if releasedate:
        releasedate = releasedate[0].replace("\n", "; ")
        return releasedate
    else:
        releasedate = ""
        return releasedate

def getBoxInfo(source):
    box = source.find("table", class_="infobox vevent")
    rows = box.find_all("tr")
    directors = []
    releasedate = []
    
    title = source.find("h1").text # get film title (from webpage heading, not info box!)
    print(title) # keep track of films processed by parser
    
    for row in rows:
        if "Directed by" in row.text: # get directors
            if row.find_all("a"):
                directorList = row.find_all("a")
                for person in directorList:
                    directors.append(person.text.strip())
            elif row.find_all("li"):
                directorList = row.find_all("li")
                for person in directorList:
                    directors.append(person.text.strip())
            else:
                directors_raw = row.find("td").text.strip()
                directors.append(directors_raw)
        elif " date" in row.text.lower() or "Original release" in row.text: # get release date
            releasedate_raw = row.find("td").text.strip()
            releasedate.append(releasedate_raw)
    
    directors = cleanDirectors(directors) # clean up director list, sometimes messy format
    releasedate = cleanReleasedates(releasedate) # clean up release date as above
    boxInfo = [title, directors, releasedate] # put all collected info from one film in a single list
    csvDatabase.append(boxInfo) # attach film list to list of all films

def parser(folder):
    filmcount = 0
    # loop over html files in folder
    for filename in os.listdir(folder):
        if filename.endswith(".html"):
            with open(folder + "\\" + filename, 'r', encoding='utf-8') as file:
               sourcecode = BeautifulSoup(file, 'html.parser')
               getBoxInfo(sourcecode)
               filmcount += 1
        else:
            continue
    
    print(filmcount)

# write list of lists to csv file
def toCSV(csvfile):
    with open(csvfile, 'w', newline='', encoding='utf-8') as output:
        writer = csv.writer(output, delimiter=',')
        writer.writerows(csvDatabase)

parser(folder) # path to html files that will be parsed
toCSV(csvfilename) # write to csv file

