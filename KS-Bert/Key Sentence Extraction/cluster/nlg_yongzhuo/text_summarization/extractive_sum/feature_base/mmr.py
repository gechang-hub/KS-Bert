# -*- coding: utf-8 -*-

from nlg_yongzhuo.data_preprocess.text_preprocess import extract_chinese, cut_sentence
from nlg_yongzhuo.data_preprocess.text_preprocess import jieba_cut,tfidf_fit
from nlg_yongzhuo.data.stop_words.stop_words import stop_words
# # sklearn
# from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
import copy


class MMRSum:
    def __init__(self):
        self.stop_words = stop_words.values()
        self.algorithm = 'mmr'

    def summarize(self, text, num=3, alpha=0.6):
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
        # 切词
        sentences_cut = [[word for word in jieba_cut(extract_chinese(sentence))
                          if word.strip()] for sentence in self.sentences]
        # 去除停用词等
        self.sentences_cut = [list(filter(lambda x: x not in self.stop_words, sc)) for sc in sentences_cut]
        self.sentences_cut = [" ".join(sc) for sc in self.sentences_cut]
        # # 计算每个句子的词语个数
        # sen_word_len = [len(sc)+1 for sc in sentences_cut]
        # 计算每个句子的tfidf
        sen_tfidf = tfidf_fit(self.sentences_cut)
        # 矩阵中两两句子相似度
        SimMatrix = (sen_tfidf * sen_tfidf.T).A # 例如: SimMatrix[1, 3]  # "第2篇与第4篇的相似度"
        # 输入文本句子长度
        len_sen = len(self.sentences)
        # 句子标号
        sen_idx = [i for i in range(len_sen)]
        summary_set = []
        mmr = {}
        for i in range(len_sen):
            if not self.sentences[i] in summary_set:
                sen_idx_pop = copy.deepcopy(sen_idx)
                sen_idx_pop.pop(i)
                # 两两句子相似度
                sim_i_j = [SimMatrix[i, j] for j in sen_idx_pop]
                score_tfidf = sen_tfidf[i].toarray()[0].sum() # / sen_word_len[i], 如果除以词语个数就不准确
                mmr[self.sentences[i]] = alpha * score_tfidf - (1 - alpha) * max(sim_i_j)
                summary_set.append(self.sentences[i])
        score_sen = [(rc[1], rc[0]) for rc in sorted(mmr.items(), key=lambda d: d[1], reverse=True)]
        if len(mmr) > num:
            score_sen = score_sen[0:num]
        return score_sen


if __name__ == '__main__':
    path = '.\m140_1.xlsx'
    # 使用pandas读入
    excel_data = pd.read_excel(path, names=None).astype(str)  # 读取文件中所有数据
    # excel_data.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
    #                       '17','18','19']
    text1 = excel_data[['6']].values.flatten().tolist()

    mmr_sum = MMRSum()
    re = []
    #for text in text1:
    for i in range(len(text1)):
        doc = text1[i]
        a = doc.count("。")
        if a>2:
            sum = mmr_sum.summarize(doc)
            r=[]
            for i in sum:
                r.append(i[1])
            a='。'.join(r)
            re.append(a)
        else:
            re.append(doc)
    # print(re)
    #
    excel_data['6'] = re
    print(excel_data)
    excel_data.to_excel(path, index=False)







