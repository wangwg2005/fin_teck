# -*- coding: utf-8 -*-

from requests_html import HTMLSession,HTML

from  datetime  import  *
from dateutil.utils import today
import json

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
        print(values[1].text,values[2].text)
        if values[2].text in date:
            print(values[4].html)
            link_str=None
            link=values[4].find("a")[0]
            attrs=link.attrs
            if "encode-open" in attrs:
                link_str="http://reportdocs.static.szse.cn"+attrs[ "encode-open"]
            else:
                link_str=attrs["href"]
            print("attrs:",link.attrs)
            r={"secCode":values[0].text,"secName":values[1].text,"date":values[2].text,"type":values[3].text,"title":values[4].text,"link":link_str}
#             print(r)
            result.append(r)
        else:
            return result
    
    


szse = "http://www.szse.cn/disclosure/supervision/inquire/index.html"
sse = "http://www.sse.com.cn/disclosure/credibility/supervision/inquiries/"


todayStr=str(str(today()-timedelta(17))[:10])

rs1=search(szse,[todayStr])
rs2=search(sse,[todayStr])
with open("szse.json","w") as f:
    f.write(json.dumps(rs1))
    
with open("sse.json","w") as f:
    f.write(json.dumps(rs2))


