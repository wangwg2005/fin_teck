# -*- coding: utf-8 -*-

from requests_html import HTMLSession,HTML

# session = HTMLSession()
# url = "http://www.sse.com.cn/disclosure/credibility/supervision/inquiries/"
# h = session.get(url=url)
# h.html.render(sleep=10)
# print(h.html.find("table.table")[0].html)

session = HTMLSession()

def search(url,date=[]):
    
    h = session.get(url=url)
    h.html.render(sleep=5)
    table=h.html.find("table.table")[0]
    rows=table.find("tr")[1:]
    result=[]
    for row in rows:
        values=row.find("td");
        if values[2].text in date:
            r={"secCode":values[0].text,"secName":values[1].text,"date":values[2].text,"type":values[3].text,"title":values[4].text,"link":row.find("a")[0].attrs["href"]}
#             print(r)
            result.append(r)
        else:
            return result
    
    


szse = "http://www.szse.cn/disclosure/supervision/inquire/index.html"
sse = "http://www.sse.com.cn/disclosure/credibility/supervision/inquiries/"

# rs=search(sse,["2020-02-27","2020-02-24"])
# print(rs)

