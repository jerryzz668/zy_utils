
import json
import os
import cv2
import random
'''
@Description: 
            主要功能：
            关键处理：
@author: lijianqing
@date: 2020/11/24 16:45
@return 
'''
class Cut_edge(object):
    def __init__(self,root_path,out_path,start_point=[0,0],crop_w = 2048,crop_h = 2048,anno=True):
        # root_path = r'C:\Users\xie5817026\Desktop\damian\jalama\jalama',labelme格式的数据路径，若有标注数据时同时存放img和json文件,若无标注信息时只处理图
        # out_path = r'C:\Users\xie5817026\Desktop\damian\jalama\jalama',切图后的路径，有则直接保存，无则创建路径后再保存。
        # #start_point=[1004,66]#shu
        # #start_point=[321,778]#hen
        # start_point=[96,46]#hen wx
        # #start_point=[96,46]#hen wx
        # print(type(start_point[0]),'--')
        # crop_w = 3308
        # crop_h = 4854
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        for i in os.listdir(root_path):
            if anno:
                if i.endswith('.json'):
                    jsons_path = os.path.join(root_path,i)
                    self.cut_json(jsons_path,root_path,out_path,start_point,crop_w,crop_h)
            else:
                if i.endswith('.jpg'):
                    img_n = os.path.join(root_path,i)#原图像名
                    print('img_n',img_n)
                    img_np = cv2.imread(img_n)#原图数据
                    self.save_new_img(img_np,i,start_point[0],start_point[1],start_point[0]+crop_w,start_point[1]+crop_h,out_path)

    def save_json(self,dic,save_path):
        json.dump(dic, open(save_path, 'w',encoding='utf-8'), indent=4)
    def save_new_img(self,img_np,img_name,xmin,ymin,xmax,ymax,out_path):
        # 切图并保存
        print('-111-',xmin,ymin,xmax,ymax)
        xmin,ymin,xmax,ymax = int(xmin),int(ymin),int(xmax),int(ymax)
        left,top,right,down = 0,0,0,0#need padding size
        img_crop = img_np[ymin:ymax,xmin:xmax]
        ret = cv2.copyMakeBorder(img_crop, top, down, left, right, cv2.BORDER_CONSTANT, value=(0,0,0))#padding
        cv2.imwrite(os.path.join(out_path, img_name), ret)
        return 0
    def get_new_location(self,point,start_point):
        print(start_point,'--')
        print(type(start_point[0]),'---',type(point[0]))
        return [point[0]-start_point[0],point[1]-start_point[1]]

    def cut_json(self,json_p,img_sourc,out_path,start_point,w,h):
        with open(json_p, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        img_n = os.path.join(img_sourc,json_data['imagePath'])#原图像名
        print('img_n',img_n)
        img_np = cv2.imread(img_n)#原图数据
        json_data['imageHeight']=h
        json_data['imageWidth']=w
        for index_object in json_data['shapes']:
            points = index_object['points']
            new_points = []
            for i in points:
                n_p = self.get_new_location(i,start_point)
                new_points.append(n_p)
            index_object['points']=new_points
        self.save_new_img(img_np,json_data['imagePath'],start_point[0],start_point[1],start_point[0]+w,start_point[1]+h,out_path)
        new_name_json = json_data['imagePath'].replace('jpg','json')
        self.save_json(json_data,os.path.join(out_path,new_name_json))
if __name__ == '__main__':
    # root_path = r'C:\Users\xie5817026\Desktop\damian\jalama\jalama'
    # out_path = r'C:\Users\xie5817026\Desktop\damian\jalama\jalama1'
    root_path = '/Users/zhangyan/Desktop/new_ja'
    out_path = '/Users/zhangyan/Desktop/output2'
    a1, a2 = random.randint(1000,3000), random.randint(1000,1400)

    Cut_edge(root_path,out_path,start_point = [a1,a2],crop_w = 2048,crop_h = 2048,anno=False)