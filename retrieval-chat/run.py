# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 14:58:47 2020

@author: Think
"""

from extract_feature import BertVector
from annoy import AnnoyIndex

f = 768
t = AnnoyIndex(f, 'angular')

q=[]
bv = BertVector()
'''
i = 0
with open('corpus/question_2.txt', 'r',encoding='UTF-8') as DR:
    for line in DR:
        if len(line)>0:
            q.append(line)
            v = bv.encode([line])
            t.add_item(i,v[0])
            i += 1
DR.close()
'''

#load the answers
ans = []
with open('corpus/answer_2.txt', 'r',encoding='UTF-8') as DR:
    for line in DR:
        if len(line)>0:
            ans.append(line)
DR.close()

#t.build(6000)
#t.save('test.ann')

#load the index tree
t.load('test.ann')

#retrieval
testq = bv.encode(['又失眠了 感觉工作压力太大 太焦虑了']) # get sentence embedding
res = t.get_nns_by_vector(testq[0], 5) # find 5 nearest
candidate = [ans[res[i]] for i in range(5)]
reply = max(candidate, key=len, default='') # pick the longest one as final reply
print(reply)

testq = bv.encode(['今天一个人去吃饭 感觉非常孤独 有很多话不知道该和谁说'])
res = t.get_nns_by_vector(testq[0], 5)
candidate = [ans[res[i]] for i in range(5)]
reply = max(candidate, key=len, default='')
print(reply)

testq = bv.encode(['马上要考试了 担心考砸 真的好紧张'])
res = t.get_nns_by_vector(testq[0], 5)
candidate = [ans[res[i]] for i in range(5)]
reply = max(candidate, key=len, default='')
print(reply)


testq = bv.encode(['分手太痛苦了！需要多久才能好啊 忍不住去想他'])
res = t.get_nns_by_vector(testq[0], 5)
candidate = [ans[res[i]] for i in range(5)]
reply = max(candidate, key=len, default='')
print(reply)

testq = bv.encode(['感觉和同事很难相处，今天又和他们吵架了'])
res = t.get_nns_by_vector(testq[0], 5)
candidate = [ans[res[i]] for i in range(5)]
reply = max(candidate, key=len, default='')
print(reply)

testq = bv.encode(['又失业了 生存压力好大 感觉未来没有希望'])
res = t.get_nns_by_vector(testq[0], 5)
candidate = [ans[res[i]] for i in range(5)]
reply = max(candidate, key=len, default='')
print(reply)

testq = bv.encode(['我感觉自己抑郁了，最近很烦，看什么都生气'])
res = t.get_nns_by_vector(testq[0], 5)
candidate = [ans[res[i]] for i in range(5)]
reply = max(candidate, key=len, default='')
print(reply)

testq = bv.encode(['要毕业了 但还没有找到工作 很迷茫 不知道未来怎么办'])
res = t.get_nns_by_vector(testq[0], 5)
candidate = [ans[res[i]] for i in range(5)]
reply = max(candidate, key=len, default='')
print(reply)

