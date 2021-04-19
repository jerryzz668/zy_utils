import json
from pycocotools.mask import encode
import pycocotools.mask as maskUtils
import numpy as np
import glob
import PIL.Image
from labelme.utils import shape as shape_labelme

class labelme2coco(object):
    def __init__(self,labelme_json=[],save_json_path='./new.json'):
        '''
        :param labelme_json: 所有labelme的json文件路径组成的列表
        :param save_json_path: json保存位置
        '''
        self.labelme_json=labelme_json
        self.save_json_path=save_json_path
        self.images=[]
        self.categories=[]
        self.annotations=[]
        # self.data_coco = {}
        self.label=[]
        self.annID=1
        self.height=0
        self.width=0

        self.save_json()

    def data_transfer(self):
        for num,json_file in enumerate(self.labelme_json):
            with open(json_file,'r', encoding='utf-8') as fp:
                data = json.load(fp)  # 加载json文件
                self.images.append(self.image(data,num))
                for shapes in data['shapes']:
                    label=shapes['label'].split('_')
                    print(label)
                    if label[0] not in self.label:
                        self.categories.append(self.categorie(label))
                        self.label.append(label[0])
                    points=shapes['points']
                    w = data['imageWidth']
                    h =data['imageHeight']
                    shape_type =shapes['shape_type']
                    level = data['level']
                    img_shape = (h,w, 3)
                    #img_shape = (w, h, 3)
                    print('json_file:',json_file)
                    self.annotations.append(self.annotation(img_shape,points,label,num,shape_type))
                    self.annID+=1

    def image(self,data,num):
        image={}
        height,width = data["imageHeight"],data["imageWidth"]
        image['height']=height
        image['width'] = width
        image['id']=num+1
        image['file_name'] = data['imagePath'].split('/')[-1]

        self.height=height
        self.width=width

        return image

    def categorie(self,label):
        categorie={}
        categorie['supercategory'] = label[0]
        categorie['id']=len(self.label)#+1 # 0 默认为背景
        categorie['name'] = label[0]
        return categorie

    def annotation(self,img_shape,points,label,num,shape_type):
        annotation={}
        mask = shape_labelme. shape_to_mask(img_shape[:2], points,shape_type)
        mask =mask+0
        print('img_shape, data["shapes"]',img_shape,shape_type,np.shape(mask))
        mask=np.asfortranarray(mask).astype('uint8')
        segm = encode(mask)#编码为rle格式
        annotation['area'] = float(maskUtils.area(segm))#计算mask编码的面积，必须放置在mask转字符串前面，否则计算为0
        segm['counts'] = bytes.decode(segm['counts'])#将字节编码转为字符串编码
        annotation['segmentation']=segm
        annotation['plevel']= plevel  # 增加
        annotation['describe']= describe  # 增加
        annotation['iscrowd'] = 0
        annotation['image_id'] = num+1
        annotation['bbox'] = list(map(float,self.getbbox(points,shape_type)))
        annotation['category_id'] = self.getcatid(label)
        annotation['id'] = self.annID
        return annotation

    def getcatid(self,label):
        for categorie in self.categories:
            if label[0]==categorie['name']:
                return categorie['id']
        return -1

    def getbbox(self,points,shape_type):
        polygons = points
        mask = shape_labelme.shape_to_mask([self.height,self.width], polygons,shape_type)
        return self.mask2box(mask)

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
        return [left_top_c, left_top_r, right_bottom_c-left_top_c, right_bottom_r-left_top_r]  # [x1,y1,w,h] 对应COCO的bbox格式

    def polygons_to_mask(self,img_shape, polygons):
        mask = np.zeros(img_shape, dtype=np.uint8)
        mask = PIL.Image.fromarray(mask)
        xy = list(map(tuple, polygons))
        PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        mask = np.array(mask, dtype=bool)
        return mask

    def data2coco(self):
        data_coco={}
        data_coco['images']=self.images
        data_coco['categories']=self.categories
        data_coco['annotations']=self.annotations
        return data_coco

    def save_json(self):
        self.data_transfer()
        self.data_coco = self.data2coco()
        # 保存json文件
        json.dump(self.data_coco, open(self.save_json_path, 'w',encoding='utf-8'), indent=4)  # indent=4 更加美观显示

labelme_json=glob.glob(r"C:\Users\Administrator\Desktop\xml_to_csv\jsons\*.json")
labelme2coco(labelme_json,r'C:\Users\Administrator\Desktop\instances_train2017.json')
