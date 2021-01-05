# IOU阈值
IOU_THR = 0.05

#计算混淆情况的score阈值
SCORE_THR = 0.01


#模型输出文件
TXT_PATH = "/home/zy/project/16class/mmdetection-master/jala-487ea3ec.bbox.json"

#标注文件
PATH_TO_COCO = '/home/zy/project/16class/mmdetection-master/data/coco/annotations/instances_val2017.json'

#是否输出漏失图片
OUT = True
INTERESTS_OUT = '/home/zy/project/16class/mmdetection-master/data/out007'
PATH_TO_TEST_IMAGES_DIR = '/home/zy/project/16class/mmdetection-master/data/coco/val2017/'


#类别list
#CLASS_NAMES = ['3Daohen', 'aokeng', 'baisezaodian', 'cashang', 'daowen','daowenxian', 'guashang', 'heidian', 'pengshang', 'shahenyin','shuiyin', 'tabian', 'yise', 'yiwu']
CLASS_NAMES = ['maoxu', 'guashang', 'keli', 'heidian', 'daowen', 'yiwu', 'yise', 'pengshang', 'diaoqi', 'aotuhen1', 'xianhen', 'yinglihen', 'aotuhen2', 'yashang']


#是否需要做类别映射，当模型和总的测试集类别标签不一致的时候使用
isMapper=False
class_mapper={0:2,1:6}


IMG_FORMAT = '/*.jpg'


import os
import shutil
from glob import glob
import json

import cv2
import numpy as np
from tqdm import tqdm
from pycocotools.coco import COCO


if not os.path.exists(INTERESTS_OUT):
    os.makedirs(INTERESTS_OUT) 
    
    
images=[]
conf_count_lingjian = {str(i / 100): set() for i in list(range(0, 100, 1))}
conf_count_kuang = {str(i / 100): {x: 0 for x in CLASS_NAMES} for i in list(range(0, 100, 1))}
conf_count_zhaohui = {str(i / 100): {x: 0 for x in CLASS_NAMES} for i in list(range(0, 100, 1))}
conf_count_guosha = {str(i / 100): {x: 0 for x in CLASS_NAMES} for i in list(range(0, 100, 1))}
conf_count_tu = {str(i / 100): 0 for i in list(range(0, 100, 1))}
quexian_count = 0
confusion_matrix = np.zeros((len(CLASS_NAMES) + 1, len(CLASS_NAMES) + 1))
coco = COCO(PATH_TO_COCO)
class_mapper={'0':'maoxu', '1':'guashang', '2':'keli', '3':'heidian', '4':'daowen', '5':'yiwu', '6':'yise', '7':'pengshang', '8':'diaoqi', '9':'aotuhen1', '10':'xianhen', '11':'yinglihen', '12':'aotuhen2', '13':'yashang'}
print(coco)




def visualize(img_np, out_pic_path, thresh, annotations,bboxes,labels):
    """visualize gt and det"""
   
    for i in range(len(bboxes)):
        if bboxes[i][4]<SCORE_THR:
            continue
        left_top = (int(bboxes[i][0]), int(bboxes[i][1]))
        right_bottom = (int(bboxes[i][2]), int(bboxes[i][3]))
        #if isMapper:
            #label=class_mapper[labels[i]]
        label=labels[i]
        label_text = CLASS_NAMES[label] if CLASS_NAMES is not None else 'cls {}'.format(label)
        cv2.rectangle(img_np, left_top, right_bottom, (0, 255, 0), 2)
        # put text
        label_text = 'DET {} | {:.02f}'.format(label_text,bboxes[i][4])
        cv2.putText(img_np, label_text, (int(bboxes[i][0]), int(bboxes[i][1] - 2)),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))
        
    for ann in annotations:
        bndbox = ann['bbox']
        xmin = int(bndbox[0])
        ymin = int(bndbox[1])
        xmax = int(bndbox[0]) + int(bndbox[2])
        ymax = int(bndbox[1]) + int(bndbox[3])
        name = CLASS_NAMES[ann['category_id']]
        cv2.putText(img_np, 'GT ' + name, (xmin, ymin - 10),
                    cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255))
        cv2.rectangle(img_np, (xmin, ymin), (xmax, ymax), (255, 255, 255), 2)
   
    cv2.imwrite(out_pic_path, img_np)



