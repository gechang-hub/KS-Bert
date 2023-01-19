#coding='utf-8'

# 提取数据
import pandas as pd
path = '.\data\HN.xlsx'
# 使用pandas读入
excel_data = pd.read_excel(path,names=None).astype(str) #读取文件中所有数据
#excel_data.columns=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18']
data=excel_data['微博正文']
# 按列分离数据

data_li = data.values.tolist()
# print (data_li)
text = []
for s_li in data_li:
    # print(s_li)
    # print(s_li[0])
    text.append(s_li)
# print(text)
r=[ ]#建立存储分词的列表

import re
import emoji
for i in range(len(text)):
    # print(text[i])
    new_datas=text[i]
    # print(new_datas)
    # 去除原始字符串中的url
    url_reg = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    new_datas = re.sub(url_reg, '', new_datas)
    # print('1')
    # 去除艾特用户
    new_datas = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", new_datas)
    # 去除转发
    re_reg = r'@.+:'
    new_datas = re.sub(re_reg, '', new_datas)
    # 去除“O网页链接”或者是“O网页”
    web_reg = r'腾讯文档互助链接：O网页链接|O网页链接|O网页'
    new_datas = re.sub(web_reg, '', new_datas)
    # 去除“L...的微博（视频）”
    video_reg = r'L.+的微博视频|L.+的微博|微博放映厅|求助视频'  # 两边固定 中间任意字符/aa.+bb/
    new_datas = re.sub(video_reg, '', new_datas)
    # 去除“(记者 xxx)”等小括号内容，包括（），文本结尾不完整内容（xxx
    reporter_reg = r'（.*?）|（[\u4e00-\u9fa5]+\D+[\u4e00-\u9fa5]+）?|（[\u4e00-\u9fa5]+）?'
    new_datas = re.sub(reporter_reg, '', new_datas)
    # 去除原始字符串中的emoji字符“[]”
    new_datas = re.sub('\[.*?\]', '', new_datas)
    emoji.demojize(new_datas)
    # 去除无意义的特定词语
    meaningless = '#综艺剪辑#|#下饭综艺#|#影视剪辑#|#盛夏理想色#|#镜头下的家乡#'
    new_datas = re.sub(meaningless, '', new_datas)
    # # # 去除日期，格式“2021（。-年）7（。-月）21（。-日）15时15分”
    # time_reg = r'\d{1,2}[时]{1}\d{1,2}[分]{1}|\d{1,2}[时]{1}|\d{1,2}[\.\-/月]{1}\d{1,2}[\.\-/日]|\d{4}[\.\-/年]{1}\d{1,2}[\.\-/月]{1}\d{1,2}[日]{1}|\d{1,2}[日]{1}'
    # new_datas = re.sub(time_reg, '', new_datas)
    # text_num = len(re.findall(r'[\u4E00-\u9FFF]', new_datas))
    # print(text_num)
    #  去除数字
    #new_datas = re.sub(r'\d', '', new_datas)
    r.append(new_datas)

excel_data['微博正文']=r
print(excel_data)
excel_data.to_excel(path,index=False)
