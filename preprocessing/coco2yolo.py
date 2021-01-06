import json
from collections import defaultdict
import os


"""hyper parameters"""
json_file_path = '/Users/zhangyan/Desktop/instances_val2017.json'
# images_dir_path = 'E:/shixi/output/cemian_cut'
output_path = '/Users/zhangyan/Desktop/txt/'

if not os.path.exists(output_path):
    os.makedirs(output_path)

"""load json file"""
name_box_id = defaultdict(list)
id_name = dict()
with open(json_file_path, encoding='utf-8') as f:
    data = json.load(f)
    annotations = data['annotations']
    imgs = data['images']


for ant in annotations:
    image_id = ant['image_id']
    # name = '%04d.jpg' % id
    name = imgs[image_id - 1]['file_name']
    cat = ant['category_id']

    if cat >= 1 and cat <= 11:
        cat = cat - 1
    elif cat >= 13 and cat <= 25:
        cat = cat - 2
    elif cat >= 27 and cat <= 28:
        cat = cat - 3
    elif cat >= 31 and cat <= 44:
        cat = cat - 5
    elif cat >= 46 and cat <= 65:
        cat = cat - 6
    elif cat == 67:
        cat = cat - 7
    elif cat == 70:
        cat = cat - 9
    elif cat >= 72 and cat <= 82:
        cat = cat - 10
    elif cat >= 84 and cat <= 90:
        cat = cat - 11

    name_box_id[name].append([ant['bbox'], cat])
    # name_box_id[name].append([ant['bbox'], 0])

# with open(output_path, 'w') as f:
#     for key in name_box_id.keys():
#         # f.write(key)
#         box_infos = name_box_id[key]
#         for info in box_infos:
#             x_min = int(info[0][0])
#             y_min = int(info[0][1])
#             x_max = x_min + int(info[0][2])
#             y_max = y_min + int(info[0][3])
#
#             box_info = " %d,%d,%d,%d,%d" % (
#                 int(info[1]), x_min, y_min, x_max, y_max)
#             f.write(box_info)
#         f.write('\n')

"""write to txt"""
for key in name_box_id.keys():
    file_name = key[:-4] + '.txt'
    f = open(output_path + file_name, 'w')
    box_infos = name_box_id[key]

    for info in box_infos:
        x_min = int(info[0][0])
        y_min = int(info[0][1])
        x_max = x_min + int(info[0][2])
        y_max = y_min + int(info[0][3])
        x_mid = (x_min + x_max)/2
        y_mid = (y_min + y_max)/2

        box_info = " %d %.03f %.03f %.03f %.03f" % (
            int(info[1]), x_mid/512, y_mid/512, int(info[0][2])/512, int(info[0][3])/512)
        # box_info = " %d %d %d %d %d" % (int(info[1]), x_min, y_min, x_max, y_max)
        f.write(box_info)
        f.write('\n')