def draw_gt_bbox(img_np, annotations, bbox, label):
    """draw gt and bbox"""
    bbox_int = bbox.astype(np.int32)
    left_top = (bbox_int[0], bbox_int[1])
    right_bottom = (bbox_int[2], bbox_int[3])
    cv2.rectangle(img_np, left_top, right_bottom, (0, 255, 0), 2)
    #if isMapper:
        #label=class_mapper[label]
    label_text = CLASS_NAMES[label] if CLASS_NAMES is not None else 'cls {}'.format(label)

    if len(bbox) > 4:
        label_text += '|{:.02f}'.format(bbox[-1])
    cv2.putText(img_np, label_text, (bbox_int[0], bbox_int[1] - 2),
                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))

    for ann in annotations:
        bndbox = ann['bbox']
        xmin = int(bndbox[0])
        ymin = int(bndbox[1])
        xmax = int(bndbox[0]) + int(bndbox[2])
        ymax = int(bndbox[1]) + int(bndbox[3])
        name = CLASS_NAMES[ann['category_id']]
        cv2.putText(img_np, 'GT ' + name, (xmin, ymin - 10),
                    cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255))
        cv2.rectangle(img_np, (xmin, ymin), (xmax, ymax), (255, 255, 255), 2)

    return img_np


def compare(image, bboxes, labels, gt_map, anns_lookup,interests_out=INTERESTS_OUT):
    """

    :param xml_path: xml路径, string
    :param bboxes:  模型检测bbox, np.array([[]])
    :param labels: 模型检测label, np.array([])
    :param gt_map: ground truth, dict()
    :param det_map: model detection, dict()
    :param zhaohui_map: 召回, dict()
    :param guosha_map: 过杀, dict()
    :return:
    """
    global conf_count_zhaohui, conf_count_guosha, conf_count_kuang
    
    img_np = cv2.imread(image)
    annotations = anns_lookup[os.path.basename(image)]
    is_out=False
   
    for i, ann in enumerate(annotations):

        gt_id = ann['category_id']


        name = CLASS_NAMES[gt_id]

        gt_map[name] += 1
        bndbox = ann['bbox']
        xmin = int(bndbox[0])
        ymin = int(bndbox[1])
        xmax = int(bndbox[0]) + int(bndbox[2])
        ymax = int(bndbox[1]) + int(bndbox[3])
        #segm = ann['segmentation'][0]

        matched_labels = {}
        for i in range(len(labels)):
            if compute_iou((xmin, ymin, xmax, ymax), bboxes[i]) > IOU_THR:
                matched_labels[i] = labels[i]
        if len(matched_labels.keys()) > 0:
            for key in conf_count_zhaohui.keys():
                if bboxes[i][4] > float(key):
#                     print('key:{},name:{}'.format(key,name))
                    conf_count_zhaohui[key][name] += 1
                
            if gt_id in matched_labels.values():
                confusion_matrix[gt_id, gt_id] += 1
            else:
                chosen_matched_label = list(matched_labels.keys())[0]
                #print(gt_id, chosen_matched_label)
                confusion_matrix[gt_id, labels[chosen_matched_label]] += 1
                img_np = draw_gt_bbox(img_np,
                                      annotations,
                                      bboxes[chosen_matched_label],
                                      labels[chosen_matched_label])
        else:
            confusion_matrix[gt_id, -1] += 1
            is_out=True
            recall_name=CLASS_NAMES[gt_id]
            lost_ann.append(ann)
            
            
    for i in range(len(bboxes)):
        for key in conf_count_kuang.keys():
            if bboxes[i][4] > float(key):
                class_name = CLASS_NAMES[labels[i]]
                conf_count_kuang[key][class_name] += 1

        for j in range(len(annotations)):
            ann = annotations[j]
            name = CLASS_NAMES[ann['category_id']]
            bndbox = ann['bbox']
            xmin = int(bndbox[0])
            ymin = int(bndbox[1])
            xmax = int(bndbox[0]) + int(bndbox[2])
            ymax = int(bndbox[1]) + int(bndbox[3])

            if compute_iou((xmin, ymin, xmax, ymax), bboxes[i]) > IOU_THR:
                break

            if j == len(annotations) - 1:
                bbox = bboxes[i, :]
                #                 print("DET IS GUOSHA +1")
                confusion_matrix[-1, labels[i]] += 1
                img_np = draw_gt_bbox(img_np, annotations, bboxes[i], labels[i])
                for key in conf_count_guosha.keys():
                    if bboxes[i][4] > float(key):
                        conf_count_guosha[key][CLASS_NAMES[labels[i]]] += 1
    if is_out:
        path1 = pathlib.Path(interests_out)
        if not path1.exists():
            path1.mkdir(exist_ok=True) 
        path = pathlib.Path(interests_out+"/"+recall_name)
        if not path.exists():
            path.mkdir(exist_ok=True)
        visualize(img_np,str(path)+"/"+os.path.basename(image),SCORE_THR,annotations,bboxes,labels)
        #cv2.imwrite(out_pic_path,SCORE_THR, img_np)

