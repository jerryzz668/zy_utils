import argparse
import base64
import json
import os
import os.path as osp
import io
import numpy as np
import PIL.ImageDraw
import PIL.Image
import yaml

# from labelme.logger import logger
# from labelme import utils

def label_colormap(N=256):

    def bitget(byteval, idx):
        return ((byteval & (1 << idx)) != 0)

    cmap = np.zeros((N, 3))
    for i in range(0, N):
        id = i
        r, g, b = 0, 0, 0
        for j in range(0, 8):
            r = np.bitwise_or(r, (bitget(id, 0) << 7 - j))
            g = np.bitwise_or(g, (bitget(id, 1) << 7 - j))
            b = np.bitwise_or(b, (bitget(id, 2) << 7 - j))
            id = (id >> 3)
        cmap[i, 0] = r
        cmap[i, 1] = g
        cmap[i, 2] = b
    cmap = cmap.astype(np.float32) / 255
    return cmap

def img_b64_to_arr(img_b64):
    f = io.BytesIO()
    f.write(base64.b64decode(img_b64))
    im=PIL.Image.open(f)
    img_arr = np.array(im)
    return img_arr

def shape_to_mask_Multiple(img_shape, points, shape_type=None,
                  line_width=10, point_size=5):
    mask = np.zeros(img_shape[:2], dtype=np.uint8)
    mask = PIL.Image.fromarray(mask)
    draw = PIL.ImageDraw.Draw(mask)
    xy = [tuple(point) for point in points]
    if shape_type == 'circle':
        assert len(xy) == 2, 'Shape of shape_type=circle must have 2 points'
        (cx, cy), (px, py) = xy
        d = math.sqrt((cx - px) ** 2 + (cy - py) ** 2)
        draw.ellipse([cx - d, cy - d, cx + d, cy + d], outline=1, fill=1)
    elif shape_type == 'rectangle':
        assert len(xy) == 2, 'Shape of shape_type=rectangle must have 2 points'
        draw.rectangle(xy, outline=1, fill=1)
    elif shape_type == 'line':
        assert len(xy) == 2, 'Shape of shape_type=line must have 2 points'
        draw.line(xy=xy, fill=1, width=line_width)
    elif shape_type == 'linestrip':
        draw.line(xy=xy, fill=1, width=line_width)
    elif shape_type == 'point':
        assert len(xy) == 1, 'Shape of shape_type=point must have 1 points'
        cx, cy = xy[0]
        r = point_size
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=1, fill=1)
    else:
        assert len(xy) > 2, 'Polygon must have points more than 2'
        draw.polygon(xy=xy, outline=1, fill=1)
    mask = np.array(mask, dtype=bool)
    return mask

def shapes_to_label_Multiple(img_shape, shapes, label_name_to_value, type='class'):
    assert type in ['class', 'instance']

    cls = np.zeros(img_shape[:2], dtype=np.int32)
    if type == 'instance':
        ins = np.zeros(img_shape[:2], dtype=np.int32)
        instance_names = ['_background_']
    for shape in shapes:
        points = shape['points']
        label = shape['label']
        shape_type = shape.get('shape_type', None)
        if type == 'class':
            cls_name = label
        elif type == 'instance':
            cls_name = label.split('-')[0]
            if label not in instance_names:
                instance_names.append(label)
            ins_id = instance_names.index(label)
        cls_id = label_name_to_value[cls_name]
        mask = shape_to_mask_Multiple(img_shape[:2], points, shape_type)
        cls[mask] = cls_id
        if type == 'instance':
            ins[mask] = ins_id

    if type == 'instance':
        return cls, ins
    return cls


def lblsave_Multiple(filename, lbl):
    if osp.splitext(filename)[1] != '.bmp':
        filename += '.bmp'
    # Assume label ranses [-1, 254] for int32,
    # and [0, 255] for uint8 as VOC.
    # print("lbl",np.unique(lbl))
    if lbl.min() >= -1 and lbl.max() < 255:
        # lbl_pil = PIL.Image.fromarray(lbl.astype(np.uint8), mode='P')
        lbl_pil = PIL.Image.fromarray(lbl.astype(np.uint8), mode='L')
        # colormap = label_colormap(255)
        # lbl_pil.putpalette((colormap * 255).astype(np.uint8).flatten())

        lbl_pil.save(filename)
    else:
        raise ValueError(
            '[%s] Cannot save the pixel-wise class label as PNG. '
            'Please consider using the .npy format.' % filename
        )

