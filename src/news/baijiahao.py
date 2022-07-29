# encoding=utf8

import requests
import os
import json
from bs4 import BeautifulSoup as bf
import time

url = 'https://mbd.baidu.com/webpage?tab=article&num=30&uk=KKlshDoWI_vbi3E1Ehi4aw&source=pc&type=newhome&action=dynamic&format=jsonp&otherext=h5_20220623143557&Tenger-Mhor=2720973306&callback=__jsonp01656312083699'

toutiao = 'https://www.toutiao.com/api/pc/list/user/feed?category=profile_all&token=MS4wLjABAAAAbXHQBrbRhOZPz042Xj2B39gfo61xUgJKDPF5GOgtJs0&max_behot_time=1656311634989&aid=24&app_name=toutiao_web&_signature=_02B4Z6wo00d01kNWTyQAAIDCw1S1ZozPOppDckuAAPJ-cCddNZSZBlnOV5d7pLa6pS2hW86C.j2P984dMzJPnoeguy66QKTAxbozz9lQo1kpDIT2UFhLH8xlXqafDS12NkXIpNgdLSeYmHlSf2'

def gen_csv():
    files = os.listdir(".")
    files = list(filter(lambda  a:"证券日报" in a,files))
    articles = []
    for file in files:
        with open(file,'r',encoding = 'utf8') as fo:
            j = json.load(fo)
            j['list'].reverse()
            articles =  articles + j['list']
            print(len(articles))
    articles = map(lambda a:a['itemData'],articles)

    articles = map(lambda a:",".join([a['article_id'], time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(int(a['created_at']))),a["title"],a['url']]) , articles)

    with open("news_202101_202206.csv",'w',encoding="utf8") as fo:
        fo.write("\n".join(list(articles)))

def extract(url):
    txt = requests.get(url).text
    # print(txt)
    res = bf(txt)
    sections = res.select("p > span")
    if len(sections) == 0:
        sections = res.select("p")
    content = "\n".join(map(lambda s:s.get_text(),sections))
    return content

last_url = "https://baijiahao.baidu.com/s?id=1725648096358301228"

def featch_article():
    with open("news_2021_20220628.csv",'r',encoding="utf8") as fo:
        lines = fo.readlines()
        
    rows = map(lambda l:l.split(","), lines)
    continu = False
    for row in rows:

        id = row[0]
        date = row[1]
        title = row[2]
        url = row[3][:-1]

        if not continu:
            if url == last_url:
                continu = True
            else:
                continue

        # print(time[:7])
        print("extracting:"+url)
        time.sleep(50)
        # try:
        #     content = extract(url)
        # except:
        #     time.sleep(60)
        #     content = extract(url)
        content = extract(url)


        with open(date[:7]+".txt",'a',encoding = 'utf8') as fo:
            json.dump({"title":title,"content":content},fo)
            fo.write("\n")




if __name__ == "__main__":
    featch_article()
    # content = extract('https://baijiahao.baidu.com/s?id=1695453771167972934')
    # gen_csv()
    # print(content)