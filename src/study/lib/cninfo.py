# -*- coding: utf-8 -*-

import requests
import tempfile
import os

# can't return result with over 3000 records.

prefix="http://static.cninfo.com.cn/"
userAgent="User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"

# sh;sz;szmb;szzx;szcy;shmb;shkcp
def getByDate(sdate,plate=""):
    
    pageNum=1
    hasMore=True
        
    
    announces=[]
    result={"totalAnnouncement":0,"announcements":announces}
    
    while hasMore:
#         print("requesting the "+str(pageNum)+"th page")
        
        try:
            r=requests.post('http://www.cninfo.com.cn/new/hisAnnouncement/query',
            data={"pageNum": pageNum,
                  "pageSize": 30,
                  "column": "szse",
                  "tabName": "fulltext",
                  "plate": plate,
                  "stock":"" ,
                  "searchkey":"", 
                  "secid": "",
                  "category":"", 
                  "trade": "",
                  "seDate": sdate+"~"+sdate,
                  "sortName": "",
                  "sortType": "",
                  "isHLtitle": "false"},
            headers={
                "User-Agent": userAgent
                }
            )
            
              

            t=r.json();
        except :
            print("something wrong happend!")
            print("status_code:"+str(r.status_code))
            print(str(r.text))
            break
        r.close
        pageNum=pageNum+1
        hasMore=t['hasMore']
        
        esclate={"sh":["shmb","shkcp"],"sz":["szmb","szzx","szcy"]}
        result["totalAnnouncement"]=t["totalAnnouncement"]
        if t["totalRecordNum"]>=3000 :
            if plate=="":
                print("query by market, total annoucements:"+str(t["totalRecordNum"]))
                shAnn=getByDate(sdate, "sh")
                szAnn=getByDate(sdate, "sz")
                announces.extend(shAnn["announcements"])
                announces.extend(szAnn["announcements"])
                totalAnn=shAnn["totalAnnouncement"]+szAnn["totalAnnouncement"]
                return {"totalAnnouncement":totalAnn,"announcements":announces} 
            elif plate in esclate:
                
                subs=esclate[plate]
                print("total number "+str(t["totalRecordNum"])+" split into "+",".join(subs))
                for board in subs:
                    anns=getByDate(sdate, board)
                    announces.extend(anns["announcements"])
#                     result["totalAnnouncement"]=result["totalAnnouncement"]+anns["totalAnnouncement"]
                
                return result
                
            
        #for test purpose
     #   if pageNum>3:
     #       print("test mode, only fetch 3 pages")
     #       hasMore=False
        
        if not hasMore:
            
            print("total announces:"+str(t["totalAnnouncement"]))
    
        announces.extend(t['announcements'])
    for ann in announces:
        ann["adjunctUrl"]=prefix+ann["adjunctUrl"]
    print("pageNums:"+str(pageNum-1))
    return result;


def download(url):
    
    r = requests.get(url, headers={
            "User-Agent": userAgent
        }, stream=True)
    if r.status_code!=200:
        print(r.status_code)
        print(r.text)
        return
    
    fp, fpath = tempfile.mkstemp(suffix=".PDF")
    with os.fdopen(fp, 'wb') as fd:
        for chunk in r.iter_content(1024*1024):
            fd.write(chunk)
    r.close()
    return fpath



