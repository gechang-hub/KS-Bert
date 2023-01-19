# -*- coding: utf-8 -*-
#29分钟

from nlg_yongzhuo.data_preprocess.text_preprocess import extract_chinese
from nlg_yongzhuo.data_preprocess.text_preprocess import cut_sentence
from nlg_yongzhuo.data_preprocess.text_preprocess import jieba_cut
from nlg_yongzhuo.data.stop_words.stop_words import stop_words
# sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

class LDASum:
    def __init__(self):
        self.stop_words = stop_words.values()
        self.algorithm = 'lda'

    def summarize(self, text, num=3, topic_min=3, judge_topic=None):
        """

        :param text: str
        :param num: int
        :return: list
        """
        # 切句
        if type(text) == str:
            self.sentences = cut_sentence(text)
        elif type(text) == list:
            self.sentences = text
        else:
            raise RuntimeError("text type must be list or str")
        len_sentences_cut = len(self.sentences)
        # 切词
        sentences_cut = [[word for word in jieba_cut(extract_chinese(sentence))
                          if word.strip()] for sentence in self.sentences]
        # 去除停用词等
        self.sentences_cut = [list(filter(lambda x: x not in self.stop_words, sc)) for sc in sentences_cut]
        self.sentences_cut = [" ".join(sc) for sc in self.sentences_cut]
        # 计算每个句子的tf
        vector_c = CountVectorizer(ngram_range=(1, 2), stop_words=self.stop_words,analyzer='word',token_pattern=u"(?u)\\b\\w+\\b")
        tf_ngram = vector_c.fit_transform(self.sentences_cut)
        # 主题数, 经验判断
#         topic_num = min(topic_min, int(len(sentences_cut) / 2))  # 设定最小主题数为3
        topic_num = max(1, min(topic_min, int(len(sentences_cut) / 2)))  # 设定最小主题数为3
        lda = LatentDirichletAllocation(n_components=topic_num, max_iter=32,
                                        learning_method='online',
                                        learning_offset=50.,
                                        random_state=2019)
        res_lda_u = lda.fit_transform(tf_ngram.T)
        res_lda_v = lda.components_

        if judge_topic:
            ### 方案一, 获取最大那个主题的k个句子
            ##################################################################################
            topic_t_score = np.sum(res_lda_v, axis=-1)
            # 对每列(一个句子topic_num个主题),得分进行排序,0为最大
            res_nmf_h_soft = res_lda_v.argsort(axis=0)[-topic_num:][::-1]
            # 统计为最大每个主题的句子个数
            exist = (res_nmf_h_soft <= 0) * 1.0
            factor = np.ones(res_nmf_h_soft.shape[1])
            topic_t_count = np.dot(exist, factor)
            # 标准化
            topic_t_count /= np.sum(topic_t_count, axis=-1)
            topic_t_score /= np.sum(topic_t_score, axis=-1)
            # 主题最大个数占比, 与主题总得分占比选择最大的主题
            topic_t_tc = topic_t_count + topic_t_score
            topic_t_tc_argmax = np.argmax(topic_t_tc)
            # 最后得分选择该最大主题的
            res_nmf_h_soft_argmax = res_lda_v[topic_t_tc_argmax].tolist()
            res_combine = {}
            for l in range(len_sentences_cut):
                res_combine[self.sentences[l]] = res_nmf_h_soft_argmax[l]
            score_sen = [(rc[1], rc[0]) for rc in sorted(res_combine.items(), key=lambda d: d[1], reverse=True)]
            #####################################################################################
        else:
            ### 方案二, 获取最大主题概率的句子, 不分主题
            res_combine = {}
            for i in range(len_sentences_cut):
                res_row_i = res_lda_v[:, i]
                res_row_i_argmax = np.argmax(res_row_i)
                res_combine[self.sentences[i]] = res_row_i[res_row_i_argmax]
            score_sen = [(rc[1], rc[0]) for rc in sorted(res_combine.items(), key=lambda d: d[1], reverse=True)]
        num_min = min(num, len(self.sentences))
        return score_sen[0:num_min]


if __name__ == '__main__':
    path = '.\m20_1.xlsx'
    # 使用pandas读入
    excel_data = pd.read_excel(path, names=None,header=None).astype(str)  # 读取文件中所有数据
    excel_data.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    text1 = excel_data[['2']].values.flatten().tolist()
    lda = LDASum()
    re = []
    #for text in text1:
    for i in range(len(text1)):
        doc = text1[i]
        a = doc.count("。")
        b = doc.count('?')
        c = doc.count('？')
        d = doc.count('；')
        e = doc.count(';')
        f = doc.count('!')
        x = doc.count(',')
        y = doc.count('，')
        # m是句数，n是逗号数量
        m = a + b + c + d + e + f
        n = x + y
        if m>1:
            sum = lda.summarize(doc)
            r=[]
            for i in sum:
                r.append(i[1])
            a='。'.join(r)
            re.append(a)
        else:
            re.append(doc)
    # print(re)

    excel_data['2'] = re
    print(excel_data)
    excel_data.to_excel(path, index=False)