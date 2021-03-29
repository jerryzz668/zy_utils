# _*_ coding:utf-8 _*_
from xml.etree import ElementTree as ET
import os

class_dic = {}
shape_dic = {}
bbox_dic = {}
cls_dic = {}
shape_class = {}
xml_dir = r"C:\Users\Administrator\Desktop\compare\compare\rending\guaijiao\outputs"


def pro_one_xml(xml_path):
    tree = ET.parse(xml_path)
    root_node = tree.getroot()
    img_path = root_node[0]
    for i in root_node.iter('item'):
        name = i[0].text
        width = i[1]
        shape = i[2].tag
        axis = []
        if shape not in shape_class:
            shape_class[shape] = [name]
        else:
            shape_class[shape].append(name)
        if shape == 'bndbox':
            bbox_dic[shape] = xml_path
        for k in i[2]:
            axis.append(k.text)
        if shape not in shape_dic:
            shape_dic[shape] = axis
        else:
            shape_dic[shape] = shape_dic[shape] + axis
        c_name = '{}_{}'.format(name, shape)
        if c_name not in class_dic:
            class_dic[c_name] = 1
        else:
            class_dic[c_name] += 1
        if name not in cls_dic:
            cls_dic[name] = 1
        else:
            cls_dic[name] += 1


for i in os.listdir(xml_dir):
    xml_path = os.path.join(xml_dir, i)
    print('parsing: {}'.format(xml_path))
    pro_one_xml(xml_path)
cc = 0
for i in class_dic:
    name, shape = i.split('_')
    print(name, shape, class_dic[i])
    cc += class_dic[i]
import pypinyin


def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s


print(bbox_dic)
print(class_dic)
print(cls_dic)

piny = []
for i in cls_dic:
    piny.append(pinyin(i))
dic_shape = {}
for i in shape_class:
    dic_shape[i] = list(set(shape_class[i]))
print('汉字类别：', cls_dic.keys())
print('汉字拼音类别：', piny)
print(dic_shape)
print('形状类别：', shape_dic.keys())
print('类别个数：', len(cls_dic), '总目标数：', cc)

piny.sort()
print('汉字拼音排序类别：', piny)
piny_dict = {}
for i, val in enumerate(piny):
    # print(i, val)
    # dict_val = {val, i}
    piny_dict.update({val: i+1})

print('排序字典', piny_dict)
