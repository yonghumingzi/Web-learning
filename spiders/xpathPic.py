# -*- coding:utf-8 -*-
import requests
import time
import os
import threading
from lxml import etree

class tieba:
	def __init__(self):
		self.url = "https://tieba.baidu.com/p/1518167157?red_tag=3032817939"
		self.headers = {
     		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
     		'Accept': 'text/plain, */*; q=0.01',
     		'Accept-Language': 'zh-CN,zh;q=0.8',
     		'X-Requested-With': 'XMLHttpRequest',
     		'Connection': 'keep-alive',
    		"referer":"https://www.baidu.com"
		}

	def getPage(self):
		response = requests.get(self.url, headers=self.headers, timeout=10)
		return response.content.decode('utf-8')

	def getImgUrls(self, content):
		selector = etree.HTML(content)
		xpath = "//img[@class='BDE_Image'][@changedsize='true'][@width][@height]/@src"
		imgUrls = selector.xpath(xpath)
		return imgUrls

	def getImg(self, imgUrl):
		try:
			img = requests.get(imgUrl, headers=self.headers, timeout=10).content
			f = open('pic'+'/'+str(time.time())+'.jpg', 'wb')
			f.write(img)
			f.close()
		except:
			print u"下载失败"

	def mkdir(self):
		isExists = os.path.exists('pic')
		if not isExists:
			os.makedirs('pic')
		else:
			return False

	def start(self):
		ts = []
		self.mkdir()
		res = self.getPage()
		imgUrls = self.getImgUrls(res)
		for imgUrl in imgUrls:
			t = threading.Thread(target = self.getImg, args = (imgUrl,))
			ts.append(t)
			t.start()
		for t in ts:
			t.join()

if __name__ == '__main__':
	picture = tieba()
	starttime = time.time()
	picture.start()
	print "Cost: "+ str(time.time() - starttime) + "s" 
