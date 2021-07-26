import os
import random
import shutil

trainval_percent = 1  # 0.95
train_percent = 0.8

labelfilepath = '/Users/zhangyan/Desktop/crops'  # 输入所有二分类txt文件夹
imgfilepath = labelfilepath  # 输入二分类图片文件夹
output_path = '/Users/zhangyan/Desktop/split_train_val'  # 输出训练、验证和测试txt和图片文件夹

if os.path.exists(output_path):
    shutil.rmtree(output_path)
os.makedirs(output_path)
os.makedirs('{}/images/train'.format(output_path))
os.makedirs('{}/images/val'.format(output_path))
os.makedirs('{}/images/test'.format(output_path))
os.makedirs('{}/labels/train'.format(output_path))
os.makedirs('{}/labels/val'.format(output_path))
os.makedirs('{}/labels/test'.format(output_path))

total = os.listdir(imgfilepath)
total_img = []
for tl in total:
    if tl.endswith('.jpg') and tl[0] != '.':
        print(tl)
        total_img.append(tl)

num = len(total_img)
list = range(num)
tv = int(num*trainval_percent)
tr = int(tv*train_percent)
trainval = random.sample(list,tv)
train = random.sample(trainval,tr)

for i in list:
    if i in trainval:
        if i in train:
            j = os.path.join(labelfilepath, total_img[i].replace('.jpg', '.json'))
            shutil.copy(j, '{}/labels/train'.format(output_path))
            jj = os.path.join(imgfilepath, total_img[i])
            shutil.copy(jj, '{}/images/train'.format(output_path))
        else:
            j = os.path.join(labelfilepath, total_img[i].replace('.jpg', '.json'))
            shutil.copy(j, '{}/labels/val'.format(output_path))
            jj = os.path.join(imgfilepath, total_img[i])
            shutil.copy(jj,'{}/images/val'.format(output_path))
    else:
        j = os.path.join(labelfilepath, total_img[i].replace('.jpg', '.json'))
        shutil.copy(j, '{}/labels/test'.format(output_path))
        jj = os.path.join(imgfilepath, total_img[i])
        shutil.copy(jj, '{}/images/test'.format(output_path))
print('Well Done！！！')

