
basepath=$(cd `dirname $0`; pwd)
preprocessing_path=${basepath%/*}"/preprocessing" # preprocessing_path
cd $preprocessing_path

input_dir="/home/jerry/Desktop/garbage/xxx"
val_ratio=0.2
coco_or_yolo="yolo"

images_train=${input_dir%/*}"/yolo/images/train"
images_val=${input_dir%/*}"/yolo/images/val"
labels_train=${input_dir%/*}"/yolo/labels/train/"
labels_val=${input_dir%/*}"/yolo/labels/val/"


python split_train_val.py $input_dir $val_ratio $coco_or_yolo
python labelme_to_yolo.py $images_train
python labelme_to_yolo.py $images_val
mv $images_train/*.txt $labels_train
mv $images_val/*.txt $labels_val
