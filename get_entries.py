"""
Builds CSV of Subjects with urls
"""
import csv

from urllib.request import urlopen
from bs4 import BeautifulSoup

BASE_URL = 'https://handbook.unimelb.edu.au/subjects/undergraduate'
APPEND_BASE = "?page="

def main():
    with open('UnderGraduateSubjects.csv', 'w') as output:
        outputcsv = csv.writer(output)
        outputcsv.writerow(["LinkAppend"])

        page_num = 1

        while True:
            print(".", end='', flush=True)
            page = BeautifulSoup(urlopen(BASE_URL + APPEND_BASE + str(page_num)), 'html.parser')
            list_path = page.find_all('li', {"class": "search-results__accordion-item"})

            # If we can no longer find any subjects, end the loop
            if not list_path:
                break

            write_urls(list_path, outputcsv)

            page_num += 1
        print("\nScraping done.")
        output.close()


def write_urls(list_path, outputcsv):
    """
    Writes a page of url suffixes
    """
    for subject in list_path:
        outputcsv.writerow([subject.a.get('href')])

if __name__ == '__main__':
    main()