def NMSBbox(bboxes, labels):
    """
    NMS
    """
    vis = np.zeros(len(bboxes))
    rmpos = []
    for p in range(len(bboxes)):
        if vis[p]:
            continue
        vis[p] = 1

        for q in range(len(bboxes) - p - 1):
            if vis[q + p + 1]:
                continue
            bbox1 = bboxes[p]
            bbox2 = bboxes[q + p + 1]
            if compute_iou(bbox1, bbox2) > 0.2:
                if bboxes[p + q + 1][4] > bboxes[p][4]:
                    rmpos.append(p)
                    break
                else:
                    rmpos.append(q + p + 1)
                    vis[q + p + 1] = 1
    rmpos.sort(reverse=True)
    for p in rmpos:
        bboxes.pop(p)
        labels.pop(p)
    return bboxes, labels


def compute_iou(bbox1, bbox2):
    """
    compute iou
    """
    bbox1xmin = bbox1[0]
    bbox1ymin = bbox1[1]
    bbox1xmax = bbox1[2]
    bbox1ymax = bbox1[3]
    bbox2xmin = bbox2[0]
    bbox2ymin = bbox2[1]
    bbox2xmax = bbox2[2]
    bbox2ymax = bbox2[3]

    area1 = (bbox1ymax - bbox1ymin) * (bbox1xmax - bbox1xmin)
    area2 = (bbox2ymax - bbox2ymin) * (bbox2xmax - bbox2xmin)

    bboxxmin = max(bbox1xmin, bbox2xmin)
    bboxxmax = min(bbox1xmax, bbox2xmax)
    bboxymin = max(bbox1ymin, bbox2ymin)
    bboxymax = min(bbox1ymax, bbox2ymax)
    if bboxxmin >= bboxxmax:
        return 0
    if bboxymin >= bboxymax:
        return 0

    area = (bboxymax - bboxymin) * (bboxxmax - bboxxmin)
    iou = area / (area1 + area2 - area)
    return iou


def load_annotations():
    """load annotations to dictionary"""
    with open(PATH_TO_COCO, 'r') as f:
        data = json.load(f)
    annotations = data['annotations']
    images = data['images']

    ann_lookup = {}
    for annotation in annotations:
        image_id = annotation['image_id']
        image_name=""
        for img_info in images:
            if img_info['id']==image_id:
                image_name=img_info['file_name']
        if image_name=="":
            print("No imagename in coco!")
            break
        if image_name not in ann_lookup.keys():
            ann_lookup[image_name] = [annotation]
        else:
            ann_lookup[image_name].append(annotation)
    print('ann_lookup', [len(ann_lookup[key]) for key in ann_lookup.keys()])

    return images,ann_lookup

def find_image_id(img_name,img_lookup):
    for img_info in img_lookup:
        if img_info['file_name']==img_name:
            return img_info['id']
    print("Not found image name in coco",img_name)
    return 0

def load_results(results_path):
    """load_results_txt"""

    with open(results_path, 'r') as f:
        data = json.load(f)
    ann_lookup = {}
    for annotation in data:
        image_id = annotation['image_id']
        if str(image_id) not in ann_lookup.keys():
            ann_lookup[str(image_id)] = [annotation]
        else:
            ann_lookup[str(image_id)].append(annotation)
    print('result_lookup', [len(ann_lookup[key]) for key in ann_lookup.keys()])
    return ann_lookup


def load_result_from_imageid(img_id,results):
    bboxes, labels = [], []
    if str(img_id) not in results.keys():
        return [],[]
    for ann in results[str(img_id)]:
        xmin=ann['bbox'][0]
        ymin=ann['bbox'][1]
        w=ann['bbox'][2]
        h=ann['bbox'][3]
        bboxes.append([xmin,ymin,xmin+w,ymin+h,ann['score']])
        labels.append(ann['category_id'])
    return bboxes,labels




imgs = glob(PATH_TO_TEST_IMAGES_DIR + IMG_FORMAT)
img_count = 0
gt_map = {}

for class_name in CLASS_NAMES:
    gt_map[class_name] = 0
lost_ann=[]
images_lookup,anns_lookup = load_annotations()
results=load_results(TXT_PATH)


print(results)
print(anns_lookup)
print(len(results))



import pathlib

