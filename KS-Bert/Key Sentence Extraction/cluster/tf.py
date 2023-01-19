#https://www.csdn.net/tags/NtjaUgzsNjc3MDktYmxvZwO0O0OO0O0O.html
# -*- coding: utf-8 -*-
#耗时五分钟
import jieba
import chardet
#读文档
import pandas as pd
path = '.\dataset\m140_1.xlsx'
# 使用pandas读入
excel_data = pd.read_excel(path,names=None,header=None).astype(str) #读取文件中所有数据
excel_data.columns=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
text1 = excel_data[['2']].values.flatten().tolist()
re=[]
for text in text1:

    document=text.replace(" ", "").replace('"', '')
    #文本只保留汉字，数字，英文，标点符号
    document = document.replace(' ', '')

    #划分句子后存入列表
    sentence_list = document.split('。')
    for m in range(len(sentence_list)):
        print(m,sentence_list[m])

    words = []
    frequency = {}
    for i in range(len(sentence_list)):
        for word in jieba.lcut(sentence_list[i]):
                # b=chardet.detect(str.encode(word))['encoding']
                # print(b)
            if chardet.detect(str.encode(word))['encoding'] !=None:
                    words.append(word)

        #去停用词
    stopwords = [line.strip() for line in open('./dataset/stopKeyWords.txt',encoding='UTF-8').readlines()]
    new_words = []
    for word in words:
        if word not in stopwords:
            new_words.append(word)
        # print(new_words)

        #词频
    dic = {}
    for word in new_words:
        if word not in dic:
            dic[word] = 1
        else:
            dic[word] = dic[word] + 1

        #词频统计得分
    res = []
    for i in range(len(sentence_list)):
        score = 0
        for word in jieba.lcut(sentence_list[i]):
            score += dic.get(word, 0)
        res.append(score)
        print('词频')
        print(res)

    score_dic = {}
    for i in range(len(sentence_list)):
        score_dic[i] = res[i]
        print(score_dic)

    result = sorted(score_dic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)

    def extrct(num):
        res = []
        for i in range(num):
            if len(sentence_list[result[i][0]]) > 0:
                 res.append(sentence_list[result[i][0]])
        return res

    extrct(1)

    score_dic = {}
    for i in range(len(sentence_list)):
        score_dic[i] = res[i]/ (len(jieba.lcut(sentence_list[i])) + 1)
        # print('1')
        print(score_dic)

        #比较大小
    e = sorted(score_dic.items(), key = lambda e:e[1])
    e1 = []
    for i in e:
         e1.append(i[0])
    print(e1)
    key=[]#取出前3句最重要的话的顺序
    if len(e1)>3:
        key.append(e1[len(e1)-1])
        key.append(e1[len(e1)-2])
        key.append(e1[len(e1) - 3])
        key.append(e1[len(e1) - 4])
        key.append(e1[len(e1) - 5])
        key.append(e1[len(e1) - 6])
        key.append(e1[len(e1) - 7])
        key.append(e1[len(e1) - 8])

        sen=[]

        for i in range(len(key)):
            sen.append(sentence_list[key[i]])
        a = ",".join(str(m) for m in sen)
        #print(a)

        re.append(a)

    else:
        re.append(document)



        #根据句数输出句的内容

excel_data['2']=re
print(excel_data)
excel_data.to_excel(path,index=False)

