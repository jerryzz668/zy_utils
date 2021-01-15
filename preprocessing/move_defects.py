# @Description: 按照label_list中缺陷的顺序依次移动到新的文件夹中
# @Author     : zhangyan
# @Time       : 2021/1/15 1:56 下午

from preprocessing.utils import *
import os
import shutil
import time

def get_json_label(json_path):
    """
    @param json_file: just json files
    @return: img_name and json_label_list
    """
    instance = json_to_instance(json_path)
    img = instance.get('imagePath')
    shapes = instance.get('shapes')
    json_label_list = []
    for i in range(len(shapes)):
        json_label_list.append(shapes[i].get('label'))
    return img, json_label_list

def make_dir(base_path, folders):
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

def move_json_file(json_path, label_list, json_save_path):
    t0 = time.time()
    make_dir(json_save_path, label_list)
    for i in range(len(label_list)):
        json_files = os.listdir(json_path)
        target_path = os.path.join(json_save_path, label_list[i])

        len_label = 0
        for json_file in json_files:
            json_file_path = os.path.join(json_path, json_file)
            img_name, json_label_list = get_json_label(json_file_path)
            if label_list[i] in json_label_list:
                shutil.move(json_file_path, target_path)
            len_label += 1
        print(label_list[i] + ' has been moved!')
    t1 = time.time()
    print('time:', t1-t0)

if __name__ == '__main__':
    # label_list = ['heidian', 'guashang', 'daowen', 'yise', 'baisezaodian', 'pengshang', 'aotuhen', 'aokeng', 'huanxingdaowen']
    label_list = ['huanxingdaowen']
    json_path = '/Users/zhangyan/Desktop/a件_0830damian/0830img/train/jsons'
    json_save_path = '/Users/zhangyan/Desktop/def'
    move_json_file(json_path, label_list, json_save_path)