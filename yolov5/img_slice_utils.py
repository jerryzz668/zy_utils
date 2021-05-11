import random
from preprocessing.utils import *


def get_crop_num(img_size, crop_size, overlap):
    '''
    :param img_size: img长或者宽
    :param crop_size: crop的边长
    :param overlap: 相邻框的交并比
    :return: 根据overlap和crop size计算滑框截取个数
    '''
    return math.ceil((img_size-crop_size)/((1-overlap)*crop_size)) + 1

def _random_crop(cx, cy, w, h, size, shift_x_left=0.75, shift_x_right=0.25, shift_y_up=0.75, shift_y_bottom=0.25):
    '''
    :param cx: 目标中心点x
    :param cy: 目标中心点y
    :param w: 图片width
    :param h: 图片height
    :param size: 截图的size
    :param shift_x_left: 截框左边框距离cx的最左随机范围（距离像素/size）
    :param shift_x_right: 截框左边框距离cx的最右随机范围（距离像素/size）
    :param shift_y_up: 截框上边框距离cy的最上随机范围（距离像素/size）
    :param shift_y_bottom: 截框上边框距离cy的最下随机范围（距离像素/size）
    :return: 返回随机截图框
    '''
    # 截框左边框、上边框距离目标中心点的offset
    ofx, ofy = random.randint(int(size*shift_x_right), int(size*shift_x_left)), random.randint(int(size*shift_y_bottom), int(size*shift_y_up))
    cx, cy = int(cx), int(cy)
    fill_size = [0, 0, 0, 0]
    if size > h:
        up, bottom = 0, h
        fill_size[0], fill_size[1] = (size-h)//2, size-h-(size-h)//2
    elif cy-ofy < 0:
        up, bottom = 0, size
    elif cy-ofy+size > h:
        up, bottom = h-size, h
    else:
        up, bottom = cy-ofy, cy-ofy+size
    if size > w:
        left, right = 0, w
        fill_size[2], fill_size[3] = (size-w)//2, size-w-(size-w)//2
    elif cx-ofx < 0:
        left, right = 0, size
    elif cx-ofx+size > w:
        left, right = w-size, w
    else:
        left, right = cx-ofx, cx-ofx+size
    return [up, bottom, left, right], fill_size

# 根据过检和漏失的增强截图策略
def aug_crop_strategy(img, instance, size, additional_info):
    # 过检增强倍数
    precision_aug = 0
    # 漏失增强倍数
    recall_aug = 2
    # 错误、难样本增强倍数
    hard_aug = 0
    crop_strategies = []
    w = instance['imageWidth']
    h = instance['imageHeight']
    for obj in instance['shapes']:
        label = obj['label']
        # obj中心坐标位置
        cx, cy = points_to_center(obj)
        if label.startswith('guojian'):
            for i in range(precision_aug):
                crop_strategies.append(_random_crop(cx, cy, w, h, size))
        elif label.startswith('loushi'):
            for i in range(recall_aug):
                crop_strategies.append(_random_crop(cx, cy, w, h, size))
        elif label.startswith('hard') or label.startswith('cuowu'):
            for i in range(hard_aug):
                crop_strategies.append(_random_crop(cx, cy, w, h, size))
    return crop_strategies

# 根据过检和漏失的动态增强截图策略
def dynamic_aug_crop_strategy(img, instance, size, additional_info):
    crop_strategies = []
    w = instance['imageWidth']
    h = instance['imageHeight']
    for obj in instance['shapes']:
        label = obj['label']
        # 正常标签，不需要增强，则continue
        if '_' not in label: continue
        # 在label字符串中，p的起始、结束位置
        start, end = label.index('_')+1, label.index('_', label.index('_')+1)
        # obj中心坐标位置
        cx, cy = points_to_center(obj)
        if label.startswith('guojian'):
            p = float(label[start: end])
            for i in range(_dynamic_function(p, False)):
                crop_strategies.append(_random_crop(cx, cy, w, h, size))
        elif label.startswith('cuowu') or label.startswith('loushi'):
            for i in range(_dynamic_function(0.1)):
                crop_strategies.append(_random_crop(cx, cy, w, h, size))
        elif label.startswith('hard'):
            p = float(label[start: end])
            for i in range(_dynamic_function(p)):
                crop_strategies.append(_random_crop(cx, cy, w, h, size))
    return crop_strategies

def _dynamic_function(p, pos=True):
    '''
    :param p: 概率
    :param pos: 正标签or负标签
    :return: 动态增强倍数
    '''
    return round(10*(1-p)**2) if pos else 1

# 检测特定标签的截图策略
def check_crop_strategy(img, instance, size, additional_info):
    # 是否目标居中
    centerness = True
    # 需要查看的labels
    check_list = additional_info['check_list']
    crop_strategies = []
    w = instance['imageWidth']
    h = instance['imageHeight']
    for obj in instance['shapes']:
        label = obj['label']
        is_target = False
        for target in check_list:
            if target in label:
                is_target = True
                break
        if not is_target: continue
        cx, cy = points_to_center(obj)
        if centerness:
            crop_strategies.append(_random_crop(cx, cy, w, h, size, 0.5, 0.5, 0.5, 0.5))
        else:
            crop_strategies.append(_random_crop(cx, cy, w, h, size))
    return crop_strategies

# 聚类截图策略
def clustering_crop_strategy(img, instance, size, additional_info):
    crop_strategies = []
    added = []  # 用来存放截取过的obj
    w = instance['imageWidth']
    h = instance['imageHeight']
    objs = instance['shapes']
    num = len(objs)
    for i, obj in enumerate(objs):
        # 如果obj被截取过，continue
        if obj in added: continue
        # 当前聚类的外边框
        current_box = Box(*points_to_xywh(obj))
        # 开始搜寻聚类的objs
        for j in range(i+1, num):
            # 下一个obj
            next_obj = objs[j]
            # 如果下一个obj被截取过，continue
            if next_obj in added: continue
            next_box = Box(*points_to_xywh(next_obj))
            # 将下一个obj融合进当前的聚类的外边框
            combine_box = _combine_boxes(current_box, next_box)
            # 如果下一个obj不适合聚类，continue
            if combine_box.w > size or combine_box.h > size: continue
            # 聚类完成，更新当前的聚类的外边框
            current_box = combine_box
            # 将下一个obj放入added列表
            added.append(next_obj)
        if current_box.w < size and current_box.h < size:
            crop_strategies.append(_random_crop(current_box.x+current_box.w/2, current_box.y+current_box.h/2, w, h, size, (size-current_box.w/2)/size, current_box.w/2/size, (size-current_box.h/2)/size, current_box.h/2/size))
        else:
            crop_strategies.append(_random_crop(current_box.x+current_box.w/2, current_box.y+current_box.h/2, w, h, size, 0.5, 0.5, 0.5, 0.5))
    return crop_strategies

def _combine_boxes(box1, box2):
    '''
    :param box1:
    :param box2:
    :return: 返回两个box的合并box
    '''
    xmin = min(box1.x, box2.x)
    ymin = min(box1.y, box2.y)
    xmax = max(box1.x+box1.w, box2.x+box2.w)
    ymax = max(box1.y+box1.h, box2.y+box2.h)
    return Box(xmin, ymin, xmax-xmin, ymax-ymin)

































