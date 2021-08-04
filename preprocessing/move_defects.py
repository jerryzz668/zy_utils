# @Description: 按照label_list中缺陷的顺序依次移动到新的文件夹中
# @Author     : zhangyan
# @Time       : 2021/1/15 1:56 下午

from preprocessing.zy_utils import *
import os
import shutil
import time

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
    make_dir2(json_save_path, label_list)
    for i in range(len(label_list)):
        json_files = os.listdir(json_path)
        target_path = os.path.join(json_save_path, label_list[i])

        len_label = 0
        for json_file in json_files:
            if not json_file.endswith('.json'): continue
            json_file_path = os.path.join(json_path, json_file)
            img_file_path = json_file_path[:json_file_path.rindex('.')] + '.jpg'
            img_name, json_label_list = get_json_label(json_file_path)
            if label_list[i] in json_label_list:
                shutil.move(json_file_path, target_path)
                try:
                    shutil.move(img_file_path, target_path)
                except:
                    print('there is no %s' % img_file_path)
            len_label += 1
        print(label_list[i] + ' has been moved!')
    t1 = time.time()
    print('time:', t1-t0)

if __name__ == '__main__':
    label_list = ['shahenyin', 'guashang']  # 按照label_list中的先后顺序,将img和json依次移动到新的文件夹中
    json_path = '/home/adt/data/data/Djian/cemian_crop_qingxi/val_cemian_crop/select/crop'
    json_save_path = '/home/adt/data/data/Djian/yolo_shahenyin_guashang/images/val'  # Automatically create a save_path folder
    move_json_file(json_path, label_list, json_save_path)