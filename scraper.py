import urllib
import httplib2
import sys
from bs4 import BeautifulSoup
    #BeautifulSoup/Soupstrainer help to organise the raw html
import re
    #regular expressions
from selenium import webdriver
    #simulate a web broswer (for redirecting)   
from urllib.request import urlopen
import pandas as pd

BASE_URL = "https://handbook.unimelb.edu.au/2017/"

def main(argv):
    path = argv[0]
    df = pd.DataFrame()
    undergrad_subjects = pd.read_csv(path)

    for link in undergrad_subjects["LinkAppend"]:
        row_num = len(df)

        URL = BASE_URL + link
        print(URL)
        df.set_value(row_num, "subject_link", URL)
        Client = urlopen(URL)
        page_html = Client.read()
        Client.close()
        page_soup = BeautifulSoup(page_html, "html.parser")

        heading = page_soup.findAll("div", {"class", "header--course-and-subject__inner"})
        assert len(heading) == 1

        subject_title = heading[0].findAll("h1")
        assert len(subject_title) == 1
        subject_title = subject_title[0].get_text()
        print("Title", ":", subject_title)
        df.set_value(row_num, "subject_name", subject_title)

        points = heading[0].findAll("span", {"class":None})
        points = points[0].get_text()
        df.set_value(row_num, "points", points)
        print("Points", ":", points)


        tables = page_soup.findAll("table")
        assert len(tables) == 1
        table_rows = tables[0].findAll('tr')
        for row in table_rows:
            thead = row.findAll('th')[0]

            tds = row.findAll('td')
            new_string = ""
            for data in tds:
                if new_string != "":
                    new_string += "|||"
                new_string += data.get_text()
            print(thead.text, ":", new_string)   
            df.set_value(row_num, thead.text.strip(), new_string.strip())

        print()
        URL = BASE_URL + link + "/eligibility-and-requirements"
        df.set_value(row_num, "ear_link", URL)
        Client = urlopen(URL)
        page_html = Client.read()
        Client.close()
        page_soup = BeautifulSoup(page_html, "html.parser")

        requirements = page_soup.findAll("div", {"class":"box"})[1]
        for html_text in str(requirements).split("<h3>")[1:]:
            html_text = "<h3>" + html_text
            html_text = BeautifulSoup(html_text, "html.parser")
            key = html_text.findAll("h3")
            assert len(key) == 1
            key = key[0].get_text()

            values = html_text.findAll("tr")
            value_string = ""
            for Info in values:
                code = Info.findAll("td")
                if not code:
                    continue
                code = code[0].get_text()
                if value_string != "":
                    value_string += "|||"
                value_string += code
            print(key, ":", value_string)
            df.set_value(row_num, key.strip(), value_string.strip())

        print()
        print()
        print()
        df.to_csv("subject_data.csv", sep = ",")

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except IndexError:
        print("Give csv to read as command line argument")
        sys.exit(1)
