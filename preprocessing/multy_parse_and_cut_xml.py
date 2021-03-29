# _*_ coding:utf-8 _*_
import time
import xml.etree.ElementTree as ET
import math, random
import os, glob, copy
import json
import base64
from os.path import isfile
from multiprocessing import Pool
import cv2
import numpy as np
import shapely
# from shapely.wkt import loads
# from shapely.geometry import LineString, polygon

START_BOUNDING_BOX_ID = 1
PRE_DEFINE_CATEGORIES = {}
ALL_LABEL_SHAPE = ['line', 'polygon', 'point', 'bndbox']

# ALL_DEFECTS_EN = ['黑点', '碰伤', '刮伤', '砂痕印', '白点', '塌边', '刀纹', '异物', '凹坑', '面花', '异色2', '异色1', '凹凸痕']
# ALL_DEFECTS = ['heidian', 'pengshang', 'guashang', 'shahenyin', 'baidian', 'tabian', 'daowen', 'yiwu', 'aokeng',
#                'mianhua', 'yise2', 'yise1', 'aotuhen']
ALL_DEFECTS_EN = ['碰伤-面', '刮伤-黑短', '砂痕印', '塌边-亮', '碰伤-边', '白点', '刮伤-黑长', '异色-黑']
ALL_DEFECTS = ['pengshang-mian', 'guashang-heiduan', 'shahenyin', 'tabian-liang', 'pengshang-bian', 'baidian', 'guashang-heizhang', 'yise-hei']

global xml_dir
global json_dir
global jpg_dir
global crop_json_dir
global need_crop
global crop_size
global crop_number
global num
xml_dir = r"C:\Users\Administrator\Desktop\compare\compare\rending\guaijiao\outputs"
json_dir = r"C:\Users\Administrator\Desktop\compare\compare\rending\guaijiao\jsons"
jpg_dir = r"C:\Users\Administrator\Desktop\compare\compare\model_result\guaijiao_result\2021-03-24 171718"
crop_json_dir = r"E:\7.project\2.microsoft\module-c\data\secondbatch1120\damian\test_cut\cut"
need_crop = False
crop_size = [1024, 1024]
crop_number = 100
num = 0


# 解析xml，取出标注数据
def parse_xml(file):
    # print("file: " + file)
    tree = ET.parse(file)
    root = tree.getroot()

    line_defect_info_list = []
    file_name = ''
    image_height, image_width = 0, 0
    for child in root:
        if child.tag == 'outputs':
            for sub_child in child:
                if sub_child.tag == 'object':
                    for item in sub_child:
                        if item.tag == 'item':
                            if item[0].text in ALL_DEFECTS_EN:
                                defect_type = ALL_DEFECTS_EN.index(item[0].text)
                                line_width = int(item[1].text)
                                label_shape = ALL_LABEL_SHAPE.index(item[2].tag)
                                # print('label shape {}'.format(label_shape))
                                line_defect_info = [defect_type, line_width, label_shape]
                                for sub_item in item:
                                    for point in sub_item:
                                        if 'points' in point.tag:
                                            print('points in tag')
                                            continue
                                        line_defect_info.append(int(point.text))
                                line_defect_info_list.append(line_defect_info)
        elif child.tag == 'path':
            file_name = os.path.split(child.text)[-1]
        elif child.tag == 'size':
            image_height = int(child[1].text)
            image_width = int(child[0].text)
    return line_defect_info_list, file_name, image_height, image_width


def cv2base64(image):
    # base64_str = cv2.imencode('.jpg', image)[1].tostring()
    # return base64.b64encode(base64_str)
    base64_str = cv2.imencode('.jpg', image)[1]
    return str((base64.b64encode(base64_str))[2:-1])


