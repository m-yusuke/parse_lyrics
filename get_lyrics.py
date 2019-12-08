#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import re
import pprint
import time
import json
import random


def get_lyrics(songinfo):
    req_song = requests.get(songinfo["url"])
    html = req_song.content
    soup = BeautifulSoup(html, "html5lib")
    if re.search("iM@S Cover Data", str(soup)):
        return None
    lyrics_sec = soup.find(class_="wikitable")
    rows = lyrics_sec.find_all("tr")
    lyrics = ""
    for row in rows:
        cell = row.find('td')
        if cell is not None:
            lyrics += cell.text

    songinfo["lyrics"] = lyrics
    songinfo.pop("url")
    return songinfo


def get_songinfos(url, route_url):
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
                    "url": "",
                    "lyrics": ""
                    }
            cells = row.find_all('td')
            if len(cells) > 0 and re.search("page does not exist", str(cells)) is None:
                songinfo["song_title"] = cells[1].text
                songinfo["url"] = route_url + cells[1].find("a").attrs['href']
                songinfos[song_index] = songinfo
                song_index += 1

    return songinfos



if __name__ == '__main__':
    route_url = "https://www.project-imas.com"
    songlist_url = route_url + "/wiki/Official_Song_Listing"

    songinfos = get_songinfos(songlist_url, route_url)
    testinfo = {
            0: {
                "song_title": "2nd SIDE",
                "title": "THE IDOLM@STER CINDERELLA GIRLS",
                "url": "https://www.project-imas.com/wiki/2nd_SIDE",
                "lyrics": ""
                },
            1: {
                "song_title": "亜麻色の髪の乙女",
                "title": "THE IDOLM@STER CINDERELLA GIRLS",
                "url": "https://www.project-imas.com/wiki/Amairo_no_Kami_no_Otome",
                "lyrics": ""
                }
            }
    num_of_song = len(songinfos)
    print(f"number of song is {num_of_song}.")
    for key, songinfo in songinfos.items():
        print(f"processing {songinfo['song_title']}")
        testinfo[key] = get_lyrics(songinfo)
        print(f"done {key + 1}/{num_of_song}.")
        randsleep = random.random() * 10
        print(f"sleeping {randsleep} seconds....")
        time.sleep(randsleep)

    with open('./lyrics/imas.json', 'w') as f:
        result = json.dump(testinfo, f, ensure_ascii=False, indent=4)
