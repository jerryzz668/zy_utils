
# ---------------------------class7----------------------start
#实物csv和实物图可视化，给他实物图和实物csv生成对应的xml标注和标注合并图，显示的时候注意类别映射字典。调用：#csv_p = r'C:\Users\xie5817026\PycharmProjects\pythonProject1\0104\ProductGradeMaterialCheck.csv'
# img_p ='D:\work\data\microsoft\jalama\data\heduiji\merge_all",ShiwuHedui(img_p,csv_p),生成'D:\work\data\microsoft\jalama\data\heduiji\merge_all\outputs",'D:\work\data\microsoft\jalama\data\heduiji\merge_all\r_imgs"
import cv2
import os
import glob
import pandas as ps
import shutil
from PIL import Image
# @Description:
# @Author     : zhangyan
# @Time       : 2021/1/14 3:54 下午

import os
import time
import xml.etree.ElementTree as ET
from xml.dom import minidom
class Dic2xml(object):
    def __init__(self,dic,xml_save_path):
        self.dic2xml(dic, xml_save_path)

    def create_Node(self,element, text=None):
        elem = ET.Element(element)
        elem.text = text
        return elem

    def link_Node(self,root, element, text=None):
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
    def saveXML(self,root, filename, indent="\t", newl="\n", encoding="utf-8"):
        rawText = ET.tostring(root)
        dom = minidom.parseString(rawText)
        with open(filename, 'w',encoding="utf-8") as f:
            dom.writexml(f, "", indent, newl, encoding)

    def get_dic_data(self,key, value):
        save_name = key.split('.')[0]+'.xml'
        anno = value.get('anno')
        w = value.get('w')
        h = value.get('h')
        return save_name, save_name, anno, None, 'true', w, h, 3

    def generate_xml(self,key, value, xml_save_path):
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

            status = self.link_Node(item, 'status', str(1))

        time_labeled = self.link_Node(root, 'time_labeled', time_label)  # 创建time_labeled节点
        labeled = self.link_Node(root, 'labeled', image_label)
        size = self.link_Node(root, 'size')
        width = self.link_Node(size, 'width', width)
        height = self.link_Node(size, 'height', height)
        depth = self.link_Node(size, 'depth', depth)

        save_path = xml_save_path#os.path.join(xml_save_path, save_name)
        # if not os.path.exists(xml_save_path):
        #     os.makedirs(xml_save_path)
        # 保存xml文件
        self.saveXML(root, save_path)
        print('{}'.format(save_name) + ' has been transformed!')

    def dic2xml(self,dic, xml_save_path):
        t = time.time()
        for key, value in dic.items():
            self.generate_xml(key, value, xml_save_path)
        print(time.time()-t)

# if __name__ == '__main__':
#     dic = {'123.jpg': {'anno': [(132, 243, 355, 467, '刮伤'), (51, 61, 72, 82, '异色')], 'w': 512, 'h': 512},
#            '456.jpg': {'anno':[(11, 21, 31, 41, '擦伤'), (11, 22, 33, 41, '白点')], 'w': 512, 'h': 512}}
#
#     xml_save_path = r'C:\Users\xie5817026\PycharmProjects\pythonProject1\0104\xml'
#     Dic2xml(dic, xml_save_path)
class ShiwuHedui(object):
    def __init__(self,source_p,csv_p,xml_p):

        #图像位置
        dic_wh = self.w_h(source_p)#图像存放位置#获取所有图像的wh字典
        if not os.path.exists(xml_p):
            os.makedirs(xml_p)
        for imgs_name in os.listdir(source_p):
            if imgs_name.endswith('jpg'):
                csv_name = imgs_name.replace('jpg','csv')
                xml_name = imgs_name.replace('jpg','xml')
                csv_pp = os.path.join(csv_p,csv_name)
                xml_save_path = os.path.join(xml_p,xml_name)
                img_dic_c = self.read_csv(csv_pp,dic_wh,imgs_name)#csv格式 #读取一张图像csv
                print('img_dic_c',img_dic_c)
                Dic2xml(img_dic_c, xml_save_path)
    def w_h(self,p):
        dic_wh = {}
        print('---')
        for i in os.listdir(p):
            i_p = os.path.join(p,i)
            # data = cv2.imread(i_p)
            data = Image.open(i_p)
            dic_wh[i]=data.size
            print(data.size)
        return dic_wh

    def read_csv(self,csv_path,dic_wh,img_name):
        r = ps.read_csv(csv_path,usecols=['photo_id','product_id','channel_id','class_name','xmin','ymin','bb_width','bb_height'])
        #r = ps.read_csv(csv_path,usecols=['任务号','工件号','图号','缺陷','PointX','PointY','Width','Height'])
        imgs_dic = {}
        x_min = r['xmin']
        y_min = r['ymin']
        w = r['bb_width']
        h = r['bb_height']
        label = r['class_name']

        for i in range(len(label)):
            img_name = img_name#'{}-{}-{}.jpg'.format(task_ids[i],gongjian_ids[i],img_ids[i])
            x_max =x_min[i]+w[i]
            y_max = y_min[i]+h[i]
            if img_name in imgs_dic:
                imgs_dic[img_name].append((x_min[i],y_min[i],x_max,y_max,label[i]))
            else:
                imgs_dic[img_name]=[(x_min[i],y_min[i],x_max,y_max,label[i])]
        img_dic_c = {}
        for i in imgs_dic:
            try:
                w,h = dic_wh[i]
                one_img_dic = {}
                one_img_dic['anno']=imgs_dic[i]
                one_img_dic['w']=w
                one_img_dic['h']=h
                img_dic_c[i]=one_img_dic
            except:
                print('--')
        print(img_dic_c)
        return img_dic_c


