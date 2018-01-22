from urllib.request import urlopen

import re
from bs4 import BeautifulSoup


def getContentLinks(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    address = getAddressSplit(url)
    contentLinks = []
    try:
        labels = bsObj.find("div", {"class": "page-tag oh"}).findAll("a", href=re.compile(".+\.html$"))
    except AttributeError as e:
        print(e)
        labels = None
    if labels is not None and len(labels) > 0:
        for label in labels:
            if label.attrs['href'] is not None:
                contentLinks.append(address + label.attrs['href'])
    return contentLinks


def getAddressSplit(url):
    paths = url.split("/")
    i = 0
    path = ""
    for i in range(0, len(paths) - 1):
        path.join(paths[i])
    return path
