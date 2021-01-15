# @Description:
# @Author     : zhangyan
# @Time       : 2021/1/14 3:54 下午

import os
import time
import xml.etree.ElementTree as ET
from xml.dom import minidom

class Dic2Xml():
    def create_Node(self, element, text=None):
        elem = ET.Element(element)
        elem.text = text
        return elem

    def link_Node(self, root, element, text=None):
        """
        @param root: element的父节点
        @param element: 创建的element子节点
        @param text: element节点内容
        @return: 创建的子节点
        """
        if text != None:
            text = str(text)
        element = self.create_Node(element, text)
        root.append(element)
        return element

    # 保存为XML文件（美化后）
    def saveXML(self, root, filename, indent="\t", newl="\n", encoding="utf-8"):
        rawText = ET.tostring(root)
        dom = minidom.parseString(rawText)
        with open(filename, 'w') as f:
            dom.writexml(f, "", indent, newl, encoding)

    def get_dic_data(self, key, value):
        save_name = key.split('.')[0]+'.xml'
        anno = value.get('anno')
        w = value.get('w')
        h = value.get('h')
        return save_name, save_name, anno, None, 'true', w, h, 3

    def generate_xml(self, key, value, xml_save_path):
        save_name, xmlpath, anno, time_label, image_label, width, height, depth = self.get_dic_data(key, value)

        root = ET.Element("doc")  # 创建根结点

        path = self.link_Node(root, 'path', xmlpath)  # 创建path节点
        outputs = self.link_Node(root, 'outputs')
        object = self.link_Node(outputs, 'object')

        for i in range(len(anno)):
            item = self.link_Node(object, 'item')  # 创建item节点

            label = anno[i][4]  # 获取label
            width_points_line = 2  # 点或线的width
            shape_type = 'rectangle'

            name = self.link_Node(item, 'name', label)  # 添加json信息到item中
            width_2 = self.link_Node(item, 'width', width_points_line)

            if shape_type == 'rectangle':
                bndbox = self.link_Node(item, 'bndbox')
                xmin = self.link_Node(bndbox, 'xmin', int(anno[i][0]))
                ymin = self.link_Node(bndbox, 'ymin', int(anno[i][1]))
                xmax = self.link_Node(bndbox, 'xmax', int(anno[i][2]))
                ymax = self.link_Node(bndbox, 'ymax', int(anno[i][3]))

            status = self.link_Node(item, 'status', str(0))

        time_labeled = self.link_Node(root, 'time_labeled', time_label)  # 创建time_labeled节点
        labeled = self.link_Node(root, 'labeled', image_label)
        size = self.link_Node(root, 'size')
        width = self.link_Node(size, 'width', width)
        height = self.link_Node(size, 'height', height)
        depth = self.link_Node(size, 'depth', depth)

        save_path = os.path.join(xml_save_path, save_name)
        if not os.path.exists(xml_save_path):
            os.makedirs(xml_save_path)
        # 保存xml文件
        self.saveXML(root, save_path)
        print('{}'.format(save_name) + ' has been transformed!')

    def dic2xml(self, dic, xml_save_path):
        t = time.time()
        for key, value in dic.items():
            self.generate_xml(key, value, xml_save_path)
        print(time.time()-t)

if __name__ == '__main__':
    dic = {'123.jpg': {'anno': [(132, 243, 355, 467, '刮伤'), (51, 61, 72, 82, '异色')], 'w': 512, 'h': 512},
           '456.jpg': {'anno': [(11, 21, 31, 41, '擦伤'), (11, 22, 33, 41, '白点')], 'w': 512, 'h': 512}}

    xml_save_path = '/Users/zhangyan/Desktop/xml'
    Dic2Xml().dic2xml(dic, xml_save_path)