# ---------------------------class7----------------------end

import numpy as np
from xml.etree import ElementTree as ET
import multiprocessing
import pypinyin
import shutil
import time
import json
import os
import cv2
import math
import glob
'''
@Xml2Labelme:
            主要功能：将mark工具标注的xml标注转为json标注，方便labelme查看及生成coco格式数据
            关键处理：1.汉字转拼音 pypinyin工具包；2.检测标注类别错标并调整类别，modify_type函数；
                    3.xml结构转为coco结构，transform_xml_2labelme函数
@author: lijianqing
@date: 2020/11/11 13:19
'''
class Xml2Labelme(object):
    def __init__(self,annotation_root_path,jsons_path,result_write,process_num=8):
        self.xml_outputs_path = os.path.join(annotation_root_path,'outputs')
        if not os.path.exists(jsons_path):
            os.makedirs(jsons_path)
        self.jsons_path = jsons_path
        self.result_write = result_write
        s = time.time()
        #self.main(self.xml_outputs_path,self.jsons_path,process_num)
        self.cut_label = self.main_share(self.xml_outputs_path,self.jsons_path,process_num)
        print('xml2labelme run time:',time.time()-s)
    def pinyin(self,word):#zhangsan = pinyin('张山')
        s = ''
        for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
            s += ''.join(i)
        return s
    def modify_type(self,type,points_l):
        type_index = {0:'none',1:'point',2:'line',3:'polygon',4:'bndbox',5:'ellipse'}
        if len(points_l)<3:#长度为0，1,2的
            if type!='ellipse' and type!='bndbox':#类别不为圆和bndbox的情况下按长度设置类别，长度为0的都为none,长度为1的都是点，长度为2的都是线，
                type=type_index[len(points_l)]
            elif len(points_l)!=2:
                type=type_index[len(points_l)]#类别为圆或bndbox，但长度小于2的，按长度设置类别，长度为0的都为none,长度为1的都是点，
            else:#类别为圆或bndbox，长度为2的，符合圆或bndbox的标准，不做修改
                type=type
        elif len(points_l)<4:#长度为3的
            if type!='line':#类别不为line的按多边形处理
                type=type_index[len(points_l)]
            else:#类别为line的，符合line标准，不做修改
                type=type
        else:#长度大于或等于4的
            if type!='line' and type!='polygon':#类别既不是line,也不是多边形的，按多边形polygon处理
                type=type_index[3]
            else:#类别为线，或多边形的，不做修改
                type=type
        return type
    def transform_xml_2labelme(self,xml_path,save_json,image_name,class_py_ch_dic):
        transform_shapes_dic = {'polygon':'polygon','line':'linestrip','bndbox':'rectangle','point':'circle','ellipse':'circle'}
        tree = ET.parse(xml_path)
        root_node = tree.getroot()
        imagePath = '{}.jpg'.format(image_name)
        xmlPath = root_node[0].text
        print('class_py_ch_dic--',xmlPath)
        imageWidth =int(root_node[4][0].text) #json_obj['imageWidth']=0
        imageHeight = int(root_node[4][1].text)#json_obj['imageHeight']=0
        imageDepth = int(root_node[4][2].text)#null
        imageLabeled = root_node[3] .text
        time_Labeled = root_node[2].text
        shapes = []
        print('root_node[1][0]',root_node[1][0])
        for i in root_node[1][0]:
            dic_instance = {}
            dic_instance['label']=self.pinyin(i[0].text)
            class_py_ch_dic[self.pinyin(i[0].text)]=i[0].text
            points_l = []
            point_axis = []
            flag = 0
            # print('kd----------:',i[1].text,'--',i[2].tag)#像素宽度
            for j in i[2].iter():
                if flag !=0:
                    #print('j.text,shape:',j.text,i[2].tag,i[1].text,)
                    point_axis.append(float(j.text))
                    if len(point_axis)==2:
                        points_l.append(point_axis)
                        point_axis=[]
                else:
                    flag = 1
            xml_tag = i[2].tag
            #modify type xml
            i_2_tag = self.modify_type(xml_tag,points_l)
            #point2circle
            if i_2_tag=='point' and len(points_l)==1:
                r = int(i[1].text)/2
                x,y = points_l[0]
                r_x = x+r
                r_y = y+r
                points_l.append([r_x,r_y])
                i_2_tag = 'ellipse'

            #2 labelme json after modify type in xml
            try:
                dic_instance['shape_type']=transform_shapes_dic[i_2_tag]
            except:
                print('标注类别为空或错误，请检测。',i[2].tag,xml_path)
            dic_instance['width']=i[1].text
            dic_instance['points'] = points_l
            dic_instance['group_id']=''
            dic_instance['flags']={}#i[3].text#state
            try:
                dic_instance['level'] = i[4].text#'level'
            except:
                #print('无照片严重程度')
                a=0
            try:
                dic_instance['mlevel'] = i[5].text#'mlevel'
            except:
                #print('无缺陷严重程度')
                a=0
            try:
                dic_instance['describe'] = i[6].text#'describe'
            except:
                #print('无描述')
                a=0
            if len(points_l)>0:#标注长度大于0时为可用的有效标注
                shapes.append(dic_instance)
        dic_all = {}
        dic_all['version']='1.0'
        dic_all['flags']={}
        dic_all['shapes']= shapes
        dic_all['imagePath']=imagePath
        dic_all['xmlPath']=xmlPath
        # print('正在处理：',imagePath)
        dic_all['imageData'] = None
        dic_all['imageHeight']=imageHeight
        dic_all['imageWidth']=imageWidth
        dic_all['imageDepth']= imageDepth
        dic_all['imageLabeled']=imageLabeled
        dic_all['time_Labeled']=time_Labeled
        with open(save_json,"w",encoding="utf-8") as f:
            content=json.dumps(dic_all,ensure_ascii=False)
            f.write(content)
            f.close()
    def main_share(self,local_path,save_path,process_num=4):
        pool = multiprocessing.Pool(processes=process_num) # 创建进程个数
        class_py_ch_dic=multiprocessing.Manager().dict()
        for i in os.listdir(local_path):
            xml_path = os.path.join(local_path,i)#xml_path
            image_name = i.split('.xml')[0]
            json_path = os.path.join(save_path,'{}.json'.format(image_name))
            print('json_path',json_path)
            pool.apply_async(self.transform_xml_2labelme,args=(xml_path,json_path,image_name,class_py_ch_dic))
        pool.close()
        pool.join()
        print('class_py_ch_dic:',class_py_ch_dic)
        class_py_ch_dic_tuple = sorted(class_py_ch_dic.items())
        class_pinyin_list,class_ch_list = zip(*class_py_ch_dic_tuple)
        print('{}'.format(class_pinyin_list))
        class_mapers = {}
        for i,key in enumerate(class_pinyin_list):
            class_mapers[key] = i
        with open(self.result_write,'a+',encoding='utf-8') as f:
            f.write('拼音-汉字-字典：{}\n'.format(class_py_ch_dic))
            f.write('拼音-index：{}\n'.format(class_mapers))
            f.write('拼音：{}\n'.format(class_pinyin_list))
            f.write('汉字：{}\n'.format(class_ch_list))
            f.write('类别数量：{}\n'.format(len(class_ch_list)))
        return class_pinyin_list

if __name__ == '__main__':
    imgs_path = r'G:\ttt\test'
    csv_path = r'G:\ttt\csv'
    xml_path = r'G:\ttt\test\outputs'#自动生成
    json_path = r'G:\ttt\test\json'#自动生成
    ShiwuHedui(imgs_path,csv_path,xml_path)
    xml2json =Xml2Labelme(imgs_path,json_path,'result',8)