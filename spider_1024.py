#！ -*-coding:utf-8 -*-
'''
Created on 2016年4月27日
1024图片下载器 你懂得
@author: SUN
'''

import urllib2
from bs4 import BeautifulSoup

#获得某帖子下的所有图片地址 
def find_image_url(href):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
    headers = { 'User-Agent' : user_agent ,"Accept":"*/*",'Referer':'http://www.google.com' }    
    url = 'http://cl.pclmm.org/' + str(href)
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        ret = response.read()    
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason 

    soupe = BeautifulSoup(ret, "html.parser")
    items = soupe.select('h4')
    url_list=[]
    for item in items:
        for brother in item.next_siblings:#所有的兄弟
            if brother.name == 'div' and brother['class'][0].startswith('tpc_content'):
                for url in brother.descendants :
                    if url == None:continue
                    if str(type(url)) == "<class 'bs4.element.NavigableString'>":continue
                    if url.name =='input':
                        try:                           
                            url_list.append(url['src'])
                        except urllib2.URLError, e:
                                if hasattr(e,"code"):
                                    print e.code
                                if hasattr(e,"reason"):
                                    print e.reason 
        break;#只循环一次
    return url_list

#获得某页的所有帖子的所有图片地址
def find_all_images(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
    headers = { 'User-Agent' : user_agent ,"Accept":"*/*",'Referer':'http://cl.pclmm.org' } 
    request = urllib2.Request(url,headers=headers)
    response = urllib2.urlopen(request)
    result = response.read()

    soup = BeautifulSoup(result,"html.parser")
    items = soup.find_all('a',attrs={"href": True, "title": True})

    i = 0
    image_list=[] #存储所有图片链接
    for item in items:
        if i > 20:break
        if item['href'].startswith('htm_data/16/1604'):
            image_list += find_image_url(item['href'])
            print i
        i += 1
    return image_list

#下载图片
def download(image_list):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
    headers = { 'User-Agent' : user_agent ,"Accept":"*/*",'Referer':'http://www.google.com' } 

    index = 0
    imgfile = None 
    try:
        for item in image_list:
                if item != None:
                    request = urllib2.Request(item, headers=headers)
                    u = urllib2.urlopen(request)
                    data = u.read()
                    imgfile = open(str(index) + '.jpg', 'wb')
                    imgfile.write(data)
                    print u"正在悄悄保存她的一张图片为",index
                    imgfile.close()
                    index += 1
    except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
    finally:
        imgfile.close()                


if __name__ == '__main__':
    image_list = find_all_images("http://cl.pclmm.org/thread0806.php?fid=16&search=&page=3")
    download(image_list)