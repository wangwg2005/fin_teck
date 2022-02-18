# -*- coding: utf-8 -*-
import os

if __name__ == "__main__":
    root_dir = r"C:\tmp\annual_report\2021"
    
    for file in os.listdir(root_dir)[:10]:
        if file[-3:] !="txt":
            continue 
        
        with open(os.path.join(root_dir,file),"r",encoding="utf8") as fo:
            lines = fo.readlines()
            
        t = "".join(lines)
        t = t.replace(" \n","\t")
        t = t.replace("\n","")
        t = t.replace("\t","\n")
        
        if "释义内容" not in t:
            continue
        else:
            start = t.index("释义内容")
            try:
                last = t.rindex("\n指 ")
            except:
                print(file)
                
                break
            end = t.index("\n",last+2)
            print(file)
            print(t[start+5:end])

        
        
        