import random
from urllib.request import urlopen
import re
import datetime
from bs4 import BeautifulSoup
def getLinks(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    labels = bsObj.find("div", {"id":"slider_relations"}).findAll("a", href=re.compile("^http://baike.baidu\.com/subview(/[\\d]+)+\.htm"))
    links = []
    for label in labels:
        links.append(label.attrs['href'])
    return links
if __name__ == "__main__":

    random.seed(datetime.datetime.now())
    links = getLinks("http://baike.baidu.com/subview/2632/19244814.htm")
    for i in range(1,6):
        if len(links) > 0:
            newURL = links[random.randint(0, len(links)-1)]
            print(newURL)
            links = getLinks(newURL)
