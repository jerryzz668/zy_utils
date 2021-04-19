# @Description:
# @Author     : zhangyan
# @Time       : 2021/4/19 8:48 下午

import numpy as np
import pandas as pd
import xlsxwriter

def confusion_mtx_to_report(data):
    loushi = []
    gt_num = []
    loujian_ratio = []
    guojian = []
    jianchu = []
    guojian_ratio = []

    for i in range(len(data)):
        loushi.append(data[i][-1])
    loushi.pop()  # 漏检数量

    for i in range(len(data)):
        gt_num.append(sum(data[i]))
    gt_num.pop()  # gt数量

    for i in range(len(loushi)):
        loujian_ratio.append(round(loushi[i]/gt_num[i], 2))  # 漏检率
    print(loujian_ratio)

    guojian = data[-1]
    guojian.pop()  # 过检数量

    for i in range(len(guojian)):
        jianchu.append(sum(guojian))  # 检出总量

    for i in range(len(guojian)):
        guojian_ratio.append(round(guojian[i]/sum(guojian), 2))  # 过检率
    print(guojian_ratio)

    excel_content = []
    excel_content.extend((gt_num, loushi, loujian_ratio, jianchu, guojian, guojian_ratio))
    return excel_content

def content_to_excel(content, save_path):
    excel_data = pd.DataFrame(content)
    writer = pd.ExcelWriter(save_path)		# 写入Excel文件
    excel_data.to_excel(writer, 'page_1', float_format='%.5f')		# ‘page_1’是写入excel的sheet名
    writer.save()
    writer.close()

if __name__ == '__main__':
    data = \
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
         [0, 78, 0, 2, 0, 0, 0, 0, 0, 0, 0, 144],
         [0, 0, 64, 0, 0, 0, 0, 0, 0, 0, 0, 62],
         [0, 4, 0, 96, 0, 3, 0, 0, 0, 0, 1, 128],
         [0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 5],
         [0, 1, 0, 1, 0, 22, 0, 0, 3, 1, 0, 65],
         [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 3],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 8],
         [0, 0, 0, 1, 2, 1, 0, 0, 1, 8, 0, 11],
         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 2],
         [1, 275, 90, 128, 5, 56, 0, 0, 5, 9, 5, 0]]
    save_path = '/Users/zhangyan/Desktop/A.xlsx'
    content = confusion_mtx_to_report(data)
    content_to_excel(content, save_path)

