import requests
from bs4 import BeautifulSoup
import re

OFFERS_URL = "https://www.lowendtalk.com/categories/offers"
MINIMUM_VIEWS = 600

r = requests.get(OFFERS_URL)

soup = BeautifulSoup(r.text, 'html.parser')
topics = soup.findAll('div', {'class': "ItemContent Discussion"})

for topic in topics:
    view_count_str = topic.contents[3].find(class_="ViewCount").span.string
    view_count = int(view_count_str.replace('K', '000'))
    if view_count > MINIMUM_VIEWS:
    # if 'K' in topic.contents[3].find(class_="ViewCount").span.string:
        print topic.contents[1].a.string
        link = topic.contents[1].a['href']
        print link
        m = re.search('lowendtalk\.com\/discussion\/([^\/]*)', link)
        print "ID: " + m.group(1)
        print view_count_str + " views"
        print
