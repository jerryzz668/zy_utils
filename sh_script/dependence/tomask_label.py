from labelme import utils
import multiprocessing
import json
import time
import cv2
import os
import shutil
import sys
from preprocessing.zy_utils import json_to_instance

class ToMaskLabel(object):
    def __init__(self,cut_jsons_path,train_and_val_path,save_mask_path,save_seg_label_path,mask_except,process_nums=8):
        self.cut_jsons_path = cut_jsons_path
        self.train_and_val_path = train_and_val_path
        self.class_mapers = self.get_categories()
        self.save_mask_path = save_mask_path
        self.save_seg_label_path = save_seg_label_path
        self.process_nums = process_nums
        self.mask_except = mask_except

        if not os.path.exists(save_mask_path):
            os.makedirs(save_mask_path)
        if not os.path.exists(save_seg_label_path):
            os.makedirs(save_seg_label_path)
        if not os.path.exists(mask_except):
            os.makedirs(mask_except)
        self.main()

    def get_categories(self):
        # 获得所有label并按字母排序
        cls = []
        class_mapers = {'a': 0}
        for file in os.listdir(self.train_and_val_path):
            if not file.endswith('.json'): continue
            instance = json_to_instance(os.path.join(self.train_and_val_path, file))
            for obj in instance['shapes']:
                if obj['label'] not in cls:
                    cls.append(obj['label'])
        cls = sorted(cls)
        for i, cl in enumerate(cls):
            class_mapers[cl] = i + 1
        return class_mapers

    def main(self):
        input_ts = []
        for file_name in os.listdir(self.cut_jsons_path):
            json_p = os.path.join(self.cut_jsons_path,file_name)
            if file_name.endswith('.json'):
                name = file_name.split('.json')[0]
                r_mask = os.path.join(self.save_mask_path,name)
                r_label = os.path.join(self.save_seg_label_path,name)
                r_mask_except = os.path.join(self.mask_except,name)
                input_ts.append((json_p,r_mask,r_label,r_mask_except))
        pool = multiprocessing.Pool(processes=self.process_nums) # 创建进程个数
        pool.map(self.toMaskLabel,input_ts)
        pool.close()
        pool.join()
    def toMaskLabel(self,input):
        json_file,r_mask,r_label,mask_except = input
        data = json.load(open(json_file,encoding='utf8'))
        data['imageDepth']=3
        img_shape = (data['imageHeight'],data['imageWidth'],data['imageDepth'])
        try:
            # print('data["shapes"]',len(data["shapes"]))
            if len(data["shapes"])==0:
                shutil.move(json_file,'{}.json'.format(mask_except))
                print(json_file,'为空，请检查json！')
            lbl, _ = utils.shapes_to_label(img_shape, data["shapes"], self.class_mapers)
            utils.lblsave(r_mask, lbl)
            img_data = cv2.imread('{}.png'.format(r_mask))
            img_data_grey = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
            cv2.imwrite('{}.png'.format(r_label), img_data_grey)
            # print('正在处理：',r_label,json_file)
        except:
            #shutil.move(json_file,'{}.json'.format(mask_except))
            print('异常处理：',json_file,'e')
if __name__ == '__main__':
    # class_mapers ={'a': 0, 'sguashang': 1, 'aotuhen1': 2, 'aotuhen2': 3, 'baidian': 4, 'bianxing': 5,
    #                'daowen': 6, 'diaoqi': 7, 'guashang': 8, 'guoqie': 9, 'heidian': 10,
    #                'jiaxi': 11, 'keli': 12, 'maoxu': 13, 'pengshang': 14, 'tabian': 15,'xianhen': 16, 'yashang': 17, 'yinglihen': 18, 'yise': 19, 'yiwu': 20}
    cut_jsons_path = sys.argv[1]  # train or val img and jsons
    train_and_val_path = sys.argv[2]  # all img and jsons
    mask = sys.argv[3]  # color mask
    save_seg_label_path = sys.argv[4]  # gray mask
    mask_except = os.path.join(os.path.dirname(cut_jsons_path), 'stuffthingmaps', 'empty_json')
    s = time.time()
    tomasklabel = ToMaskLabel(cut_jsons_path=cut_jsons_path,train_and_val_path=train_and_val_path,save_mask_path=mask,
                              save_seg_label_path=save_seg_label_path,mask_except=mask_except,process_nums=8)
    print('tomask_label:',time.time()-s)