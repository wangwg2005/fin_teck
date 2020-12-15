# -*- coding: utf-8 -*-
#from TongHuaShun
from requests_html import HTMLSession,HTML

# session = HTMLSession()
# url = "http://www.sse.com.cn/disclosure/credibility/supervision/inquiries/"
# h = session.get(url=url)
# h.html.render(sleep=10)
# print(h.html.find("table.table")[0].html)

session = HTMLSession()
url = "http://data.10jqka.com.cn/market/rzrqgg/code/002118/"
h = session.get(url=url)

##这个脚本有问题

st=""
page=1;
work=True
rl=True
while work:
    h.html.render(script=st,sleep=10)
    tables=h.html.find(".m-table")
    if len(tables)<2:
        print("no table exists")
        break;
    table=tables[1]
    rows=table.find("tr")[2:]
    for row in rows:
        print(row.text.replace("\n",":"))
    links=h.html.find("a.changePage")
    print(h.html.find("a.cur")[1].text)
    work=links[-1].text=="尾页"
    st="()=>{let links=document.getElementsByClassName(\"changePage\");links[links.length-2].click();}"

