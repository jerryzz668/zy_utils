#source_annotation_file---|---
#                         |--->xml-->labelme
#                         |--->labelme-->cut
#                         |--->labelme-->coco
#                         |--->labelme-->mask
#                         |--->mask-->label
#                         |--->coco dataset
def xml2cocodata(annotation_root,out_coco_dataset,intermediate_data=False):
    if intermediate_data:
        print('保存中间产生的数据')
    else:
        print('删除中间产生的数据')
    return 1
def xml2labelme_jsons(annotation_root_path):
    return 1
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
        #print(type,'----',points_l)
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
        xmlPath = root_node[0].text.split('tmp')[-1]
        print('class_py_ch_dic--',xmlPath)
        imageWidth =int(root_node[3][0].text) #json_obj['imageWidth']=0
        imageHeight = int(root_node[3][1].text)#json_obj['imageHeight']=0
        imageDepth = int(root_node[3][2].text)#null
        imageLabeled = root_node[2] .text
        time_Labeled = ''#root_node[2].text
        shapes = []
        #print('root_node[1][0]',root_node[1][0])
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
            # print('xml_tag',xml_tag)
            #modify type xml
            i_2_tag = self.modify_type(xml_tag,points_l)
            #print('i_2_tag',i_2_tag)
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
                print(i_2_tag,'标注类别为空或错误，请检测。',i[2].tag,xml_path)
            dic_instance['width']=i[1].text
            dic_instance['points'] = points_l
            dic_instance['group_id']=''
            dic_instance['flags']={}#i[3].text#state
            try:
                dic_instance['level'] = ''#i[4].text#'level'
            except:
                #print('无照片严重程度')
                a=0
            try:
                dic_instance['plevel'] = self.pinyin(i[5].text) #i[5].text#'mlevel'
            except:
                #print('无缺陷严重程度')
                dic_instance['plevel'] ='0'
                a=0
            try:
                dic_instance['describe'] = self.pinyin(i[6].text)#i[6].text#'describe'
            except:
                dic_instance['describe'] = 'no'
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

