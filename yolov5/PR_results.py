"""
@Description:
@Author     : zhangyan
@Time       : 2021/7/19 上午11:06
"""
from preprocessing.zy_utils import *
from collections import Counter
import pandas as pd

# gt和全漏失统计
def gt_total_missing_statistics(gt_txt_dir, total_missing_list, iou_threshold):
    total_missing_number = []
    for missing in total_missing_list:
        total_missing_path = os.path.join(gt_txt_dir, missing)
        txt_lines = read_txt(total_missing_path)
        for line in txt_lines:
            words = line.split(' ')
            cls_id = int(words[0])
            total_missing_number.append(cls_id)
    return Counter(total_missing_number)

# 非全漏失和过检统计
def missing_over_detect_statistics(gt_txt_dir, pre_txt_dir, iou_threshold):
    gt_list = os.listdir(gt_txt_dir)
    pre_list = os.listdir(pre_txt_dir)
    no_total_missing_number = []
    no_total_missing_list = [i for i in gt_list if i in pre_list]
    for missing in no_total_missing_list:
        gt_txt_lines = read_txt(os.path.join(gt_txt_dir, missing))
        pre_txt_lines = read_txt(os.path.join(pre_txt_dir, missing))
        for gt_line in gt_txt_lines:
            temp = []
            gt_x, gt_y, gt_w, gt_h, gt_c = yolo_to_xywh(gt_line)
            gt_box = Box(gt_x, gt_y, gt_w, gt_h, gt_c)
            for i, pre_line in enumerate(pre_txt_lines):
                pre_x, pre_y, pre_w, pre_h, pre_c = yolo_to_xywh(pre_line)
                pre_box = Box(pre_x, pre_y, pre_w, pre_h, pre_c)
                if gt_box.get_iou(pre_box) < iou_threshold:  # 不管类别，只算iou
                    temp.append(i)
                elif gt_box.get_iou(pre_box) > iou_threshold and pre_c != gt_c:
                    pass
            if len(temp) == len(pre_txt_lines):
                no_total_missing_number.append(int(gt_line[0]))
    return Counter(no_total_missing_number)

def txt_to_dataframe(gt_txt_dir, pre_txt_dir, cls_yaml_dir, iou_threshold):
    cfg_yolo = yaml_to_instance(cls_yaml_dir)
    cfg_cls_name = cfg_yolo['names']
    # cls_id_name_dict = dict(zip(range(len(cfg_cls_name)),cfg_cls_name))
    gt_list = os.listdir(gt_txt_dir)
    pre_list = os.listdir(pre_txt_dir)

    gt_number_arr = gt_total_missing_statistics(gt_txt_dir, gt_list, iou_threshold)  # gt
    total_missing_list = [i for i in gt_list if i not in pre_list]
    total_missing_number_arr = gt_total_missing_statistics(gt_txt_dir, total_missing_list, iou_threshold)  # 全漏失
    no_total_missing_number_arr = missing_over_detect_statistics(gt_txt_dir, pre_txt_dir, iou_threshold)  # 非全漏失
    overdetect_number_arr = missing_over_detect_statistics(pre_txt_dir, gt_txt_dir, iou_threshold)  # guojian

    gt = dict(gt_number_arr)  # gt_dic
    x = Counter(total_missing_number_arr)
    y = Counter(no_total_missing_number_arr)
    missing = dict(x+y)  # missing_dic
    over_detect = dict(overdetect_number_arr)  # over_detect_dic

    missing = dic_align(gt, missing)
    over_detect = dic_align(gt, over_detect)

    gt = sorted(gt.items(), key=lambda item: item[0])  # 转gt_list并排序
    missing = sorted(missing.items(), key=lambda item: item[0])  # 转missing_list并排序
    over_detect = sorted(over_detect.items(), key=lambda item:item[0])  # 转over_detect_list并排序

    cate, gt, missing, over_detect = pd.DataFrame(cfg_cls_name), pd.DataFrame(gt), pd.DataFrame(missing), pd.DataFrame(over_detect)
    dataframe = (pd.concat((cate, gt, missing, over_detect), axis=1))
    # print(dataframe)
    df = dataframe.iloc[:, [0, 2, 4, 6]]
    df.columns = ['cate', 'gt', 'missing', 'over_detect']
    # df = df.set_index('cate')
    # print(df)
    df.loc[len(cate)+1] = df.apply(lambda x: x.sum())
    df.iat[len(df.values)-1, 0] = 'total'
    print(df)
    return df

if __name__ == '__main__':
    gt_txt_dir = '/home/jerry/Desktop/for_missing_and_over/gt'
    pre_txt_dir = '/home/jerry/Desktop/for_missing_and_over/pre'
    cls_yaml_dir = '/home/jerry/Desktop/for_missing_and_over/kesen_33074_hy_512.yaml'
    iou_threshold = 0.3

    txt_to_dataframe(gt_txt_dir, pre_txt_dir, cls_yaml_dir, iou_threshold)
