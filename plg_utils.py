import json
import math
import os
import cv2
import numpy as np
from pypinyin import pinyin, NORMAL


IMG_TYPES = ['jpg', 'png']

def create_empty_json_instance(img_file_path: str):
    '''
    :param img_file_path: img路径
    :return: 构建一个空的labelme json instance对象
    '''
    instance = {'version': '1.0',
                'shapes': [],
                'imageData': None,
                'imagePath': img_file_path[img_file_path.rindex(os.sep)+1:]}
    img = cv2.imread(img_file_path)
    instance['imageHeight'], instance['imageWidth'], instance['imageDepth'] = img.shape
    instance_to_json(instance, img_file_path[:img_file_path.rindex('.')]+'.json')
    return instance

def word_to_pinyin(word: str):
    '''
    :param word: 输入的中文字符串
    :return: 英文字符串
    '''
    s = ''
    for i in pinyin(word, style=NORMAL):
        s += i[0].strip()
    return s

# -----以下代码用来进行坐标转换-----
def extract_xys(axiss):
    '''
    :param axiss: xml中的坐标系父节点
    :return: list[x1,y1,...,xn,yn]
    '''
    return [float(axis.text) for axis in axiss]

def points_to_xywh(obj):
    '''
    :param obj: labelme instance中待检测目标obj{}
    :return: box左上坐标+wh
    '''
    points = obj['points']
    shape_type = obj['shape_type']
    if shape_type == 'circle':
        center = [points[0][0], points[0][1]]
        radius = math.sqrt((points[1][0]-center[0])**2+(points[1][1]-center[1])**2)
        return [center[0]-radius-1, center[1]-radius-1, 2*radius+3, 2*radius+3]
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    return [min_x-1, min_y-1, max_x-min_x+3, max_y-min_y+3]

def points_to_center(obj):
    '''
    :param obj: labelme instance中待检测目标obj{}
    :return: box中心坐标
    '''
    points = obj['points']
    shape_type = obj['shape_type']
    if shape_type == 'circle':
        return points[0][0], points[0][1]
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    return (min_x+max_x)/2, (min_y+max_y)/2
# -----以上代码用来进行坐标转换-----

def instance_clean(instance):
    '''
    :param instance: labelme json instance
    :return: 将不良points进行清洗、更正
    '''
    for obj in instance['shapes']:
        points = obj['points']
        if obj['shape_type'] in ('line', 'linestrip'):
            # 排除标注小组的重复落点
            points_checked = [points[0]]
            for point in points:
                if point != points_checked[-1]:
                    points_checked.append(point)
            obj['points'] = points_checked
            points = points_checked
            # 排除标注小组的往返落点
            if len(points) >= 3:
                temp = get_angle((points[-3][0]-points[-2][0], points[-3][1]-points[-2][1]), (points[-1][0]-points[-2][0], points[-1][1]-points[-2][1]))
                if temp > -0.001 and temp < 0.001: del points[-1]
            if len(points) == 1: obj['shape_type'] = 'point'
            elif len(points) == 2: obj['shape_type'] = 'line'
            else: obj['shape_type'] = 'linestrip'

def instance_points_to_polygon(instance):
    '''
    :param instance: labelme json instance
    :return: 将instance['shapes']中points的标签，由rectangle和circle变为polygon，从而更好地进行crop和fill
    '''
    objs = instance['shapes']
    for obj in objs:
        shape_type = obj['shape_type']
        points = obj['points']
        if shape_type == 'rectangle':
            xs = [point[0] for point in points]
            ys = [point[1] for point in points]
            min_x, min_y = min(xs), min(ys)
            max_x, max_y = max(xs), max(ys)
            obj['points'] = [[min_x, min_y], [max_x, min_y], [max_x, max_y], [min_x, max_y]]
            obj['shape_type'] = 'polygon'
        elif shape_type == 'circle':
            center = [points[0][0], points[0][1]]
            radius = math.sqrt((points[1][0]-center[0])**2+(points[1][1]-center[1])**2)
            obj['points'] = []
            obj['shape_type'] = 'polygon'
            for i in range(0, 360, 10):
                obj['points'].append([center[0]+math.cos(math.pi*i/180)*radius, center[1]+math.sin(math.pi*i/180)*radius])

# -----以下代码求两线段交点坐标-----
class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Line(object):
    # a=0, b=0, c=0
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

def getLinePara(line):
    line.a =line.p1.y - line.p2.y
    line.b = line.p2.x - line.p1.x
    line.c = line.p1.x *line.p2.y - line.p2.x * line.p1.y

