import os
import json
import shutil

class Box:
    # xy是左上角坐标
    def __init__(self, category, x, y, w, h):
        self.category = category
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_area(self):
        return self.w * self.h

    def get_iou(self, box):
        total_area = self.get_area() + box.get_area()
        inter_area = calculate_inter_area(self, box)
        iou = inter_area*1.0/(total_area-inter_area)
        return iou

    def matches(self, box, threshold=0.5):
        result = False
        if self.category == box.category and self.get_iou(box)>=threshold: result = True
        return result

    def matches_miss(self, box, threshold=0.5):
        result = False
        if self.get_iou(box)>=threshold: result = True
        return result

def calculate_inter_area(b1: Box, b2: Box):
    left_x, left_y = max([b1.x, b2.x]), max([b1.y, b2.y])
    right_x, right_y = min([b1.x+b1.w, b2.x+b2.w]), min([b1.y+b1.h, b2.y+b2.h])
    height = right_y - left_y
    width = right_x - left_x
    area = height * width if height>0 and width>0 else 0
    return area

# precision and recall analysis
# [{'filename':xxx, 'boxes':[box1, box2, ...]}...{}]
def pr_analysis(gt_boxes: list, infer_boxes: list):
    correct_list = []
    recall_list = []
    precision_list = []
    for gt_box in gt_boxes:
        # [box1, box2, ...]
        judge_right = []
        for gt in gt_box['boxes']:
            # 如果infer_boxes里面有匹配该gt_box的box,放入correct_list
            # 如果infer_boxes里面无匹配该gt_box的box,则放入recall_list
            # 最后infer_boxes里剩下的是过杀
            for infer_box in infer_boxes:
                if infer_box['filename'] == gt_box['filename']:
                    infer_right = infer_box
                    for infer in infer_box['boxes']:
                        if gt.matches(infer):
                            judge_right.append(int(1))
        if len(judge_right) == len(gt_box['boxes']):
            correct_list.append(infer_right)

    for gt_box in gt_boxes:
        judge_miss = []
        for gt in gt_box['boxes']:
            for infer_box in infer_boxes:
                if infer_box['filename'] == gt_box['filename']:
                    infer_miss = infer_box
                    for infer in infer_box['boxes']:
                        if gt.matches_miss(infer):
                            judge_miss.append(int(1))
        if len(judge_miss) < len(gt_box['boxes']):
            recall_list.append(infer_miss)

    for gt_box in gt_boxes:
        judge_over = []
        for gt in gt_box['boxes']:
            for infer_box in infer_boxes:
                if infer_box['filename'] == gt_box['filename']:
                    infer_over = infer_box
                    for infer in infer_box['boxes']:
                        if gt.matches_miss(infer):
                            judge_over.append(int(1))
        if len(judge_over) < len(infer_box['boxes']):
            precision_list.append(infer_over)
    return correct_list, recall_list, precision_list


# 返回两个list,输入的是两个绝对路径
# [{'filename':xxx, 'boxes':[box1, box2, ...]}...{}]
def txts_to_boxes(gt_txt_folder_path: str, infer_txt_folder_path: str, img_size):
    infer_txts = os.listdir(infer_txt_folder_path)
    gt_txts =os.listdir(gt_txt_folder_path)
    infer_boxes, gt_boxes = [], []
    for infer_txt in infer_txts:
        # 一个infer_txt对应一张img，每张原图有N个缺陷，就有N个boxes
        filename = infer_txt
        instance = {'filename': filename, 'boxes': []}
        with open(infer_txt_folder_path + filename, 'r', encoding='utf-8') as f:
            # txt_to_box(f, instance, img_size
            for line in f.readlines():
                object = line.split(' ')
                category = int(object[0])
                x = (float(object[1]) - float(object[3]) / 2) * img_size[0]
                y = (float(object[2]) - float(object[4]) / 2) * img_size[1]
                w, h = float(object[3]) * img_size[0], float(object[4]) * img_size[1]
                instance['boxes'].append(Box(category, int(x), int(y), int(w), int(h)))
        infer_boxes.append(instance)
    for gt_txt in gt_txts:
        filename = gt_txt
        instance = {'filename': filename, 'boxes': []}
        with open(gt_txt_folder_path + filename, 'r', encoding='utf-8') as f:
            # txt_to_box(f, instance, img_size)
            for line in f.readlines():
                object = line.split(' ')
                category = int(object[-5])
                x = (float(object[-4]) - float(object[-2]) / 2) * img_size[0]
                y = (float(object[-3]) - float(object[-1]) / 2) * img_size[1]
                w, h = float(object[-2]) * img_size[0], float(object[-1]) * img_size[1]
                instance['boxes'].append(Box(category, int(x), int(y), int(w), int(h)))
        gt_boxes.append(instance)
    return gt_boxes, infer_boxes

