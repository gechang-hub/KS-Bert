#coding='utf-8'
import pandas as pd
path = '.\data\卫辉.xlsx'
# 使用pandas读入
excel_data = pd.read_excel(path,names=None).astype(str) #读取文件中所有数据
data=excel_data['发布时间']
data_li = data.values.tolist()
text = []
for s_li in data_li:
    text.append(s_li)

#方法一：
a={}
for i in text:
    a[i] = text.count(i)
print(a)

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

x=list(a.keys())
y=list(a.values())
print(y)

path = '.\data\卫辉.xlsx'
# 使用pandas读入
excel_data = pd.read_excel(path,names=None).astype(str) #读取文件中所有数据
data_pre=excel_data['lda_pre']
data_li_pre = data_pre.values.tolist()
text_pre = []
for s_li_pre in data_li_pre:
    text_pre.append(s_li_pre)
i=0
class0=[]
class1=[]
class2=[]
class3=[]
class4=[]
class5=[]
class6=[]
class7=[]
for n in range(len(y)):
    m = []
    while(i<len(text_pre)):
        m=text_pre[i:i+y[n]]
        i=i+y[n]
        break
    class0.append(m.count('0'))
    class1.append(m.count('1'))
    class2.append(m.count('2'))
    class3.append(m.count('3'))
    class4.append(m.count('4'))
    class5.append(m.count('5'))
    class6.append(m.count('6'))
    class7.append(m.count('7'))
print(class0)
print(class1)
print(class2)
print(class3)
print(class4)
print(class5)
print(class6)
print(class7)

width = 0.5

fig, ax = plt.subplots()
plt.xticks(rotation = 90)
ax.bar(x, class0, width, label='0')
ax.bar(x, class1, width, label='1')
ax.bar(x, class2, width, label='2')
ax.bar(x, class3, width, label='3')
ax.bar(x, class4, width, label='4')
ax.bar(x, class5, width, label='5')
ax.bar(x, class6, width, label='6')
ax.bar(x, class7, width, label='7')

ax.set_ylabel('Y')
ax.set_title('lda_pre')
ax.legend()  #显示图中左上角的标识区域

plt.show()







