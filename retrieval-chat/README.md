# Auto Reply Based on Retrieval

对语料的预处理脚本的结果在corpus目录下，获得自动回复的代码在run.py中。

用bert-utils，基于bert预训练模型生成句向量。https://github.com/terrifyzhao/bert-utils
一个句向量生成的例子：
```
from bert.extrac_feature import BertVector
bv = BertVector()
bv.encode(['今天天气不错'])
```

将所有question转为句向量后，用Annoy构建向量索引树，存在test.ann文件中。https://github.com/spotify/annoy
注意：Annoy需要用pip install --user annoy获取；test.ann有可能超出github允许的最大文件，如果出错，可以联系jiayu获得完整文件。
一个通过Annoy获取最近邻向量的例子：
```
testq = bv.encode(['又失眠了 感觉工作压力太大 太焦虑了']) # get sentence embedding
res = t.get_nns_by_vector(testq[0], 5) # find 5 nearest
candidate = [ans[res[i]] for i in range(5)]
reply = max(candidate, key=len, default='') # pick the longest one as final reply
print(reply)
```



