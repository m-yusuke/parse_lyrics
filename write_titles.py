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

    for table in tables:
        rows = table.findAll("tr")
        if re.search("(Famison|SideM|iDOLM@STER\.KR|Xenoglossia|Radio|Cover)", str(rows[0])) is None:
            use_tables.append(table)

    titles = []
    for use_table in use_tables:
        rows = use_table.findAll("tr")
        for row in rows:
            temp = row.find(['td', 'th']).text
            if re.search("(Title \(English\)|List of)", str(temp)) is not None or str(temp) == '':
                continue
            print(temp)
            titles.append(temp)

    with open("titles.txt", 'w') as f:
        for title in titles:
            f.write(title + '\n')

