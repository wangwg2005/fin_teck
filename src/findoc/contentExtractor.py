# -*- coding: utf-8 -*-

from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import re


from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

salt_number=35

def convert_pdf(pdf_path, page=1):  
    fp = open(pdf_path, 'rb')  # 以二进制读模式打开
    # 用文件对象来创建一个pdf文档分析器
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()



    lines=[]
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 用来计数页面，图片，曲线，figure，水平文本框等对象的数量
        num_page, num_image, num_curve, num_figure, num_TextBoxHorizontal = 0, 0, 0, 0, 0

        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            layout=device.get_result()
            
            for x in layout:
                if isinstance(x,LTTextBoxHorizontal):
                    lines.append(x.get_text())
    print("lines of f",len(lines))
    return "".join(lines)

def convert2lines(txt):
    lines=txt.split(" \n")
    return list(map(lambda l:l.replace("\n",""),lines))

def extract_corelation(path):
    print("extracting corelation from "+path)
    txt=convert_pdf(path)
    lines=convert2lines(txt)
    pat="(。|：|，)?.{1,18}(需|须).*?股东大会.*?(，|。)"
    
    result={"target":""}
    for l in lines:
        m=re.search(pat, l)
        if m!=None:
            result["target"]=m.group(0)[:-1]
            return result
    
    
        
    return result

def is_connected(lines):
    
    for l in lines:
        if "本次交易构成关联交易" in l:
            return True
    
    
        
    return False


def extract_cash_product(path):
    print("extracting cash product from "+path)
    txt=convert_pdf(path) 
    
    pat="(私募基金|信托|单一计划)"
    
    
    m=re.search(pat, txt)
    result={"keyword":""}
    if m!=None:
        result["keyword"]=m.group(1)
    
    return result

def extract_meeting(path):
    print("extracting meeting from "+path)
    meeting={}
    txt=convert_pdf(path)
    meeting["date"]=re.search("：[0-9]{4}[^0-9].*日",txt).group()[1:].replace(" ","")
    patt="关于.+?的议案"
    lines=convert2lines(txt)
    props=[]
    for l in lines:
        props.extend(re.findall(patt, l))
        
    props=list(map(lambda x:x.replace(" ",""),props))
        
    meeting["proposal"]=list(filter(lambda x:x.find("股东大会")<0,set(props)))
#     meeting["proposal"]=list(set(patt.findall(txt)))
#     if len(meeting["proposal"])==0:
#         
#         lines=list(filter(lambda l:l[:2]=="关于" or l.find("议案")>-1  , lines))
#         num_line=len(lines)
#         for i in range(num_line):
#             if lines[i][:2]=="关于" and lines[i].find("股东大会")<0 and lines[i+1].find("议案")>-1:
#                 meeting["proposal"].append(lines[i]+lines[i+1])
#         
#     meeting["proposal"]=list(filter(lambda m:m.find("召开")<0,meeting["proposal"]))
    return meeting


# print(is_connected("c:\\tmp\\201.PDF"))C:\tmp\annual_report\tmp
import os
dir_path=r"C:\tmp\annual_report\tmp"

for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file[-3:]!= "pdf":
            continue
#         if file[:6]!='000002':
#             continue
        
        tpath="C:\\tmp\\annual_report\\tmp\\txt\\"+file[:-3]+"txt"
#         if os.path.exists(tpath):
#             print(tpath,"exists, pass")
#             continue
        fpath=os.path.join(root,file)
        print("converting",fpath)
        try:
            content=convert_pdf(fpath, 1)
        except:
            print("error happend when converting file ",fpath)
            content=""
        
        with open(tpath,'w',encoding="utf8") as fo:
            fo.write(content)


  
#print(extract_corelation("c:\\tmp\\202.PDF"))