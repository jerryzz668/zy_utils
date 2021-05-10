import os
import json
import cv2
class Merge_cut4(object):
    def __init__(self,cut_json_p,source_img_p,save_p):
        self.main(cut_json_p,source_img_p,save_p)
    def parse_para(self,input_json):
        print('input_json',input_json)
        with open(input_json, 'r', encoding='utf-8') as f:
            ret_dic = json.load(f)
        return ret_dic
    def save_json(self,dic,save_path):
        json.dump(dic, open(save_path, 'w',encoding='utf-8'), indent=4)
    def def_new_json(self,new_name,out_p,w,h,shapes):
        new_json = {}
        new_json['flags'] = {}
        new_json['imageData'] = None
        new_json['imageDepth'] = 3
        new_json['imageHeight'] = h
        new_json['imageLabeled'] = "true"
        new_json['imagePath'] = new_name
        new_json['imageWidth'] = w
        new_json['shapes'] = shapes
        new_json['time_Labeled'] = None
        new_json['version'] = "1.0"
        self.save_json(new_json,out_p)
        # print('生成了',os.path.join(out_p,new_name))
        return new_json

    def fy(self,x,y,points,w,h):
        x0=0
        y0=0
        #print('jjj',y)
        if x=='1':
            x0=w/2-50
        if y=='1':
            y0=h/2-50
            print('y0',y0)
        points_new = []
        for i in points:
            x = i[0]+x0
            y = i[1]+y0
            points_new.append([x,y])
        return points_new

    def main(self,cut_json_p,source_img_p,save_p):
        # cut_json_p = r'D:\work\data\microsoft\jalama\test1231\1203\1203damian\0.1\nms\275'#切图的json文件，不可以带与图像混合存放
        # source_img_p = r'D:\work\data\microsoft\jalama\test1231\1203\1203damian\imgs'#原图的图像文件
        # save_p = r'D:\work\data\microsoft\jalama\test1231\1203\1203damian\0.1merge\275'#合并图的结果文件
        img_dic = {}
        for n in os.listdir(cut_json_p):
            print('n',n)
            x,y,name = n.split('_')
            img_name = name.replace('.json','.jpg')
            if img_name in img_dic:
                img_dic[img_name].append(n)
            else:
                img_dic[img_name]=[n]
        print('len',len(img_dic))
        #print('len',img_dic)
        for img_one in img_dic:
            img_p = os.path.join(source_img_p,img_one)
            try:
                imgsize = cv2.imread(img_p).shape

                h=imgsize[0]
                w=imgsize[1]
                shapes = []
                # print(h,w)
                for json_one in img_dic[img_one]:
                    j_p = os.path.join(cut_json_p,json_one)
                    print(j_p)
                    data = self.parse_para(j_p)
                    shapes_json = data['shapes']
                    for k in shapes_json:
                        points = k['points']
                        x,y,name = json_one.split('_')
                        print(x,y,'--')
                        new_points = self.fy(x,y,points,w,h)
                        k['points']=new_points
                        shapes.append(k)
                json_name = img_one.replace('.jpg','.json')
                save_name = os.path.join(save_p,json_name)
                #print(save_name)
                self.def_new_json(new_name=img_one,out_p = save_name,w=w,h=h,shapes=shapes)

            except:
                print('----------'+img_p)
if __name__ == '__main__':
    Merge_cut4(cut_json_p = '/home/lijq/data/A/380_r/preanno/dm/prejson',
               source_img_p = '/home/lijq/data/A/test_a_coco/coco_test_confirm/dmy',
               save_p = r'/home/lijq/data/A/380_r/preanno/dm/premerge')##切图的json文件，不可以带与图像混合存放,