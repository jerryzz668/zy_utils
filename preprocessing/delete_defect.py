import os
import glob
import sys
import shutil
from preprocessing.zy_utils import json_to_instance, instance_to_json, make_dir

def cut_defect(json_file_path, defect_list, json_out_path):
    shape_list = []
    instance = json_to_instance(json_file_path)

    for obj in instance['shapes']:
        if (obj["label"]) in defect_list:
            shape_list.append(obj)
    instance['shapes'] = shape_list
    instance_to_json(instance, json_out_path)

def cut_defects(json_path, defect_list):
    json_o_path = os.path.join(os.path.dirname(json_path),
                               os.path.basename(json_path) + '_update')  # Automatically create output json folders
    make_dir(json_o_path)
    json_list = glob.glob('{}/*.json'.format(json_path))

    for json_file_path in json_list:
        json_name = os.path.basename(json_file_path)
        jpg_name = json_name.split('.')[0] + '.jpg'
        json_out_path = os.path.join(json_o_path, json_name)
        cut_defect(json_file_path, defect_list, json_out_path)
        try:
            shutil.copy(os.path.join(json_path, jpg_name), os.path.join(json_o_path, jpg_name))
        except:
            print('there is no {}'.format(jpg_name))

if __name__ == '__main__':
    # python delete_defect.py json_path defect_list
    defect_list = ['yashang', 'huashang']  # 需要保留的缺陷
    json_path = '/home/jerry/data/kesen/labelme_28413_hy/pr_save'  # input json path
    cut_defects(json_path, defect_list)  # Automatically create output json folders
    # cut_defects(sys.argv[1], sys.argv[2])  # Automatically create output json folders
