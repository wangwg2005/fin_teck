# -*- coding: utf-8 -*-
from cninfo import getByDate
from dateutil.utils import today
from _datetime import timedelta
import time
import json,os
from functools import reduce
import matplotlib.pyplot as plt
import pandas as pd




def dump_from_today():
    for i in range(20,30):
      dateStr=str(today()-timedelta(i))[:10]
      print("dumping "+dateStr)
      res=getByDate(dateStr)
      
      with open(r'C:\doc\cnin_list\\'+dateStr+".json",'w', encoding='UTF-8') as f:
          f.write(json.dumps(res))

def dump(year="2019"):
    prefix=year+'-'
    for i in range(1,367):
        print("the day of the "+year+" year :"+str(i))
        dstr=prefix+str(i)
        timeStruct = time.strptime(dstr, "%Y-%j")
#转换为时间戳: 
        timeStamp = int(time.mktime(timeStruct)) 
        
        localTime = time.localtime(timeStamp) 
        strTime = time.strftime("%Y-%m-%d", localTime) 
        print("dumping "+strTime)
        prefix_path=r"C:\doc\cnin_list\\"+strTime[:7]
        if not os.path.exists(prefix_path):
            os.makedirs(prefix_path,  exist_ok=True)
        
        fpath=os.path.join(prefix_path,strTime+".json")
        if os.path.exists(fpath):
            continue
        
        res=getByDate(strTime)
        
#         print(res)
#         if res['totalAnnouncement']==0:
#             continue
        
        if not os.path.exists(prefix_path):
            os.makedirs(name=prefix_path, exist_ok=True)
      
        with open(fpath,'w', encoding='UTF-8') as f:
          f.write(json.dumps(res))
        time.sleep(3)



def check_num():
    dir="C:\doc\cnin_list\\"
    
    result={}
     
    for root,dirs, files in os.walk(dir):
        if root[-7:-3]!="2020":
            continue
        print("checking "+root)
        for name in files:
            if name[-4:]!="json":
                continue
                #print(name)
            fpath=os.path.join(root,name)
            with open(fpath,'r',encoding="utf-8") as f:
                #l="{\"a\":"+f.readline().replace("'","\"")+"}"
                obj=json.load(f)
   
            
            
#             verify number and fix it           
            if obj["totalAnnouncement"]!=len(obj["announcements"]):
                print(name+" target number:"+str(obj["totalAnnouncement"])+", real number:"+str(len(obj["announcements"])))
                os.remove(fpath, dir_fd=None)
                res=getByDate(name[:10])
                print("new size:",len(res["announcements"]))
                with open(root+"\\"+name,'w',encoding="utf-8") as f:
                    f.write(json.dumps(res))

def dump_number():
    dir="C:\doc\cnin_list\\"
    
    result={}
     
    for root,dirs, files in os.walk(dir):
        if root[-7:-3]!="2020":
            continue
        print("checking "+root)
        for name in files:
            if name[-4:]!="json":
                continue
                #print(name)
            fpath=os.path.join(root,name)
            with open(fpath,'r',encoding="utf-8") as f:
                #l="{\"a\":"+f.readline().replace("'","\"")+"}"
                obj=json.load(f)
                
            categories=map(lambda a: a["announcementType"].split("||"), obj["announcements"])
            categories=list(categories)
            cat_len=len(categories)
            if cat_len>0:
                categories=reduce(lambda a,b:a+b,categories)
            
            
            categories={ a: categories.count(a) for a in categories}
            
            result[name[:10]]=categories
            
    with open(os.path.join(dir,"count.json"),"w") as f:
        json.dump(result, f)
    
         
         
def plot_number():
    dir="C:\doc\cnin_list\\"
    
    result={}
    
    fpath=os.path.join(dir,"count1.json")
    
    if not os.path.exists(fpath):
     
        for root,dirs, files in os.walk(dir):
            if root[-7:-3]!="2020":
                continue
            print("checking "+root)
            for name in files:
                if name[-4:]!="json":
                    continue
                    
                fpath=os.path.join(root,name)
                with open(fpath,'r',encoding="utf-8") as f:
                    #l="{\"a\":"+f.readline().replace("'","\"")+"}"
                    obj=json.load(f)
                result[name[:10]]=obj["totalAnnouncement"]
                
        with open(fpath,"w") as f:
            json.dump(result, f)
    else:
        with open(fpath,"r") as f:
            result=json.load(f)
            
            
    plt.plot_date(pd.to_datetime(list(result.keys())), result.values(), linestyle='solid')
    plt.gcf().autofmt_xdate()
    plt.show()
            


if __name__=="__main__":

#     dump("2020")
#     check_num()
#     dump_number()
    plot_number()