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
    req_title = requests.get(route_url + "/wiki/Category:Songs")
    with open("titles.txt", 'r') as f:
        req_titles = f.readlines()

    title_html = req_title.content
    title_soup = BeautifulSoup(title_html, "html5lib")
    groups = title_soup.find_all(class_="mw-category-group")
    
    titleinfos = get_titleinfos(groups)
    song_url = route_url + titleinfos[0]["url"]
    print(song_url)
    
    lyrics = get_lyrics(song_url)
    print(lyrics)
