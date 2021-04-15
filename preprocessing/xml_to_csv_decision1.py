"""
description: 
author: zhangyan
date: 2021-04-09 15:44
"""

from pycocotools.mask import decode
import cv2
from skimage import morphology
import numpy as np
import math
import logging
import json

def json_to_instance(json_file_path):
    '''
    :param json_file_path: json文件路径
    :return: json instance
    '''
    with open(json_file_path, 'r', encoding='utf-8') as f:
        instance = json.load(f)
    return instance

def _extract_length(mask, by_skeleton=True):
    """
    extract_length
    :param by_skeleton:
    :param mask: mask of target
    :return: length of the image _crop
    """
    height, width = mask.shape[0], mask.shape[1]
    #print(height, width)
    if by_skeleton:
        # 使用骨架算法
        skeleton = morphology.skeletonize(mask)
        length = sum(skeleton.flatten())
        if length < min(height, width):
            length = min(height, width)  # 圆形缺陷的skeleton会被提取为一个点
        return length

    else:
        contours, _ = cv2.findContours(mask.astype(np.uint8) * 255, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        xs = contours[0][0][:, 0]
        ys = contours[0][0][:, 1]
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        # 计算目标区域中心点
        center_point = ((xmin + xmax) // 2, (ymax + ymin) // 2)
        # 找离中心点最远的点
        max_distance = 0
        for row in range(height):
            for col in range(width):
                if mask[row, col] == 0:
                    continue
                else:
                    distance = math.sqrt(
                        ((row - center_point[1]) ** 2) + ((col - center_point[0]) ** 2))
                    if distance > max_distance:
                        max_distance = distance
                        p1 = (row, col)
        # 找离p1最远的点
        length = 0
        for row in range(height):
            for col in range(width):
                if mask[row, col] == 0:
                    continue
                else:
                    distance_top1 = math.sqrt(((row - p1[1]) ** 2) + ((col - p1[0]) ** 2))
                    if distance_top1 > length:
                        length = distance_top1
                        p2 = (row, col)
    return length


def _extract_width(mask):
    """
    extract_width
    :param image:
    :param mask:
    :return:
    """
    # TODO: 圆形mask会被提取成一个点
    _, distance = morphology.medial_axis(mask, return_distance=True)
    distance[morphology.skeletonize(mask) == 0] = 0
    distance_values = distance[distance != 0]
    if len(distance_values) == 0:
        return 1
    width = sum(distance_values) / len(distance_values) * 2
    return width

def _extract_length_width_bydt(mask):
    """extract_length and width by distance transform"""
    height, width = mask.shape[0], mask.shape[1]
    # 使用骨架算法
    skeleton = morphology.skeletonize(mask)
    length = sum(skeleton.flatten())
    if length < min(height, width):
        length = min(height, width)  # 圆形缺陷的skeleton会被提取为一个点

    # distance transform
    dist_img = cv2.distanceTransform(mask.astype('uint8'), cv2.DIST_L2, cv2.DIST_MASK_3)
    width = np.median(dist_img[skeleton]) * 2

    return length, width
def _extract_brightness(mask, image):
    """
    extract_brightness
    :param mask:
    :param image:
    :return:
    """
    try:
        segm_pixels = image[mask == 1].flatten().tolist()
    except Exception as e:
        logging.debug('Mask shape: {}, image_shape: {}'.format(mask.shape, image.shape))
        return 0, 0, 0
    if len(segm_pixels) == 0:
        return 0, 0, 0

    # return np.median(segm_pixels), np.percentile(segm_pixels, 80), \
    #        np.percentile(segm_pixels, 20)

    top_k = max(1, int(len(segm_pixels) * 0.2))
    top_k_idx = sorted(segm_pixels, reverse=True)[0:top_k]
    low_k_idx = sorted(segm_pixels)[0:top_k]
    return sum(segm_pixels) / len(segm_pixels), sum(top_k_idx) / len(top_k_idx), sum(
        low_k_idx) / len(low_k_idx)


def _extract_gradients(mask, image,limit_scale=100):
    """
    extract_gradients
    :param mask:
    :param image:
    :return:
    """
    # if mask.shape[0] >= limit_scale or mask.shape[1] >= limit_scale:
    #     scale = limit_scale / max(mask.shape[0], mask.shape[1])
    #     new_w, new_h = int(image.shape[1] * scale), int(image.shape[0] * scale)
    #     image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    #     mask = cv2.resize(mask, (new_w, new_h), interpolation=cv2.INTER_AREA)
    #     mask = mask.astype(np.bool)
    #
    # else:
    #     mask = mask.astype(np.bool)

    gray_x = cv2.Sobel(image, cv2.CV_32F, 1, 0)  # x方向一阶导数
    gray_y = cv2.Sobel(image, cv2.CV_32F, 0, 1)  # y方向一阶导数
    gradx = cv2.convertScaleAbs(gray_x)  # 转回原来的uint8形式
    grady = cv2.convertScaleAbs(gray_y)
    grad = cv2.addWeighted(gradx, 0.5, grady, 0.5, 0)  # 图像融合
    # 提取mask边缘点的梯度值
    # print(mask)
    mask = np.ascontiguousarray(mask)
    contours,_ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    # 提取边缘点
    edge_points = []
    for contour in contours:
        #print(contour)
        for i in range(contour.shape[0]):
            edge_point = contour[i, 0, :]
            edge_points.append(edge_point)

    # 计算边缘点梯度均值
    grad_sum = 0
    for ep in edge_points:
        x, y = ep[0], ep[1]
        grad_sum += grad[y, x]
    return grad_sum if len(edge_points) == 0 else grad_sum / len(edge_points)

def _extract_feat(self, bbox, mask, limit_scale=100):
    """
    extract_feat
    :param image: image crop, list
    :param mask: mask of target, np.ndarray
    :limit_scale: mask的宽或高超过这个值就会做resize, int
    :return: features of the feature, dict
    """
    image = self.image_np[bbox[1]: bbox[1] + mask.shape[0], bbox[0]: bbox[0] + mask.shape[1]]
    scale = 1
    if mask.shape[0] >= limit_scale or mask.shape[1] >= limit_scale:
        scale = limit_scale / max(mask.shape[0], mask.shape[1])
        new_w, new_h = int(image.shape[1] * scale), int(image.shape[0] * scale)
        image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        mask = cv2.resize(mask, (new_w, new_h), interpolation=cv2.INTER_AREA)
        mask = mask.astype(np.bool)
        length, width = self._extract_length_width_minarea(mask)

    else:
        mask = mask.astype(np.bool)
        length, width = self._extract_length_width_bydt(mask)
    length /= scale
    width /= scale
    pixel_area = self._extract_pixel_area(mask)
    pixel_area = pixel_area / scale / scale
    brightness, max20brightness, min20brightness = self._extract_brightness(mask, image)
    gradients = self._extract_gradients(mask, image)
    contrast = self._extract_contrast(mask, image)

    feature_result = {'length': length,
                      'width': width,
                      'pixel_area': pixel_area,
                      'brightness': brightness,
                      'max20brightness': max20brightness,
                      'min20brightness': min20brightness,
                      'gradients': gradients,
                      'contrast': contrast
                      }
    return feature_result
def _extract_contrast(mask, image, up_scale=100):
    """
    extract_contrast
    :param mask:
    :param image:
    :param up_scale:
    :return:
    """
    image_norm = image / 255
    fgs = image[mask != 0].flatten()
    bgs = image[mask == 0].flatten()
    if len(fgs) == 0:
        fg_mean = 0
    else:
        fg_mean = sum(fgs) / len(fgs)
    if len(bgs) == 0:
        bg_mean = 0
    else:
        bg_mean = sum(bgs) / len(bgs)

    contrast = abs(fg_mean - bg_mean)

    return contrast * up_scale

coco_path = "/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/Anew/all/select_gs_dw/gsdw/gsdw/409.json"
coco = json_to_instance(coco_path)
imgs = coco.get('images')
cate = coco.get('categories')
anno = coco.get('annotations')
#print(imgs)
print(cate)
# print(anno)
dic_id_img = {}
for i in imgs:
    dic_id_img[i['id']]=i['file_name']

dic_id_cate = {}
for i in cate:
    dic_id_cate[i['id']]=i['name']

# segm = anno[0].get('segmentation')
# mask = decode(segm)
# print(mask.shape)
# image = cv2.imread('/home/lijq/PycharmProjects/micro-i-tools/1/887_4168_2.jpg')
# print(image.shape)
# print(mask)

# csv需要获取img_name, class_name, xmin, ymin, bb_width, bb_height, score, length, width, pixel_area, gradients, contrast, brightness, plevel, describe

# length = _extract_length(mask)
# width = _extract_width(mask)
# print('length,width',length,width)
# contrast = _extract_contrast(mask, image, up_scale=100)
# print('contrast:',contrast)
# brightness = _extract_brightness(mask, image)
# print('brightness:',brightness)
# gradients = _extract_gradients(mask, image)
# print('gradients:',gradients)
imgs_root = '/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/Anew/all/select_gs_dw/gsdw/gsdw/all'
output_csv_path='/home/lijq/data/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/Anew/all/select_gs_dw/gsdw/gsdw/409.csv'

#XUNHUAN
import os
if not os.path.exists(output_csv_path):
    with open(output_csv_path,'w') as f:
        f.write('img_name,class_name,class_name1,xmin,ymin,bb_width,bb_height,score,length,width,pixel_area,gradients,contrast,brightness,plevel,describe\n')
for i in range(len(anno)):
    anno_single = anno[i]
    img_id = anno_single['id']
    try:
        img_name = dic_id_img[img_id]
        class_id = anno_single['category_id']
        class_name = dic_id_cate[class_id]
        class_name1 = class_name.split('-')[0]
        xmin, ymin, bb_width, bb_height = anno_single['bbox']

        xmin, ymin, bb_width, bb_height = int(xmin), int(ymin), int(bb_width), int(bb_height)
        print(xmin, ymin, bb_width, bb_height)
        try:
            score=anno_single['score']
        except:
            score=1
        segm = anno_single['segmentation']
        mask = decode(segm)
        print(mask.shape)
        # length = _extract_length(mask)
        # width = _extract_width(mask)
        length,width = _extract_length_width_bydt(mask)
        pixel_area = anno_single['area']
        img_p = os.path.join(imgs_root,img_name)
        image = cv2.imread(img_p)
        print(xmin, ymin, bb_width, bb_height)
        print(image.shape)
        mask_cut = mask[ymin:ymin+bb_height,xmin:xmin+bb_width]
        print(mask_cut.shape)
        image_cut = image[ymin:ymin + bb_height,xmin:xmin + bb_width, :]
        print(image_cut.shape)
        gradients = _extract_gradients(mask_cut, image_cut)
        contrast = _extract_contrast(mask_cut, image_cut, up_scale=100)
        brightness, top_brightness,low_brightness= _extract_brightness(mask_cut, image_cut)
        '''
        gradients = _extract_gradients(mask, image)
        contrast = _extract_contrast(mask, image, up_scale=100)
        brightness = _extract_brightness(mask, image)
        '''
        plevel =anno_single['plevel']
        describe = anno_single['describe']
        with open(output_csv_path,'a') as f:
            f.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
                img_name, class_name,class_name1, xmin, ymin, bb_width, bb_height, score, length, width, pixel_area, gradients[0],
                contrast, brightness, plevel, describe
            ))
        print(img_name, class_name,class_name1, xmin, ymin, bb_width, bb_height, score, length, width, pixel_area, gradients[0], contrast, brightness, plevel, describe)
    except:
        print('skip---')
