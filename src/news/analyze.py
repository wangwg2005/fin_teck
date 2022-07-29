# -*- coding: utf-8 -*-

import jieba
import json

jieba.load_userdict("words.txt")

def word_filter(words):
    ws = filter(lambda word:len(word)>1,words)
    return ws

def analyze():
    with open("news_2021_20220628.csv",'r',encoding='utf8') as fo:
        lines = fo.readlines()

    kv = {}

    for l in lines:
        cols = l.split(",")
        kv[cols[2]]=cols

    print(kv)

    with open("2022-01.txt",'r',encoding='utf8') as fo:
        objs = fo.readlines()

    objs = map(lambda l:json.loads(l),objs)

    print(objs)

    for obj in objs:
        print(f'title:{obj["title"]},url:{kv[obj["title"]][3]} time:{kv[obj["title"]][1]}')
        print(list(word_filter(jieba.cut(obj["content"]))))



if __name__ == "__main__":
    analyze()