
sh_script=$(cd `dirname $0`; pwd)
dependence=$sh_script"/dependence"
cd $dependence

input_dir="$1"
coco_or_yolo="$2"
remain_bg="$3"
gen_mask="$4"
val_ratio=0.2

# coco_path
train2017=${input_dir%/*}"/coco/train2017"
val2017=${input_dir%/*}"/coco/val2017"
anno_train=${input_dir%/*}"/coco/annotations/instances_train2017.json"
anno_val=${input_dir%/*}"/coco/annotations/instances_val2017.json"
color_mask_train=${input_dir%/*}"/coco/stuffthingmaps/color_mask_train"
color_mask_val=${input_dir%/*}"/coco/stuffthingmaps/color_mask_val"
gray_mask_train=${input_dir%/*}"/coco/stuffthingmaps/train2017"
gray_mask_val=${input_dir%/*}"/coco/stuffthingmaps/val2017"


if [ -f ${input_dir%/*}"/yolo" ] & [ $coco_or_yolo == "yolo" ]; then
	rm -rf ${input_dir%/*}"/yolo"
elif [ -f ${input_dir%/*}"/coco" ] & [ $coco_or_yolo == "coco" ]; then
	rm -rf ${input_dir%/*}"/coco"
fi

if [ $coco_or_yolo == "yolo" ]; then
	python labelme_to_yolo.py $input_dir
	python split_train_val.py $input_dir $val_ratio $coco_or_yolo
elif [ $coco_or_yolo == "coco" ] & [ ! $remain_bg ]; then
	echo generating coco
	python split_train_val.py $input_dir $val_ratio $coco_or_yolo
	python labelme_to_coco.py $train2017 $input_dir $anno_train "nobg"
	python labelme_to_coco.py $val2017 $input_dir $anno_val "nobg"
elif [ $coco_or_yolo == "coco" ] & [ $remain_bg == "bg" ] & [ ! $gen_mask ]; then
	echo generating coco with bg
	python split_train_val.py $input_dir $val_ratio $coco_or_yolo
	python labelme_to_coco.py $train2017 $input_dir $anno_train $remain_bg
	python labelme_to_coco.py $val2017 $input_dir $anno_val $remain_bg
elif [ $coco_or_yolo == "coco" ] & [ $remain_bg == "bg" ] & [ $gen_mask == "mask" ]; then	
	echo generating coco with bg and mask
	python split_train_val.py $input_dir $val_ratio $coco_or_yolo
	python labelme_to_coco.py $train2017 $input_dir $anno_train $remain_bg
	python labelme_to_coco.py $val2017 $input_dir $anno_val $remain_bg
	python tomask_label.py $train2017 $input_dir $color_mask_train $gray_mask_train
	python tomask_label.py $val2017 $input_dir $color_mask_val $gray_mask_val
	rm -rf $color_mask_train
	rm -rf $color_mask_val
	rm -rf ${input_dir%/*}"/coco/stuffthingmaps/empty_json"
fi

echo "Process finished!"
