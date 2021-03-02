#-*- codeing = utf-8 -*-

from bs4 import BeautifulSoup           #网页解析，获取数据
import re                               #正则表达式，进行文字匹配
import urllib.request,urllib.error      #指定URL，获取网页数据
import xlwt                             #进行Excel操作
import sqlite3                          #进行SQLite数据库操作

def main():
    baseurl = "http://news.4399.com/gonglue/hxjy/wuqi/"
    #1、爬取网页
    data_list = get_data(baseurl)
    save_path = ".\\武器.xls"
    #3、保存数据
    save_data(data_list,save_path)

find_url = re.compile(r'<a href="http://news.4399.com/gonglue/hxjy/wuqi/(.*?).html">')

find_name = re.compile(r'<h1 class="m1-tit">(.*?)</h1>')

find_attribute_name = re.compile(r'<span class="m1-att-name">(.*?)</span>')

find_attribute_num = re.compile(r'<span class="m1-att-num">(.*?)</span>')

#爬取网页
def get_data(baseurl):
    data_list = []

    #url_list = []
    #逐一寻找网页
    html = ask_url(str(baseurl))
    soup = BeautifulSoup(html,"html.parser")
    for item in soup.find_all('div',class_="panel"):
        item = str(item)
        url_list = re.findall(find_url,item)
        #url_list.append(url)
    # print(url_list[10])
        
    for i in range(0,300):
        url = baseurl + str(url_list[i]) + '.html'
        #url = url_list[i]
        html = ask_url(url)

        #逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="w youhua1 mb10"):
            #print(item)
            data = []
            item = str(item)

            #武器名字
            name = re.findall(find_name,item)
            temp = name[0]
            data.append(temp)

            #武器属性名字
            # attribute_name = re.findall(find_attribute_name,item)
            # data.append(attribute_name)

            #武器属性数值
            attribute_num = re.findall(find_attribute_num,item)
            temp = attribute_num
            for i in range(0,len(attribute_num)):
                data.append(temp[i])
        
            data_list.append(data)

    print(data_list)

    return data_list




#得到指定一个URL的网页内容
def ask_url(url):
    # head = {                        #模拟浏览器头部信息，向服务器发送消息
    #     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
    # }

    head = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
    }

    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("ANSI")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

    return html



#保存数据
def save_data(data_list,save_path):
    print("save....")
    book = xlwt.Workbook(encoding="ANSI",style_compression=0)
    sheet = book.add_sheet('火线精英武器',cell_overwrite_ok=True)
    col = ("武器名字","威力","射速","精准","便携","稳定")

    #按列写入
    for i in range(0,6):
        sheet.write(0,i,col[i])
    num = 0
    for i in range(0,len(data_list)):
        print("第%d条"%(i+1))
        data = data_list[i]
        if(len(data)==6):
            for j in range(0,len(data)):
                sheet.write(num+1,j,data[j])
            num += 1

    book.save(save_path)



if __name__ == "__main__":
    #调用函数
    main()
    print("爬取完毕")


