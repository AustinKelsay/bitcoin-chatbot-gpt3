from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    print(body)
    soup = BeautifulSoup(body, 'lxml')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return [t.strip() for t in visible_texts if t.strip() != '']

html = urllib.request.urlopen('https://www.gwern.net/Bitcoin-is-Worse-is-Better').read()
print(text_from_html(html))