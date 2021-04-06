# @Description: json->xml
# @Author     : zhangyan
# @Time       : 2020/12/25 4:28 下午

import json
import os
import time
import xml.etree.ElementTree as ET
from xml.dom import minidom
from concurrent.futures.thread import ThreadPoolExecutor

def create_Node(element, text=None):
    elem = ET.Element(element)
    elem.text = text
    return elem

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

# 保存为XML文件（美化后）
def saveXML(root, filename, indent="\t", newl="\n", encoding="utf-8"):
    rawText = ET.tostring(root)
    dom = minidom.parseString(rawText)
    with open(filename, 'w', encoding='utf-8') as f:
        dom.writexml(f, "", indent, newl, encoding)

def json_to_instance(json_file_path):
    """
    @param json_file_path: json文件路径
    @return: json_instance
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        instance = json.load(f)
    return instance

def get_json_data(json_path):
    json_data = json_to_instance(json_path)

    xmlpath = json_data.get('xmlPath')
    img_name = json_data.get('imagePath')
    save_name = img_name.split('.')[0]+'.xml'

    time_label = json_data.get('time_Labeled')  # null
    image_label = json_data.get('imageLabeled')  # true
    width = json_data.get('imageWidth')
    height = json_data.get('imageHeight')
    depth = json_data.get('imageDepth')
    shape = json_data.get('shapes')
    return save_name, xmlpath, shape, time_label, image_label, width, height, depth

def generate_xml(json_path, category, xml_save_path):
    save_name, xmlpath, shape, time_label, image_label, width, height, depth = get_json_data(json_path)

    root = ET.Element("doc")  # 创建根结点

    path = link_Node(root, 'path', xmlpath)  # 创建path节点
    outputs = link_Node(root, 'outputs')
    object = link_Node(outputs, 'object')

    for i in range(len(shape)):
        try:
            item = link_Node(object, 'item')  # 创建item节点

            label_ori = shape[i].get('label')  # 获取json信息
            label = category.get(label_ori)
            width_points_line = shape[i].get('width')  # 点或线的width
            shape_type = shape[i].get('shape_type')
            points = shape[i].get('points')

            name = link_Node(item, 'name', label)  # 添加json信息到item中
            width_2 = link_Node(item, 'width', width_points_line)

            if shape_type == 'linestrip':
                line = link_Node(item, 'line')
                for j in range(len(points)):
                    x = link_Node(line, 'x{}'.format(j+1), int(points[j][0]))
                    y = link_Node(line, 'y{}'.format(j+1), int(points[j][1]))

            if shape_type == 'polygon':
                polygon = link_Node(item, 'polygon')
                for j in range(len(points)):
                    x = link_Node(polygon, 'x{}'.format(j+1), int(points[j][0]))
                    y = link_Node(polygon, 'y{}'.format(j+1), int(points[j][1]))

            if shape_type == 'circle':
                if int(points[1][0] - points[0][0])*2 == width_points_line:
                    point = link_Node(item, 'point')
                    x = link_Node(point, 'x', int(points[0][0]))
                    y = link_Node(point, 'y', int(points[0][1]))
                else:
                    ellipse = link_Node(item, 'ellipse')
                    xmin = link_Node(ellipse, 'xmin', int(points[0][0]))
                    ymin = link_Node(ellipse, 'ymin', int(points[0][1]))
                    xmax = link_Node(ellipse, 'xmax', int(points[1][0]))
                    ymax = link_Node(ellipse, 'ymax', int(points[1][1]))

            if shape_type == 'rectangle':
                bndbox = link_Node(item, 'bndbox')
                xmin = link_Node(bndbox, 'xmin', int(points[0][0]))
                ymin = link_Node(bndbox, 'ymin', int(points[0][1]))
                xmax = link_Node(bndbox, 'xmax', int(points[1][0]))
                ymax = link_Node(bndbox, 'ymax', int(points[1][1]))

            status = link_Node(item, 'status', str(0))
        except:
            print(save_name+'无缺陷')

    time_labeled = link_Node(root, 'time_labeled', time_label)  # 创建time_labeled节点
    labeled = link_Node(root, 'labeled', image_label)
    size = link_Node(root, 'size')
    width = link_Node(size, 'width', width)
    height = link_Node(size, 'height', height)
    depth = link_Node(size, 'depth', depth)

    save_path = os.path.join(xml_save_path, save_name)
    if not os.path.exists(xml_save_path):
        os.makedirs(xml_save_path)
    # 保存xml文件
    saveXML(root, save_path)
    print('{}'.format(save_name) + ' has been transformed!')

def json2xml(json_path_file, xml_save_path, num_worker):
    t = time.time()
    jsonlist = os.listdir(json_path_file)
    # thread_pool = ThreadPoolExecutor(max_workers=num_worker)  # 多线程
    # print('Thread Pool is created!')
    # for json in jsonlist:
    #     json_path = os.path.join(json_path_file, json)
    #     thread_pool.submit(generate_xml, json_path, category, xml_save_path)
    # thread_pool.shutdown(wait=True)
    for json in jsonlist:  # 单线程
        json_path = os.path.join(json_path_file, json)
        # 过滤文件夹和图片文件
        if not os.path.isfile(json_path) or json[json.rindex('.') + 1:] not in ['json']: continue
        generate_xml(json_path, category, xml_save_path)
    print(time.time()-t)

if __name__ == '__main__':
    # category = {'a': '良品', 'aotuhen': '凹凸痕', 'aotuhen1': '凹凸痕1', 'aotuhen2': '凹凸痕2', 'baidian': '白点', 'bianxing': '变形',
    #             'daowen': '刀纹', 'diaoqi': '掉漆', 'guashang': '刮伤', 'guoqie': '过切', 'heidian': '黑点', 'jiaxi': '加铣',
    #             'keli': '颗粒', 'maoxu': '毛絮', 'pengshang': '碰伤', 'tabian': '塌边', 'xianhen': '线痕', 'yashang': '压伤',
    #             'yinglihen': '应力痕', 'yise': '异色', 'yiwu': '异物'}  # json中的label->xml中的汉字标注
    category = {'liewen': '裂纹', 'bianxing': '变形', 'zhanya': '粘料', 'queliao': '缺料', 'pengshang': '碰伤', 'zangwu': '脏污',
                'huashang': '划伤'}
    json_path_file = r'C:\Users\Administrator\Desktop\test_575'  # json file path
    xml_save_path = r'C:\Users\Administrator\Desktop\xml'  # Automatically create a save_path folder
    json2xml(json_path_file, xml_save_path, 8)














