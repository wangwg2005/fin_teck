# -*- coding: utf-8 -*-

from requests_html import HTMLSession, HTML
from news import News


class Xueqiu(News):
    
    def __init__(self,url):
        self.url=url
        
    def element_classes(self):
        return {"source":".source","time":".time","title":".article__bd__title","comment_list":".comment__mod--all"}
    
    def comment_classes(self):
        return {"comment_item":".comment__item","user_name":".user-name","time":".time"}
    
    def parse_comment(self):
        
        selectors=self.comment_classes()
        
        comment_list=self.comment_list.find(selectors["comment_item"])
        
        comms=[]
        com={}
        for comment in comment_list:
            com["id"]=comment.attrs["data-id"]
            com["user_name"]=comment.find(selectors["user_name"])[0].text
            com["time"]=comment.find(selectors["time"])[0].text
            com["content"]=comment.find("p")[0].text
            comms.append(com)
            
        self.comments=comms
        

def scrapy(url):
    
    anew=Xueqiu(url)

    session = HTMLSession()
    
    rep=session.get(url)
    rep.html.render()
    
    rep.html.find(".pagination__next")[0]
    
    rep.html.find(".pagination__next")[0].click()
    
    
#     a=rep.html.search("{repost_number} 转发 · {comment_number} 评论 · {like_number} 赞")
#     print(a["repost_number"])
    
    
    for k,v in anew.element_classes().items():
        print(v)
        element=rep.html.find(v)[0]        
        
        setattr(anew,k,element)
        print(element.text)
        
    anew.parse_comment()
    print("comments")
    print(anew.comments)
        
scrapy("https://xueqiu.com/S/SH600518/175551627")


