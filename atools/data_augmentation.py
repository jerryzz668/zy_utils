from preprocessing.zy_utils import instance_to_json, json_to_instance
import albumentations as A
import random
import os 
from glob import glob
from atools.tools import *
from tqdm import tqdm 

def random_vertical_flip(img, points=[], rate=0.5):
    p = random.random()
    if p < rate:
        img = cv2.flip(img, 0)
        new_points = []
        if points != []:
            for point in points:
                point = np.array(point)
                point[:, 1] = img.shape[0] - point[:, 1]
                point = point.tolist()
                new_points.append(point)
            return img, new_points 
        else:
            return img, points
    else:
        return img, points

def random_horizontal_flip(img, points=[], rate=0.5):
    p = random.random()
    if p < rate:
        img = cv2.flip(img, 1)
        new_points = []
        if points != []:
            for point in points:
                point = np.array(point)
                point[:, 0] = img.shape[1] - point[:, 0]
                point = point.tolist()
                new_points.append(point)
            return img, new_points
        else:
            return img, points
    else:
        return img, points


def random_rot90(img, points=[], rate=0.5):
    p = random.random()
    if p < rate:
        img = np.rot90(img)
        new_points = []
        if points != []:
            for point in points:
                point = np.array(point)
                new_point = point.copy()
                new_point[:, 0] = point[:, 1]
                new_point[:, 1] = img.shape[0] - point[:, 0]
                new_point = new_point.tolist()
                new_points.append(new_point)
            return img, new_points
        else:
            return img, points
    else:
        return img, points

def transform(rate=0.5):
    transform = A.Compose([
                    A.MedianBlur(blur_limit=3, always_apply=False, p=rate),
                    A.GaussNoise(var_limit=(0,2), p=rate),
                    A.RandomBrightnessContrast(brightness_limit=0.05, contrast_limit=0.1, p=rate),
                    
                    ])
    return transform

def visulization(img, bboxs):
    plt_img = img.copy()
    for bbox in bboxs:
        x1, y1, x2, y2 = bbox
        cv2.rectangle(plt_img, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 2)
    plt.imshow(plt_img, cmap='gray')
    plt.show()

def modify_json_file(bboxs, instance):
    shapes = instance['shapes']
    assert len(bboxs) == len(shapes)
    for bbox, shape in zip(bboxs, shapes):
        shape['points'] = bbox
    return instance 

def random_data_aug(paramter):
    img_dir = paramter['img_dir']
    save_dir = paramter['save_dir']
    num_aug = paramter['num_aug']
    aug_name_list = paramter['aug_name_list']
    is_transform = paramter['is_transform']
    is_random = paramter['is_random']
    if is_random:
        rate = paramter['per_aug_rate']
    else:
        rate = 1
    make_dir(save_dir)
    img_path_list = glob(os.path.join(img_dir, '*.jpg'))
    for img_path in tqdm(img_path_list):
        json_path = img_path.replace('.jpg', '.json')
        use_label = True
        if not os.path.exists(json_path):
            use_label = False
        ori_img = cv2.imread(img_path)
        img_name = os.path.basename(img_path) 
        if use_label:
            instance = json_to_instance(json_path)
            instance['imageData'] = None
            shapes = instance['shapes']
            ori_points = []
            for shape in shapes:
                points = shape['points']
                ori_points.append(points)
            if ori_points == []:
                continue
            ori_points = ori_points
        else:
            ori_points = []
        image = ori_img.copy()
        points = ori_points.copy()
        if is_transform:
            transform_ = transform(rate)
            image = transform_(image=image)["image"]
        if is_random:
            for i in range(num_aug):
                for aug_name in aug_name_list:
                    image, points = aug_name(image, points, rate)
                out_img_name = 'arg' + str(i) + '_' + img_name   
                if use_label:
                    inst = instance.copy()
                    out_json_name = out_img_name.replace('.jpg', '.json')

                    inst = modify_json_file(points, inst)
                    inst['imagePath'] = out_img_name
                    inst['imageHeight'], inst['imageWidth'] = image.shape[0], image.shape[1]
                    inst = eval(str(inst))
                    instance_to_json(inst, os.path.join(save_dir, out_json_name))
                cv2.imwrite(os.path.join(save_dir, out_img_name), image)
        else:
            for aug_name in aug_name_list:
                new_image, new_points = aug_name(image, points, rate)

                tran_name = str(aug_name).split(' ')[1]
                out_img_name = 'arg' + str(tran_name) + '_' + img_name
                if use_label:
                    inst = instance.copy()
                    out_json_name = out_img_name.replace('.jpg', '.json')
                    inst = modify_json_file(new_points, inst)
                    inst['imagePath'] = out_img_name
                    inst['imageHeight'], inst['imageWidth'] = new_image.shape[0], new_image.shape[1]
                    instance_to_json(inst, os.path.join(save_dir, out_json_name))
                cv2.imwrite(os.path.join(save_dir, out_img_name), new_image)
                
if __name__ == '__main__':


    input_dir = '/home/jerry/data/Micro_AD/A_loushi/combined/blend'
    parameter = {
        'img_dir':input_dir,
        'save_dir': '{}_augmented'.format(input_dir),
        'num_aug':3,
        'aug_name_list':[random_rot90, random_vertical_flip, random_horizontal_flip],
        'is_transform': False,
        'is_random': False,
        'per_aug_rate':1,
    }
    random_data_aug(parameter)


    


