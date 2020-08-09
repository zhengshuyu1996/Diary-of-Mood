# coding=utf-8
import os
import random
import jieba
import json

gConfig = {
    'resource_data': './efaqa-corpus-zh.utf8',
    'train_enc': 'working_dir/train.enc',
    'train_dec': 'working_dir/train.dec',
    'test_enc': 'working_dir/test.enc',
    'test_dec': 'working_dir/test.dec'
}

conv_path = gConfig['resource_data']

if not os.path.exists(conv_path):
    exit()


convs = []  # 用于存储对话集合
ask = []        # 问
response = []   # 答

lines = open(conv_path, encoding='utf-8').readlines()
for line in lines:
    conv = json.loads(line)
    conv = conv["chats"]
    if len(conv) == 1:
        continue

    conv = [" ".join(jieba.cut(i["value"])) for i in conv]

    last_ask = ""
    for i in conv:
        if len(last_ask) > 0:
            ask += [last_ask]
            response += [i]
        last_ask = i

print('Total length:', len(ask))

def convert_seq2seq_files(questions, answers, TESTSET_SIZE):
    # 创建文件
    train_enc = open(gConfig['train_enc'],'w')  # 问
    train_dec = open(gConfig['train_dec'],'w')  # 答
    test_enc  = open(gConfig['test_enc'], 'w')  # 问
    test_dec  = open(gConfig['test_dec'], 'w')  # 答

    test_index = random.sample([i for i in range(len(questions))],TESTSET_SIZE)

    for i in range(len(questions)):
        if i in test_index:
            test_enc.write(questions[i]+'\n')
            test_dec.write(answers[i]+ '\n' )
        else:
            train_enc.write(questions[i]+'\n')
            train_dec.write(answers[i]+ '\n' )
        if i % 1000 == 0:
            print(len(range(len(questions))), '处理进度：', i)

    train_enc.close()
    train_dec.close()
    test_enc.close()
    test_dec.close()

convert_seq2seq_files(ask, response, 20000)
# 生成的*.enc文件保存了问题
# 生成的*.dec文件保存了回答
