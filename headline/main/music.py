from bs4 import BeautifulSoup
from requests import get

from ..models import Music


def saveMusicPost(title, link, source):
    music = Music(
        title=title,
        link=link,
        source=source
    )
    music.save()


# Scrape NotJustOK
def notjustok():
    url = 'http://notjustok.com/'
    html = get(url).text

    soup = BeautifulSoup(html, 'html.parser')
    _posts = soup.findAll(class_="status-publish")
    posts = [post.find(class_="title") for post in _posts]
    data = [saveMusicPost(post.find("a").text, post.find("a").get("href"), 'NotJustOk') for post in posts if post]
    return {
        "data": data,
        "source": "NotJustOK"
    }


# Scrape TooXClusive
def tooXClusive():
    url = 'http://notjustok.com/'
    html = get(url).text

    soup = BeautifulSoup(html, 'html.parser')
    _posts = soup.find(id="loop").findAll(class_="status-publish")
    posts = [saveMusicPost(i.find("h2").find("a").text, i.find("h2").find("a").get("href"), 'TooXClusive') for i in _posts if i]
    return {
        "posts": posts,
        "source": "TooXClusive"
    }
