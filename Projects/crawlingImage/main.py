import random
from urllib.error import HTTPError
import datetime
from Projects.crawlingImage.getImageLinks import getImageLinks, getNextPage, getTitle, getImage

if __name__ == '__main__':
    random.seed(datetime.datetime.now())
    typeLinks = []
    contentLinks = []
    visitedPage = set()
    Images = {}
    path = ""
    url = ""
    for i in range(0, 30):
        print(url)
        try:
            getImageLinks(url, path)
        except HTTPError as e:
            print(e)
        finally:
            url = getNextPage(url)