# 单个txt文件f转为box对象
def txt_to_box(f, instance, img_size):
    for line in f.readlines():
        object = line.split(' ')
        category = int(object[-5])
        x = (float(object[-4]) - float(object[-2]) / 2) * img_size[0]
        y = (float(object[-3]) - float(object[-1]) / 2) * img_size[1]
        w, h = float(object[-2]) * img_size[0], float(object[-1]) * img_size[1]
        instance['boxes'].append(Box(category, int(x), int(y), int(w), int(h)))



# 输出漏检、过杀和正确检出的json和jpg文件
def filter(correct_list: list, recall_list: list, precision_list: list, gt_boxes: list, img_size, category_name: list,
           correct_folder_path: str, recall_folder_path: str, precision_folder_path: str, imgs_folder_path: str):

    list_to_json(gt_boxes, img_size, category_name, imgs_folder_path)
    list_to_json(correct_list, img_size, category_name, correct_folder_path)
    list_to_json(recall_list, img_size, category_name, recall_folder_path)
    list_to_json(precision_list, img_size, category_name, precision_folder_path)


    for img_name in os.listdir(imgs_folder_path):
        for correct_json_name in os.listdir(correct_folder_path):
            if correct_json_name.replace('.json', '.jpg') == img_name: shutil.copy(imgs_folder_path + img_name, correct_folder_path)
        for recall_json_name in os.listdir(recall_folder_path):
            if recall_json_name.replace('.json', '.jpg') == img_name: shutil.copy(imgs_folder_path + img_name, recall_folder_path)
        for precision_json_name in os.listdir(precision_folder_path):
            if precision_json_name.replace('.json', '.jpg') == img_name: shutil.copy(imgs_folder_path + img_name, precision_folder_path)


# 返回的是一个json，输入的是一个list
# [{'filename':xxx, 'boxes':[box1, box2, ...]}...{}]
def list_to_json(input: list, img_size, category_name: list, save_path: str):
    for i in input:
        new_json = {}
        new_json['version'] = '1.0'
        new_json['flags'] = {}
        new_json['imageData'] = None
        new_json['imageDepth'] = 3
        new_json['imageHeight'] = int(img_size[1])
        new_json['imageLabeled'] = str(True)
        new_json['imagePath'] = i['filename'].replace('.txt', '.jpg')
        new_json['imageWidth'] = int(img_size[0])
        new_json['shapes'] = []
        new_json['time_Labeled'] = None
        #[box1, box2, ...]
        for j in i['boxes']:
            instance = {'label': category_name[j.category], 'points': [], 'width': j.category, 'group_id': None, 'shape_type': 'rectangle', 'flags': {}}
            x1, y1, x2, y2 = j.x, j.y, j.x + j.w, j.y + j.h
            instance['points'].extend([[int(x1), int(y1)], [int(x2), int(y2)]])
            new_json['shapes'].append(instance)
        with open(save_path + '{}.json'.format(i['filename'][:-4]), 'w', encoding='utf-8') as f:
            f.write(json.dumps(new_json, indent=4))




if __name__ == '__main__':
    gt_path = 'E:/PR/gt_txts/'  # gt的txt文件夹
    infer_path = 'E:/PR/infer_txts/'   # infer的txt文件夹
    gt_boxes, infer_boxes = txts_to_boxes(gt_path, infer_path, (768, 768))
    correct_list, recall_list, precision_list = pr_analysis(gt_boxes, infer_boxes)
    name = ['baomo', 'cashang', 'huashang', 'pengshang', 'yashang', 'yise']
    zhengque_path = 'E:/PR/zhengque/'  # 正确检出的文件夹
    loujian_path = 'E:/PR/loujian/'  # 漏检的文件夹
    guosha_path = 'E:/PR/guosha/' # 过杀的文件夹
    imgs_path = 'E:/PR/imgs/'  # 所有img的文件夹
    filter(correct_list, recall_list, precision_list, gt_boxes, (768, 768), name, zhengque_path, loujian_path, guosha_path, imgs_path)



















