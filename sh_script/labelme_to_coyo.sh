
basepath=$(cd `dirname $0`; pwd)
cd dependence

input_dir="$1"
coco_or_yolo="$2"
val_ratio=0.2

# yolo_path
images_train=${input_dir%/*}"/yolo/images/train"
images_val=${input_dir%/*}"/yolo/images/val"
labels_train=${input_dir%/*}"/yolo/labels/train/"
labels_val=${input_dir%/*}"/yolo/labels/val/"

# coco_path
train2017=${input_dir%/*}"/coco/train2017"
val2017=${input_dir%/*}"/coco/val2017"
annotations=${input_dir%/*}"/coco/annotations/"
anno_train=${input_dir%/*}"/coco/annotations/instances_train2017.json"
anno_val=${input_dir%/*}"/coco/annotations/instances_val2017.json"

if (( $coco_or_yolo == `ls ${input_dir%/*} | grep yolo` )); then
	rm -rf ${input_dir%/*}"/yolo"
elif (( $coco_or_yolo == `ls ${input_dir%/*} | grep coco` )); then
	rm -rf ${input_dir%/*}"/coco"
fi

if [ $coco_or_yolo == "yolo" ]
then
	python labelme_to_yolo.py $input_dir
	python split_train_val.py $input_dir $val_ratio $coco_or_yolo
else	
	python split_train_val.py $input_dir $val_ratio $coco_or_yolo
	python labelme_to_coco.py $train2017 $input_dir $anno_train
	python labelme_to_coco.py $val2017 $input_dir $anno_val
fi

echo "Process finished!"