# 转化标注数据为标准json数据(单张图
# 1.读取xml数据，按照顺序每两个点转化为一个矩形，
# 2.判断矩形角点所在方位，按规则保存矩形角点数据
# 3.对每条标注缺陷所拥有的角点进行划分为一个多边形，保存到相应变量
# 4.保存由xml解析的所有参数为一个完整json
def save2json(lines, image_height, image_width, json_file, image_name, image_dir, need_crop, crop_size, crop_json_dir,
              crop_number, crop_num):
    image_path = os.path.join(image_dir, image_name)
    with open(image_path, "rb") as f:
        base64_str = base64.b64encode(f.read())
    base64_str = base64_str.decode('utf-8')
    json_dict = {"version": "4.2.10", "flags": {}, "shapes": [], "imagePath": image_name, "imageData": None,
                 "imageHeight": image_height,
                 "imageWidth": image_width}
    # json_dict["imageData"]=null
    image = cv2.imread(os.path.join(image_dir, image_name), cv2.IMREAD_GRAYSCALE)

    # step2 先遍历一次转为标准poly
    # crop_num=0
    for index, line in enumerate(lines):
        poly_points = parse_infects_2_polys(line)
        shape = {"label": ALL_DEFECTS[line[0]], "points": poly_points, "group_id": {}, "shape_type": "polygon",
                 "flags": {}}
        json_dict['shapes'].append(shape)

    if need_crop:
        # crop model 1 遍历每个poly生成crop_box,  2 判断属于crop_box的缺陷，保存信息
        json_dict_copy = copy.deepcopy(json_dict)
        shapes = json_dict_copy["shapes"]
        for shape in shapes:
            if crop_num >= crop_number:
                break

            # todo 指定类别优先切图时打开此注释
            # if shape['label'] is not ALL_DEFECTS[2]:
            #     continue

            index = shapes.index(shape)
            points = shape["points"]
            if len(points) <= 0:
                continue
            left_top = gen_crop_box(points, crop_size)

            # todo 如果切图不改变宽度，left==0
            crop_left = int(left_top['left'])
            # crop_left = 0
            crop_top = int(left_top['top'])
            crop_right = crop_left + crop_size[0]
            crop_bottom = crop_top + crop_size[1]
            if crop_right > image_width or crop_bottom > image_height or crop_left < 0 or crop_top < 0:
                continue
            crop_image = image[crop_top:crop_bottom, crop_left:crop_right]

            aug_jpg_name = str(os.path.splitext(image_name)[0]) + '_000' + str(index) + '.jpg'
            aug_json_name = str(os.path.splitext(image_name)[0]) + '_000' + str(index) + '.json'
            crop_image_path = os.path.join(crop_json_dir, aug_jpg_name)
            if not os.path.exists(crop_json_dir):
                os.mkdir(crop_json_dir)
            cv2.imwrite(crop_image_path, crop_image)

            with open(crop_image_path, "rb") as f:
                base64_crop = base64.b64encode(f.read())
            base64_crop = base64_crop.decode('utf-8')
            crop_json_dict = {"version": "4.2.10", "flags": {}, "shapes": [],
                              "imagePath": aug_jpg_name, "imageData": base64_crop, "imageHeight": crop_size[1],
                              "imageWidth": crop_size[0]}

            crop_num += 1
            # todo 参与过切图的bbox在此轮运算中被舍去，不重复运算
            for shape1 in shapes:
                # whether crop_box contains object
                # if not is_polys_out_of_crop_box(shape1, left_top, crop_size):
                #     continue
                clip_out_of_image(shape1, left_top, crop_size)
                label = shape1["label"]

                # new poly
                points1 = copy.deepcopy(shape1["points"])
                points1=re_order_polys(points1)
                # todo 需要根据面级筛选时打开注释
                # if cal_area(points1) < 40000:
                #     continue
                for point in points1:
                    point[0] = max(0, point[0] - crop_left)
                    point[1] = max(0, point[1] - crop_top)
                crop_shape = {"label": label, "points": points1, "group_id": {}, "shape_type": "polygon", "flags": {}}
                crop_json_dict['shapes'].append(crop_shape)

                json_fp_crop = open(os.path.join(crop_json_dir, aug_json_name), 'w')
                json_str_crop = json.dumps(crop_json_dict)
                json_fp_crop.write(json_str_crop)
                json_fp_crop.close()

                shapes.remove(shape1)

    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict)
    json_fp.write(json_str)
    json_fp.close()


def re_order_polys(points):
    points = np.reshape(points, (-1, 2))
    points = np.sort(points, axis=0)
    start_point, end_point = points[0], points[len(points) - 1]
    left_points = []
    right_points = []
    for rect_point in points:
        if is_point_beside_line_left(start_point, end_point, rect_point):
            left_points.append(rect_point)
        else:
            right_points.append(rect_point)
    left_points = np.sort(-left_points, axis=0)
    right_points = np.sort(right_points, axis=0)
    return np.reshape(np.concatenate(start_point, right_points, end_point, left_points), (1, -1))


def cal_area(points):
    left, top, right, bottom = 7000, 7000, 0, 0
    for point in points:
        left = min(point[0], left)
        right = max(point[0], right)
        top = min(point[1], top)
        bottom = max(point[1], bottom)
    return (bottom - top) * (right - left)


