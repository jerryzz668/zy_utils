import json
import numpy as np
import pandas as pd
import os
import cv2

# 训练集对应类别标注
train_lable = {
    "badge": 1,
    "offground": 2,
    "ground": 3,
    "safebelt": 4
}
label_modify = {0: 3, 1: 2, 2: 4, 3: 1}
show_label = {1: 'guarder', 2: 'safebeltperson', 3: 'offgroundperson'}

# 图片存放的路径
picture_path = '/home/jerry/Desktop/tianchi/Track3_helmet/3_test_imagesa'  # 不动
# 模型输出txt结果 yolov5
path = '/home/jerry/Documents/yolov5-5.0/runs/detect/exp3/labels'
# path = r'E:\weiyi\tianchi\results\test'
# 测试集图片名字、顺序
test_json = '/home/jerry/Desktop/tianchi/Track3_helmet/3_testa_user.csv'  # 不动
# 提交结果保存路径
results_path = '/home/jerry/Desktop/tianchi/Track3_helmet/results/results_aug_iou0.48_badge'

df = pd.read_csv(test_json, header=0)
df = df["image_url"]
results = []  # 提交结果


# 求勋章的iou
def badge_iou(preson_frame, thing_frame, p=0.95):
    x_min = max(preson_frame[0], thing_frame[0])
    y_min = max(preson_frame[1], thing_frame[1])
    x_max = min(preson_frame[2], thing_frame[2])
    y_max = min(preson_frame[3], thing_frame[3])
    # print(x_max-x_min,y_max-y_min)
    # 负值直接为0
    if (x_max - x_min) <= 0 or (y_max - y_min) <= 0:
        return False

    intersection = (x_max - x_min) * (y_max - y_min)
    thing = (thing_frame[2] - thing_frame[0]) * (thing_frame[3] - thing_frame[1])
    iou = intersection / thing
    # print(iou)
    if iou >= p:
        return True
    else:
        return False


# 求安全带的iou
def safebelt_iou(preson_frame, thing_frame, p=0.3):
    x_min = max(preson_frame[0], thing_frame[0])
    y_min = max(preson_frame[1], thing_frame[1])
    x_max = min(preson_frame[2], thing_frame[2])
    y_max = min(preson_frame[3], thing_frame[3])
    # print(x_max-x_min,y_max-y_min)
    # 负值直接为0
    if (x_max - x_min) <= 0 or (y_max - y_min) <= 0:
        return False

    intersection = (x_max - x_min) * (y_max - y_min)
    thing = (thing_frame[2] - thing_frame[0]) * (thing_frame[3] - thing_frame[1])
    iou = intersection / thing
    # print(iou)
    if iou >= p:
        return True
    else:
        return False


def add_results(img_id, cate_id, off_gro):
    global results
    result = {"image_id": img_id,
              "category_id": cate_id,
              "bbox": [off_gro[0], off_gro[1], off_gro[2], off_gro[3]],
              "score": float(off_gro[4])}
    results.append(result)
    return result


def generate_json(filename, img_w, img_h, temp_result, save_path):
    temp_shape = []
    for result in temp_result:
        print(result)
        shape = {'label': show_label[result['category_id']] + '-' + str('%.2f' % (result['score'])),
                 'shape_type': 'rectangle'}
        bbox = result['bbox']
        shape['points'] = [[bbox[0], bbox[1]], [bbox[2], bbox[3]]]
        temp_shape.append(shape)
    print(temp_shape)
    new_json = {'version': "1.0",
                'shapes': temp_shape,
                'imageData': None,
                'imageHeight': img_h,
                'imageWidth': img_w,
                'imageDepth': 3,
                'imagePath': filename}
    json.dump(new_json, open(save_path, 'w', encoding='utf-8'), indent=4)


for id_s, one_img_name in enumerate(df):
    temp_result = []
    basename = os.path.basename(one_img_name)
    one_txt_path = os.path.join(path, basename.split('.')[0] + '.txt')
    pic_pth = os.path.join(picture_path, basename)
    save_json = os.path.join(results_path, basename.split('.')[0] + '.json')

    try:  # 防止空文件,空文件情况直接跳过
        one_txt = pd.read_csv(one_txt_path, header=None)
        # print(one_txt_path)
        img = cv2.imread(pic_pth)
        img_h, img_w, c = img.shape
        print(img_w, ' ', img_h)
    except:
        # print('none: ', id_s, ':', one_txt_path)
        continue
    one_txt = one_txt[0]
    # 将2、3两类取出来，即先判断是否是人（天上的加上地上的）
    offground, ground = [], []  # 人
    badge, safebelt = [], []  # 物体
    for one_res in one_txt:
        one_res = one_res.split(" ")
        one_res[0] = label_modify[int(one_res[0])]
        frame = np.array([one_res[1], one_res[2], one_res[3], one_res[4], one_res[5]]).astype(np.float32)  # x,y,w,h
        frame[2] *= img_w  # w
        frame[3] *= img_h  # h
        frame[0] *= img_w  # x
        frame[0] -= frame[2] / 2
        frame[1] *= img_h  # y
        frame[1] -= frame[3] / 2
        bbox = np.array(
            [int(frame[0]), int(frame[1]), int(frame[0]) + int(frame[2]), int(frame[1]) + int(frame[3]), frame[4]])
        # 框的格式化为点的格式x_min,y_min,x_max,y_max
        if int(one_res[0]) == 2:
            offground.append(bbox)  # xmin,ymin,xmax,ymax
        elif int(one_res[0]) == 3:
            ground.append(bbox)
        elif int(one_res[0]) == 1:
            badge.append(bbox)
        elif int(one_res[0]) == 4:
            safebelt.append(bbox)
        else:
            break

    # 判断是否为天上的人
    if len(offground) != 0:
        for off in offground:
            offgroundperson = True  # 表示为离地的人,也就是第三类,不是作业人员也不是监督人员
            # 判断是否有勋章
            if len(badge) != 0:
                for bad in badge:
                    my_iou = badge_iou(off[0:4], bad[0:4])
                    # print(my_iou)
                    # offgroundperson = 1 - my_iou
                    if my_iou:
                        result = add_results(id_s, 1, off)
                        temp_result.append(result)

            # 判断是否有穿安全带
            if len(safebelt) != 0:
                for safe in safebelt:
                    my_iou = safebelt_iou(off[0:4], safe[0:4])
                    # print(my_iou)
                    # offgroundperson = 1 - my_iou
                    if my_iou:
                        result = add_results(id_s, 2, off)
                        temp_result.append(result)

            if offgroundperson:
                result = add_results(id_s, 3, off)
                temp_result.append(result)

    # 判断是否为地上的人
    # 路人是不提交结果的
    if len(ground) != 0:
        for gro in ground:
            # 判断是否有勋章
            if len(badge) != 0:
                for bad in badge:
                    my_iou = badge_iou(gro[0:4], bad[0:4])
                    # print(my_iou)
                    if my_iou:
                        result = add_results(id_s, 1, gro)
                        temp_result.append(result)
            # 判断是否有穿安全带
            if len(safebelt) != 0:
                for safe in safebelt:
                    my_iou = safebelt_iou(gro[0:4], safe[0:4])
                    # print(my_iou)
                    if my_iou:
                        result = add_results(id_s, 2, gro)
                        temp_result.append(result)

    # 保存json
    generate_json(basename, img_w, img_h, temp_result, save_json)
    # print('----------------')

print(len(results))
result_json = os.path.join(results_path, 'results.json')
json.dump(results, open(result_json, 'w'), indent=4)
