This is a family of object detection and segmentation utils, such as, mmdetection, yolov5, yolox and other image processing utils. It is suitable for project.

### Quick Start Examples

---

```shell
$ git clone https://gitee.com/jerryzz668/zy_utils.git
$ cd zy_utils
$ python setup.py develop
```
### Convert to yolo

---
First, prepare images and corresponding jsons in one folder,then
```shell
bash sh_script/labelme_to.sh path_to_input_folder yolo
```
### Convert to coco

---
Convert to coco without background and mask, you can run as follows:
```shell
bash sh_script/labelme_to.sh path_to_input_folder coco
```
Convert to coco with background and without mask, you can run as follows:
```shell
bash sh_script/labelme_to.sh path_to_input_folder coco bg
```
Convert to coco with background and mask, you can run as follows:
```shell
bash sh_script/labelme_to.sh path_to_input_folder coco bg mask
```