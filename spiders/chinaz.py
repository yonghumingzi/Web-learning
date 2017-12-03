# -*- coding:utf-8 -*-
import requests
from urllib import quote
import re
import time
import os
from lxml import etree

headers = {
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate, sdch',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'If-None-Match': '507b1d38bb69d31:0'
}

headers2 = {
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Referer': 'http://down.chinaz.com/soft/36465.htm',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'Connection': 'close'
}

cookies = {
	'qHistory': 'aHR0cDovL3Rvb2wuY2hpbmF6LmNvbS90b29scy9zY3JpcHRlbmNvZGUuYXNweCtKU+WKoOWvhi/op6Plr4Z8aHR0cDovL3Rvb2wuY2hpbmF6LmNvbS90b29scy90ZXh0ZW5jcnlwdC5hc3B4K+aWh+Wtl+WcqOe6v+WKoOWvhi/op6Plr4Z8aHR0cDovL3Rvb2wuY2hpbmF6LmNvbS90b29scy91cmxlbmNvZGUuYXNweCtVcmxFbmNvZGXnvJbnoIEv6Kej56CBfGh0dHA6Ly90b29sLmNoaW5hei5jb20vdG9vbHMvbWQ1LmFzcHgrTUQ15Yqg5a+GL+ino+WvhnxodHRwOi8vdG9vbC5jaGluYXouY29tL3Rvb2xzL3VuaWNvZGUuYXNweCtVbmljb2Rl57yW56CB6L2s5o2i',
	'UM_distinctid': '15fee03ed2c19e-01509e856b6f72-5d4e211f-100200-15fee03ed2d506',
	'ASPSESSIONIDQQDDTSTR': 'IDEHBMGBNMMIKDLAFPEJEIFL',
	'dp4ucQueryKey': '123',
	'countcookie36465': 'visited',
	'CNZZDATA749609': 'cnzz_eid%3D1750566633-1502269832-http%253A%252F%252Fdown.chinaz.com%252F%26ntime%3D1512304503', 
	'CNZZDATA433095': 'cnzz_eid%3D1180375065-1502266065-null%26ntime%3D1512302152'
}

def mkdir():
	isExists = os.path.exists('codes')
	if not isExists:
		os.makedirs('codes')
	else:
		return False

def main():
	global headers, headers2, cookies
	s = requests.session()
	print u"请输入想查询的内容"
	query = quote(raw_input())
	response = s.get('http://down.chinaz.com/query.asp?search_code=0&q='+query, headers=headers, timeout=5).content
	numPath = '//*[@id="downchinaz"]/div[2]/div[5]/div[1]/div/div/strong/text()'
	urlPath = '//*[@id="downchinaz"]/div[2]/div[5]/div[2]/div/h4/'
	downPath = '//*[@id="down"]/div[2]/ul/li/a/@href'
	selector = etree.HTML(response)
	num = selector.xpath(numPath)
	codeUrls = selector.xpath(urlPath+'a/@href')
	codeNames = selector.xpath(urlPath+'a/text()')
	codeTimes = selector.xpath(urlPath+'span[@class="date"]/text()')
	print "num: "+str(num)
	print "codeUrls: "+str(codeUrls)
	print type(num[1])
	print num[1]
	if num[0][1:] == query:
		page = (int(num[1])/10)+1
		print page
		print u"搜索到符合的结果共"+num[1]+u"项，共%d页" % page
		print u"第一页的内容："
		length = len(codeUrls)
		for i in xrange(length):
			print str(i) +". "+codeNames[i] + " " + codeUrls[i] + u" 发布时间："+codeTimes[i]
		print u"请输入您要下载的源码序号"
		index = int(raw_input())
		for i in xrange(length):
			if index == i:
				content = s.get('http://down.chinaz.com'+codeUrls[i], timeout=5).content
				selector2 = etree.HTML(content)
				ref = selector2.xpath(downPath)
				print ref[0]
				name = codeNames[i]
		mkdir()
		try:
			code = s.get('http://down.chinaz.com'+ref[0], headers=headers2, cookies=cookies).content
			if "<meta http-equiv='refresh' content='5;url=/'>" in code:
				print u"被拦了……"
			f = open('codes'+'/'+name+'.zip', 'wb')
			f.write(code)
			f.close()
		except:
			print u"下载失败"
	else:
		print u"打开页面失败"

if __name__=='__main__':
	starttime = time.time()
	main()
	print u"共用时"+ str(time.time() - starttime) + "s" 