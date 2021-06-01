
import json
import io
import os

import os.path as osp

import PIL.Image

#import yaml

import base64

def b64_to_image(img_b64):
    f = io.BytesIO()
    f.write(base64.b64decode(img_b64))
    img = PIL.Image.open(f)
    return img

def class_crop_image(img, point_pos, size = 200):
    
    width, height = img.size
    
    x = point_pos[0]
    y = point_pos[1]

    crop_size = size / 2
    
    left_x = x - crop_size
    left_y = y - crop_size

    right_x = x + crop_size
    right_y = y + crop_size
    
    if(left_x - crop_size < 0):
        left_x = 0
    if(left_y - crop_size < 0):
        left_y = 0
    if(right_x + crop_size > width):
        right_x = width - 1
    if(right_y + crop_size > height):
        right_y = height - 1
    
    crop_img = img.crop((left_x, left_y, right_x, right_y))

    return crop_img

def json_to_dataset_class(json_path, out_path):

    json_file = json_path
    
    out_dir = out_path        

    if not osp.exists(out_dir):

        os.mkdir(out_dir)

    file_list = os.listdir(json_file)

    for i in range(0, len(file_list)):

        path = os.path.join(json_file, file_list[i])

        if os.path.isfile(path):

            data = json.load(open(path))

            if data['imageData']:

                imageData = data['imageData']

            else:
                print ("Can not get the image data in json file")
                imagePath = os.path.join(os.path.dirname(path), data['imagePath'])

                with open(imagePath, 'rb') as f:

                    imageData = f.read()

                    imageData = base64.b64encode(imageData).decode('utf-8')

            img = b64_to_image(imageData)

            crop_index = 0
            
            for shape in data['shapes']:
                points = shape['points']

                for kk in range(len(points)):
                    point = points[kk]
                    crop_image = class_crop_image(img, point)
                    
                    crop_index += 1
                    imgName = file_list[i].split(".")[0] + "_Crop_image_" + str(crop_index) + ".bmp"
                    #print (imgName)
                    img_path = os.path.join(out_dir, imgName)
                    crop_image.save(img_path)
                    print('Saved to: %s' % img_path)

# 示例
# 函数:json_to_dataset_class:将json文件中记录的矩形框,在原图上截取出小图，保存为训练class网所需要的样本
Json_path_class='K:\\shunmei_medical\\maofa\\json\\'#class网络的json文件(由集成通过人机交互提供)
sample_path_class="K:\\shunmei_medical\\json_out"   #根据json文件裁剪后的小图保存文件夹（由集成建立提共）
json_to_dataset_class(Json_path_class, sample_path_class)
