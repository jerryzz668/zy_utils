
basepath=$(cd `dirname $0`; pwd)
preprocessing_path=${basepath%/*}"/preprocessing" # preprocessing_path
cd $preprocessing_path

input_dir="$1"
val_ratio=0.2
coco_or_yolo="$2"

#input_dir="/home/jerry/Desktop/garbage/xxx"
#val_ratio=0.2
#coco_or_yolo="coco"

# yolo_path
images_train=${input_dir%/*}"/yolo/images/train"
images_val=${input_dir%/*}"/yolo/images/val"
labels_train=${input_dir%/*}"/yolo/labels/train/"
labels_val=${input_dir%/*}"/yolo/labels/val/"

# coco_path
train2017=${input_dir%/*}"/coco/train2017"
val2017=${input_dir%/*}"/coco/val2017"
annotations=${input_dir%/*}"/coco/annotations/"
coco_path=${input_dir%/*}"/coco/coco.json"

if [ $coco_or_yolo == "yolo" ]
then
	python split_train_val.py $input_dir $val_ratio $coco_or_yolo
	python labelme_to_yolo.py $images_train
	python labelme_to_yolo.py $images_val
	mv $images_train/*.txt $labels_train
	mv $images_val/*.txt $labels_val
else	
	python split_train_val.py $input_dir $val_ratio $coco_or_yolo
	python labelme_to_coco.py $train2017
	mv $coco_path $annotations"instances_train2017.json"
	python labelme_to_coco.py $val2017
	mv $coco_path $annotations
	python modify_coco_cate.py $annotations"instances_train2017.json" $annotations"coco.json"
	mv $annotations"modified_coco.json" $annotations"instances_val2017.json"
	rm $annotations"coco.json"

	echo "converted"
fi
