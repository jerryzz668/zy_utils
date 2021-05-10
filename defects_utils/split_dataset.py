import random, glob, shutil
import os
from os.path import exists, join, basename

if __name__ == '__main__':
    root_dir     = "/home/kerry/mnt/mark/apple575/train_data/train_val_all/liewen_train"
    val_data_dir = '/home/kerry/mnt/mark/apple575/train_data/train_val_all/liewen_val'
    val_percent = 0.30

    if not exists(val_data_dir):
        os.mkdir(val_data_dir)

    source_img = glob.glob(join(root_dir, "*.jpg"))

    random.shuffle(source_img)
    val_num = int((1-val_percent) * len(source_img))

    for img in source_img[val_num: ]:

        name = basename(img)
        json = join(root_dir, name.split('.')[0] + '.json')
        txt  = join(root_dir, name.split('.')[0] + '.txt')

        shutil.move(img, val_data_dir)
        shutil.move(json, val_data_dir)
        shutil.move(txt, val_data_dir)
