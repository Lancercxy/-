from urllib.request import urlopen, Request
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import ssl
import json
import csv
ssl._create_default_https_context = ssl._create_unverified_context
#hotword ,number
def Pdouban():   #定义一个爬虫函数,参数hotword是热词用于检索，number是检索数量
    #新建一个csv的文件
    # csv_show = open('D:\office\爬豆瓣\豆瓣电影06.csv', 'w', encoding='gbk', newline='')
    # writer = csv.writer(csv_show)
    #CVS写入的参数为一个list
    # writer.writerow(['热词', '电影名', '导演', '链接', '上映日期', '类型', '评分', '评价人数'])
    head = 'https://movie.douban.com/top250'
    # url = '/typerank?type_name=动作片&type=5&interval_id=100:90&action='
    # url = quote(url, safe=";/?:@&=+$,", encoding="utf-8")   #将中文转成码
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70'}
    ret = Request(head, headers=headers)
    # print(ret)
    html = urlopen(ret)
    # strhtml = requests.get(head, headers=headers)
    # print(strhtml)
    soup = BeautifulSoup(html, 'lxml')
    # print(soup.find_all('li'))
    # print(soup)
    # content > div > div.article > div.gaia.gaia-lite.gaia-movie.slide-mode > div.list-wp > div > div.slide-container > div > div:nth-child(2) > a:nth-child(1) > div > img
    data = soup.select('#content > div > div.article > ol')
    # print(data)
    for link in soup.find_all('li'):
        if link.a.img != None:
            print(link.a.img['alt'])#img['alt']
        #     print(link.div['class'])
    # print(result)

    # print(html.read())
    # content > div > div.article > div.gaia.gaia-lite.gaia-movie.slide-mode > div.list-wp > div > div.slide-container > div > div:nth-child(2) > a:nth-child(1)
    # print(html.read())
    # bs = json.loads(html.read().decode('utf8')) #将json转化成字典
    # bs = json.loads(html.read().decode('utf8'))
    # print(bs)
    # 新建一个列表接收所有电影信息
    movies = []

    for i in range(0, int(10)): #根据输入的数量开始循环
        movie_name = bs['subjects'][i]['title']     #电影名
        score = bs['subjects'][i]['rate']           #评分
        img_url = bs['subjects'][i]['cover']        #图片连接
        movieUrl = bs['subjects'][i]['url']         #获取一个电影详情的连接
        ret2 = Request(movieUrl, headers=headers)
        html2 = urlopen(ret2)
        bs2 = BeautifulSoup(html2, 'lxml')   #打开该电影链接
        subspan1 = bs2.find('div', {'id': 'content'})   #定位到所需信息的位置

        for b in subspan1.find_all('div', {'id': 'info'}):  #定位到基本信息位置
            attrs_name = b.find('span', {'class': 'attrs'}).get_text()              #导演
            actor = b.find('span', {'class': 'actor'}).get_text()                   #演员
            date = b.find('span', {'property': 'v:initialReleaseDate'}).get_text()  #上映日期
            type = b.find('span', {'property': 'v:genre'}).get_text()           #类型
            #area = b.xpath('//*[@id="info"]/text()[2]').get_text()                 #地区

        for b2 in subspan1.find_all('div', {'id': 'interest_sectl'}):
            rating_sum = b2.find('span', {'property': 'v:votes'}).get_text()         #评价人数

        for b3 in subspan1.find_all('div', {'class': 'related-info'}):
            indent = b3.find('div', {'class': 'indent'}).get_text()                   #简介

        html2 = urlopen(img_url)  # 打开海报链接
        d = "D:\office\爬豆瓣\电影海报/" + movie_name + ".jpg"  # 保存路径
        with open(d, 'wb') as f:
            f.write(html2.read())
            f.close()
            print("海报保存成功 " + movie_name)
        print('电影: ' + movie_name, end='')
        print(b.get_text(), end='')
        print('评分: '+score)
        print('评价人数: '+rating_sum+'人')
        print('简介: ' + indent)
        #将信息添加进列表中
        movies.append({'热词': '动作', '电影名': movie_name, '导演': attrs_name, '链接': movieUrl,
                            '上映日期': date, '类型': type, '评分': score, '评价人数': rating_sum})
        # 将电影信息写入cvs文件
        writer.writerow([movies[i]['热词'], movies[i]['电影名'], movies[i]['导演'], movies[i]['链接'],
                         movies[i]['上映日期'],movies[i]['类型'], movies[i]['评分'], movies[i]['评价人数']])
    # 关闭文件
    csv_show.close()

print('热词: 热门、最新、经典、豆瓣高分、冷门佳片、华语、动作、喜剧、爱情、科幻、悬疑、恐怖、治愈……')
# word = input('请输入需要检索的热词：')
# num = input('请输入需要检索的电影数（0-50）：')
# Pdouban(word, num)
Pdouban()