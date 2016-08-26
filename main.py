#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import json
import datetime as dt

OFFERS_URL = "https://www.lowendtalk.com/categories/offers"
MINIMUM_VIEWS = 600

r = requests.get(OFFERS_URL)

soup = BeautifulSoup(r.text, 'html.parser')
topics = soup.findAll('div', {'class': "ItemContent Discussion"})

text_body = ""
html_body = "<ul>"

for topic in topics:
    view_count_str = topic.contents[3].find(class_="ViewCount").span.string
    view_count = int(view_count_str.replace('K', '000'))
    if view_count > MINIMUM_VIEWS:
    # if 'K' in topic.contents[3].find(class_="ViewCount").span.string:
        title = topic.contents[1].a.string.encode('utf-8')
        link = topic.contents[1].a['href']
        m = re.search('lowendtalk\.com\/discussion\/([^\/]*)', link)
        topic_id = m.group(1)
        view_count_str2 = view_count_str + " views"
        text_body += "{0}\n{1} - {2}\n\n".format(title, link, view_count_str2)
        html_body += """
            <li>
                <h2>{0}</h2>
                <a href="{1}">Link</a> - {2}
            </li>
        """
        html_body = html_body.format(title, link, view_count_str2)

html_body += "</ul>"

header = "<h1>Hi!</h1>"

RECIPIENT = 'benadriansarmiento@gmail.com'
with open('mailgun-creds.json') as data_file:
    data = json.load(data_file)

    today = dt.datetime.today().strftime("%m/%d/%Y")

    request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(data['sandbox'])
    request = requests.post(request_url, auth=('api', data['key']), data={
        'from': 'LET Offers <let.offers.sandbox@mailgun.com>',
        'to': RECIPIENT,
        'subject': 'LET Offers - ' + today,
        'text': '{0}\n\n{1}'.format(header, text_body),
        'html': '<h1>{0}</h1><div>{1}</div>'.format(header, html_body)
    })

    print 'Status: {0}'.format(request.status_code)
    print 'Body:   {0}'.format(request.text)
