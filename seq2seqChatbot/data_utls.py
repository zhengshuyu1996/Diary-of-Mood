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

    last_ask = json.loads(line)["title"]
    longest_ans = ""
    num = 0

    for message in conv:
        if (message["sender"] == "owner" or num+1 == len(conv)):
            if len(longest_ans) > 0:
                last_ask = last_ask.replace('\\n', '').replace('\\r', '').replace('\\t', '')\
                                    .replace(chr(9), '').replace(chr(10), '').replace(chr(13), '')
                last_ask = " ".join(jieba.cut(last_ask))
                ask += [last_ask]
                longest_ans = longest_ans.replace('\\n', '').replace('\\r', '').replace('\\t', '')\
                                    .replace(chr(9), '').replace(chr(10), '').replace(chr(13), '')
                longest_ans = " ".join(jieba.cut(longest_ans))
                response += [longest_ans]

                longest_ans = ""
                last_ask = message["value"]
        else:
            if not ("付费" in message["value"] or "付款" in message["value"] or "头像" in message["value"] or "咨询" in message["value"] or message["label"]["negative"]):
                if len(message["value"]) > len(longest_ans):
                    longest_ans = message["value"]
        num += 1

print('Total length:', len(ask))
print('Total length:', len(response))

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

convert_seq2seq_files(ask, response, 10000)
# 生成的*.enc文件保存了问题
# 生成的*.dec文件保存了回答
