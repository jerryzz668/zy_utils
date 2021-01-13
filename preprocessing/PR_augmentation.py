from preprocessing.utils import *
import shutil


def precision_recall_visualize(target_folder_path, img_boxes_query, saved_folder_name, iou_thres=0.3, hard_thres=0.5, recall=True, precision=True):
    '''
    :param target_folder_path: json文件夹路径
    :param img_boxes_query: 该方法根据json文件名返回box列表
    :return: 可视化漏失、过检结果
    '''
    # 漏失、过检文件夹
    pr_folder_path = os.path.join(target_folder_path, saved_folder_name)
    if not os.path.exists(pr_folder_path): os.makedirs(pr_folder_path)
    img_files = os.listdir(target_folder_path)
    total_objs = 0
    over_detect = 0
    no_detect = 0
    # 遍历img
    for img_file in img_files:
        img_file_path = os.path.join(target_folder_path, img_file)
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
        predict_boxes = img_boxes_query(img_file_path)
        # 总待检测目标
        total_objs += len(instance['shapes'])
        # 全漏失情况
        if recall and len(predict_boxes) == 0 and len(instance['shapes']) != 0:
            for obj in instance['shapes']:
                obj['label'] = 'loushi_' + obj['label']
            instance_to_json(instance, json_out_path)
            shutil.copy(img_file_path, img_out_path)
            print('%s has been analyzed.' % (img_file_path))
            continue
        necessary = False
        temp = []
        # 漏失统计
        for obj in instance['shapes']:
            x, y, w, h = points_to_xywh(obj)
            gt_box = Box(x, y, w, h, obj['label'])
            # 漏检 错检
            false_negative, false_label, hard = True, True, True
            for i, predict_box in enumerate(predict_boxes):
                if gt_box.get_iou(predict_box) > iou_thres:
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
                obj['label'] = 'loushi_' + obj['label']
                # 总漏失
                no_detect += 1
            elif false_label:
                obj['label'] = 'cuowu_%s_' % (w_category) + obj['label']
            elif hard:
                obj['label'] = 'hard_' + obj['label']
            if false_negative or false_label or hard:
                necessary = True
        # 过检统计
        if precision:
            for i, predict_box in enumerate(predict_boxes):
                if i not in temp:
                    # 总过检
                    over_detect += 1
                    obj = {'label': 'guojian_'+predict_box.category, 'shape_type': 'rectangle', 'points': [[predict_box.x, predict_box.y], [predict_box.x+predict_box.w, predict_box.y+predict_box.h]]}
                    instance['shapes'].append(obj)
                    necessary = True
        if necessary:
            instance_to_json(instance, json_out_path)
            shutil.copy(img_file_path, img_out_path)
        print('%s has been analyzed.' % (img_file_path))
    print('Total objects: %d, missing %d, over-detect: %d' % (total_objs, no_detect, over_detect))

if __name__ == '__main__':
    from PIL import Image
    # 自定义自己的img-boxes对应方法，Box类参考utils.py
    # def img_boxes_query_mmdet(img_file_path):
    #     bbox_json_path = '/Users/zhangyan/Desktop/internship/cm_gj/cm1/半残废coco数据集/zy_20_val.bbox.json'
    #     val_json_path = '/Users/zhangyan/Desktop/internship/cm_gj/cm1/半残废coco数据集/coco/annotations/instances_train2017.json'
    #     # img_file_path = '/Users/zhangyan/Desktop/val2017/1447-0007-11_-6_870.jpg'
    #
    #     img_file_name = img_file_path[img_file_path.rindex(os.sep) + 1:]
    #     cls_id_name_dict = {0: 'a', 1: 'aotuhen', 2: 'aotuhen1', 3: 'aotuhen2', 4: 'baidian', 5: 'bianxing',
    #                         6: 'daowen',
    #                         7: 'diaoqi', 8: 'guashang', 9: 'guoqie', 10: 'heidian', 11: 'jiaxi', 12: 'keli',
    #                         13: 'maoxu',
    #                         14: 'pengshang', 15: 'tabian', 16: 'xianhen', 17: 'yashang', 18: 'yinglihen', 19: 'yise',
    #                         20: 'yiwu'}
    #
    #     # 从val_json中找到图像名字对应的id
    #     val_json_data = json_to_instance(val_json_path)
    #     images = val_json_data.get('images')
    #     for obj in images:
    #         if obj['file_name'] == img_file_name:
    #             img_id = obj['id']
    #
    #     # 从bbox.json中获取defects的6个值
    #     boxes = []
    #     try:
    #         bbox_json_data = json_to_instance(bbox_json_path)
    #     except FileNotFoundError:
    #         return boxes
    #     for i in bbox_json_data:
    #         if i['image_id'] == img_id:
    #             cls_id = int(i['category_id'])
    #             x, y, w, h = float(i['bbox'][0]), float(i['bbox'][1]), float(i['bbox'][2]), float(i['bbox'][3])
    #             confidence, cls_name = float(i['score']), cls_id_name_dict[cls_id]
    #             boxes.append(Box(x, y, w, h, cls_name, confidence))
    #     return boxes

    # yolo_strategy
    def img_boxes_query(img_file_path):
        # cls_id_name_dict = {0: 'baomo', 1: 'cashang', 2: 'huashang', 3: 'pengshang', 4: 'yashang', 5: 'yise'}
        cls_id_name_dict = {0: 'aokeng', 1:'aotuhen', 2:'baisezaodian',3: 'daowen', 4:'guashang', 5:'heidian',6: 'pengshang', 7:'yise'}
        txt_folder_path = '/Users/zhangyan/Desktop/labels'
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
    precision_recall_visualize(target_folder_path='/Users/zhangyan/Desktop/a件_0830damian/0830damian_yolo/images/train',
                               # 自定义的query方法
                               img_boxes_query=img_boxes_query,
                               # 保存在图片文件夹下的特定目录名
                               saved_folder_name='PR',
                               # 计算漏失
                               recall=True,
                               # 计算过检
                               precision=True)




























