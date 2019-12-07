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


def get_lyrics(song_url):
    req_song = requests.get(song_url)
    song_html = req_song.content
    song_soup = BeautifulSoup(song_html, "html5lib")
    if re.search("iM@S Cover Data", str(song_soup)):
        return None
    lyrics_sec = song_soup.find(class_="wikitable")
    rows = lyrics_sec.find_all("tr")
    lyrics = ""
    for row in rows:
        cell = row.find('td')
        if cell is not None:
            lyrics += cell.text

    return lyrics


if __name__ == '__main__':
    route_url = "https://www.project-imas.com"
    titles_url = route_url + "/wiki/Category:Songs"
    req_title = requests.get(titles_url)
    with open("titles.txt", 'r') as f:
        req_titles = f.readlines()

    titleinfos = []
    while True:
        print(titles_url)
        title_html = req_title.content
        title_soup = BeautifulSoup(title_html, "html5lib")
        groups = title_soup.find_all(class_="mw-category-group")

        titleinfos += get_titleinfos(groups)

        content = title_soup.find(id="mw-pages")
        seeks = content.find_all("a", recursive=False)
        if seeks[-1].text == "next page":
            titles_url = route_url + seeks[-1].attrs['href']
            req_title = requests.get(titles_url)
        else:
            break
    
    for i in titleinfos:
        print(f"title = {i['title']}, url = {i['url']}")
    song_url = route_url + titleinfos[0]["url"]
    #print(song_url)
    
    #lyrics = get_lyrics(song_url)
    #print(lyrics)
