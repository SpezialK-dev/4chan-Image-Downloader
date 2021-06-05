#!/usr/bin/python3
import os
import requests
from bs4 import BeautifulSoup  # needed for html analysis


def analyse(link):
    if link.find("/"):
        name1 = (link.split("/", 3)[3])
        # split two times to just get the board
        name2 = (name1.split("/", 1)[0])
        return name2


# creating a new folder
def folder():
    # the download path need top be changed to you liking
    path = "downloads"
    try:
        os.makedirs(path)
    except OSError:
        print("Failed to create a new folder\nMaybe because it already exists?")
    return path


# getting the actual links to download from
def scraper(link):
    # pretending to be a browser
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    html = requests.get(link, headers=header)
    # because we can't find anything in a response sadly so I have to do this bs
    html2 = html.text
    return html2


def titelfunk(link):
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    html = requests.get(link, headers=header)
    html2 = html.text
    soup = BeautifulSoup(html2, "html.parser")
    error = soup.find_all("title")
    try:
        print(error[0].text)
    except IndexError:
        print("returning jpg")
        return ".jpg"
    else:
        return ".png"


def links(response, board, path):
    soup = BeautifulSoup(response, "html.parser")
    img_tags = soup.find_all("img")
    toFind = ("/" + board + "/")
    n = 1
    length = len(img_tags)
    while length > n:
        rep = (img_tags[n])
        res = repr(rep)
        n = n + 1
        spl = (res.split('"', 9)[7])
        numb = (spl.split(toFind, 1)[1])
        numb2 = (numb.split("s", 1)[0])
        imageFormat = ".jpg"
        name3 = (str(numb2) + imageFormat)
        link = ("https://i.4cdn.org/" + board + "/" + name3)
        imageFormat = titelfunk(link)
        name3 = (str(numb2) + imageFormat)
        print(name3)
        link = ("https://i.4cdn.org/" + board + "/" + name3)
        try:
            download(link, numb2, path, name3)
        except ConnectionError:
            link = ("https://i.4cdn.org/" + board + "/" + name3)
            try:
                download(link, numb2, path, name3)
            except ConnectionError:
                print("Unsupported file type")


def download(link, name, path, name2):
    # making the full  name
    fullname = os.path.join(path, name2)
    # the actual download
    r = requests.get(link)
    try:
        open(fullname, 'wb').write(r.content)
    except OSError:
        print("Failed to download", name, " !")
    else:
        print("Success in downloading ", name, " !")


# executing the program
Link = input("Your link here:")
Path = folder()
Board = analyse(Link)
Html = scraper(Link)
links(Html, Board, Path)