def gen_crop_box(poly_points, crop_size):
    # print(poly_points)
    poly_x0 = poly_points[0][0]
    poly_y0 = poly_points[0][1]
    offset_x = random.randint(10, crop_size[0] - 10)
    offset_y = random.randint(10, crop_size[1] - 10)
    crop_left = max(poly_x0 - offset_x, 0)
    crop_top = max(poly_y0 - offset_y, 0)
    return {"left": crop_left, "top": crop_top}


def is_polys_out_of_crop_box(shape, left_top, crop_size):
    points = shape["points"]
    for point in points:
        x = point[0]
        y = point[1]
        if x >= left_top['left'] + crop_size[0] or x <= left_top['left'] or y >= left_top['top'] + crop_size[1] or y <= \
                left_top['top']:
            return False
    return True


def clip_out_of_image(shape, left_top, crop_size):
    points = shape["points"]
    inter_points = []
    crop_left = left_top['left']
    crop_right = crop_left + crop_size[0]
    crop_top = left_top['top']
    crop_bottom = crop_top + crop_size[1]
    arr = np.array(points).reshape(-1, 2)
    # print(np.where((arr[:, 0] < 100) ))
    # print(np.delete(arr, np.where((arr[:, 0] < 100)), axis=0))
    points_out_of_image = np.where((arr[:, 0] > crop_right) | (arr[:, 0] < crop_left) | (arr[:, 1] > crop_bottom) | (
            arr[:, 1] < crop_top))
    if len(points_out_of_image) > 1:
        line_right = [(crop_right, crop_top), (crop_right, crop_bottom)]
        intersection_point = cal_intersection(points, line_right)
        inter_points.append(intersection_point)
        line_left = [(crop_left, crop_top), (crop_left, crop_bottom)]
        intersection_point = cal_intersection(points, line_left)
        inter_points.append(intersection_point)
        line_bottom = [(crop_left, crop_bottom), (crop_right, crop_bottom)]
        intersection_point = cal_intersection(points, line_bottom)
        inter_points.append(intersection_point)
        line_top = [(crop_left, crop_top), (crop_right, crop_top)]
        intersection_point = cal_intersection(points, line_top)
        inter_points.append(intersection_point)

    remain_points = np.delete(arr, points_out_of_image, axis=0).tolist()

    # todo 加入交点
    if len(inter_points) > 0:
        print('intersection points {}'.format(inter_points))
        remain_points = np.concatenate(remain_points, inter_points)
    shape["points"] = remain_points
    # for point in points:
    #     x = point[0]
    #     y = point[1]
    #     crop_left = left_top['left']
    #     crop_right = crop_left + crop_size[0]
    #     crop_top = left_top['top']
    #     crop_bottom = crop_top + crop_size[1]
    #     if x > crop_right:
    #         line_right = [(crop_right, crop_top), (crop_right, crop_bottom)]
    #         intersection_point = cal_intersection(points, line_right)
    #         inter_points.append(intersection_point)
    #     elif x < crop_left:
    #         line_left = [(crop_left, crop_top), (crop_left, crop_bottom)]
    #         intersection_point = cal_intersection(points, line_left)
    #         inter_points.append(intersection_point)
    #     elif y > crop_bottom:
    #         line_bottom = [(crop_left, crop_bottom), (crop_right, crop_bottom)]
    #         intersection_point = cal_intersection(points, line_bottom)
    #         inter_points.append(intersection_point)
    #     elif y < crop_top:
    #         line_top = [(crop_left, crop_top), (crop_right, crop_top)]
    #         intersection_point = cal_intersection(points, line_top)
    #         inter_points.append(intersection_point)


def cal_intersection(poly, line):
    # polygon = [(4.0, -2.0), (5.0, -2.0), (4.0, -3.0), (3.0, -3.0), (4.0, -2.0)]
    shapely_poly = shapely.geometry.Polygon(poly)

    # line = [(4.0, -2.0000000000000004), (2.0, -1.1102230246251565e-15)]
    shapely_line = shapely.geometry.LineString(line)

    # intersection_line = list(shapely_poly.intersection(shapely_line).coords)
    try:
        intersection_line = shapely_poly.intersection(shapely_line)
        if intersection_line.is_empty:
            return []
    except:
        print('except occur {}')
        return []
    print(intersection_line)

    return intersection_line.coords

    #
    # from shapely.geometry import Polygon
    # poly = loads('POLYGON (poly)')
    # line = loads('LINESTRING (line)')

    # intersection = poly.exterior.intersection(line)
    #
    # if intersection.is_empty:
    #     print("shapes don't intersect")
    # elif intersection.geom_type.startswith('Multi') or intersection.geom_type == 'GeometryCollection':
    #     for shp in intersection:
    #         print(shp)
    # else:
    #     print(intersection)


