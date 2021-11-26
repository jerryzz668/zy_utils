from labelme.utils import shape as shape_labelme
from pycocotools.mask import encode
import pycocotools.mask as maskUtils
import numpy as np
import json
import multiprocessing
import glob
import time
import os
import sys
from preprocessing.zy_utils import json_to_instance
from tqdm import tqdm

class labelme2coco(object):
    def __init__(self, labelme_json, save_json_path, train_and_val_path, remain_bg):
        '''
        :param labelme_json: 所有labelme的json文件路径组成的列表
        :param save_json_path: json保存位置
        '''
        self.labelme_json = labelme_json
        self.save_json_path = save_json_path
        self.train_and_val_path = train_and_val_path
        self.remain_bg = remain_bg
        self.height = 0
        self.width = 0
        self.save_json()

    def get_categories(self):
        # 获得所有label并按字母排序
        cls = []
        categories = []
        class_mapers = {'a': 0}
        for file in os.listdir(self.train_and_val_path):
            if not file.endswith('.json'): continue
            instance = json_to_instance(os.path.join(self.train_and_val_path, file))
            for obj in instance['shapes']:
                if obj['label'] not in cls:
                    cls.append(obj['label'])
        cls = sorted(cls)
        # print('cls'*80,cls)
        if self.remain_bg == 'bg':
            categories.append({'supercategory': 'background', 'id': 0, 'name': 'background'})
            for i, cl in enumerate(cls):
                categorie = {}
                categorie['supercategory'] = cl
                categorie['id'] = i + 1
                categorie['name'] = cl
                categories.append(categorie)
                class_mapers[cl] = i + 1
        elif self.remain_bg == 'nobg':
            for i, cl in enumerate(cls):
                categorie = {}
                categorie['supercategory'] = cl
                categorie['id'] = i
                categorie['name'] = cl
                categories.append(categorie)
        # print('categories1111111111111111',categories)
        return categories, class_mapers

    def addshape(self, shape, data, num, annotations, categories, labels):

        label = shape['label'].split('_')

        if label[0] not in labels:
            labels.append(label[0])
            categories.append(self.categorie(label, labels))

        points = shape['points']
        w = data['imageWidth']
        h = data['imageHeight']
        shape_type = shape['shape_type']
        img_shape = (h, w, 3)
        annotations.append(self.annotation(img_shape, points, label, num, shape_type, annotations, categories))

    def data_transfer(self):
        pool = multiprocessing.Pool(processes=32)  # 创建进程个数
        images = []
        # images=multiprocessing.Manager().list()
        annotations = multiprocessing.Manager().list()
        # print('anno', annotations)
        categories = multiprocessing.Manager().list()
        labels = multiprocessing.Manager().list()
        for num, json_file in tqdm(enumerate(self.labelme_json)):
            with open(json_file, 'r', encoding='utf-8') as fp:
                data = json.load(fp)  # json
                images.append(self.image(data, num))
                for shape in data['shapes']:
                    pool.apply_async(self.addshape, args=(shape, data, num, annotations, categories, labels))
        pool.close()
        pool.join()

        return (images, annotations, categories)

    def image(self, data, num):
        image = {}
        height, width = data["imageHeight"], data["imageWidth"]
        image['height'] = height
        image['width'] = width
        image['id'] = num + 1
        image['file_name'] = data['imagePath'].split('/')[-1]

        self.height = height
        self.width = width

        return image

    def categorie(self, label, labels):
        categorie = {}
        categorie['supercategory'] = label[0]
        categorie['id'] = len(labels) - 1  # +1 # 0 默认为背景
        categorie['name'] = label[0]
        return categorie

    def annotation(self, img_shape, points, label, num, shape_type, annotations, categories):
        annotation = {}
        mask = shape_labelme.shape_to_mask(img_shape[:2], points, shape_type)
        annotation['bbox'] = list(map(float, self.mask2box(mask)))
        mask = mask + 0
        # print('img_shape, data["shapes"]',img_shape,shape_type,np.shape(mask))
        mask = np.asfortranarray(mask).astype('uint8')
        segm = encode(mask)  # 编码为rle格式
        annotation['area'] = float(maskUtils.area(segm))  # 计算mask编码的面积，必须放置在mask转字符串前面，否则计算为0
        segm['counts'] = bytes.decode(segm['counts'])  # 将字节编码转为字符串编码
        annotation['segmentation'] = segm
        annotation['iscrowd'] = 0
        annotation['image_id'] = num + 1

        categories, _ = self.get_categories()
        # print('categories',categories)
        annotation['category_id'] = self.getcatid(label, categories)
        annotation['id'] = len(annotations) + 1
        return annotation

    def getcatid(self, label, categories):
        for categorie in categories:
            if label[0] == categorie['name']:
                return categorie['id']
        return -1

    def mask2box(self, mask):
        '''从mask反算出其边框
        mask：[h,w]  0、1组成的图片
        1对应对象，只需计算1对应的行列号（左上角行列号，右下角行列号，就可以算出其边框）
        '''
        # np.where(mask==1)
        index = np.argwhere(mask == 1)
        rows = index[:, 0]
        clos = index[:, 1]
        # 解析左上角行列号
        left_top_r = np.min(rows)  # y
        left_top_c = np.min(clos)  # x

        # 解析右下角行列号
        right_bottom_r = np.max(rows)
        right_bottom_c = np.max(clos)
        return [left_top_c, left_top_r, right_bottom_c - left_top_c,
                right_bottom_r - left_top_r]  # [x1,y1,w,h] 对应COCO的bbox格式

    def data2coco(self, images, annotations, categories):
        data_coco = {}
        data_coco['images'] = images
        data_coco['categories'] = list(categories)
        data_coco['annotations'] = list(annotations)
        return data_coco

    def get_label_dic(self, categories):
        out_cates = []
        for cate in categories:
            out_cate = '{}:{}'.format(cate['name'], cate['id'])
            out_cates.append(out_cate)
        return out_cates
    def save_json(self):
        start = time.time()
        images, annotations, _ = self.data_transfer()
        categories, _ = self.get_categories()
        # print('categories', categories)
        print('------label_id_dict', self.get_label_dic(categories), '------')
        data_coco = self.data2coco(images, annotations, categories)
        json.dump(data_coco, open(self.save_json_path, 'w', encoding='utf-8'), indent=4)
        print('runtime:', time.time() - start)

if __name__ == '__main__':
    # labelme_path = '/home/jerry/Documents/Micro_ADR/R78/labeled_train'  # input_json_path
    labelme_path = sys.argv[1]
    train_and_val_path = sys.argv[2]  # get categories from here
    coco_path = sys.argv[3]
    remain_bg = sys.argv[4]
    # labelme_path = '/home/jerry/Desktop/garbage/coco/val2017'
    # train_and_val_path = '/home/jerry/Desktop/garbage/xxx'  # get categories from here
    # coco_path = '/home/jerry/Desktop/garbage/coco/annotations/instances_val2017.json'
    # remain_bg = 'bg'

    labelme_json = glob.glob('{}/*.json'.format(labelme_path))
    # coco_path = os.path.join(os.path.dirname(labelme_path), 'coco.json')
    labelme2coco(labelme_json, coco_path, train_and_val_path, remain_bg)

