
import base64
import json
import os
import os.path as osp
import io
import PIL.Image
import PIL.ImageDraw
import yaml
import numpy as np
import cv2
import random
import time 

def shape_to_mask(img_shape, points, shape_type=None,
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


def img_b64_to_arr(img_b64):
    f = io.BytesIO()
    f.write(base64.b64decode(img_b64))
    im=PIL.Image.open(f)
    img_arr = np.array(im)
    return img_arr


def shapes_to_label(img_shape, shapes, label_name_to_value, type='class'):
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
        mask = shape_to_mask(img_shape[:2], points, shape_type)
        cls[mask] = cls_id
        if type == 'instance':
            ins[mask] = ins_id

    if type == 'instance':
        return cls, ins
    return cls


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


def _validate_colormap(colormap, n_labels):
    if colormap is None:
        colormap = label_colormap(n_labels)
    else:
        assert colormap.shape == (colormap.shape[0], 3), \
            'colormap must be sequence of RGB values'
        assert 0 <= colormap.min() and colormap.max() <= 1, \
            'colormap must ranges 0 to 1'
    return colormap


# similar function as skimage.color.label2rgb
def label2rgb(
    lbl, img=None, n_labels=None, alpha=0.5, thresh_suppress=0, colormap=None,):
    if n_labels is None:
        n_labels = len(np.unique(lbl))

    colormap = _validate_colormap(colormap, n_labels)
    colormap = (colormap * 255).astype(np.uint8)

    lbl_viz = colormap[lbl]
    lbl_viz[lbl == -1] = (0, 0, 0)  # unlabeled

    if img is not None:
        img_gray = PIL.Image.fromarray(img).convert('LA')
        img_gray = np.asarray(img_gray.convert('RGB'))
        # img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # img_gray = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
        lbl_viz = alpha * lbl_viz + (1 - alpha) * img_gray
        lbl_viz = lbl_viz.astype(np.uint8)

    return lbl_viz



def draw_label(label, img=None, label_names=None, colormap=None, **kwargs):
    """Draw pixel-wise label with colorization and label names.
    label: ndarray, (H, W)
        Pixel-wise labels to colorize.
    img: ndarray, (H, W, 3), optional
        Image on which the colorized label will be drawn.
    label_names: iterable
        List of label names.
    """
    import matplotlib.pyplot as plt

    backend_org = plt.rcParams['backend']
    plt.switch_backend('agg')

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0,
                        wspace=0, hspace=0)
    plt.margins(0, 0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    if label_names is None:
        label_names = [str(l) for l in range(label.max() + 1)]

    colormap = _validate_colormap(colormap, len(label_names))

    label_viz = label2rgb(
        label, img, n_labels=len(label_names), colormap=colormap, **kwargs
    )
    plt.imshow(label_viz)
    plt.axis('off')

    plt_handlers = []
    plt_titles = []
    for label_value, label_name in enumerate(label_names):
        if label_value not in label:
            continue
        fc = colormap[label_value]
        p = plt.Rectangle((0, 0), 1, 1, fc=fc)
        plt_handlers.append(p)
        plt_titles.append('{value}: {name}'
                          .format(value=label_value, name=label_name))
    plt.legend(plt_handlers, plt_titles, loc='lower right', framealpha=.5)

    f = io.BytesIO()
    plt.savefig(f, bbox_inches='tight', pad_inches=0)
    plt.cla()
    plt.close()

    plt.switch_backend(backend_org)

    out_size = (label_viz.shape[1], label_viz.shape[0])
    out = PIL.Image.open(f).resize(out_size, PIL.Image.BILINEAR).convert('RGB')
    out = np.asarray(out)
    return out





def lblsave(filename, lbl):
    if osp.splitext(filename)[1] != '.png':
        filename += '.png'
    # Assume label ranses [-1, 254] for int32,
    # and [0, 255] for uint8 as VOC.
    if lbl.min() >= -1 and lbl.max() < 255:
        lbl_pil = PIL.Image.fromarray(lbl.astype(np.uint8), mode='P')
        colormap = label_colormap(255)
        lbl_pil.putpalette((colormap * 255).astype(np.uint8).flatten())
        lbl_pil.save(filename)
    else:
        raise ValueError(
            '[%s] Cannot save the pixel-wise class label as PNG. '
            'Please consider using the .npy format.' % filename
        )


def json2img(name_json,dir_img,dir_label):

    #json_file = r'C:\Users\xinghe.zhou\Desktop\5005预处理后图像\横\json\D43-005_2-1.json'
    json_file = name_json

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
        if label_name in label_name_to_value:
            label_value = label_name_to_value[label_name]
        else:
            label_value = len(label_name_to_value)
            label_name_to_value[label_name] = label_value
    lbl = shapes_to_label(img.shape, data['shapes'], label_name_to_value)

    label_names = [None] * (max(label_name_to_value.values()) + 1)
    for name, value in label_name_to_value.items():
        label_names[value] = name
    lbl_viz = draw_label(lbl, img, label_names)
    saved_name = os.path.splitext(os.path.basename(json_file))[0]+'.png'
    #lblsave(osp.join('C:\\Users\\xinghe.zhou\\Desktop\\', saved_name), lbl)
    lblsave(osp.join(dir_label, saved_name), lbl)
    PIL.Image.fromarray(img).save(osp.join(dir_img, saved_name))


def json2imgscale(dir_json,dir_img,dir_label):

    count = os.listdir(dir_json) 
    for i in range(0, len(count)):
        path = os.path.join(dir_json, count[i])
        if os.path.isfile(path):
            json2img(path,dir_img,dir_label)
    print('完成分类和转换')
    






def readImage(img_dir, lable_dir, path, labelPath):

    img_path = os.path.join(img_dir, path)
    #print (img_path)

    img = cv2.imread(img_path)
    
    label_path = os.path.join(lable_dir, labelPath)
    #print (label_path)
    
    labelImg = cv2.imread(label_path)
   
    return img, labelImg

def randomCrop(threshold, img, labelImg): 
    start3 = time.clock()
    while True:
        random_x = random.randint(0, img.shape[1]-259)
        random_y = random.randint(0, img.shape[0]-259)
        patch = img[random_y:random_y+256, random_x:random_x+256, :]
        labelpatch = labelImg[random_y:random_y+256, random_x:random_x+256, :]
        end3 = time.clock()
        flag=1
    
        if (end3-start3)>2:
            flag=0
            return flag,patch, labelpatch
        if np.sum(labelpatch[:,:,2] > 0) < threshold:
            continue

        else:
            return flag,patch, labelpatch

def writeImage(img, label, outlittleImagePath, outlittleLabelPath, imgName, labelName):
    
        cv2.imwrite(os.path.join(outlittleImagePath, imgName), img)
   
        cv2.imwrite(os.path.join(outlittleLabelPath, labelName), label)

def function(ImgDataDir, Datalabel,outlittleImagePath, outlittleLabelPath):

    
    threshold = 40
    
    patchPerImg = 10
    
    imgFiles = sorted(os.listdir(ImgDataDir))
    #print(len(ImgDataDir))
    
    labelFiles = sorted(os.listdir(Datalabel))
    #print(len(Datalabel))
   
    for imgPath, labelPath in zip(imgFiles, labelFiles):
       
        img, label = readImage(ImgDataDir, Datalabel, imgPath, labelPath)
        
        for t in range(patchPerImg):
          
            print('processing ...:', imgPath)
           
            flag,patch_img, patch_label = randomCrop(threshold, img, label)
          
            if flag==0:
              
                continue
           
            patch_img_name = imgPath.split('.')[0]+str(t)+'.bmp'
           
            patch_label_name = labelPath.split('.')[0] + str(t) + '.bmp'
           
            writeImage(patch_img, patch_label, outlittleImagePath, outlittleLabelPath, patch_img_name, patch_label_name)

def main():
    json2imgscale('C:\\Users\\freesense\\Desktop\\json','C:\\Users\\freesense\\Desktop\\bmp','C:\\Users\\freesense\\Desktop\\graypng')
    
    function('C:\\Users\\freesense\\Desktop\\bmp','C:\\Users\\freesense\\Desktop\\graypng','C:\\Users\\freesense\\Desktop\\littlebmp','C:\\Users\\freesense\\Desktop\\littlegraypng')


main()