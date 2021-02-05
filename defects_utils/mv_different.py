import glob
import os
from shutil import copyfile


if __name__ == "__main__":

    sourcepath  = '/home/kerry/mnt/mark/apple575/train_data/train_val/1221/label_575_1221_neg/'
    valpath     = '/home/kerry/mnt/mark/apple575/train_data/train_val/1221/label_575_1221_neg_val/'
    trainpath   = '/home/kerry/mnt/mark/apple575/train_data/train_val/1221/label_575_1221_neg_train/'

    if not os.path.exists(trainpath):
        os.makedirs(trainpath)

    val_list    = glob.glob(valpath + "*.json")
    valname_list = []
    for _ in val_list:
        valname_list.append(os.path.basename(_))
    source_list = glob.glob(sourcepath + "*.json")

    for jsonfrom in source_list:
        json_name = os.path.basename(jsonfrom)

        if json_name not in valname_list:

            print(jsonfrom)
            img_name = os.path.basename(jsonfrom).split('.')[0]+'.jpg'
            imgfrom = os.path.join(sourcepath, img_name)
            jsonto = os.path.join(trainpath, json_name)
            imgto = os.path.join(trainpath, img_name)

            copyfile(imgfrom, imgto)
            copyfile(jsonfrom, jsonto)


