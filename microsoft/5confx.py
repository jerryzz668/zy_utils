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
        self.compute_confmx()

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
        print('cm',cm)
        print('cmp',cm_pro)

        self.plot_confusion_matrix(cm,classes,'nums')
        self.plot_confusion_matrix(cm_pro,classes,'pro',normalize=True)
        print('confx',cm)
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


if __name__ == '__main__':
    print('分析标注结果生成混淆矩阵')
    AnnalyResult(r'C:\Users\Administrator\Desktop\gt\jsons',#biaozhu jsons
                 r'G:\ttt\test\json',#pre jsons
                 r'C:\Users\Administrator\Desktop\gt\outputs_path',#splite result file
                 '140model_0420testdata')# 混淆矩阵图像名字，不带后缀