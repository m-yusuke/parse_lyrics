#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import re


def get_titleinfos(groups):
    titleinfos = []
    for group in groups:
        group_titles = group.find_all("li")
        for group_title in group_titles:
            a = group_title.find('a')
            tmp = {"title": group_title.text, "url": a.attrs['href']}
            titleinfos.append(tmp)

    return titleinfos


if __name__ == '__main__':
    route_url = "https://www.project-imas.com"
    rr = requests.get(route_url + "/wiki/Category:Songs")
    with open("titles.txt", 'r') as f:
        req_titles = f.readlines()

    html = rr.content
    soup = BeautifulSoup(html, "html5lib")
    groups = soup.find_all(class_="mw-category-group")
    
    titleinfos = get_titleinfos(groups)
    url = route_url + titleinfos[0]["url"]
    print(url)
