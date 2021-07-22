"""
@Description:
@Author     : zhangyan
@Time       : 2021/7/21 下午4:15
"""

from preprocessing.zy_utils import *
from PR_results import txt_to_dataframe

def search_best_iouconf(gt_txt_path, source, cls_yaml_dir, weights, yolo_project, img_size, iou, conf):
    detect_py = os.path.join(yolo_project, 'detect.py')  # detect.py path
    grid = grid_search(iou, conf)  # grid search results

    exp_grid = os.path.join(yolo_project, 'runs/detect/grid')  # detect结果路径
    iou_conf_arr = []
    for [iou, conf] in grid:  # 循环生成不同iou和conf的 missing and over_detect
        try:
            shutil.rmtree(exp_grid)
        except:
            print('no_grid_file')
        os.system('python {} --weights {} --source {} --img-size {} --iou-thres {} --conf-thres {} --save-txt --save-conf --nosave --name {}'.format(detect_py, weights, source, img_size, iou, conf, exp_grid))
        df = txt_to_dataframe(gt_txt_path, os.path.join(yolo_project, 'runs/detect/grid/labels'), cls_yaml_dir, iou)
        PR_total = np.floor(np.array(df.iloc[-1, 1:]))
        iou_conf = np.array([iou, conf])
        line_content = np.concatenate((iou_conf, PR_total)).tolist()
        iou_conf_arr.append(line_content)
        print(line_content)
    shutil.rmtree(exp_grid)

    df_iou_conf = pd.DataFrame(iou_conf_arr)
    df_iou_conf.columns = ['iou', 'conf', 'gt', 'missing', 'over_detect']
    sorted_df_iou_conf = df_iou_conf.sort_values('missing', ascending=True)
    print(sorted_df_iou_conf)
    return sorted_df_iou_conf

if __name__ == '__main__':
    source = '/home/jerry/Documents/Micro_AD/0425_yolo/yolo/images/val'  # 需推理的图像路径
    gt_txt_path = '/home/jerry/Documents/Micro_AD/0425_yolo/yolo/labels/val'  # 需推理图像的标注_txt格式
    weights = '/home/jerry/Documents/yolov5-5.0/runs/train/exp13/weights/best.pt'  # 训练好的模型
    cls_yaml_dir = '/home/jerry/Documents/yolov5-5.0/data/loushi.yaml'  # yaml
    yolo_project = '/home/jerry/Documents/yolov5-5.0'  # yolo项目路径
    img_size = 512  # 测试图像大小
    iou = [0.3, 0.8, 10]  # grid_search 范围 【start, stop, step】
    conf = [0.3, 0.8, 10]  # grid_search 范围 【start, stop, step】

    search_best_iouconf(gt_txt_path, source, cls_yaml_dir, weights, yolo_project, img_size, iou, conf)


