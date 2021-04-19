# @Time    : 2021/4/19 下午8:48
# @Author  : zhangyan
# @Description:

import numpy as np
import pandas as pd

data = \
[[0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   3],
 [0,  78,   0,   2,   0,   0,   0,   0,   0,   0,   0, 144],
 [0,   0,  64,   0,   0,   0,   0,   0,   0,   0,   0,  62],
 [0,   4,   0,  96,   0,   3,   0,   0,   0,   0,   1, 128],
 [0,   0,   0,   0,   7,   0,   0,   0,   0,   0,   0,   5],
 [0,   1,   0,   1,   0,  22,   0,   0,   3,   1,   0,  65],
 [0,   0,   0,   0,   0,   0,   2,   0,   0,   0,   0,   3],
 [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1],
 [0,   0,   0,   0,   0,   0,   0,   0,   2,   0,   0,   8],
 [0,   0,   0,   1,   2,   1,   0,   0,   1,   8,   0,  11],
 [0,   0,   0,   0,   0,   1,   0,   0,   0,   0,   2,   2],
 [1, 275,  90, 128,   5,  56,   0,   0,   5,   9,   5,   0]]

loushi = []
gt_num = []
loujian_ratio = []
guojian = []
jianchu = []
guojian_ratio = []

for i in range(len(data)):
    loushi.append(data[i][-1])
loushi.pop()  # 漏检数量
print(loushi)

for i in range(len(data)):
    gt_num.append(sum(data[i]))
gt_num.pop()  # gt数量
print(gt_num)

for i in range(len(loushi)):
    loujian_ratio.append(round(loushi[i]/gt_num[i], 2))  # 漏检率
print(loujian_ratio)

guojian = data[-1]
guojian.pop()  # 过检数量
print(guojian)

for i in range(len(guojian)):
    jianchu.append(sum(guojian))  # 检出总量
print(jianchu)

for i in range(len(guojian)):
    guojian_ratio.append(round(guojian[i]/sum(guojian), 2))  # 过检率
print(guojian_ratio)

excel_content = []
excel_content.append(gt_num)
excel_content.append(loushi)
excel_content.append(loujian_ratio)
excel_content.append(jianchu)
excel_content.append(guojian)
excel_content.append(guojian_ratio)
print(excel_content)

excel_data = pd.DataFrame(excel_content)
save_path = '/home/zj-1/Desktop/A.xlsx'
writer = pd.ExcelWriter(save_path)		# 写入Excel文件
excel_data.to_excel(writer, 'page_1', float_format='%.5f')		# ‘page_1’是写入excel的sheet名
writer.save()

writer.close()

