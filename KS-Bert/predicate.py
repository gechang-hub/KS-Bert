import time

import pandas as pd

from data_process import Token, process, batch_iter
from bert_classify import *
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

best = 0.0
n = 0
print("Loading Training data...")
print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
input_id, input_segment_, mask_, label = Token(pm.train_filename)
print(label)
test_id, test_segment, test_mask, test_label = Token(pm.test_filename)

label = process(label)
print(label)
def evaluate(sess, test_id, test_segment, test_mask, test_label):
    A = 1e-10
    pre_label=[]
    pre_label=[]
    a=len(test_label)
    for i in range(len(test_label)):
        pre_lab = sess.run(predict, feed_dict={input_x: [test_id[i]],
                                               input_segment: [test_segment[i]],
                                               mask: [test_mask[i]],
                                               keep_pro: 1.0})
        #print(pre_lab)
        a=len(test_label)
        pre_label.append(pre_lab)
        result = test_label[i]#真实的
        if int(pre_lab) == int(result):
            A += 1

    #P = A / float(len(test_label))

    return pre_label,a

pre_label,a= evaluate(session, test_id, test_segment, test_mask, test_label)
print(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()))
# predict_label=[]
# for i in range(len(pre_label)):
#     predict_label.append(pre_label[i][0])
# print(predict_label)

b = []
for i in range(a):
     c=pre_label[i][0]
     b.append(c)
print(b)
df = pd.DataFrame(b, columns=['pre'])
df.to_excel("./官050pre.xlsx", index=False)

