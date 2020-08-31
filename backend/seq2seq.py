#!/usr/bin/env Python
# coding=utf-8

import os
import jieba
import sys
sys.path.append('..')
import tensorflow as tf
from seq2seqChatbot import execute

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


'''
    初始化seq2seqModel
'''
#_________________________________________________________________
seq_sess = tf.Session()
seq_sess, seq_model, enc_vocab, rev_dec_vocab = execute.init_session(seq_sess, conf='../seq2seqChatbot/seq2seq_serve.ini')
print('load session')
#_________________________________________________________________


def reply(req_msg):

    # req_msg = request.form['msg']
    # res_msg = '^_^'

    req_msg = " ".join(jieba.cut(req_msg))
    # print(req_msg)
    # print(''.join([f+' ' for fh in req_msg for f in fh]))
    # req_msg=''.join([f+' ' for fh in req_msg for f in fh])
    print(req_msg)

    res_msg = execute.decode_line(seq_sess, seq_model, enc_vocab, rev_dec_vocab, req_msg)

    res_msg = res_msg.replace('_UNK', '^_^')
    res_msg = res_msg.strip()

    # 如果接受到的内容为空，则给出相应的恢复
    if res_msg == '':
        res_msg = '请与我聊聊天吧'

    return res_msg


if __name__ == '__main__':
    sent = '分手太痛苦了！需要多久才能好啊 忍不住去想他'
    print(reply(sent))
