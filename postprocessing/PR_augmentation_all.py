from preprocessing.zy_utils import IMG_TYPES, json_to_instance, create_empty_json_instance, instance_to_json, points_to_xywh, Box, yaml_to_instance, dic_align
import shutil, os
from prettytable import PrettyTable
from PIL import Image

def precision_recall_visualize(gt_img_json, img_boxes_query, saved_folder_name, predict_label, label_dict, iou_thres=0.1, hard_thres=0.5,guo_thres=0.3, recall=True, precision=True):

    '''
    :param gt_img_json: json文件夹路径
    :param img_boxes_query: 该方法根据json文件名返回box列表
    :return: 可视化漏失、过检结果
    '''
    # 漏失、过检文件夹
    pr_folder_path = os.path.join(gt_img_json, saved_folder_name)
    if not os.path.exists(pr_folder_path): os.makedirs(pr_folder_path)
    img_files = os.listdir(gt_img_json)
    labels_total = {}
    lou_total = {}
    guo_total = {}
    total_objs = 0
    over_detect = 0
    no_detect = 0
    # 遍历img
    for img_file in img_files:
        img_file_path = os.path.join(gt_img_json, img_file)
        # 过滤文件夹和非图片文件
        if not os.path.isfile(img_file_path) or img_file[img_file.rindex('.')+1:] not in IMG_TYPES: continue
        img_out_path =os.path.join(pr_folder_path, img_file)
        json_out_path = img_out_path[:img_out_path.rindex('.')] + '.json'
        # 读取img的json文件载入instance对象
        try:
            json_file_path = img_file_path[:img_file_path.rindex('.')] + '.json'
            instance = json_to_instance(json_file_path)
        except Exception as e:
            instance = create_empty_json_instance(img_file_path)
        # predict_boxes = img_boxes_query(img_file_path, predict_label, cls_id_name_dict)
        predict_boxes = img_boxes_query(img_file_path, predict_label)
        # print(img_file_path)
        if len(predict_boxes) == 0 and len(instance['shapes']) == 0:
            continue
        # 总待检测目标
        total_objs += len(instance['shapes'])
        # --------------------------全漏失情况--------------------------
        if recall and len(predict_boxes) == 0 and len(instance['shapes']) != 0:
            # tt = instance['shapes'].copy()
            tt = instance['shapes']
            for obj in tt:
                if obj['label'] not in label_dict:
                    instance['shapes'].remove(obj)
                    continue

                if obj['label'] not in labels_total:
                    labels_total[obj['label']] = 1
                else:
                    labels_total[obj['label']] = labels_total[obj['label']] + 1
                if obj['label'] not in lou_total:
                    lou_total[obj['label']] = 1
                else:
                    lou_total[obj['label']] = lou_total[obj['label']] + 1

                obj['label'] = 'loushi_' + obj['label']
                obj['score'] = 0

                no_detect += 1
            instance_to_json(instance, json_out_path)
            shutil.copy(img_file_path, img_out_path)
            print('%s has been analyzed!' % (img_file))
            continue
        # --------------------------------------------------------------
        necessary = False
        temp = []
        # 普通漏失统计
        # tt = instance['shapes'].copy()
        tt = instance['shapes']
        for obj in tt:
            if obj['label'] not in label_dict:
                instance['shapes'].remove(obj)
                continue

            if obj['label'] not in labels_total:
                labels_total[obj['label']] = 1
            else:
                labels_total[obj['label']] = labels_total[obj['label']] + 1

            x, y, w, h = points_to_xywh(obj)
            gt_box = Box(x, y, w, h, obj['label'])
            # 漏检 错检
            false_negative, false_label, hard = True, True, True
            for i, predict_box in enumerate(predict_boxes):
                # 如果label_dict为dic
                if gt_box.get_iou(predict_box) > iou_thres and type(label_dict) == type(labels_total) and predict_box.confidence > label_dict[obj['label']]:  # 按照PR_list进行过滤
                    obj['score'] = predict_box.confidence
                    false_negative = False
                    temp.append(i)
                    if gt_box.category == predict_box.category:
                        false_label = False
                        if predict_box.confidence > hard_thres:
                            hard = False
                    else:
                        w_category = predict_box.category

                # 如果label_dict为list
                elif gt_box.get_iou(predict_box) > iou_thres and type(label_dict) == type(temp):
                    obj['score'] = predict_box.confidence
                    false_negative = False
                    temp.append(i)
                    if gt_box.category == predict_box.category:
                        false_label = False
                        if predict_box.confidence > hard_thres:
                            hard = False
                    else:
                        w_category = predict_box.category

            if not recall: continue
            if false_negative:
                if obj['label'] not in lou_total:
                    lou_total[obj['label']] = 1
                else:
                    lou_total[obj['label']] = lou_total[obj['label']] + 1
                obj['label'] = 'loushi_' + obj['label']
                obj['score'] = 0
                # 总漏失
                no_detect += 1
            elif false_label:
                obj['label'] = 'cuowu_%s_' % (w_category) + obj['label']
                obj['score'] = 0
            elif hard:
                obj['label'] = 'hard_' + obj['label']
                obj['score'] = 0

            if false_negative or false_label or hard:
                necessary = True
        # 过检统计
        if precision:
            for i, predict_box in enumerate(predict_boxes):
                if i not in temp:  # 如果该检测框没有使用过
                    # 如果label_dict为dic
                    if type(label_dict) == type(labels_total):
                        if predict_box.category not in label_dict or predict_box.confidence < label_dict[predict_box.category]:  # 按照PR_list进行过滤
                            continue
                    # 如果label_dict为list
                    elif type(label_dict) == type(temp):
                        if predict_box.category not in label_dict:  # 按照PR_list进行过滤
                            continue

                    if predict_box.category not in guo_total:
                        guo_total[predict_box.category] = 1
                    else:
                        guo_total[predict_box.category] = guo_total[predict_box.category] + 1
                    # 总过检
                    if predict_box.confidence < guo_thres:
                        continue
                    over_detect += 1
                    obj = {'label': 'guojian_'+predict_box.category, 'shape_type': 'rectangle', 'points': [[predict_box.x, predict_box.y], [predict_box.x+predict_box.w, predict_box.y+predict_box.h]], 'score': predict_box.confidence}
                    instance['shapes'].append(obj)
                    necessary = True
        
        if necessary:
            instance_to_json(instance, json_out_path)
            shutil.copy(img_file_path, img_out_path)
        print('%s has been analyzed!' % (img_file))
    # print('Total objects: %d, missing %d, over-detect: %d' % (total_objs, no_detect, over_detect))
    # print('Total objects:',labels_total)
    # print('lou_total objects:', lou_total)
    # print('guo_total objects:', guo_total)

    lou_total = dic_align(labels_total, lou_total)
    guo_total = dic_align(labels_total, guo_total)
    # print(labels_total,lou_total,guo_total)

    PR_gt, PR_missing, PR_over_detect = 0, 0, 0
    table = PrettyTable(['category', 'gt', 'missing', 'over_detect'])
    for label in label_dict:
        table.add_row([label, labels_total[label], lou_total[label], guo_total[label]])
        PR_gt += labels_total[label]
        PR_missing += lou_total[label]
        PR_over_detect += guo_total[label]
    print(table.get_string(sortby='missing', reversesort=True))

    print('Total objects: %d, missing %d, over-detect: %d' % (PR_gt, PR_missing, PR_over_detect))

