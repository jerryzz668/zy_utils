"""
@Description:
@Author     : zhangyan
@Time       : 2021/7/21 下午4:15
"""

from preprocessing.zy_utils import *
from PR_results import txt_to_dataframe

gt_txt_path = '/home/jerry/Documents/Micro_AD/0425_yolo/yolo/labels/val'
yolo_project = '/home/jerry/Documents/yolov5-5.0'
cls_yaml_dir = '/home/jerry/Documents/yolov5-5.0/data/loushi.yaml'

iou = [0.3, 0.8, 2]
conf = [0.3, 0.8, 2]
grid = grid_search(iou, conf)
print(grid)

iou_conf_arr = []
for [iou, conf] in grid:
    os.system('python {} --iou-thres {} --conf-thres {} --save-txt --save-conf --nosave --name {}'.format(os.path.join(yolo_project, 'detect.py'), iou, conf, 'grid'))
    df = txt_to_dataframe(gt_txt_path, os.path.join(yolo_project, 'runs/detect/grid'), cls_yaml_dir, iou)
    PR_total = np.array(df.iloc[-1, 1:])
    print('PR_total',PR_total)
    iou_conf = np.array([iou, conf])
    line_content = np.concatenate((iou_conf, PR_total)).tolist()
    iou_conf_arr.append(line_content)
    print(line_content)

df_iou_conf = pd.DataFrame(iou_conf_arr)
df_iou_conf.columns = ['iou', 'conf', 'gt', 'missing', 'over_detect']
sorted_df_iou_conf = df_iou_conf.sort_values('missing', ascending=True)
print(sorted_df_iou_conf)

