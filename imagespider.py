#！ -*- coding:utf-8 -*-

'''
抓取百度 图片
'''
import urllib2
from bs4 import BeautifulSoup
import urllib

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent} 
keyword = 'eclipse'
url = 'http://image.baidu.com/search/wisemidresult?word=%E7%BE%8E%E9%A3%9F&tn=wisemidresult&ie=utf8&fmpage=result&pn=0&rn=6&size=mid&ct_3=%E6%90%9C%E5%9B%BE%E7%89%87'
try:
    request = urllib2.Request(url, headers=headers)  #注意后面的参数是 a=b指定呢
    response = urllib2.urlopen(request)
    ret = response.read()
    print ret.title
except urllib2.URLError, e:
    if hasattr(e,"code"):
                print e.code
    if hasattr(e,"reason"):
        print e.reason  #报异常httplib.BadStatusLine，是headers验证的问题

soupe = BeautifulSoup(ret, "html.parser")

items = soupe.select("img .i")

i = 0
for item in items:
    if item != None:
        imageURL = item['src']
        u = urllib2.urlopen(imageURL)
        data = u.read()
        f = open(str(i) + '.jpg', 'wb')
        f.write(data)
        print u"正在悄悄保存她的一张图片为",i
        f.close()
        i += 1
        
#         print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'    