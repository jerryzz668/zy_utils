#---------------------------class6----------------------start
#对于coco格式的文件进行框抑制。输入coco格式的路径，需要保存的路径，以及抑制iou阈值。输出一个类，调用输出路径。nms = Pre_nms('C:/Users/xie5817026/PycharmProjects/pythonProject1/1228/htc462.json','./',0.1)
#print(nms.out_coco)
import shutil
import json
import os
import numpy as np
class Pre_nms(object):
    def __init__(self,pre_coco_json,out_p,iou_thr = 0.1):#seg,coco,output
        self.out_coco = self.main(pre_coco_json,out_p,iou_thr =iou_thr)
    def get_box(self,object1):
        xmin,ymin,w,h = object1['bbox']
        xmax,ymax = xmin+w,ymin+h
        return [xmin,ymin,xmax,ymax]
    def get_box_score(self,object1):
        xmin,ymin,w,h = object1['bbox']
        xmax,ymax = xmin+w,ymin+h
        score = object1['score']
        return [xmin,ymin,xmax,ymax,score]
    def save_json(self,dic,path):
        json.dump(dic, open(path, 'w',encoding='utf-8'), indent=4)
        return 0
    def parse_para(self,input_json):#解析标注数据
        with open(input_json, 'r', encoding='utf-8') as f:
            ret_dic = json.load(f)
            images = ret_dic['images']
            categories = ret_dic['categories']
            annotations = ret_dic['annotations']
        dic_img_id = {}
        for i_obj in annotations:
            img_id = i_obj['image_id']
            if img_id in dic_img_id:
                dic_img_id[img_id].append(i_obj)
            else:
                dic_img_id[img_id]=[i_obj]
        print('dic_img_id:',len(dic_img_id))
        return (images,categories,dic_img_id)
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
    def single_img_annotation(self,annotations):#预测结果json,annotations=[{'image_id':1,...},{}]，flag=1预测标注；flag=0实际标注
        img_id_anno_dic={}
        print(len(annotations),'--')
        for annotation in annotations:
            try:
                image_id = annotation['image_id']
                #print(annotation,'--',c)
            except:
                print('---1')

            if image_id in img_id_anno_dic:
                img_id_anno_dic[image_id].append(annotation)
            else:
                img_id_anno_dic[image_id]=[annotation]
        return img_id_anno_dic#{'1':[{},{}]}
    def py_cpu_nms(self,dets, thresh):
        #print('det',dets)
        x1 = dets[:,0]
        y1 = dets[:,1]
        x2 = dets[:,2]
        y2 = dets[:,3]
        areas = (y2-y1+1) * (x2-x1+1)
        scores = dets[:,4]
        keep = []
        index = scores.argsort()[::-1]
        while index.size >0:
            i = index[0]       # every time the first is the biggst, and add it directly
            keep.append(i)
            x11 = np.maximum(x1[i], x1[index[1:]])    # calculate the points of overlap
            y11 = np.maximum(y1[i], y1[index[1:]])
            x22 = np.minimum(x2[i], x2[index[1:]])
            y22 = np.minimum(y2[i], y2[index[1:]])
            w = np.maximum(0, x22-x11+1)    # the weights of overlap
            h = np.maximum(0, y22-y11+1)    # the height of overlap

            overlaps = w*h
            ious = overlaps / (areas[i]+areas[index[1:]] - overlaps)
            idx = np.where(ious<=thresh)[0]
            index = index[idx+1]   # because index start from 1
        return keep
    def save_nms_coco_model(self,images,categories,annotations,savejson='pre_nms.json'):
        new_dic = {}
        new_dic['images'] = images
        new_dic['categories'] = categories
        new_dic['annotations'] = annotations
        self.save_json(new_dic,savejson)
    def main(self,coco_json,out_p,iou_thr = 0.1):
        out_coco_name = 'htc{}'.format(coco_json.split('htc')[-1])#instances_test_cemian.json
        #out_coco_name = 'instances{}'.format(coco_json.split('instances')[-1])#instances_test_cemian.json
        print(out_coco_name,'---')
        if not os.path.exists(out_p):
            os.makedirs(out_p)
        out_coco = os.path.join(out_p,out_coco_name)
        images,categories,annotations = self.parse_para(coco_json)#gt
        annotations_nms_before = []
        annotations_nms_after = []
        for img_id in annotations:#{'imgid1':[anno1,anno2]}
            anno_img = annotations[img_id]
            if len(anno_img)==0:
                print(img_id,'预测目标为0')
            boxxes = []
            box_id_dic ={}
            for anno_obj in anno_img:#[anno1,anno2]
                bbox = self.get_box_score(anno_obj)
                boxxes.append(bbox)
                box_id_dic[len(boxxes)-1]=anno_obj
                annotations_nms_before.append(anno_obj)
            if len(boxxes)==0:
                print('det is zero')
            else:
                keep = self.py_cpu_nms(np.array(boxxes), thresh=iou_thr)#抑制后的索引
                for index_s in keep:
                    annotations_nms_after.append(box_id_dic[index_s])
        print('iou阈值：{}；抑制前：{}，抑制后：{},rate:{}'.format(iou_thr,len(annotations_nms_before),len(annotations_nms_after),len(annotations_nms_after)/len(annotations_nms_before)))
        self.save_nms_coco_model(images,categories,annotations_nms_after,out_coco)
        # for i in annotations_nms_after:
        #     img_i = i['image_id']
        #     print('====',img_i)
        return out_coco

if __name__ == '__main__':
    #nms
    merge_coco = '/home/lijq/data/A/380_r/dm/htc380dm.json'
    coco_model_json_nms_path='/home/lijq/data/A/380_r/preanno/dm/nms'
    iou_thr=0.4
    Pre_nms(merge_coco,coco_model_json_nms_path,iou_thr)
