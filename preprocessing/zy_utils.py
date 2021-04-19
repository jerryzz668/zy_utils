"""
description: my dependent utils
author: zhangyan
date: 2021-04-02 17:42
"""

import os
import json
import pandas as pd
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

def content_to_excel(content, save_path):
    excel_data = pd.DataFrame(content)
    writer = pd.ExcelWriter(save_path)		# 写入Excel文件
    excel_data.to_excel(writer, 'page_1', float_format='%.5f')		# ‘page_1’是写入excel的sheet名
    writer.save()
    writer.close()