def json2img_Multiple(name_json,dir_img,dir_label):
    # logger.warning('This script is aimed to demonstrate how to convert the'
    #                'JSON file to a single image dataset, and not to handle'
    #                'multiple JSON files to generate a real-use dataset.')
                
    json_file=name_json

    # count = os.listdir(json_file) 
    # for i in range(0, len(count)):

    #     path = os.path.join(json_file, count[i])

    #     if os.path.isfile(path):

    data = json.load(open(json_file))

    if data['imageData']:
        imageData = data['imageData']
    else:
        imagePath = os.path.join(os.path.dirname(json_file), data['imagePath'])
        with open(imagePath, 'rb') as f:
            imageData = f.read()
            imageData = base64.b64encode(imageData).decode('utf-8')
    img = img_b64_to_arr(imageData)

    label_name_to_value = {'_background_': 0}
    for shape in sorted(data['shapes'], key=lambda x: x['label']):
        label_name = shape['label']
        # print("label_name",label_name)
        # print("label_name.type",type(label_name))

        # print(int(label_name))
        if label_name in label_name_to_value:
            label_value = label_name_to_value[label_name]
            # print("label_value",label_value)
        else:
            # label_value = len(label_name_to_value)
            label_value=int(label_name)
            a=1
            label_value=label_value+1
            # print(type(label_value))
            label_name_to_value[label_name] = label_value
            # print("label_value2",label_value)
    # print("label_name_to_value",list(label_name_to_value))
    # print("label_name_to_value:{}".format(list(label_name_to_value)))
    lbl = shapes_to_label_Multiple(img.shape, data['shapes'], label_name_to_value)
    # print("lbl",lbl)
    # print("label_name_to_value.values()",(label_name_to_value.values()))
    label_names = [None] * (len(label_name_to_value.values()))
    # # label_names = [None] * (max(label_name_to_value.values()) + 1)
    # # print("len(label_name_to_value.values()",len(label_name_to_value.values()))
    # print("len(label_name_to_value.values()2=",[None]*(len(label_name_to_value.values())))
    # i=0
    # print("i:",i)
    # print("label_name_to_value",list(label_name_to_value.items()))
    # for name, value in label_name_to_value.items():
        
    #     print("name",name)
    #     print("value",value)
    #     label_names[i] = name
    #     print("i:",i)
    #     i=i+1
        

    # lbl_viz = utils.draw_label(lbl, img, label_names)
    # out_dir = osp.basename(count[i]).replace('.', '_')

    # out_dir = osp.join(osp.dirname(count[i]), out_dir)

    # if not osp.exists(out_dir):

    #     os.mkdir(out_dir)

    saved_name = os.path.splitext(os.path.basename(json_file))[0]+'.bmp'
    PIL.Image.fromarray(img).save(osp.join(dir_img, saved_name))
    lblsave_Multiple(osp.join(dir_label, saved_name), lbl)
    # PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, 'label_viz.png'))
    # print("label_names:",list(label_names))
    # with open(osp.join(out_dir, 'label_names.txt'), 'w') as f:
    #     for lbl_name in label_names:
    #         print("lbl_name:",type(lbl_name))
    #         f.write(lbl_name + '\n')

    # logger.warning('info.yaml is being replaced by label_names.txt')
    # info = dict(label_names=label_names)
    # with open(osp.join(out_dir, 'info.yaml'), 'w') as f:
    #     yaml.safe_dump(info, f, default_flow_style=False)

    # logger.info('Saved to: {}'.format(out_dir))


# if __name__ == '__main__':
#     main()
# json2img(name_json,dir_img,dir_label)

def json_to_dataset_seg(Fs_Root_path,dir_json):
    train_seg_path=Fs_Root_path+"\\train_seg"
    if not osp.exists(train_seg_path):
        os.mkdir(train_seg_path)
    out_image_path=train_seg_path+"\\image_test"
    if not osp.exists(out_image_path):
        os.mkdir(out_image_path)
    out_label_path=train_seg_path+"\\label_test"
    if not osp.exists(out_label_path):
       os.mkdir(out_label_path)
    print(out_image_path)
    count = os.listdir(dir_json) 
    for i in range(0, len(count)):
        path = os.path.join(dir_json, count[i])
        print("path",path)
        if os.path.isfile(path):
            json2img_Multiple(path,out_image_path,out_label_path)


#使用示例
Fs_Root_path='D:\\test'#根目录
Json_path_seg='C:\\Users\\fs\\Desktop\\t\\png'#分割网Json文件夹路径
json_to_dataset_seg(Fs_Root_path,Json_path_seg)