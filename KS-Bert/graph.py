import pandas as pd
def excel_one_line_to_list():
    df = pd.read_excel("./测pre.xlsx", usecols=[0],
                       names=None)  # 读取项目名称列,不要列名
    df_li = df.values.tolist()
    result = []
    for s_li in df_li:
        result.append(s_li[0])
    print(result)
if __name__ == '__main__':
    excel_one_line_to_list()