def parse_infects_2_polys(line):
    poly_points = []
    type = ALL_DEFECTS_EN[line[0]]
    label_shape = ALL_LABEL_SHAPE[line[2]]
    lines_defect_list = ALL_DEFECTS_EN
    poly_defect_list = ALL_DEFECTS_EN
    dot_defect_list = ALL_DEFECTS_EN
    bbox_defect_list = ALL_DEFECTS_EN

    if type in lines_defect_list and label_shape == 'line':
        poly_points = convert_lines_2_rects(line)
    elif type in poly_defect_list and label_shape == 'polygon':
        poly_points = convert_poly(line)
    elif type in dot_defect_list and label_shape == 'point':
        poly_points = convert_dot_2_poly(line)
    elif type in bbox_defect_list and label_shape == 'bndbox':
        poly_points = convert_bndbox_2_poly(line)

    return poly_points


def convert_bndbox_2_poly(defect_info):
    left = defect_info[3]
    top = defect_info[4]
    right = defect_info[5]
    bottom = defect_info[6]
    return [[left, top], [right, top], [right, bottom], [left, bottom]]


def convert_dot_2_poly(defect_info):
    r, x, y = defect_info[1] / 2, defect_info[3], defect_info[4]
    left = x - r
    top = y - r
    right = x + r
    bottom = y + r
    return [[left, top], [right, top], [right, bottom], [left, bottom]]


def convert_poly(defect_info):
    poly = []
    index = 3
    while index < len(defect_info):
        if index + 1 >= len(defect_info):
            break
        x1, y1 = defect_info[index], defect_info[index + 1]
        point = [x1, y1]
        poly.append(point)
        index += 2
    return poly


def convert_lines_2_rects(multy_line):
    line_width = multy_line[1]
    final_poly_points = []
    left_points_all = []
    right_points_all = []

    index = 3
    while index < len(multy_line):
        if index + 3 >= len(multy_line):
            break
        x1, y1 = multy_line[index], multy_line[index + 1]
        x2, y2 = multy_line[index + 2], multy_line[index + 3]
        # 1直线2点转换为矩形4点
        rect_points = generate_rect_with_lines_and_width([x1, y1], [x2, y2], line_width, index)
        # 2先对矩形4点按位于直线左右侧进行分组
        left_points = []
        right_points = []
        for rect_point in rect_points:
            if is_point_beside_line_left([x1, y1], [x2, y2], rect_point):
                left_points.append(rect_point)
            else:
                right_points.append(rect_point)
        # 3再根据点到p1距离对点排序
        if len(left_points) <= 0 or len(right_points) <= 0:
            print(index)
        else:
            if index <= 3:
                sort_points_by_distance(left_points, [x1, y1])
                sort_points_by_distance(right_points, [x1, y1])
                left_points_all.append(left_points[0])
                left_points_all.append(left_points[1])
                right_points_all.append(right_points[0])
                right_points_all.append(right_points[1])
            else:
                left_points_all.append(left_points[0])
                right_points_all.append(right_points[0])

        index = index + 2
    for point in left_points_all:
        final_poly_points.append(point)

    for point in right_points_all[::-1]:
        final_poly_points.append(point)

    return final_poly_points


# 判断位于直线同侧的两个点到直线的距离，并排序
def sort_points_by_distance(two_points, base_point):
    if cal_distance(two_points[0], base_point) > cal_distance(two_points[1], base_point):
        temp_point = two_points[0]
        two_points[0] = two_points[1]
        two_points[1] = temp_point


def cal_distance(point1, point2):
    return math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2))


# 根据斜率，基准点，线宽计算矩形4个角点
def generate_rect_with_lines_and_width(point0, point1, line_width, index):
    x0, y0, x1, y1 = point0[0], point0[1], point1[0], point1[1]
    if x0 == x1:
        n1 = n2 = y0
        m1 = x0 - line_width
        m2 = x0 + line_width
        n3 = n4 = y1
        m3 = x1 - line_width
        m4 = x1 + line_width
    elif y0 == y1:
        m1 = m2 = x0
        n1 = y0 - line_width
        n2 = y0 + line_width
        m3 = m4 = x1
        n3 = y1 - line_width
        n4 = y1 + line_width
    else:
        k = -(x1 - x0) / (y1 - y0)
        m1, n1, m2, n2 = cal_rect_corner_point(k, point0, line_width / 2)
        m3, n3, m4, n4 = cal_rect_corner_point(k, point1, line_width / 2)

    if index <= 3:
        rect_points = [[m1, n1], [m2, n2], [m3, n3], [m4, n4]]
    else:
        rect_points = [[m3, n3], [m4, n4]]
    return rect_points


