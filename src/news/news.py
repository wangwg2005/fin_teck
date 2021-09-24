# -*- coding: utf-8 -*-

class News:
    
    def __init__(self,url):
        self.url=url
    
    @property
    def element_classes(self):
        return self.element_class
    
#     @property
#     def url(self):
#         return self.url
#     
#     @url.setter
#     def url(self,url):
#         self.url=url
    
    def parse(self,ele):
        pass
    
    def parse_comments(self,comments):
        for comment in comments:
            comment