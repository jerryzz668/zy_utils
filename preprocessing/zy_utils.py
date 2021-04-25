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
from openpyxl.styles import Font, Alignment
import xml.etree.ElementTree as ET

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

# 写入新的excel   ### 内容， 保存路径, 路径下sheet， 表头， 表头列， 插入位置行数，插入位置列数
def content_to_excel(content, save_path, sheet_name = None, header = False, index=False, row=None, col=None):
    excel_data = pd.DataFrame(content)
    writer = pd.ExcelWriter(save_path)  # 写入Excel文件
    excel_data.to_excel(writer, sheet_name=sheet_name, header=header, index=index, startrow=row, startcol=col)
    writer.save()
    writer.close()

# 追加写入excel（可指定位置）
def write_excel_xlsx_append(file_path, data_name, data, row=0, col=0, sheet_name='sheet1'):
    workbook = xl.load_workbook(file_path)  # 打开工作簿
    sheet = workbook[sheet_name]
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            sheet.cell(row=(i + row + 1), column=(j + col + 1), value=data[i][j])  # 追加写入数据，注意是从i+row行，j + col列开始写入
    workbook.save(file_path)  # 保存工作簿
    print("xlsx格式表格【追加】写入{}成功！".format(data_name))

# 创建一个excel，sheet
def create_empty_excel(save_path, sheet):
    wb = xl.Workbook()
    ws = wb.create_sheet(sheet, 0)
    wb.save(save_path)

# 读取excel中的sheet
def read_excel(excel_path, sheet_name):
    book = xl.load_workbook(excel_path)
    sheet = book[sheet_name]
    return sheet

# 美化excel
def beautify_excel(excel_path):
    font = Font(name='宋体', size=11, color='FF000000', bold=True, italic=False)
    align = Alignment(horizontal='center', vertical='center', wrap_text=False)

    book = xl.load_workbook(excel_path)  # 加载excel
    sheet_names = book.sheetnames  # 获取所有的sheet名称
    sheet_names.remove('Sheet')

    for sheet in sheet_names:
        for row in book['{}'.format(sheet)]['A1:A5']:
            for cell in row:
                cell.font = font
                cell.alignment = align

        for row in book['{}'.format(sheet)]['A12:Z19']:
            for cell in row:
                cell.alignment = align

    book.save(excel_path)

# 创建节点
def create_Node(element, text=None):
    elem = ET.Element(element)
    elem.text = text
    return elem

# 链接节点到根节点
def link_Node(root, element, text=None):
    """
    @param root: element的父节点
    @param element: 创建的element子节点
    @param text: element节点内容
    @return: 创建的子节点
    """
    if text != None:
        text = str(text)
    element = create_Node(element, text)
    root.append(element)
    return element

def compute_iou(bbox1, bbox2):
    """
    compute iou
    """
    bbox1xmin = bbox1[0]
    bbox1ymin = bbox1[1]
    bbox1xmax = bbox1[2]
    bbox1ymax = bbox1[3]
    bbox2xmin = bbox2[0]
    bbox2ymin = bbox2[1]
    bbox2xmax = bbox2[2]
    bbox2ymax = bbox2[3]

    area1 = (bbox1ymax - bbox1ymin) * (bbox1xmax - bbox1xmin)
    area2 = (bbox2ymax - bbox2ymin) * (bbox2xmax - bbox2xmin)

    bboxxmin = max(bbox1xmin, bbox2xmin)
    bboxxmax = min(bbox1xmax, bbox2xmax)
    bboxymin = max(bbox1ymin, bbox2ymin)
    bboxymax = min(bbox1ymax, bbox2ymax)
    if bboxxmin >= bboxxmax:
        return 0
    if bboxymin >= bboxymax:
        return 0

    area = (bboxymax - bboxymin) * (bboxxmax - bboxxmin)
    iou = area / (area1 + area2 - area)
    return iou

class Box:
    # x, y是左上角坐标
    def __init__(self, x, y, w, h, category=None, confidence=None):
        self.category = category
        self.confidence = confidence
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_area(self):
        return self.w * self.h

    def get_iou(self, box2):
        inter_area = calculate_inter_area(self, box2)
        return inter_area/(self.get_area()+box2.get_area()-inter_area)

def calculate_inter_area(box1, box2):
    '''
    :param box1: Box对象
    :param box2: Box对象
    :return: box1与box2的交面积
    '''
    left_x, left_y = max([box1.x, box2.x]), max([box1.y, box2.y])
    right_x, right_y = min([box1.x + box1.w, box2.x + box2.w]), min([box1.y + box1.h, box2.y + box2.h])
    height = right_y - left_y
    width = right_x - left_x
    area = height * width if height>0 and width>0 else 0
    return area