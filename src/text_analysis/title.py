# -*- coding: utf-8 -*-

title_tree=[]
changed_tree=list()

NUM_CHN="一二三四五六七八九"
NUM_ARAB="0123456789"



changed=False

def is_num_chn(str):
    return str[0] in NUM_CHN

def is_num_arab(str):
    return str[0] in NUM_ARAB

def has_prefix(str):
    return str[0] in "第(（"

def ind_type(str):
    if is_num_chn(str):
        return 0
    elif is_num_arab(str):
        return 1
    elif has_prefix(str):
        return 2
    
def compare_title_level(t1,t2):
    t1_type=ind_type(t1)
    t2_type=ind_type(t2)
    
    if t1_type!=t2_type:
        return False
    
    if t1_type!=2:
        return True
    return t1[0]==t2[0] and compare_title_level(t1[1:], t2[1:])



in_white_title=False

def push_title(name):
    global changed
    changed=True
    size=len(title_tree)
#     print(name)
#     print(title_tree)
#     print(changed_tree)    
    if size==0 :
        if name[0]=="第":
            title_tree.append(name)
            changed_tree.append(name)
        else:
            changed=False
        return
    
    
    ind=get_index(title_tree, name)
    
        
    if ind==size:
        title_tree.append(name)
        changed_tree.append(name) 
    elif ind<size:
        
        title_tree[ind]=name
        
        size_changed=len(changed_tree)
        
        offset=ind+size_changed-size
        if offset<=0:
            changed_tree.clear()
            changed_tree.append(name)
        else:
            changed_tree[offset]=name
        
        for name_des in title_tree[ind+1:]:
            title_tree.remove(name_des)
            if name_des in changed_tree:
                changed_tree.remove(name_des)
                
    global in_white_title
    
    in_white_title= len(title_tree)>2 and ("公司所属行业情况" in title_tree[2] or "公司所处行业基本情况" in title_tree[2])
        
    
            
def get_index(t_array,title):
    size=len(title_tree)
    ind=0
    
    while ind<size:
        if compare_title_level(title_tree[ind],title):
            break
        
        ind=ind+1
    return ind

def in_white_titles():
    return in_white_title
            
def get_title_tree(): 
    changed=False
    return "\n".join(title_tree)

def get_changed_tree():
#     print("printing changed tree:",changed_tree)
    global changed
    changed=False
    tree_str="\n".join(changed_tree)
    changed_tree.clear()
    return tree_str


def clear():
    title_tree.clear()
    changed_tree.clear()
    changed=False
            