def getCrossPoint(l1, l2):
    getLinePara(l1)
    getLinePara(l2)
    d = l1.a * l2.b - l2.a * l1.b
    p=Point()
    if d == 0: return None
    p.x = (l1.b * l2.c - l2.b * l1.c)*1.0 / d
    p.y = (l1.c * l2.a - l2.c * l1.a)*1.0 / d
    return p

def get_cross_point(x1, y1, x2, y2, x3, y3, x4, y4):
    p1 = Point(x1, y1)
    p2 = Point(x2, y2)
    l1 = Line(p1, p2)
    p3 = Point(x3, y3)
    p4 = Point(x4, y4)
    l2 = Line(p3, p4)
    cp = getCrossPoint(l1, l2)
    if cp == None \
            or cp.x < min([x1, x2])-0.01 \
            or cp.x > max([x1, x2])+0.01 \
            or cp.y < min([y1, y2])-0.01 \
            or cp.y > max([y1, y2])+0.01 \
            or cp.x < min([x3, x4])-0.01 \
            or cp.x > max([x3, x4])+0.01 \
            or cp.y < min([y3, y4])-0.01 \
            or cp.y > max([y3, y4])+0.01:
        return None
    else:
        return [cp.x, cp.y]
# -----以上求两线段交点坐标-----

def json_to_instance(json_file_path):
    '''
    :param json_file_path: json文件路径
    :return: json instance
    '''
    with open(json_file_path, 'r', encoding='utf-8') as f:
        instance = json.load(f)
    return instance

def instance_to_json(instance, json_file_path):
    '''
    :param instance: json instance
    :param json_file_path: 保存为json的文件路径
    :return: 将json instance保存到相应文件路径
    '''
    with open(json_file_path, 'w', encoding='utf-8') as f:
        content = json.dumps(instance, ensure_ascii=False, indent=2)
        f.write(content)

def points_to_coco_segmentation(obj, line_pixel):
    '''
    :param obj: labelme instance中待检测目标obj{}
    :param line_pixel: labelme中line、linestrip points的加宽像素值
    :return: coco segmentation[[x1,y1,x2,y2,...,xn,yn]]
    '''
    points = obj['points']
    shape_type = obj['shape_type']
    if shape_type == 'rectangle':
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        min_x, min_y = min(xs), min(ys)
        max_x, max_y = max(xs), max(ys)
        result = [[min_x, min_y, max_x, min_y, max_x, max_y, min_x, max_y]]
    elif shape_type == 'circle':
        center = [points[0][0], points[0][1]]
        radius = math.sqrt((points[1][0]-center[0])**2+(points[1][1]-center[1])**2)
        temp = []
        for i in range(0, 360, 10):
            temp.append(center[0]+math.cos(math.pi*i/180)*radius)
            temp.append(center[1]+math.sin(math.pi*i/180)*radius)
        result = [temp]
    elif shape_type == 'line' or shape_type == 'linestrip':
        result = [line_pixel_widen(points, line_pixel)]
    else:
        result = [np.asarray(points).flatten().tolist()]
    return result

def line_pixel_widen(points, line_pixel):
    '''
    :param points: labelme中标签为line、linestrip的points
    :param line_pixel: 加宽的像素点
    :return: 返回coco中直线segmentation的坐标点
    '''
    line1 = []
    line2 = []
    for i, point in enumerate(points):
        belong_to_line1 = True
        if i == 0:
            vector2 = (points[i+1][0] - point[0], points[i+1][1] - point[1])
            angle_horiz = get_horiz_angle(vector2) + math.pi/2
            line1.append(perturbation_around_point(point, angle_horiz, line_pixel)[0])
            line2.append(perturbation_around_point(point, angle_horiz, line_pixel)[1])
            continue
        elif i == len(points)-1:
            vector1 = (points[i-1][0] - point[0], points[i-1][1] - point[1])
            angle_horiz = get_horiz_angle(vector1) + math.pi/2
            perturb_points = perturbation_around_point(point, angle_horiz, line_pixel)
            if get_cross_point(perturb_points[0][0], perturb_points[0][1], line1[-1][0], line1[-1][1], points[i-1][0], points[i-1][1], point[0], point[1]) != None:
                belong_to_line1 = False
        else:
            vector1 = (points[i-1][0] - point[0], points[i-1][1] - point[1])
            vector2 = (points[i+1][0] - point[0], points[i+1][1] - point[1])
            angle_horiz = get_mid_horiz_angle(vector1, vector2)
            radius = line_pixel/math.sin(get_angle(vector1, vector2)/2)
            perturb_points = perturbation_around_point(point, angle_horiz, radius)
            if get_cross_point(perturb_points[0][0], perturb_points[0][1], line1[-1][0], line1[-1][1], points[i-1][0], points[i-1][1], point[0], point[1]) != None:
                belong_to_line1 = False
        if belong_to_line1:
            line1.append(perturb_points[0])
            line2.append(perturb_points[1])
        else:
            line1.append(perturb_points[1])
            line2.append(perturb_points[0])
    # import matplotlib.pyplot as plt
    # line = [[points[i][0], points[i][1], points[i - 1][0], points[i - 1][1]] for i in range(1, len(points))]
    # plt.plot([p[0] for p in points], [p[1] for p in points], 'g-')
    # plt.plot([l[0] for l in line1], [l[1] for l in line1], 'b:')
    # plt.plot([l[0] for l in line2], [l[1] for l in line2], 'b:')
    # plt.show()
    return np.asarray(line1 + list(reversed(line2))).flatten().tolist()

