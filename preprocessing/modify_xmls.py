# @Description:
# @Author     : zhangyan
# @Time       : 2020/12/30 10:45 上午

import xml.etree.ElementTree as ET
from xml.dom import minidom
import time
import os

# 保存为XML文件（美化后）
def save_XML(root, filename, indent="", newl="", encoding="utf-8"):
    rawText = ET.tostring(root)
    dom = minidom.parseString(rawText)
    with open(filename, 'w', encoding="utf-8") as f:
        dom.writexml(f, "", indent, newl, encoding)

# 修正name中带有'刮伤-边'的类别
def modify_xml(xml_path, save_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    object = root[1][0]
    for item in object.findall('item'):
        # using root.findall() to avoid removal during traversal
        category = item.find('name').text
        if '-' in category:  # 修正xml
            # object.remove(item)
            category_modify = category.split('-')[0]
            item.find('name').text = category_modify
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_name = xml_path[xml_path.rindex(os.sep)+1:]
    xml_save_path = os.path.join(save_path, save_name)
    save_XML(root, xml_save_path)

def modify_xmls(xml_path, save_path):
    t = time.time()
    xml_list = os.listdir(xml_path)
    for xml in xml_list:
        xml_file = os.path.join(xml_path, xml)  # 输入xml文件
        modify_xml(xml_file, save_path)
        print('{}'.format(xml) + ' has been modified!')
    print('解析耗时: {}'.format(time.time()-t))

if __name__ == '__main__':
    xml_path = '/Users/zhangyan/Desktop/xml'  # xml_folder
    save_path = '/Users/zhangyan/Desktop/xml_save'  # Automatically create a save_path folder
    modify_xmls(xml_path, save_path)


