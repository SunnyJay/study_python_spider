#！ -*- coding:utf-8 -*-

'''
抓取糗事百科 作者和内容
采用多种方法
'''
import urllib2
from bs4 import BeautifulSoup

# 方法一 
# 比较复杂 因为使用了descendants
def fun1(soupe):
    items = soupe.find_all("div", class_="article block untagged mb15")
    #print type(items) #<class 'bs4.element.ResultSet'>
    for item in items:
        #1.针对每个article block untagged mb15 div标签，遍历它所有的子孙节点）
        for child in item.descendants : 
            
            # 2.子孙里面有标签类型，也有非标签类型(NavigableString,而且还是空白，具体原因不清楚),针对标签进行处理
            if str(type(child)) == "<class 'bs4.element.Tag'>":   #即标签类型
                #标签名字是h2的就是作者名称
                if child.name == 'h2':
                    print '作者:',child.get_text()
                    
                #标签是div，且内容不为空，或者class是content，就是要找的内容
                #elif child.name  == 'div' and child.string != None: #或者 elif child['class'][0]='content':
                elif child.name  == 'div' and child['class'][0] == 'content': #重要！ 一定要注意child['class']返回的是列表
                    print '内容:', child.get_text() #很奇怪 有些内容为什么get_text可以输出，但是string就不能输出。初步怀疑，只要有些内容里面有子标签如br，就会出问题
                elif child.name =='span' and  child.i != None and child['class'][0] == 'stats-vote':
                    print child.get_text() 
                elif child.name =='span' and  child.i != None and child['class'][0] == 'stats-comments': # 因为会碰到其他地方使用span，所以过滤
                    print child.a.get_text() #重要！记住这种形式, tag.subtag.xx 可以直接访问到下级tag
                    #print child.attrs #打印tag的属性
                    #print child['class'] #打印其class属性的值
            #else:
            #    print type(child) #NavigableString
            
        print '****************************'
        #########################################
        # 1. find_all返回的是tag集合  <class 'bs4.element.ResultSet'>  可进行遍历
        # 2. item.descendants 返回子子孙孙
        # 3. div标签本身的属性： name、attrs、string(内容或None)， 对于存在的属性可以child['属性']，注意返回的是列表，还得用下标标识
        # 4. 很奇怪 有些内容为什么get_text可以输出，但是string就不能输出。初步怀疑，只要有些内容里面有子标签如br，就会出问题
        # 5. print child.a.get_text() #重要！记住这种形式, tag.subtag.xx 可以直接访问到下级tag
        # 6. 某个tag.get_text()会返回该tag下的所以文本内容，包括子孙的！重要！
        ########################################     
    
# 方法二
#  更简单 学会使用 select parent next_sibling
def fun2(soupe):
    #items = soupe.find_all("div", class_="article block untagged mb15")
    items = soupe.select('h2') # .表示类
    for item in items:
        print '作者:',item.get_text()
        #print type(item.parent.parent.next_sibling.next_sibling) #需要两个next_sibling，第一个next_sibling是空白！！重要！
        print '内容:',item.parent.parent.next_sibling.next_sibling.get_text().replace("\n"," ")
        href = item.parent.parent.next_sibling.next_sibling.next_sibling.next_sibling.a['href']
        detail(href);
        print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        

# 查找具体评论
def detail(href):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }         
    url = 'http://www.qiushibaike.com' + str(href) #拼接url
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
    items = soupe.select('.replay') # .表示类
    for item in items:
            print '    评论者:',item.a.get_text()
            print '            评论内容:',item.span.get_text().replace("\n"," ")  #直接访问儿子 item.span
                
                
if __name__ == '__main__':
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent } 
    
    for i in range(1):
        page = i
        url = 'http://www.qiushibaike.com/hot/page/' + str(page)
        try:
            request = urllib2.Request(url, headers=headers)  #注意后面的参数是 a=b指定呢
            response = urllib2.urlopen(request)
            ret = response.read()
        except urllib2.URLError, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason  #报异常httplib.BadStatusLine，是headers验证的问题
        soupe = BeautifulSoup(ret, "html.parser")
        
        fun2(soupe)
        print '-------------------------------------------第',i,'页结束-------------------------------------------'