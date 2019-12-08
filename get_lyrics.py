#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import re
import pprint


def get_lyrics(songinfo):
    songattr = {
            "title": "",
            "song_title": "",
            "lyrics": ""
            }
    req_song = requests.get(song_url)
    song_html = req_song.content
    song_soup = BeautifulSoup(song_html, "html5lib")
    lyrics_sec = song_soup.find(class_="wikitable")
    rows = lyrics_sec.find_all("tr")
    lyrics = ""
    for row in rows:
        cell = row.find('td')
        if cell is not None:
            lyrics += cell.text

    songattr["lyrics"] = lyrics

    return songattr


def get_songinfos(url):
    req_url = requests.get(url)
    html = req_url.content
    songinfos = {}
    titles = [
            "THE IDOLM@STER",
            "THE IDOLM@STER CINDERELLA GIRLS",
            "THE IDOLM@STER MILLION LIVE!",
            "THE IDOLM@STER SideM",
            "THE IDOLM@STER SHINYCOLORS"
            ]
    soup = BeautifulSoup(html, "html5lib")
    tables = soup.find_all("table")

    song_index = 0
    for table in tables:
        if re.search("(Famison|SideM|iDOLM@STER\.KR|Xenoglossia|Radio|Cover)", str(table)):
            continue
        elif re.search("Cinderella Girls", str(table)):
            title = titles[1]
        elif re.search("Million Live", str(table)):
            title = titles[2]
        elif re.search("Shiny Colors", str(table)):
            title = titles[4]
        else:
            title = titles[0]

        tbody = table.find("tbody")
        rows = tbody.find_all('tr')
        for row in rows:
            songinfo = {
                    "song_title": "",
                    "title": title,
                    "url": ""
                    }
            cells = row.find_all('td')
            if len(cells) > 0 and re.search("page does not exist", str(cells)) is None:
                songinfo["song_title"] = cells[1].text
                songinfo["url"] = cells[1].find("a").attrs['href']
                songinfos[song_index] = songinfo
                song_index += 1

    return songinfos



if __name__ == '__main__':
    route_url = "https://www.project-imas.com"
    songlist_url = route_url + "/wiki/Official_Song_Listing"

    songinfos = get_songinfos(songlist_url)

    pprint.pprint(songinfos)
    
    #lyrics = get_songinfo(song_url)
    #print(lyrics)