'''
@CutLabelme: 根据给定size(w,h)和标注切图
            主要功能：将mark工具标注的xml标注转为json标注，方便labelme查看及生成coco格式数据
            关键处理：1.将全图标注数据根据给定size计算终止切图策略，由digui函数实现；
                    2.切图策略计算过程中，记录最新框的中心位置；
                    3.计算切图的大小和对应新json中坐标位置；
                    4.超出边界的目标切落在区域内的。
@author: lijianqing
@date: 2020/11/24 16:45
@return 
'''
class CutLabelme(object):
    def __init__(self,annotation_root_path,img_jsons,out_path_result_cut,cut_label,process_nums,cut_w,cut_h,result_write):
        self.annotation_root_path=annotation_root_path
        self.result_write=result_write
        self.img_jsons = img_jsons
        self.out_path_result_cut = out_path_result_cut
        self.cut_label = cut_label
        self.process_nums = process_nums
        self.cut_w = cut_w
        self.cut_h = cut_h
        self.main()
    def save_json(self,dic,save_path):
        json.dump(dic, open(save_path, 'w',encoding='utf-8'), indent=4)
    def save_new_img(self,img_np,img_name,xmin,ymin,xmax,ymax,out_path,img_x,img_y):
        # 切图并保存
        xmin,ymin,xmax,ymax = int(xmin),int(ymin),int(xmax),int(ymax)
        left,top,right,down = 0,0,0,0#need padding size
        if xmax>img_x:
            right = xmax-img_x
            xmax=img_x
            # print('out of width')
        if ymax>img_y:
            down = ymax-img_y
            ymax=img_y
            # print('out of hight')
        if ymin<0:
            top = abs(ymin)
            ymin=0
            # print('out of hight')
        if xmin<0:
            left = abs(xmin)
            xmin=0
            # # print('out of width')
        img_crop = img_np[ymin:ymax,xmin:xmax]
        ret = cv2.copyMakeBorder(img_crop, top, down, left, right, cv2.BORDER_CONSTANT, value=(0,0,0))#padding
        cv2.imwrite(os.path.join(out_path, img_name), ret)
        return 0
    def count_bbox_size(self,per_object):
        points = per_object['points']
        x,y = zip(*points)#split x,y
        if per_object['shape_type']=='circle':
            center_point = points[0]
            r_p = points[1]
            r = round(math.sqrt((center_point[0]-r_p[0])**2+(center_point[1]-r_p[1])**2),2)
            min_x = round(center_point[0]-r,2)
            min_y = round(center_point[1]-r,2)
            max_x = round(center_point[0]+r,2)
            max_y = round(center_point[1]+r,2)
        else:
            min_x = round(min(x),2)
            min_y= round(min(y),2)
            max_x = round(max(x),2)
            max_y = round(max(y),2)
        # print('max_x,max_y,min_x,min_y',max_x,max_y,min_x,min_y,'---',i['shape_type'])
        return  max_x,max_y,min_x,min_y
    def get_new_location(self,point,mid_point,crop_w=64,crop_h=64):
        #将缺陷放于中心位置
        p_x = point[0]-mid_point[0]+crop_w/2
        p_y = point[1]-mid_point[1]+crop_h/2
        if p_x<0:
            p_x=0
        if p_y<0:
            p_y=0
        if p_x>crop_w:
            p_x=crop_w
        if p_y>crop_h:
            p_y=crop_h
        return [p_x,p_y]
    def cut_json(self,json_p):
        #print('jsons-----',json_p)
        counter_per_cut = 0
        with open(json_p, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        img_n = os.path.join(self.annotation_root_path,json_data['imagePath'])#原图像名
        # print('img_n 图像位置：',img_n)
        img_np = cv2.imread(img_n)#原图数据
        # print('img_np----图像数据',img_np)
        shapes_img_l = {}
        c = 0
        #筛选需要切的label
        for i in json_data['shapes']:
            c+= 1
            if i['label'] in self.cut_label:
                shapes_img_l[c]=i
        #print(shapes_img_l)
        cut_one_img = []
        mid_point = []
        # try:
        self.recursion_cut(shapes_img_l,counter_per_cut,self.cut_w,self.cut_h,cut_one_img,mid_point)#聚类
        # except:
        #     print('-------',json_p)
        ###core    start
        #print('cut_one_img',cut_one_img)
        for index_object in range(len(cut_one_img)):
            for shapes_object in cut_one_img[index_object]:
                new_points = []
                for loc in shapes_object['points']:
                    n_p = self.get_new_location(loc,mid_point[index_object],self.cut_w,self.cut_h)
                    new_points.append(n_p)
                shapes_object['points'] = new_points
            new_name_img = '{}_{}_{}.jpg'.format(mid_point[index_object][0],mid_point[index_object][1],index_object)
            new_name_json = '{}_{}_{}.json'.format(mid_point[index_object][0],mid_point[index_object][1],index_object)
            #生成新的img文件，抠图过程中会出现超出边界的坐标
            source_x_min,source_x_max = mid_point[index_object][0]-self.cut_w/2,mid_point[index_object][0]+self.cut_w/2#抠图位置
            source_y_min,source_y_max= mid_point[index_object][1]-self.cut_h/2,mid_point[index_object][1]+self.cut_h/2
            x_min,x_max,y_min,y_max = int(source_x_min),int(source_x_max),int(source_y_min),int(source_y_max)
            try:
                self.save_new_img(img_np,new_name_img,x_min,y_min,x_max,y_max,self.out_path_result_cut,json_data['imageWidth'],json_data['imageHeight'])
            except:
                print('new_name_img',new_name_img,'img_n',img_n)
            #生成新的json文件
            # crop_szie_w,crop_szie_h = crop_szie,crop_szie
            self.def_new_json(json_data,self.cut_w,self.cut_h,new_name_json,cut_one_img[index_object],self.out_path_result_cut,new_name_img)
    def def_new_json(self,json_data,crop_szie_w,crop_size_h,new_name,shapes_img,out_p,new_name_img):
        new_json = {}
        new_json['flags'] = json_data['flags']
        new_json['imageData'] = None
        new_json['imageDepth'] = json_data['imageDepth']
        new_json['imageHeight'] = crop_size_h
        new_json['imageLabeled'] = json_data['imageLabeled']
        new_json['imagePath'] = new_name_img
        new_json['imageWidth'] = crop_szie_w
        new_json['shapes'] = shapes_img
        new_json['time_Labeled'] = json_data['time_Labeled']
        new_json['imagePathSource'] = json_data['imagePath']
        new_json['version'] = json_data['version']
        self.save_json(new_json,os.path.join(out_p,new_name))
        # print('生成了',os.path.join(out_p,new_name))
        return new_json
    def def_dic_element(self,shapes_img,i,points):
        dic_element = {}
        dic_element['flags']=i['flags']
        dic_element['group_id']=i['group_id']
        dic_element['label']=i['label']
        dic_element['points'] = points
        dic_element['shape_type']=i['shape_type']
        dic_element['width']=i['width']
        shapes_img.append(dic_element)
        return shapes_img
    def recursion_cut(self,shapes_img_l,counter_per_cut,crop_w,crop_h,cut_one_img,mid_point):
        counter_per_cut += 1
        if len(shapes_img_l)==0:
            #print('递归结束了',counter_per_cut)
            return 0
        next_allow = {}#记录不可以放一起的标注
        allow = []
        max_bbox = []
        for i in shapes_img_l:
            max_x,max_y,min_x,min_y = self.count_bbox_size(shapes_img_l[i])#获取标注的位置
            w,h = max_x-min_x,max_y-min_y
            #与已有点比较距离
            if len(max_bbox)>0:
                a,b,c,d = max_bbox
                mmin_x = min(min_x,c)
                mmin_y = min(min_y,d)
                mmax_x = max(max_x,a)
                mmax_y = max(max_y,b)
                ww,hh = mmax_x-mmin_x,mmax_y-mmin_y
                # print('最大长宽',ww,hh)
                if ww<crop_w and hh <crop_h:
                    max_bbox = mmax_x,mmax_y,mmin_x,mmin_y
                    allow.append(shapes_img_l[i])
                else:
                    next_allow[i]=shapes_img_l[i]#不可以放一起的
            else:
                max_bbox = [max_x,max_y,min_x,min_y]
                allow.append(shapes_img_l[i])

        #计算聚类后类别在原图的中心点。
        w,h = max_bbox[0]-max_bbox[2],max_bbox[1]-max_bbox[3]
        mid_x = math.ceil(max_bbox[2]+w/2)
        mid_y = math.ceil(max_bbox[3]+h/2)
        # print('中心点',math.ceil(mid_x),math.ceil(mid_y))
        cut_one_img.append(allow)
        mid_point.append((mid_x,mid_y))
        self.recursion_cut(next_allow,counter_per_cut,crop_w,crop_h,cut_one_img,mid_point)
    def main(self):
        # if '\\' in self.annotation_root_path:
        #     annotation_root_path.replace('\\','/')
        # if '\\' in self.out_path_result_cut:
        #     out_path_result_cut.replace('\\','/')
        # if not os.path.exists(out_path_result_cut):
        #     os.makedirs(out_path_result_cut)
        jsons_path_list = glob.glob('{}/*.json'.format(self.img_jsons))
        pool1 = multiprocessing.Pool(processes=self.process_nums)
        start_time = time.time()
        pool1.map(self.cut_json,jsons_path_list)
        print('cut_labelme_img run time:',time.time()-start_time)
        pool1.close()
        pool1.join()
'''
@UtilsMicroI: 统计切图前后目标的数据并且
@author: lijianqing
@date: 2020/11/25 16:24
@return 
'''
class UtilsMicroI(object):
    def __init__(self,source_jsons_path,cut_jsons_path,result_write,expect_annotations_file):
        self.source_jsons_path = source_jsons_path
        self.cut_jsons_path = cut_jsons_path
        self.result_write = result_write
        self.expect_annotations_file = expect_annotations_file
        self.mian()
    def parse_para(self,input_json):
        with open(input_json, 'r', encoding='utf-8') as f:
            ret_dic = json.load(f)
        return ret_dic
    def counter_cate(self,json_path,imagePathSource):
        jsons = glob.glob(r'{}\*.json'.format(json_path))
        img_annotations_dic= {}
        cate_nums_dic = {}
        for i in jsons:
            ret_dic = self.parse_para(i)
            shapes = ret_dic['shapes']
            imagePath = ret_dic[imagePathSource]
            for j in shapes:
                if imagePath not in img_annotations_dic:
                    lis = []
                else:
                    lis=img_annotations_dic[imagePath]
                lis.append(j['label'])
                #cate_nums
                if j['label'] in cate_nums_dic:
                    cate_nums_dic[j['label']] += 1
                else:
                    cate_nums_dic[j['label']] = 1
            img_annotations_dic[imagePath]=lis
        return (img_annotations_dic,cate_nums_dic)

    def sum_val_dic(self,counter_dic):
        counter_sum = 0
        for i in counter_dic:
            counter_sum += counter_dic[i]
        return counter_sum
    def mian(self):
        source_img_dic,source_annotations_nums = self.counter_cate(self.source_jsons_path,'imagePath')
        if self.cut_jsons_path:
            cut_img_dic,cut_annotations_nums = self.counter_cate(self.cut_jsons_path,'imagePathSource')
        if not os.path.exists(self.expect_annotations_file):
            os.makedirs(self.expect_annotations_file)
            with open(self.result_write,'a+',encoding='utf-8') as f:
                f.write('expect_annotations_file:{}\n'.format(self.expect_annotations_file))
            for img_name in source_img_dic:
                if not img_name in cut_img_dic:
                    jsons_name=img_name.replace('.jpg','.json')
                    shutil.copy(os.path.join(self.source_jsons_path,jsons_name),os.path.join(self.expect_annotations_file,jsons_name))
                    print('标注异常，无法cut的标注文件名：',jsons_name)
        source_anno_sum = self.sum_val_dic(source_annotations_nums)
        cut_anno_sum = self.sum_val_dic(cut_annotations_nums)
        source_annotations_c = sorted(source_annotations_nums.items(),key=lambda x:x[1],reverse=True)
        cut_annotations_c = sorted(cut_annotations_nums.items(),key=lambda x:x[1],reverse=True)
        with open(self.result_write,'a+',encoding='utf-8') as f:
            f.write('source_annotations_c:{}\n'.format(source_annotations_c))
            f.write('source_anno_sum:{}\n'.format(source_anno_sum))
            f.write('cut_annotations_c:{}\n'.format(cut_annotations_c))
            f.write('cut_anno_sum:{}\n'.format(cut_anno_sum))
        print('原标注：共{}个,cut 标注共{}个'.format(source_anno_sum,cut_anno_sum))
        print('原标注：\n{}'.format(source_annotations_c))
        print('cut标注：\n{}'.format(cut_annotations_c))

class Select_data(object):
    def __init__(self,data_rootpath,save_path):
        xml_path = os.path.join(data_rootpath,'outputs')
        except_save_path = os.path.join(save_path,'except_save_path')
        img_path_ls = glob.glob('{}/*.jpg'.format(data_rootpath))
        for i in os.listdir(xml_path):
            img_name = i.replace('.xml','.jpg')
            img_path = os.path.join(data_rootpath,img_name)
            if not img_path in  img_path_ls:
                if not os.path.exists(except_save_path):
                    os.makedirs(except_save_path)
                shutil.move(os.path.join(xml_path,i),os.path.join(except_save_path,i))
                print('xml无对应的img',i)
from labelme.utils import shape as shape_labelme
from pycocotools.mask import encode
import pycocotools.mask as maskUtils
from labelme.utils import shape as shape_labelme
from pycocotools.mask import encode
import pycocotools.mask as maskUtils
import numpy as np
import json
import multiprocessing
import glob
import time
class labelme2coco(object):
    def __init__(self,labelme_json=[],save_json_path='./new.json',resume_cate = None):
        '''
        :param labelme_json: 所有labelme的json文件路径组成的列表
        :param save_json_path: json保存位置
        '''
        self.labelme_json=labelme_json
        self.save_json_path=save_json_path
        self.height=0
        self.width=0
        self.save_json()
    def addshape(self,shape,data,num,annotations,categories,labels):
        label=shape['label'].split('_')
        # print('label',label[0],'labels:',labels,'--')
        if label[0] not in labels:
            # print(categories,'c---')
            labels.append(label[0])
            categories.append(self.categorie(label,labels))
            # print(categories,'c---1')
        # print('label1',label,'labels:',labels,'--')
        points=shape['points']
        plevel=shape['plevel']
        describe=shape['describe']
        w = data['imageWidth']
        h =data['imageHeight']
        shape_type =shape['shape_type']
        img_shape = (h,w, 3)
        # print('json_file:')
        annotations.append(self.annotation(img_shape,points,plevel, describe, label,num,shape_type,annotations,categories))

    def data_transfer(self):
        pool = multiprocessing.Pool(processes=32) # 创建进程个数
        images = []
        #images=multiprocessing.Manager().list()
        annotations = multiprocessing.Manager().list()
        print('anno',annotations)
        categories = multiprocessing.Manager().list()
        labels = multiprocessing.Manager().list()
        for num,json_file in enumerate(self.labelme_json):
            with open(json_file,'r',encoding='utf-8') as fp:
                print('json_file:---',json_file)
                data = json.load(fp)  # json
                #print('data',data)
                images.append(self.image(data,num))
                for shape in data['shapes']:
                    print('len(annotations)',len(annotations))
                    pool.apply_async(self.addshape,args=(shape,data,num,annotations,categories,labels))
        pool.close()
        pool.join()

        return (images,annotations,categories)

    def image(self,data,num):
        image={}
        height,width = data["imageHeight"],data["imageWidth"]
        image['height']=height
        image['width'] = width
        image['id']=num+1
        image['file_name'] = data['imagePath'].split('/')[-1]

        self.height=height
        self.width=width

        return image

    def categorie(self,label,labels):
        categorie={}
        categorie['supercategory'] = label[0]
        categorie['id']=len(labels)-1#+1 # 0 默认为背景
        categorie['name'] = label[0]
        return categorie

    def annotation(self,img_shape,points,plevel, describe, label,num,shape_type,annotations,categories):
        annotation={}
        mask = shape_labelme. shape_to_mask(img_shape[:2], points,shape_type)
        annotation['bbox'] = list(map(float,self.mask2box(mask)))
        mask =mask+0
        # print('img_shape, data["shapes"]',img_shape,shape_type,np.shape(mask))
        mask=np.asfortranarray(mask).astype('uint8')
        segm = encode(mask)#编码为rle格式
        annotation['area'] = float(maskUtils.area(segm))#计算mask编码的面积，必须放置在mask转字符串前面，否则计算为0
        segm['counts'] = bytes.decode(segm['counts'])#将字节编码转为字符串编码
        annotation['segmentation']=segm
        annotation['plevel']=plevel
        annotation['describe']=describe
        annotation['iscrowd'] = 0
        annotation['image_id'] = num+1
        # print('categories',categories)
        annotation['category_id'] = self.getcatid(label,categories)
        annotation['id'] = len(annotations)+1
        return annotation

    def getcatid(self,label,categories):
        for categorie in categories:
            if label[0]==categorie['name']:
                return categorie['id']
        return -1

    def mask2box(self, mask):
        '''从mask反算出其边框
        mask：[h,w]  0、1组成的图片
        1对应对象，只需计算1对应的行列号（左上角行列号，右下角行列号，就可以算出其边框）
        '''
        # np.where(mask==1)
        index = np.argwhere(mask == 1)
        rows = index[:, 0]
        clos = index[:, 1]
        # 解析左上角行列号
        left_top_r = np.min(rows)  # y
        left_top_c = np.min(clos)  # x

        # 解析右下角行列号
        right_bottom_r = np.max(rows)
        right_bottom_c = np.max(clos)
        return [left_top_c, left_top_r, right_bottom_c-left_top_c, right_bottom_r-left_top_r]  # [x1,y1,w,h] 对应COCO的bbox格式

    def data2coco(self,images,annotations,categories):
        # print(annotations,'===',type(annotations))
        # print(list(categories),'===',type(list(categories)))
        data_coco={}
        data_coco['images']=images
        data_coco['categories']=list(categories)
        data_coco['annotations']=list(annotations)
        return data_coco

    def save_json(self):
        # print('save')
        images,annotations,categories=self.data_transfer()
        # print('images',images)
        # print('annotations',annotations)
        print('categories',categories)
        data_coco = self.data2coco(images,annotations,categories)
        #print(data_coco)
        # # 保存json文件
        json.dump(data_coco, open(self.save_json_path, 'w',encoding='utf-8'), indent=4)

import json
class Modify_COCO_Cate(object):
    def __init__(self,cz_coco,coco,save_coco):
        self.cz_coco = cz_coco#参照cocojson
        self.coco = coco#待修改的cocojson
        self.save_coco = save_coco#修改后的cocojson
        self.modify(cz_coco,coco,save_coco)
    def save_json(self,dic,save_path):
        json.dump(dic, open(save_path, 'w',encoding='utf-8'), indent=4)  # indent=4 更加美观显示
    def parse_para(self,input_json):
        with open(input_json, 'r', encoding='utf-8') as f:
            ret_dic = json.load(f)
        return ret_dic
    def modify(self,cz_json,coco_json,save_coco_json):
        cz_json_data = self.parse_para(cz_json)
        cz_categories = cz_json_data['categories']
        coco_json_data = self.parse_para(coco_json)
        coco_json_cate = coco_json_data['categories']
        save_coco_dic ={}
        cz_cate_dic = {}
        coco_id_2_id_cate_dic = {}
        for i in cz_categories:
            cate_name = i['supercategory']
            cate_id = i['id']
            cz_cate_dic[cate_name]=cate_id
        for i in coco_json_cate:
            coco_cate_id = i['id']
            coco_cate_name = i['supercategory']
            coco_id_2_id_cate_dic[coco_cate_id]=cz_cate_dic[coco_cate_name]

        coco_annotations = coco_json_data['annotations']
        save_coco_annotations = []
        for i in coco_annotations:
            i['category_id']=coco_id_2_id_cate_dic[i['category_id']]
            save_coco_annotations.append(i)

        save_coco_dic['images']=coco_json_data['images']
        save_coco_dic['categories'] = cz_categories
        save_coco_dic['annotations']=save_coco_annotations
        self.save_json(save_coco_dic,save_coco_json)
if __name__ == "__main__":
    annotation_root_path = '/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/NEWSTART/adcm/cemian'
    out_coco_root_path = '/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/NEWSTART/adcm/cemian'
    # Select_data(annotation_root_path,out_coco_root_path)#过滤xml与img不符合情况

    img_jsons=os.path.join(annotation_root_path,'jsons')
    process_nums = 8
    result_write = os.path.join(out_coco_root_path,'2new_a_class_label.txt')
    xml2json =Xml2Labelme(annotation_root_path,img_jsons,result_write,process_nums)
    # # #
    # cut_label = xml2json.cut_label
    # cut_w,cut_h=2000,2000
    # out_path_result_cut= os.path.join(out_coco_root_path,'cuts')
    # expect_annotations_file = os.path.join(out_coco_root_path,'except_jsons')
    # #
    # print('root_path of cut_img:',out_path_result_cut)
    # cut_labelme = CutLabelme(annotation_root_path,img_jsons,out_path_result_cut,cut_label,process_nums,cut_w,cut_h,result_write)
    # utils_wy = UtilsMicroI(img_jsons,out_path_result_cut,result_write,expect_annotations_file)
    # #2coco
    # labelme_json=glob.glob('{}/*.json'.format(cut_labelme.out_path_result_cut))
    # coco_path = os.path.join(out_coco_root_path,'instances_coco.json')
    # labelme2coco(labelme_json,coco_path)
    #
    #
    # cz_json= r'D:\work\data\microsoft\jalama\second_data_merge_3\coco\annotations\instances_val2017.json'
    # save_json_path =os.path.join(out_coco_root_path,'instances_modify.json')
    # Modify_COCO_Cate(cz_json,coco_path,save_json_path)
    #
    #
    #2coco
    # labelme_json=glob.glob('/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/Anew/all/select_gs_dw/gsdw/gsdw/guaijiao/*.json')
    # coco_path = os.path.join('/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/Anew/all/select_gs_dw/gsdw/gsdw','instances_test_gj2017.json')
    # labelme2coco(labelme_json,coco_path)
    #
    # cz_json= '/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/second_A/2cuts/splite/annotations/instances_train2017.json'
    # save_json_path =os.path.join('/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/second_A/2cuts/splite/annotations','instances_val2017.json')
    # Modify_COCO_Cate(cz_json,coco_path,save_json_path)


