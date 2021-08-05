# @Description: 按照label_list中缺陷的顺序依次移动到新的文件夹中
# @Author     : zhangyan
# @Time       : 2021/1/15 1:56 下午

import os
import shutil
import time
from preprocessing.zy_utils import json_to_instance, make_dir2

def get_json_label(json_path):
    """
    @param json_file: just json files / json files and img files also can be put in one folder
    @return: img_name and json_label_list
    """
    instance = json_to_instance(json_path)
    img = instance.get('imagePath')
    shapes = instance.get('shapes')
    json_label_list = []
    for i in range(len(shapes)):
        json_label_list.append(shapes[i].get('label'))
    return img, json_label_list

def move_json_file(json_path, label_list, json_save_path):
    t0 = time.time()
    attention = False
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
                shutil.move(json_file_path, target_path)  # Attention: this is move
                try:
                    shutil.move(img_file_path, target_path)  # Attention: this is move
                except:
                    print('there is no %s' % img_file_path)
            else:
                attention = True
        if attention:
            print('There is no {}!'.format(label_list[i]))
        if not attention:
            print(label_list[i] + ' has been moved!')
    t1 = time.time()
    print('time:', t1-t0)

if __name__ == '__main__':
    label_list = ['shahenyin', 'guashang']  # 按照label_list中的先后顺序,将img和json同时移动到新的文件夹中
    json_path = '/home/jerry/data/kesen/labelme_31490_jbl/labelme_val'
    json_save_path = '/home/jerry/data/kesen/labelme_31490_jbl/garbage'  # Automatically create a save_path folder
    move_json_file(json_path, label_list, json_save_path)