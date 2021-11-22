# @Description: 按照label_list中缺陷的顺序依次移动到新的文件夹中
# @Author     : zhangyan
# @Time       : 2021/1/15 1:56 下午

import os
import shutil
import time
from preprocessing.zy_utils import json_to_instance, make_dir2

def get_json_label(json_path):
    instance = json_to_instance(json_path)
    img = instance.get('imagePath')
    shapes = instance.get('shapes')
    json_label_list = []
    for i in range(len(shapes)):
        json_label_list.append(shapes[i].get('label'))
    return img, json_label_list

def move_json_file(json_path, json_save_path, label_list):
    t0 = time.time()
    make_dir2(json_save_path, label_list)
    for i in range(len(label_list)):
        json_files = os.listdir(json_path)
        target_path = os.path.join(json_save_path, label_list[i])

        for json_file in json_files:
            if not json_file.endswith('.json'): continue
            json_file_path = os.path.join(json_path, json_file)
            img_file_path = json_file_path[:json_file_path.rindex('.')] + '.jpg'
            img_name, json_label_list = get_json_label(json_file_path)
            if label_list[i] in json_label_list:
                shutil.copy(json_file_path, target_path)  # Attention: you can change copy to move~
                try:
                    shutil.copy(img_file_path, target_path)  # Attention: you can change copy to move~
                except:
                    print('there is no %s' % img_file_path)

        print(label_list[i] + ' has been moved!')
    t1 = time.time()
    print('time:', t1-t0)

if __name__ == '__main__':
    label_list = ['daowen']  # 按照label_list中的先后顺序,将img和json同时移动到新的文件夹中

    json_path = '/home/jerry/data/Micro_D/D_loushi/D_ng/11-10-D-labelme/labelme_split/dm'
    json_save_path = '/home/jerry/data/Micro_D/D_loushi/D_ng/11-10-D-labelme/labelme_split/dm_dw'  # Automatically create a save_path folder
    move_json_file(json_path, json_save_path, label_list)