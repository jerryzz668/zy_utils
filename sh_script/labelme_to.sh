
basepath=$(cd `dirname $0`; pwd)
cd dependence

input_dir="$1"
coco_or_yolo="$2"
val_ratio=0.2

# coco_path
train2017=${input_dir%/*}"/coco/train2017"
val2017=${input_dir%/*}"/coco/val2017"
anno_train=${input_dir%/*}"/coco/annotations/instances_train2017.json"
anno_val=${input_dir%/*}"/coco/annotations/instances_val2017.json"


if [ -f ${input_dir%/*}"/yolo" ] & [ $coco_or_yolo == "yolo" ]; then
	rm -rf ${input_dir%/*}"/yolo"
elif [ -f ${input_dir%/*}"/coco" ] & [ $coco_or_yolo == "coco" ]; then
	rm -rf ${input_dir%/*}"/coco"
fi

if [ $coco_or_yolo == "yolo" ]; then
	python labelme_to_yolo.py $input_dir
	python split_train_val.py $input_dir $val_ratio $coco_or_yolo
elif [ $coco_or_yolo == "coco" ]; then	
	python split_train_val.py $input_dir $val_ratio $coco_or_yolo
	python labelme_to_coco.py $train2017 $input_dir $anno_train
	python labelme_to_coco.py $val2017 $input_dir $anno_val
fi

echo "Process finished!"
