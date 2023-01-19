#coding='utf-8'
#小于1min
import pandas as pd
path = '.\data\m20_1.xlsx'
# 使用pandas读入
excel_data = pd.read_excel(path,names=None,header=None).astype(str) #读取文件中所有数据
excel_data.columns=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
text1 = excel_data[['2']].values.flatten().tolist()
# 按列分离数据

# data_li = data.values.tolist()
# # print (data_li)
# text = []
# for s_li in data_li:
#     text.append(s_li)
#
# print(text[0])
# print(text[1])
# print(text[2])

#提取关键句
from textrank4zh import TextRank4Sentence
re=[ ]#建立存储分词的列表
for text in text1:
    #分情况计算句子长度：以逗号，问好，分号，句号，感叹号划分

        print(text)

        # text = text[i]
        tr4s = TextRank4Sentence()
        tr4s.analyze(text=text, lower=True, source='no_stop_words')
        key_sentences = tr4s.get_key_sentences(num=2, sentence_min_len=1)
        list = []
        for sentence in key_sentences:
            print(sentence['weight'], sentence['sentence'])
            list.append(sentence['sentence'])
            a = ",".join(str(i) for i in list)
        re.append(a)
    # except:
    #     re.append('1')
#print(re[0])#将所有分词结果存入re列表

#依次写入result列
excel_data['2']=re
print(excel_data)
excel_data.to_excel(path,index=False)



