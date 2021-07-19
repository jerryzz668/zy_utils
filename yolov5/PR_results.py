"""
@Description:
@Author     : zhangyan
@Time       : 2021/7/19 上午11:06
"""
from preprocessing.zy_utils import *
import collections
"""
输入两个txt文件夹（）
输出print每个类别的总缺陷个数，missing,over-detect
"""

gt_txt_dir = '/home/jerry/Desktop/for_missing_and_over/gt'
pre_txt_dir = '/home/jerry/Desktop/for_missing_and_over/pre'
cls_yaml_dir = '/home/jerry/Desktop/for_missing_and_over/kesen_33074_hy_512.yaml'
iou_threshold = 0.3

cfg_yolo = yaml_to_instance(cls_yaml_dir)
cfg_cls_name = cfg_yolo['names']
cls_id_name_dict = dict(zip(range(len(cfg_cls_name)),cfg_cls_name))

gt_list = os.listdir(gt_txt_dir)
pre_list = os.listdir(pre_txt_dir)

# 1.gt统计
gt_number = []
for gt_file in gt_list:
    gt_lines = read_txt(os.path.join(gt_txt_dir, gt_file))
    for line in gt_lines:
        word = line.split(' ')
        cls_id = int(word[0])
        gt_number.append(cls_id)
gt_number_arr = collections.Counter(gt_number).most_common()
print(gt_number)
print(gt_number_arr)

# 2.全漏失统计
total_missing_number = []
total_missing_list = [i for i in gt_list if i not in pre_list]
for missing in total_missing_list:
    total_missing_path = os.path.join(gt_txt_dir, missing)
    txt_lines = read_txt(total_missing_path)
    for line in txt_lines:
        words = line.split(' ')
        cls_id = int(words[0])
        total_missing_number.append(cls_id)
total_missing_number_arr = collections.Counter(total_missing_number).most_common()
print(total_missing_number)
print(total_missing_number_arr)

# 3.非全漏失统计
no_total_missing_number = []
no_total_missing_list = [i for i in gt_list if i in pre_list]
for missing in no_total_missing_list:
    gt_txt_lines = read_txt(os.path.join(gt_txt_dir, missing))
    pre_txt_lines = read_txt(os.path.join(pre_txt_dir, missing))
    for gt_line in gt_txt_lines:
        gt_iou_list = []
        gt_x, gt_y, gt_w, gt_h, gt_c = yolo_to_xywh(gt_line)
        gt_box = Box(gt_x, gt_y, gt_w, gt_h, gt_c)
        for i, pre_line in enumerate(pre_txt_lines):
            pre_x, pre_y, pre_w, pre_h, pre_c = yolo_to_xywh(pre_line)
            pre_box = Box(pre_x, pre_y, pre_w, pre_h, pre_c)
            if gt_box.get_iou(pre_box) > iou_threshold:  # 不管类别，只算iou
                gt_iou_list.append([i, gt_box.get_iou(pre_box)])
        if not gt_iou_list:
            no_total_missing_number.append(gt_line[0])
no_total_missing_number_arr = collections.Counter(no_total_missing_number).most_common()
print(no_total_missing_number)
print(no_total_missing_number_arr)

# 4.过检统计
over_detect_number = []
for pre_file in pre_list:
    pre_txt_lines = read_txt(os.path.join(pre_txt_dir, pre_file))
    gt_txt_lines = read_txt(os.path.join(gt_txt_dir, pre_file))
    for pre_line in pre_txt_lines:
        pre_iou_list = []
        pre_x, pre_y, pre_w, pre_h, pre_c = yolo_to_xywh(pre_line)
        pre_box = Box(pre_x, pre_y, pre_w, pre_h, pre_c)
        for gt_line in gt_txt_lines:
            gt_x, gt_y, gt_w, gt_h, gt_c = yolo_to_xywh(gt_line)
            gt_box = Box(gt_x, gt_y, gt_w, gt_h, gt_c)
            if pre_box.get_iou(gt_box) < iou_threshold:
                pre_iou_list.append(pre_box.get_iou(gt_box))
        if len(pre_iou_list) == len(gt_txt_lines):
            over_detect_number.append(pre_line[0])
over_detect_number_arr = collections.Counter(over_detect_number).most_common()
print(over_detect_number)
print(over_detect_number_arr)