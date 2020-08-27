# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 20:50:23 2020

@author: Think
"""
import json

conv_path = 'EFA_Dataset.txt'
tag = {}
tag['owner'] = 'Q: '
tag['audience'] = 'A: '
filter_list=['测试','预约','头像','私聊','付费','关注','专家']

lines = open(conv_path, encoding='utf-8').readlines()
number = 0

filename = 'QA_en_2.txt'
with open(filename,'a+',encoding='UTF-8')as PW:
  for line in lines:
    conv = json.loads(line)
    sender = 'owner'
    reply = conv["title"]
    maxlen = 0
    
    for sentence in conv["chats"]:
        if any(word in sentence["value"] for word in filter_list):
            continue
        last_sender = sender
        sender = sentence["sender"]
        if sender == last_sender:
            if sender =='owner':
                s = sentence["value"]
                reply += " " + s
            else:
                if len(sentence["value"]) > maxlen:
                    reply = sentence["value"]
                    maxlen = len(sentence["value"])
        else:
            PW.write(tag[last_sender]+reply+'\n')
            if sender =='owner':
                s = sentence["value"]
                reply = s
            else:
                reply = sentence["value"]
                maxlen = len(sentence["value"])
            
    if sender == last_sender:
            PW.write(tag[last_sender]+reply+'\n')
    PW.write('===\n')

count=0

temp = ''
with open('QA_en_2.txt', 'r',encoding='UTF-8') as FR:
    with open('question_2.txt', 'a+',encoding='UTF-8') as FW:
        with open('answer_2.txt', 'a+',encoding='UTF-8') as FD:
            for line in FR:
                if 'Q:' in line:
                    temp = line[3:]
                elif 'A:' in line:
                    FD.write(line[3:])
                    FW.write(temp)
FR.close()
FW.close()
FD.close()
            



    
            
            
        
