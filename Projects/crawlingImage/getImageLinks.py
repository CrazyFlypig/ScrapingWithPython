from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import urlopen, urlretrieve

import re

import os
from bs4 import BeautifulSoup


def getImageLinks(url, path):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")

    try:
        labels = bsObj.find("div", {"id": "ks_xp"}).findAll("img", src=re.compile("^http://.+jpg$"))
        if labels is None or len(labels) <= 0:
            labels = bsObj.find("div", {"id": "ks_xp"}).findAll("a", src=re.compile("^http://.+ jpg$"))
        title = getTitle(bsObj)
        dir = path + "\\" + title
        if os.path.exists(dir):
            print("Dir is exists")
        else:
            os.mkdir(dir)
            print(dir + " mkdir successful!")
        i = 0
        for label in labels:
            src = label.attrs['src']
            urlretrieve(src, dir + "\%d.jpg" % i)
            print(dir + "\%d.jpg download successful!" % i)
            i = i + 1
    except AttributeError or HTTPError as e:
        print(e)


def getNextPage(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    try:
        nextPage = bsObj.find("div", {"class": "pagea"}).find("a", href=re.compile("^/.+\\.html$"))
    except AttributeError as e:
        print(e)
    url = getAddress(url) + nextPage.attrs['href']
    return url


def getAddress(url):
    netloc = urlparse(url).netloc
    return "http://" + netloc


def getTitle(bsObj):
    try:
        title = str(bsObj.find("div", {"class": "title"}).get_text())
    except AttributeError as e:
        print(e)
    if title.find("[") >= 0:
        title = title.split("[")[0]
    if title.find("(") >= 0:
        title = title.split("(")[0]
    return title


def getImage(url, path):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    try:
        labels = bsObj.find("div", {"id": "gridMulti"}).findAll("img", src=re.compile("^https://.+tinysrgb$"))
        if labels is None or len(labels) <= 0:
            labels = bsObj.find("div", {"id": "ks_xp"}).findAll("a", src=re.compile("^http://.+gif$"))
        # title = getTitle(bsObj)
        dir = path + "\\zog"
        if os.path.exists(dir):
            print("Dir is exists")
        else:
            os.mkdir(dir)
            print(dir + " mkdir successful!")
        i = 0
        for label in labels:
            src = label.attrs['src']
            urlretrieve(src, dir + "\%d.jpg" % i)
            print(dir + "\%d.jpg download successful!" % i)
            i = i + 1
    except AttributeError or HTTPError as e:
        print(e)