def perturbation_around_point(point, angle, radius):
    '''
    :param point: 目标坐标点
    :param angle: 微扰角度
    :param radius: 微扰幅度
    :return: 返回一个坐标点的周围两个微扰点
    '''
    return [point[0] + radius * math.cos(angle), point[1] + radius * math.sin(angle)],\
           [point[0] - radius * math.cos(angle), point[1] - radius * math.sin(angle)]

def get_mid_horiz_angle(vector1, vector2):
    '''
    :param vector1: 向量1
    :param vector2: 向量2
    :return: 两个向量的中间向量与水平线(1,0)的夹角
    '''
    angle_horiz_1 = get_horiz_angle(vector1)
    angle_horiz_2 = get_horiz_angle(vector2)
    return (angle_horiz_1 + angle_horiz_2)/2

def get_horiz_angle(vector):
    '''
    :param vector: 一个向量
    :return: 该向量和水平线(1,0)的夹角(-180-180)
    '''
    angle_horiz = get_angle((1, 0), vector) if vector[1] > 0 else -get_angle((1, 0), vector)
    return angle_horiz

def get_angle(vector1, vector2):
    '''
    :param vector1: 向量1
    :param vector2: 向量2
    :return: 向量之间的夹角(0-180)
    '''
    inner_product = vector1[0]*vector2[0] + vector1[1]*vector2[1]
    cosin = inner_product/(math.sqrt((vector1[0]**2+vector1[1]**2)*(vector2[0]**2+vector2[1]**2)))
    return math.acos(cosin)

def crop_is_empty(instance, crop_size, iou_thres=0.2):
    '''
    :param instance: labelme json instance
    :param crop_size: crop范围[上，下，左，右]
    :return: bool值
    '''
    flag = True
    for obj in instance['shapes']:
        if obj_in_crop(obj, crop_size, iou_thres):
            flag = False
            break
    return flag

def obj_in_crop(obj, crop_size, iou_thres=0.2):
    '''
    :param points: labelme json中一个obj的points
    :param crop_size: crop范围[上，下，左，右]
    :param iou_thres: iou阈值
    :return: bool值
    '''
    crop_box = Box(crop_size[2], crop_size[0], crop_size[3] - crop_size[2], crop_size[1] - crop_size[0])
    x, y, w, h = points_to_xywh(obj)
    obj_box = Box(x, y, w, h)
    inter_area = calculate_inter_area(obj_box, crop_box)
    return inter_area != 0 and inter_area/obj_box.get_area() >= iou_thres

def point_in_crop(point, crop_size):
    '''
    :param point: labelme json中一个obj的points-point[x,y]
    :param crop_size: crop范围[上，下，左，右]
    :return: bool值
    '''
    return point[0] > crop_size[2] and \
           point[0] < crop_size[3] and \
           point[1] > crop_size[0] and \
           point[1] < crop_size[1]

class Box:
    # xy是左上角坐标
    def __init__(self, x, y, w, h, category=None, confidence=None):
        self.category = category
        self.confidence = confidence
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_area(self):
        return self.w * self.h

    def get_iou(self, box2):
        inter_area = calculate_inter_area(self, box2)
        return inter_area/(self.get_area()+box2.get_area()-inter_area)

def calculate_inter_area(box1, box2):
    '''
    :param box1: Box对象
    :param box2: Box对象
    :return: box1与box2的交面积
    '''
    left_x, left_y = max([box1.x, box2.x]), max([box1.y, box2.y])
    right_x, right_y = min([box1.x + box1.w, box2.x + box2.w]), min([box1.y + box1.h, box2.y + box2.h])
    height = right_y - left_y
    width = right_x - left_x
    area = height * width if height>0 and width>0 else 0
    return area


if __name__ == '__main__':
    print(perturbation_around_point([1,1], -1.57/2, 1.414))

























