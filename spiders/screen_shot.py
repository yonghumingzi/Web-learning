#-*- coding:utf-8 -*-
from selenium import webdriver
from time import sleep

url = "http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp"
driver = webdriver.Firefox()
driver.get(url)
driver.implicitly_wait(10)

print u"请输入学号:"
username = raw_input()
print u"请输入密码:"
password = raw_input()
#登陆
driver.find_element_by_id('username').send_keys(username)
driver.find_element_by_id("password").send_keys(password)
driver.implicitly_wait(10)
driver.find_element_by_class_name("subbut").click()
#点到对应位置
driver.implicitly_wait(10)
driver.switch_to_frame("topFrame")
driver.find_element_by_xpath('/html/body/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/div/table/tbody/tr/td[7]/a').click()
driver.implicitly_wait(10)
driver.switch_to_default_content()  
driver.switch_to_frame("bottomFrame")
driver.switch_to_frame("menuFrame")
driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/div/table/tbody/tr[5]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/a').click()
driver.implicitly_wait(10)
driver.switch_to.parent_frame()
driver.switch_to_frame("mainFrame")
driver.switch_to_frame("lnqbIfra")
#裁图
driver.get_screenshot_as_file('score.png')
print u"----成功----"
sleep(3)
#退出
driver.quit()