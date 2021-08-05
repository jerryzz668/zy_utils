from pycocotools.mask import decode
import numpy as np
import json
import cv2
import os
'''
@Description: 将coco格式的json转化为对应图像的json文件，用于labelme查看或后续生成可使用的coco
@author: lijianqing
@date: 2020/12/11 15:37
'''
class Coco2Labelme(object):
    def __init__(self,coco_path,out_path):
        self.coco_path = coco_path
        self.out_path = out_path
        self.main()

    def save_json(self,dic,save_path):
        json.dump(dic, open(save_path, 'w', encoding='utf-8'), indent=4)
    def def_new_json(self, i, new_name, out_p):
        new_json = {}
        new_json['flags'] = {}
        new_json['imageData'] = None
        new_json['imageDepth'] = 3
        new_json['imageHeight'] = i['img_h']
        new_json['imageLabeled'] = "true"
        new_json['imagePath'] = i['img_path']
        new_json['imageWidth'] = i['img_w']
        new_json['shapes'] = i['shapes']
        new_json['time_Labeled'] = None
        new_json['version'] = "1.0"
        self.save_json(new_json,os.path.join(out_p,new_name))
        # print('生成了',os.path.join(out_p,new_name))
        return new_json
    def def_dic_element(self,shapes_img,i):
        dic_element = {}
        dic_element['label'] = i['label']
        # shape_type = modify_type('polygon',i['points'])
        dic_element['width'] = 1
        if len(i['points']) == 1:
            points = [[i['bbox'][0], i['bbox'][1]], [i['bbox'][0]+i['bbox'][2], i['bbox'][1]+i['bbox'][3]]]
            shape_type = 'rectangle'
        else:
            points = i['points']
            shape_type = 'polygon'
        dic_element['shape_type'] = shape_type
        dic_element['points'] = points
        dic_element['group_id'] = ""
        dic_element['flags'] = {}
        dic_element['level'] = ""
        dic_element['area'] = i['area']
        dic_element['bbox'] = i['bbox']
        dic_element['imagePathSource'] = i['imagePathSource']
        shapes_img.append(dic_element)
        return shapes_img
    def parse_para(self,input_json):
        with open(input_json, 'r', encoding='utf-8') as f:
            ret_dic = json.load(f)
        return ret_dic
    def parse_img_c_a(self,coco_data):
        imgs_cate = coco_data['images']
        cate_cate = coco_data['categories']
        annotations = coco_data['annotations']
        img_id_name_dic = {}
        cate_id_name_dic = {}
        annotation_imgid_anno_dic = {}
        for i in imgs_cate:
            img_id_name_dic[i['id']] = i['file_name']
        for i in cate_cate:
            cate_id_name_dic[i['id']] = i['name']
        for i in annotations:
            img_id = i['image_id']
            if img_id not in annotation_imgid_anno_dic:
                annotation_imgid_anno_dic[img_id] = [i]
            else:
                annotation_imgid_anno_dic[img_id].append(i)
        return (img_id_name_dic, cate_id_name_dic, annotation_imgid_anno_dic)
    # mask转二值图 黑白两色
    def mask2bw(self,mask):
        # print('mask_shape',mask)
        # print(mask)
        for i in range(len(mask)):
            for j in range(len(mask[i])):
                if mask[i][j]==1:
                    mask[i][j]=255
        return mask
    # 提取二值图轮廓
    def getContoursBinary(self,blimg):
        print(blimg.shape)
        ret, binary = cv2.threshold(blimg, 0.5, 255, cv2.THRESH_BINARY)
        print(binary.shape)
        # ret, binary = cv2.threshold(blimg, 127, 255, cv2.THRESH_BINARY)
        # _, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        # print(contours)
        return contours
    def main(self):
        coco_data = self.parse_para(self.coco_path)
        img_id_name_dic,cate_id_name_dic,annotation_imgid_anno_dic = self.parse_img_c_a(coco_data)
        for i in annotation_imgid_anno_dic:
            shapes = []
            one_img_anno = annotation_imgid_anno_dic[i]
            obj = {}
            anno_dic = {}
            for j in one_img_anno:
                segmentation = j['segmentation']
                img_w, img_h = segmentation['size']
                mask = decode(segmentation)
                # mask = self.mask2bw(mask)
                contours = self.getContoursBinary(mask)
                # print('contours',contours)
                if len(contours) != 0:
                    points=np.squeeze(contours[0]).tolist()
                    if len(np.shape(points)) == 1:  # (1,1,2)-np.squeeze->(2,)  ---->(1,2)
                        points = [points]
                    obj['label'] = cate_id_name_dic[j['category_id']]
                    obj['area'] = j['area']
                    print('-area--', j['area'])
                    obj['bbox'] = j['bbox']
                    obj['imagePathSource'] = ""
                    obj['points'] = points
                    shapes = self.def_dic_element(shapes,obj)

            anno_dic['shapes'] = shapes
            anno_dic['img_w'] = img_w
            anno_dic['img_h'] = img_h
            # print('img_id_name_dic',img_id_name_dic)
            anno_dic['img_path'] = img_id_name_dic[i]
            new_name=img_id_name_dic[i].replace('.jpg', '.json')
            self.def_new_json(anno_dic, new_name, self.out_path)
coco2labelme = Coco2Labelme('/home/lijq/PycharmProjects/micro-i-tools/instances_train20171.json',
                            '/home/lijq/Desktop/merge_ad_cut/coco2lableme')