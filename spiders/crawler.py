# -*- coding:utf-8 -*-

import requests
import urllib
from lxml import etree
import sqlite3
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://top.chinaz.com/all/'

nameList = []
urlList = []
rankList = []
contList = []

headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'close' 
}

def getPage(url):
    global headers
    try:
        a = requests.get(url, headers=headers).content
        html = etree.HTML(a)
        return html
    except:
        return False

def getInList(page):
    global nameList, urlList, rankList, contList
    namepath = '//*[@id="content"]/div[3]/div[3]/div/ul/li/div[2]/h3/a/text()'
    urlpath = '//*[@id="content"]/div[3]/div[3]/div/ul/li/div[2]/h3/span/text()'
    rankpath = '//*[@id="content"]/div[3]/div[3]/div/ul/li/div[2]/div/p[1]/a/text()'
    contpath = '//*[@id="content"]/div[3]/div[3]/div/ul/li/div[2]/p/text()'
    nameList += page.xpath(namepath)
    urlList += page.xpath(urlpath)
    rankList += page.xpath(rankpath)
    contList += page.xpath(contpath)
    for line in contList:
        line = line[15:]

def morepages(index):
    for id in xrange(1,index+1):
        url='http://top.chinaz.com/all/index_%d.html' % id
        html = getPage(url)
        getInList(html)

def createTable():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    create_table = '''
        CREATE TABLE alexa(
            id INT PRIMARY KEY     NOT NULL,
            name TEXT  NOT NULL,
            url CHAR(50)  NOT NULL,
            rank INT  NOT NULL,
            content TEXT
        );
        '''
    try:
        c.execute(create_table)
    except:
        pass
    conn.commit()
    conn.close()


def insertData(length):
    global nameList, urlList, rankList, contList
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    sql = 'INSERT INTO alexa (id, name, url, rank, content) VALUES (?,?,?,?,?);'
    data = []
    c.execute('SELECT id FROM alexa;')
    prev = c.fetchall()[-1][0]
    for i in xrange(length):
        data.append((
            i+prev+1, nameList[i], urlList[i], rankList[i], contList[i]))
    sql = sql[:-1] + ';'
    c.executemany(sql, data)
    conn.commit()
    c.execute('SELECT id FROM alexa;')
    print u"爬取完成，目前共"+str(c.fetchall()[-1][0])+u"组数据。"
    conn.close()

def main():
    global nameList, urlList, rankList, contList
    print u"请输入您要爬取的页数："
    id = int(raw_input())
    if id == 1:
        html = getPage(url)
        getInList(html)
    elif id > 1:
        morepages(id)
    if len(nameList) == len(urlList) == len(rankList) == len(contList):
        length = len(nameList)
        createTable()
        insertData(length)
    else:
       print u"爬取出错"

if __name__  == '__main__':
    main()