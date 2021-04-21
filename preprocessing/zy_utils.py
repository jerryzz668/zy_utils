"""
description: my dependent utils
author: zhangyan
date: 2021-04-02 17:42
"""

import os
import json
import pandas as pd
import openpyxl as xl
from pypinyin import pinyin, NORMAL

def mkdir(save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)


def json_to_instance(json_file_path):
    '''
    :param json_file_path: json文件路径
    :return: json instance
    '''
    with open(json_file_path, 'r', encoding='utf-8') as f:
        instance = json.load(f)
    return instance

def filtrate_file(path):
    list = os.listdir(path)
    for obj in list:
        file_path = os.path.join(path, obj)
        if not os.path.isfile(file_path) or obj[obj.rindex('.') + 1:] not in ['json', 'jpg', 'png']: continue

def word_to_pinyin(word):
    """
    @param word:
    @return:
    """
    # pinyin return [[py1],[py2],...,[pyn]]
    s = ''
    for i in pinyin(word, style=NORMAL):
        s += i[0].strip()
    return s

def read_txt(path):
    with open(path, "r") as f:  # 打开文件
        data = f.read()  # 读取文件
    return data

def content_to_excel(content, save_path, header = False, index=False, row=None, col=None):  # 写入内容， 保存路径, 表头， 表头列， 插入位置行数，插入位置列数
    excel_data = pd.DataFrame(content)
    writer = pd.ExcelWriter(save_path)		# 写入Excel文件
    # excel_data.to_excel(writer, 'page_1', float_format='%.5f')		# ‘page_1’是写入excel的sheet名
    excel_data.to_excel(writer, sheet_name='page_1', header=header, index=index, startrow=row, startcol=col)
    writer.save()
    writer.close()

def write_excel_xlsx_append(file_path, data, row=0, col=0, sheet_name='sheet1'):  # 追加写入excel（可指定位置）
    workbook = xl.load_workbook(file_path)  # 打开工作簿
    sheet = workbook[sheet_name]
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            sheet.cell(row=(i + row + 1), column=(j + col + 1), value=data[i][j])  # 追加写入数据，注意是从i+row行，j + col列开始写入
    workbook.save(file_path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")