# 自定义自己的img-boxes对应方法，Box类参考utils.py
# yolo_strategy
def yolo_strategy(img_file_path, predict_label):
    label_dict_all = ['guashang']  # 全部缺陷list，按照数据集生成顺序  （personal habit: ordered by alphabetical）
    cls_id_name_dict=dict(zip(range(len(label_dict_all)), label_dict_all))

    txt_folder_path = predict_label
    txt_file = img_file_path[img_file_path.rindex(os.sep)+1:img_file_path.rindex('.')] + '.txt'
    txt_file_path = os.path.join(txt_folder_path, txt_file)
    img = Image.open(img_file_path)
    width = img.width
    height = img.height
    boxes = []
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return boxes
    # 遍历txt文件中的每一个检测目标
    for line in lines:
        words = line.split(' ')
        cls_id = int(words[0])
        cls_name = cls_id_name_dict[cls_id]
        cx, cy, w, h = float(words[1]) * width, float(words[2]) * height, float(words[3]) * width, float(words[4]) * height
        confidence = float(words[5])
        # 一个Box代表一个检测目标的xywh、label、confidence
        boxes.append(Box(cx-w/2, cy-h/2, w, h, cls_name, confidence))
    return boxes

# json_strategy
def pre_json_query(img_file_path, predict_label):
    json_file = img_file_path[img_file_path.rindex(os.sep)+1:img_file_path.rindex('.')] + '.json'
    json_file_path = os.path.join(predict_label, json_file)

    boxes = []
    try:
        instance = json_to_instance(json_file_path)
    except FileNotFoundError:
        return boxes
    # 遍历json中每一个检测框
    shapes = instance['shapes']
    for shape in shapes:
        points = shape['points']
        x1,y1,x2,y2 = points[0][0], points[0][1], points[1][0], points[1][1]
        xmin, ymin, xmax, ymax = min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
        x, y ,w ,h  = float(xmin), float(ymin), float(xmax-xmin), float(ymax-ymin)
        cls_name = shape['label']
        confidence = shape['score']
        boxes.append(Box(x,y,w,h,cls_name,confidence))
    return boxes 

if __name__ == '__main__':
    label_dict = ['guashang']  # 需要PR de list
    # label_dict = {'huashang': 0.5, 'yahen': 0.5}  # 需要PR de dic
    precision_recall_visualize(# input_img&json
                               gt_img_json='/home/jerry/Desktop/garbage/yolo_series/gs_data/gs',
                               # inference_result
                               predict_label='/home/jerry/Desktop/garbage/yolo_series/gs_data/labels',
                               # 自定义的query方法
                               img_boxes_query=yolo_strategy,
                               # save_path
                               saved_folder_name='PR',
                               label_dict=label_dict,
                               # 计算漏失
                               recall=True,
                               # 计算过检
                               precision=True)