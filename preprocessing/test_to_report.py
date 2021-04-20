# @Description:
# @Author     : zhangyan
# @Time       : 2021/4/19 8:48 下午

import numpy as np
import pandas as pd
import os
import random
import openpyxl as xl
from openpyxl.drawing.image import Image as XLImage



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

import numpy as np
import json
import pandas as pd
import itertools
import os

# import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import time
import shutil
class AnnalyResult(object):
    def __init__(self,yt_labelme,test_labelme,out_path,title_png):
        self.yt_labelme = yt_labelme
        self.test_labelme = test_labelme
        self.out_path = out_path
        self.title_png = title_png
        self.gt_class =[]
        self.pre_class=[]
        start_time=time.time()
        self.main()
        end_time=time.time()
        print('run time:',end_time-start_time)
        self.cm = self.compute_confmx()
    def getcm(self):
        return self.cm
    def get_points_box(self,points,type='polygon',width=2):
        points = np.array(points)
        if type=='point' and len(points)==1:
            box = [points[0][0]-width/2,points[0][1]-width/2,points[0][0]+width/2,points[0][1]+width/2]
            return box
        if type=='circle' and len(points)==2:
            r= np.sqrt((points[0][0]-points[1][0])**2+(points[0][1]-points[1][1])**2)
            box = [points[0][0]-r,points[0][1]-r,points[0][0]+r,points[0][1]+r]
            return box
        box = [min(points[:,0]),min(points[:,1]),max(points[:,0]),max(points[:,1])]
        return box
    def parse_para_re(self,input_json):
        with open(input_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    def save_json(self,dic,path):
        json.dump(dic, open(path, 'w',encoding='utf-8'), indent=4)
        return 0
    def compute_iou(self,bbox1, bbox2):
        """
        compute iou
        :param bbox1:
        :param bbox2:
        :return: iou
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
    def l_g_ls(self,require,part,iou_thr,f_l_flag):#过检记录：某个预测框与所有gt的iou等于0，表明该预测框为过检框,一张图预测不出结果时需要考虑漏检如何计算。
        result_l = []
        for j in require:
            result_flag = 0
            gt_points = j['points']
            for k in part:
                pre_points = k['points']
                bbox_gt = self.get_points_box(gt_points,j['shape_type'])
                bbox_re = self.get_points_box(pre_points,k['shape_type'])
                iou=self.compute_iou(bbox_gt,bbox_re)
                if iou<iou_thr:#<iou_thr:
                    #print('iou:',iou),#过检和漏检与gt的iou都为0
                    result_flag+=1
                    #print('r',result_flag,len(part))
            if result_flag==len(part):#iou为0的数量与所有预测标注的数量是否相等，若相等表明缺陷漏检，若为0的记录小于0则表明缺陷未漏检。
                if f_l_flag=='loujian':#loushi
                    self.gt_class.append(j['label'])
                    self.pre_class.append('z_lou_or_guo')
                else:#guojian
                    self.gt_class.append('z_lou_or_guo')
                    self.pre_class.append(j['label'])
                result_l.append(j)
                print('result_l',result_l)
        return result_l
    def jiandui_ls(self,require,part,iou_thr):
        jd=[]
        for j in require:
            gt_points = j['points']
            for k in part:
                pre_points = k['points']
                bbox_gt = self.get_points_box(gt_points,j['shape_type'])
                bbox_re = self.get_points_box(pre_points,k['shape_type'])
                iou=self.compute_iou(bbox_gt,bbox_re)
                if iou>=iou_thr:
                    if not k in jd:
                        jd.append(k)
                        self.gt_class.append(j['label'])
                        self.pre_class.append(k['label'])
        return jd
    def compute_confmx(self):
        classes =sorted(list(set(self.gt_class)),reverse=False)#类别排序
        cm = confusion_matrix(self.gt_class, self.pre_class,classes)#根据类别生成矩阵，此处不需要转置
        cm_pro = (cm.T/np.sum(cm, 1)).T
        # print('cm',cm)
        # print('cmp',cm_pro)
        #
        self.plot_confusion_matrix(cm,classes,'nums')
        self.plot_confusion_matrix(cm_pro,classes,'pro',normalize=True)
        return cm
        # print('confx',cm)
    def new_json(self,cz,shapes,save_json):
        new_json_dic = {}
        new_json_dic['flags']=cz['flags']
        new_json_dic['imageData']=cz['imageData']
        new_json_dic['imageDepth']=cz['imageDepth']
        new_json_dic['imageLabeled']=cz['imageLabeled']
        new_json_dic['imagePath']=cz['imagePath']
        new_json_dic['imageHeight']=cz['imageHeight']
        new_json_dic['imageWidth']=cz['imageWidth']
        new_json_dic['shapes']=shapes
        new_json_dic['time_Labeled']=cz['time_Labeled']
        new_json_dic['version']=cz['version']
        if len(shapes)!=0:
            self.save_json(new_json_dic,save_json)

    def proce_compute(self,input_json,pre_json,save_path):
        gt_anno_data = self.parse_para_re(input_json)
        print('gt_json',input_json)
        pre_anno_data = self.parse_para_re(pre_json)
        gt_shapes = gt_anno_data['shapes']
        pre_shapes = pre_anno_data['shapes']
        jiandui_shapes=[]
        jiandui_shapes = self.jiandui_ls(gt_shapes,pre_shapes,0.01)
        guojian_shapes=[]
        guojian_shapes = self.l_g_ls(pre_shapes,gt_shapes,0.01,'guojian')
        merge_gt_pre_shapes = []
        merge_gt_pre_shapes.extend(gt_shapes)
        merge_gt_pre_shapes.extend(guojian_shapes)
        loujian_shapes = []
        try:
            loujian_shapes = self.l_g_ls(gt_shapes,pre_shapes,0.01,'loujian')
        except:
            loujian_shapes.extend(gt_shapes)
        print('---',len(guojian_shapes),len(loujian_shapes),len(jiandui_shapes),len(gt_shapes),len(merge_gt_pre_shapes))
        guojian_path = os.path.join(save_path,'guojian')
        loujian_path = os.path.join(save_path,'loujian')
        jiandui_path = os.path.join(save_path,'jiandui')
        merge_gt_pre_path = os.path.join(save_path,'merge_gt_pre')
        if not os.path.exists(guojian_path):
            os.makedirs(guojian_path)
        if not os.path.exists(loujian_path):
            os.makedirs(loujian_path)
        if not os.path.exists(jiandui_path):
            os.makedirs(jiandui_path)
        if not os.path.exists(merge_gt_pre_path):
            os.makedirs(merge_gt_pre_path)
        img_name = gt_anno_data['imagePath']
        json_name = img_name.replace('.jpg','.json')
        guojian_json = os.path.join(guojian_path,json_name)
        loujian_json = os.path.join(loujian_path,json_name)
        jiandui_json = os.path.join(jiandui_path,json_name)
        merge_gt_pre_json = os.path.join(merge_gt_pre_path,json_name)
        self.new_json(gt_anno_data,guojian_shapes,guojian_json)
        self.new_json(gt_anno_data,loujian_shapes,loujian_json)
        self.new_json(gt_anno_data,jiandui_shapes,jiandui_json)
        self.new_json(gt_anno_data,merge_gt_pre_shapes,merge_gt_pre_json)

    def main(self):
        for i in os.listdir(self.yt_labelme):
            if i.endswith('.json'):
                input_json = os.path.join(self.yt_labelme,i)
                pre_json = os.path.join(self.test_labelme,i)
                except_json = os.path.join("D:/work/data/microsoft/jalama/sixth/third_cut/test/exception",i)
                try:
                    self.proce_compute(input_json,pre_json,self.out_path)
                except:
                    shutil.move(input_json,except_json)
                    print('未预测数据',input_json)
    def plot_confusion_matrix(self,cm,classes,title,normalize=False, cmap=plt.cm.Blues):
        #plt.figure()

        plt.figure(figsize=(12, 8), dpi=120)
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title('{}_{}'.format(self.title_png,title))
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=90)
        plt.yticks(tick_marks, classes)


        # plt.axis("equal")
        ax = plt.gca()
        left, right = plt.xlim()
        ax.spines['left'].set_position(('data', left))
        ax.spines['right'].set_position(('data', right))
        for edge_i in ['top', 'bottom', 'right', 'left']:
            ax.spines[edge_i].set_edgecolor("white")

        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            num = float('{:.2f}'.format(cm[i, j])) if normalize else int(cm[i, j])
            plt.text(j, i, num,
                     verticalalignment='center',
                     horizontalalignment="center",
                     color="white" if num > thresh else "black")
        plt.ylabel('ground turth')
        plt.xlabel('predict')
        plt.tight_layout()
        save_p = os.path.join(self.out_path,'./{}_{}.png'.format(self.title_png,title))
        cm_txt = save_p.replace('.png','.txt')
        with open(cm_txt,'a+') as f:
            f.write('{}:\n'.format(title))
            f.write(str(cm))
            f.write('\n')
        #plt.savefig(save_p, transparent=True, dpi=800)
        plt.savefig(save_p, transparent=True, dpi=300)
        #plt.show()





def confusion_mtx_to_report(data):
    """
    @param data: confusion_mtx
    @return: gt_num, loushi, loujian_ratio, jianchu, guojian, guojian_ratio
    """
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
    # guojian.pop()  # 过检数量
    guojian = guojian[0:-1]

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


def addimage_to_excel(outputs_path, test_path, save_path, sheet_name, ratio_array):
    '''
    ratio_array中设定展示百分之多少的图片
    '''
    excel_col = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK', 'AL',
                 'AM',
                 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD',
                 'BE',
                 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ', 'BR', 'BS', 'BT', 'BU', 'BV',
                 'BW',
                 'BX', 'BY', 'BZ', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG', 'CH', 'CI', 'CJ', 'CK', 'CL', 'CM', 'CN',
                 'CO',
                 'CP', 'CQ', 'CR', 'CS', 'CT', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF',
                 'DG',
                 'DH', 'DI', 'DJ', 'DK', 'DL', 'DM', 'DN', 'DO', 'DP', 'DQ', 'DR', 'DS', 'DT', 'DU', 'DV', 'DW', 'DX',
                 'DY',
                 'DZ']
    book = xl.load_workbook(save_path)

    # 查找loujian图片
    img_names = list()
    for f in os.listdir(os.path.join(outputs_path, 'loujian')):
        if f.find('.json'):
            img_names.append(f)
    number = int(len(img_names) * ratio_array[0])  # 决定展示图片个数
    if not number:
        number = 1
    show_img_names = random.sample(img_names, number)

    # 插入loujian图片
    sheet = book[sheet_name]
    # new_sheet = book.create_sheet(title='loujian')
    col = 0
    sheet[excel_col[col] + '10'] = '漏检图片'
    for name in show_img_names:
        img_name = os.path.join(test_path, name[:-5] + '.jpg')
        # print(img_name)
        img = XLImage(img_name)
        idx = excel_col[col] + '11'
        sheet.add_image(img, idx)
        col = col + 2

    # 查找guojian图片
    img_names = list()
    for f in os.listdir(os.path.join(outputs_path, 'guojian')):
        if f.find('.json'):
            img_names.append(f)
    number = int(len(img_names) * ratio_array[1])  # 决定插入图片个数
    if not number:
        number = 1
    show_img_names = random.sample(img_names, number)

    # 插入guojian图片
    col = 9
    sheet[excel_col[col] + '10'] = '过检图片'
    for name in show_img_names:
        img_name = os.path.join(test_path, name[:-5] + '.jpg')
        # print(img_name)
        img = XLImage(img_name)
        idx = excel_col[col] + '11'
        sheet.add_image(img, idx)
        col = col + 2

    book.save(save_path)

if __name__ == '__main__':
    imgs_path = r'G:\ttt\test'  # 测试img路径
    csv_path = r'G:\ttt\csv'  # csv路径   和img分开存放
    gt_json = r'G:\ttt\gt\jsons'  # biaozhu jsons
    split_result_file = r'G:\ttt\outputs_path'  # split result file
    save_path = r'C:\Users\Administrator\Desktop\A.xlsx'  # report_path
    xml_path = r'G:\ttt\test\outputs'  # 自动生成
    json_path = r'G:\ttt\test\json'  # 自动生成
    ShiwuHedui(imgs_path,csv_path,xml_path)
    xml2json =Xml2Labelme(imgs_path,json_path,'result',8)

    print('分析标注结果生成混淆矩阵')
    annalyresult = AnnalyResult(gt_json,
                 json_path,#pre jsons
                 split_result_file,
                 '140model_0420testdata')# 混淆矩阵图像名字，不带后缀
    cm = annalyresult.getcm()
    content = confusion_mtx_to_report(cm)
    content_to_excel(content, save_path)
    addimage_to_excel(split_result_file, imgs_path, save_path, 'page_1', [0.1, 0.1])


