#!/usr/bin/python3
import os
import requests
from bs4 import BeautifulSoup  # needed for html analysis

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

# the download path need top be changed to you liking
path = "downloads"

try:
    os.makedirs(path)
except OSError:
    print("Failed to create a new folder\nMaybe because it already exists?")


# getting the actual links to download from
def scraper(link):
    # pretending to be a browser
    html = requests.get(link, headers=header)
    # because we can't find anything in a response sadly so I have to do this bs
    return html.text


def titelfunk(link):
    html = requests.get(link, headers=header).text
    soup = BeautifulSoup(html, "html.parser")
    error = soup.find_all("title")
    try:
        print(error[0].text)
    except IndexError:
        print("returning jpg")
        return ".jpg"
    else:
        return ".png"


def links(response):
    soup = BeautifulSoup(response, "html.parser")
    img_tags = soup.find_all("img", attrs={"loading": "lazy"})
    for img in img_tags:
        href = img.parent.attrs["href"]
        name = href.split("/")[-1]
        download("https:"+href, name)


def download(link, name):
    # making the full  name
    fullname = os.path.join(path, name)
    # the actual download
    r = requests.get(link)
    try:
        open(fullname, 'wb').write(r.content)
    except OSError:
        print("Failed to download '{}' !".format(name))
    else:
        print("Success in downloading '{}' !".format(name))


# executing the program
Link = input("Your link here: ")
Html = scraper(Link)
links(Html)
