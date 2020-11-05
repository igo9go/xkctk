#!/usr/bin/env python
# -*- coding: utf-8 -*-

URL = 'http://xkctk.hangzhou.gov.cn/tzgg/2019726/1564127010933_1.html'

import requests
from db.mongodb import MongoCollection
import os

data_collection = MongoCollection('data')

article_collection = MongoCollection('articles')

data = article_collection.get(geren_pdf={'$ne': ''})

for item in data:
    url = item['geren_pdf']
    path = os.path.dirname(__file__) + '/pdf/' + item['title'] + '.pdf'
    r = requests.get(url)
    f = open(path, "wb")
    f.write(r.content)
    f.close()
    print(url)

print('ok')
exit()
r = requests.get(URL)
text = r.text.encode(r.encoding).decode(r.apparent_encoding)

from bs4 import BeautifulSoup

soup = BeautifulSoup(text, 'lxml')

print((soup.find('div', 'details').find_all('a')))
price = 108
print("the book's price is %s" % price)

for n in range(1, 20):
    print(n)