# 根据斜率，基准点，线宽计算矩形2个角点
def cal_rect_corner_point(k, base_point, line_width):
    b = base_point[1] - k * base_point[0]
    x0, y0 = base_point[0], base_point[1]
    m1 = (k * (y0 - b) + x0) / (k * k + 1) + math.sqrt(
        ((k * (y0 - b) + x0) / (k * k + 1)) * ((k * (y0 - b) + x0) / (k * k + 1)) - (
                ((y0 - b) * (y0 - b) + x0 * x0 - line_width * line_width) / (k * k + 1)))
    n1 = k * m1 + b
    m2 = (k * (y0 - b) + x0) / (k * k + 1) - math.sqrt(
        ((k * (y0 - b) + x0) / (k * k + 1)) * ((k * (y0 - b) + x0) / (k * k + 1)) - (
                ((y0 - b) * (y0 - b) + x0 * x0 - line_width * line_width) / (k * k + 1)))
    n2 = k * m2 + b
    return m1, n1, m2, n2


# 判断点位于直线的左侧还是右侧
# 设线段端点为从 A(x1, y1)到 B(x2, y2), 线外一点 P(x0，y0)，
# 判断该点位于有向线 A→B 的那一侧。
# a = ( x2-x1, y2-y1)
# b = (x0-x1, y0-y1)
# a x b = | a | | b | sinφ (φ为两向量的夹角)
# | a | | b |  ≠ 0 时，  a x b  决定点 P的位置
# 所以  a x b  的 z 方向大小决定 P位置
# (x2-x1)(y0-y1) – (y2-y1)(x0-x1)  >  0   左侧
# (x2-x1)(y0-y1) – (y2-y1)(x0-x1)  <  0   右侧
# (x2-x1)(y0-y1) – (y2-y1)(x0-x1)  =  0   线段上
def is_point_beside_line_left(point1, point2, point):
    judge = (point2[0] - point1[0]) * (point[1] - point1[1]) - (point2[1] - point1[1]) * (point[0] - point1[0])
    if judge > 0:
        return True
    return False


def multy_process(xml_file):
    try:
        xml_name = os.path.split(xml_file)[-1]
        json_name = os.path.join(json_dir, str(os.path.splitext(xml_name)[0]) + '.json')
        image_name = str(os.path.splitext(xml_name)[0]) + '.jpg'

        if not os.path.isfile(os.path.join(jpg_dir, image_name)):
            return
        if os.path.isfile(json_name):
            return
        lines, file_name, image_height, image_width = parse_xml(os.path.join(xml_dir, xml_file))

        num = 0
        save2json(lines, image_height, image_width, json_name, image_name, jpg_dir, need_crop, crop_size, crop_json_dir,
                  crop_number, num)
        print('convert succeed : %s ,contain %d lines.' % (json_name, len(lines)))
    except:
        print('exception file : {}'.format(xml_file))


if __name__ == '__main__':
    files = [f for f in os.listdir(xml_dir) if isfile(os.path.join(xml_dir, f))]
    if not os.path.exists(json_dir):
        os.mkdir(json_dir)

    start = time.time()
    pool = Pool(16)
    pool.map(multy_process, files)
    pool.close()
    pool.join()
    end = time.time()
    print(end - start)

    # if not os.path.exists(json_dir):
    #     os.mkdir(json_dir)
    # for xml_file in files:
    #     xml_name = os.path.split(xml_file)[-1]
    #     json_name = os.path.join(json_dir, str(os.path.splitext(xml_name)[0]) + '.json')
    #     image_name = str(os.path.splitext(xml_name)[0]) + '.jpg'
    #
    #     if not os.path.isfile(os.path.join(jpg_dir, image_name)):
    #         continue
    #     if os.path.isfile(json_name):
    #         continue
    #     lines, file_name, image_height, image_width = parse_xml(os.path.join(xml_dir, xml_file))
    #
    #     num = 0
    #     save2json(lines, image_height, image_width, json_name, image_name, jpg_dir, need_crop, crop_size, crop_json_dir,
    #               crop_number, num)
    #     if num >= crop_number:
    #         break
    #     print('convert succeed : %s ,contain %d lines.' % (json_name, len(lines)))
