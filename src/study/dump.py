# -*- coding: utf-8 -*-
from cninfo import getByDate
from dateutil.utils import today
from _datetime import timedelta
import time
import json,os



def dump_from_today():
    for i in range(20,30):
      dateStr=str(today()-timedelta(i))[:10]
      print("dumping "+dateStr)
      res=getByDate(dateStr)
      
      with open('../cninfo_list/'+dateStr+".json",'w', encoding='UTF-8') as f:
          f.write(json.dumps(res))

def dump(year="2019"):
    prefix=year+'-'
    for i in range(1,366):
        print("the day of the "+year+" year :"+str(i))
        dstr=prefix+str(i)
        timeStruct = time.strptime(dstr, "%Y-%j")
#转换为时间戳: 
        timeStamp = int(time.mktime(timeStruct)) 
        
        localTime = time.localtime(timeStamp) 
        strTime = time.strftime("%Y-%m-%d", localTime) 
        print("dumping "+strTime)
        prefix_path="../cninfo_list/"+strTime[:7]
        fpath=prefix_path+"/"+strTime+".json"
        if os.path.exists(fpath):
            continue
        
        res=getByDate(strTime)
        
#         print(res)
        if res['totalAnnouncement']==0:
            continue
        
        if not os.path.exists(prefix_path):
            os.makedirs(name=prefix_path, exist_ok=True)
      
        with open(fpath,'w', encoding='UTF-8') as f:
          f.write(json.dumps(res))
        time.sleep(3)

dump("2016")

# def check_num():
#     dir="../cninfo_list"
#     
#     for root,dirs, files in os.walk(dir):
#         if root[-7:-3]!="2019":
#             continue
#         print("checking "+root)
#         for name in files:
#             if name[-4:]=="json":
#                 #print(name)
#                 l=""
#                 with open(root+"\\"+name,'r',encoding="utf-8") as f:
#                     #l="{\"a\":"+f.readline().replace("'","\"")+"}"
#                     l=f.readline()
#               
#                 obj=json.loads(l)
#                 if obj["totalAnnouncement"]!=len(obj["announcements"]):
#                     print(name+" target number:"+str(obj["totalAnnouncement"])+" real number:"+str(len(obj["announcements"])))
# #                     res=getByDate(name[:10])
# #                     with open(root+"\\"+name,'w',encoding="utf-8") as f:
# #                         f.write(json.dumps(res))
#         
#         
# check_num()