from urllib.parse import urlparse
from urllib.request import urlopen

import re
from bs4 import BeautifulSoup


def getTypeLinks(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    netloc = urlparse(url).netloc
    typelinks = []
    try:
        lables = bsObj.find("div", {"class": "photo-set"}).findAll("a", href=re.compile(
            "http://" + netloc + "(/([\\w]|[\\d])+)+\.html$"))
    except AttributeError as e:
        print(e)
        lables = None
    if lables is not None and len(lables) > 0:
        for lable in lables:
            if lable.attrs['href'] is not None:
                typelinks.append(lable.attrs['href'])
    return typelinks
