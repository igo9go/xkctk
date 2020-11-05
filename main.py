#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from utils.base import hash_string
from db.mongodb import MongoCollection
from parse_pdf import parse
import os

URL = 'http://xkctk.hangzhou.gov.cn/tzgg/'
page_url = 'http://xkctk.hangzhou.gov.cn/tzgg/index_%s.html'

article_collection = MongoCollection('articles')


def get_html_content(url):
    r = requests.get(url)
    data = r.text.encode(r.encoding).decode(r.apparent_encoding)
    return data


def get_all_list():
    html_doc = get_html_content(URL)
    soup = BeautifulSoup(html_doc, 'lxml')
    # 获取首页数据
    # get_list(URL)
    # 获取分页数据
    all_page = int(soup.find('div', 'pageturn2').find('span').get_text())
    if all_page > 0:
        for n in range(2, all_page + 1):
            url = page_url % n
            get_list(url)
            print(n)


def get_list(url):
    html_doc = get_html_content(url)
    soup = BeautifulSoup(html_doc, 'lxml')
    contents = soup.find_all("a", "text")

    for item in contents:
        article = {}
        url = item.get('href')
        article['title'] = item.get_text()
        article['url'] = url
        article['id'] = hash_string(url)
        content = get_contents(url)
        article.update(content)
        article_collection.insert('id', article)


def get_contents(url):
    html_doc = get_html_content(url)
    soup = BeautifulSoup(html_doc, 'lxml')
    title = soup.h1.string.strip()
    time = soup.find('div', 'tilinfo').get_text().strip()
    # content = soup.find('div', 'details'),
    pdf_url = []
    if title.find('结果公告') >= 0 or title.find('个人阶梯摇号结果') >= 0:
        # 有公告pdf
        pdfs = soup.find('div', 'details').find_all('a')
        for pdf in pdfs:
            pdf_url.append(pdf.get('href'))

    result = {
        'title': title,
        'time': time,
        'content': html_doc,
        'geren_pdf': pdf_url[0] if len(pdf_url) > 0 else '',
        'qiye_pdf': pdf_url[1] if len(pdf_url) > 1 else ''
    }
    return result


def save_pdf(pdf_url, pdf_name):
    r = requests.get(pdf_url)
    path = os.path.dirname(__file__) + '/pdf/' + pdf_name + '.pdf'
    f = open(path, "wb")
    f.write(r.content)
    f.close()


def get_bianhao_from_pdf():
    data = article_collection.get(geren_pdf={'$ne': ''})
    for item in data:
        url = item['geren_pdf']
        path = os.path.dirname(__file__) + '/pdf/' + item['title'] + '.pdf'
        if not item.has_key['is_save'] or item['is_save'] != 1:
            save_pdf(url, path)
            item['is_save'] = 1

        if not item.has_key['is_parse'] or item['is_parse'] != 1:
            parse(path)
            item['is_parse'] = 1
        article_collection.update_or_insert('id', item)


if __name__ == '__main__':
    get_all_list()
    get_bianhao_from_pdf()
    print('ok')
