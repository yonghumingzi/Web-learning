# -*- coding=utf-8 -*-
import requests
import hashlib
import re
import sys

print "[+] 请输入用户名: "
username = raw_input()
print "[+] 请输入密码: "
password = raw_input()

while 1:
	s = requests.session()
	url = "http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp"
	try:
		r = s.get(url,timeout=5).content
	except:
		continue
	pattern1 = re.compile('<input type="hidden" name="lt" value="(.*?)" />',re.S)
	lt_value = re.search(pattern1,r).group(1)
	pattern2 = re.compile('<input type="hidden" name="execution" value="(.*?)" />',re.S)
	exec_value = re.search(pattern2,r).group(1)
	data = {
		'username':username,
		'password':password,
		'submit':'',
		'lt':lt_value,
		'execution':exec_value,
		'_eventId':'submit',
		'rmShown':'1'
	}
	headers = {
		'Referer':'http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp',
		'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; LCTE)'
	}
	try:
		r = s.post(url,data=data,headers=headers,timeout=5).content
		r = s.get('http://jwxt.xidian.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2016-2017%D1%A7%C4%EA%B5%DA%B6%FE%D1%A7%C6%DA(%C1%BD%D1%A7%C6%DA)#qb_2016-2017%E5%AD%A6%E5%B9%B4%E7%AC%AC%E4%BA%8C%E5%AD%A6%E6%9C%9F(%E4%B8%A4%E5%AD%A6%E6%9C%9F)')
		if '<table>' in r.content:
			break
	except:
		pass
	pattern = re.compile('<tr class="odd" onMouseOut="this.className=\'even\';" onMouseOver="this.className=\'evenfocus\';">.*?<td align="center">.*?</td>.*?<td align="center">.*?</td>.*?<td align="center">(.*?)</td>.*?<td align="center">.*?</td>.*?<td align="center">(.*?)</td>.*?<td align="center">(.*?)</td>.*?<td align="center">.*?<p align="center">(.*?)&nbsp;</P>.*?</td>.*?</tr>',re.S)
	items = re.finditer(pattern,r.content)
	print u"[+] 想查的课名字是："
	name = raw_input().decode(sys.stdin.encoding).split()
	i = len(name)
	k = 0
	for item in items:
		j = 0
		for a in xrange(i):
			if name[a] in item.group(1).decode('gb2312'):
				j = j + 1
		if j == i:
			print u"科目:" + item.group(1).decode('gb2312').strip() + u"\n学分:" + item.group(2).decode('gb2312').strip() + u"    修种:" + item.group(3).decode('gb2312').strip() + u"    分数:" + item.group(4).decode('gb2312').strip() + '\n-----------------------------------------------------------------'
			k = k + 1
	if k == 0:
		print u"[+] 查询不到此科目成绩"
	print "[+] 是否继续查询？(1 or 0)"
	while 1:
		judge = input()
		if judge == 1:
			break
		elif judge == 0:
			exit(0)
		else:
			print "[+] 请重输!"
			continue