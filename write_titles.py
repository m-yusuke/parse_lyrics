#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import re


if __name__ == '__main__':
    rr = requests.get("https://www.project-imas.com/wiki/Official_Song_Listing")
    html = rr.content
    soup = BeautifulSoup(html, "html5lib")
    tables = soup.findAll("table")
    use_tables = []

    for i in range(len(tables)):
        rows = tables[i].findAll("tr")
        if re.search("(Famison|SideM|iDOLM@STER\.KR|Xenoglossia|Radio|Cover)", str(rows[0])) is None:
            use_tables.append(tables[i])

    titles = []
    for index in range(len(use_tables)):
        rows = use_tables[index].findAll("tr")
        for i in range(len(rows)):
            temp = rows[i].find(['td', 'th']).text
            if re.search("(Title \(English\)|List of)", str(temp)) is not None or str(temp) == '':
                continue
            print(temp)
            titles.append(temp)

    with open("titles.txt", 'w') as f:
        for title in titles:
            f.write(title + '\n')

