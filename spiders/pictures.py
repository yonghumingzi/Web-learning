# -*- coding=utf-8 -*-

import requests
import re
import os
import sys
import time

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
 		response = requests.get(self.url, headers=self.headers, timeout=5)
 		return response.content.decode('utf-8')

 	def getImg(self):
 		pattern = re.compile('<img.*?class="BDE_Image".*?src="(https://imgsa\.baidu\.com/forum/w%3D580/sign=.*?\.jpg)".*?width=".*?".*?height=".*?".*?changedsize="true">.*?<br>',re.S)
 		page = self.getPage()
 		imgUrls = re.findall(pattern,page)
 		i = 0
 		for imgUrl in imgUrls:
 			try:
 				print u"[+]正在抓取第" + str(i) + u"张图片"
 				i += 1
 				img = requests.get(imgUrl, headers=self.headers, timeout=10)
 				data = img.content
 				f = open('pics'+'/'+str(time.time())+'.jpg','wb')
 				f.write(data)
 				f.close()
 			except:
 				print u"[+] 抓取失败"
 		print "[+] 抓取完成"

 	def mkdir(self):
 		isExists = os.path.exists('pics')
 		if not isExists:
 			os.makedirs('pics')
 		else:
 			return False

	def start(self):
		self.mkdir()
		self.getImg()

picture = tieba()
starttime = time.time()
picture.start()
print "Cost: "+ str(time.time() - starttime) + "s" 