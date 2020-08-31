# coding: utf-8

from __future__ import print_function

import os
import tensorflow as tf
import tensorflow.contrib.keras as kr
import sys
sys.path.append('..')
from sosClassify.cnn_model import TCNNConfig, TextCNN
from sosClassify.data.cnews_loader import read_category, read_vocab

try:
    bool(type(unicode))
except NameError:
    unicode = str


class CnnModel:
    def __init__(self):
        base_dir = '../sosClassify/data/'
        vocab_dir = os.path.join(base_dir, 'vocab.txt')
        save_dir = '../sosClassify/checkpoints/textcnn'
        save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径

        self.config = TCNNConfig()
        self.categories, self.cat_to_id = read_category()
        self.words, self.word_to_id = read_vocab(vocab_dir)
        self.config.vocab_size = len(self.words)
        self.model = TextCNN(self.config)

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型

    def predict(self, message):
        # 支持不论在python2还是python3下训练的模型都可以在2或者3的环境下运行
        content = unicode(message)
        data = [self.word_to_id[x] for x in content if x in self.word_to_id]

        feed_dict = {
            self.model.input_x: kr.preprocessing.sequence.pad_sequences([data], self.config.seq_length),
            self.model.keep_prob: 1.0
        }

        y_pred_cls = self.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        return y_pred_cls[0]


sos_model = CnnModel()


if __name__ == '__main__':
    test_demo = ['女 在生气的时候控制不住自己的脾气 会有想自残的倾向 觉得生无可恋 信任不了所有人 亲人 包括自己的父母',
                 '又一次用刀划伤了自己，不想活了',
                 '分手太痛苦了！需要多久才能好啊 忍不住去想他']
    for i in test_demo:
        print(sos_model.predict(i))