for image in tqdm(imgs):
        #print(image)
    img_count += 1
    img_id=find_image_id(os.path.basename(image),images_lookup)
    total_boxes, total_labels = load_result_from_imageid(img_id,results)

        # NMS
    total_boxes, total_labels = NMSBbox(total_boxes, total_labels)

    total_boxes = np.array(total_boxes)
    total_labels = np.array(total_labels)
    if isMapper:
        for i in range(len(total_labels)):
            total_labels[i]=class_mapper[total_labels[i]]
        #         print(total_boxes, total_labels)
    img_name = os.path.basename(image)

    if img_name in anns_lookup.keys():
        compare(image, total_boxes, total_labels, gt_map, anns_lookup)
    else:
        #print('ann dont exists')
        continue
            # for i in range(len(total_labels)):
            #     print("--DET IS GUOSHA +1")
            #     for key in conf_count_kuang.keys():
            #         if total_boxes[i][4] > float(key):
            #             conf_count_kuang[key][CLASS_NAMES[total_labels[i]]] += 1
            #             conf_count_guosha[key][CLASS_NAMES[total_labels[i]]] += 1

for key in conf_count_lingjian.keys():
    conf_count_lingjian[key] = len(conf_count_lingjian[key])

print("gt count: {}\n".format(sum(gt_map.values())))

for thr in conf_count_zhaohui.keys():
    total_num = sum(list(conf_count_zhaohui[thr].values()))
    conf_count_zhaohui[thr] = total_num

for thr in conf_count_guosha.keys():
    total_num = sum(list(conf_count_guosha[thr].values()))
    conf_count_guosha[thr] = total_num
print("召回情况: {}\n".format(conf_count_zhaohui))
print("过杀情况: {}\n".format(conf_count_guosha))

    #     confusion_matrix_cor = correct_tn(confusion_matrix)
np.save('confusion.npy', confusion_matrix)



import pandas as pd
an=pd.DataFrame(lost_ann)
print(CLASS_NAMES)
print(an.groupby('category_id').count())


import numpy as np
import matplotlib.pyplot as plt


def plot_confmat(confusion_mat, classes, set_name='', out_dir='./'):
    """plot confusion matrix"""
    # 归一化
    confusion_mat_N = confusion_mat.copy()
    for i in range(len(classes)):
        confusion_mat_N[i, :] = confusion_mat[i, :] / confusion_mat[i, :].sum()

    # 获取颜色
    cmap = plt.cm.get_cmap('Greys')  # 更多颜色: http://matplotlib.org/examples/color/colormaps_reference.html
    plt.imshow(confusion_mat_N, cmap=cmap)
    plt.colorbar()

    # 设置文字
    xlocations = np.array(range(len(classes)))
    plt.xticks(xlocations, list(classes), rotation=60)
    plt.yticks(xlocations, list(classes))
    plt.xlabel('Predict label')
    plt.ylabel('True label')
    plt.title('Confusion_Matrix_' + set_name)

    # 打印数字
    for i in range(confusion_mat_N.shape[0]):
        for j in range(confusion_mat_N.shape[1]):
            plt.text(x=j, y=i, s=int(confusion_mat[i, j]), va='center', ha='center', color='red', fontsize=10)
    # 保存
    plt.savefig(os.path.join(out_dir, 'Confusion_Matrix_' + + '.png'))
    plt.close()


def correct_tn(confusion_mat):
    """correct true negative"""
    for i in range(confusion_mat.shape[0] - 1):
        confusion_mat[i, -1] = gt_map[CLASS_NAMES[i]] - sum(confusion_mat[i, :-1])

    return confusion_mat


def show_confusion(npy_path):
    """show confusion"""
    confusion_mat = np.load(npy_path)
    confusion_mat = correct_tn(confusion_mat)
    print(confusion_mat)
    plot_confmat(confusion_mat, labels)


confusion_mat = correct_tn(confusion_matrix)
#print(confusion_mat)
confusion_mat_N = confusion_mat.copy()
for i in range(len(CLASS_NAMES)):
    confusion_mat_N[i, :] = confusion_mat[i, :] / confusion_mat[i, :].sum()

# 获取颜色
cmap = plt.cm.get_cmap('Greys')  # 更多颜色: http://matplotlib.org/examples/color/colormaps_reference.html
plt.figure(figsize=(10, 10))
plt.imshow(confusion_mat_N, cmap=cmap)
plt.colorbar()

# 设置文字
xlocations = np.array(range(len(CLASS_NAMES)))
plt.xticks(xlocations, list(CLASS_NAMES), rotation=60)
plt.yticks(xlocations, list(CLASS_NAMES))
plt.xlabel('Predict label')
plt.ylabel('True label')
plt.title('jala-487ea3ec_iou{}_score{}'.format(IOU_THR,SCORE_THR))
title = TXT_PATH[TXT_PATH.rindex(os.sep)+1:].split('.')[0]
plt.title('{}_iou{}_score{}'.format(title, IOU_THR, SCORE_THR))

# 打印数字
for i in range(confusion_mat_N.shape[0]):
    for j in range(confusion_mat_N.shape[1]):
        plt.text(x=j, y=i, s=int(confusion_mat[i, j]), va='center', ha='center', color='red', fontsize=10)
plt.show()
