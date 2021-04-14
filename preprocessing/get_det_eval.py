from tools.projects.microsoft_gj.microsoft_gj_global_var import VAL_JSON
import json
import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import itertools
import os

def calculate_inter_area(box1, box2):
    '''
    :param box1: Box对象
    :param box2: Box对象
    :return: box1与box2的相交面积
    '''
    left_x, left_y = max([box1.x, box2.x]), max([box1.y, box2.y])
    right_x, right_y = min([box1.x + box1.w, box2.x + box2.w]), \
                       min([box1.y + box1.h, box2.y + box2.h])
    height = right_y - left_y
    width = right_x - left_x
    area = height * width if height > 0 and width > 0 else 0
    return area

class Box:
    # x,y是左上角坐标
    def __init__(self, x, y, w, h, category=None, confidence=None):
        self.category = category
        self.confidence = confidence
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_area(self):
        return self.w * self.h

    def get_iou(self, box2):
        inter_area = calculate_inter_area(self, box2)
        return inter_area / (self.get_area() + box2.get_area() - inter_area)

def get_det_eval(y_true, y_pred, iou_thres=0.1, confidence_thres=0.25, is_Test=False, out_path=None):

    '''
    Args:
        y_true:  ground truth值，格式和y_pred完全一致，只是其score不会被用到，可以随便填一个值。
        y_pred:  检测模型产生的结果, 是一个3层的list。第1层是图片级别信息的集合；第2层是bbox级别信息的集合；
        第3层是单个bbox的结果，其格式为[x, y, w, h, score, class_id]。
        示例：[[], [[x, y, w, h, score, class_id], [x, y, w, h, score, class_id]], [], 
                [[x, y, w, h, score, class_id]]]。
        iou_thres:
        confidence_thres:
    returns:
        res: dict of metric results, includes total_gts, total_dts, miss_det, over_det, 
             miss_det_rate, over_det_rate
    '''
    total_gts, total_dts, over_det, miss_det = 0, 0, 0, 0
    # 标记检测结果对应标签
    gt_class = []
    pre_class = []
    # 标记每个缺陷的 id:name
    label_id_name = {}

    res = dict()
    new_y_pred = [[] for _ in y_pred]
    # 先统计 类别id-类别名称的对应
    if is_Test:
        with open(VAL_JSON, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            label_id_name = {i['id']: i['name'] for i in json_data["categories"]}
            print(label_id_name)
    for i, predict_img in enumerate(y_pred):
        for predict_box in predict_img:
            if predict_box[4] >= confidence_thres:
                new_y_pred[i].append(predict_box)
                total_dts += 1
    for img_file in range(len(y_true)):
        total_gts += len(y_true[img_file])
        necessary = False
        temp = []
        for obj in y_true[img_file]:
            x, y, w, h = obj[0], obj[1], obj[2], obj[3]
            gt_box = Box(x, y, w, h, obj[5])
            false_negative = True
            for i, predict_img in enumerate(new_y_pred[img_file]):
                predict_box = Box(predict_img[0], predict_img[1],
                                  predict_img[2], predict_img[3],
                                  predict_img[5], predict_img[4])
                if gt_box.get_iou(predict_box) > iou_thres:
                    if is_Test:
						gt_class.append(label_id_name[obj[5]])
						pre_class.append(label_id_name[predict_img[5]])
                    false_negative = False
                    temp.append(i)
            if false_negative:
                miss_det += 1
                if is_Test:
                    gt_class.append(label_id_name[obj[5]])
                    pre_class.append("z_lou_or_guo")
        for i, predict_img in enumerate(new_y_pred[img_file]):
            if i not in temp:
                over_det += 1
                if is_Test:
                        pre_class.append(label_id_name[predict_img[5]])
                        gt_class.append("z_lou_or_guo")
    res['total_gts'] = total_gts
    res['total_dts'] = total_dts
    res['miss_det'] = miss_det
    res['over_det'] = over_det
    res['miss_det_rate'] = miss_det / (total_gts if total_gts else 1)
    res['over_det_rate'] = over_det / (total_dts if total_dts else 1)
    if is_Test:
        cm, cm_pro = compute_confmx(gt_class, pre_class, out_path)
        return res, cm, cm_pro
    return res

def compute_confmx(gt_class, pre_class, out_path=None):
    classes = sorted(list(set(gt_class)), reverse=False)  # 类别排序
    cm = confusion_matrix(gt_class, pre_class, classes)  # 根据类别生成矩阵，此处不需要转置
    cm_pro = (cm.T / np.sum(cm, 1)).T
    # print('cm',cm)
    # print('cmp',cm_pro)
    conf_matrix_path = os.path.join(out_path, 'conf_matrix')
    plot_confusion_matrix(cm, classes, 'nums', "result_data", conf_matrix_path)
    plot_confusion_matrix(cm_pro, classes, 'pro', "result_data", conf_matrix_path, normalize=True)
    # print('confx',cm)
    return cm, cm_pro


def plot_confusion_matrix(cm, classes, title, title_png, out_path, normalize=False, cmap=plt.cm.Blues):
    # plt.figure()
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    plt.figure(figsize=(12, 8), dpi=120)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title('{}_{}'.format(title_png, title))
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90)
    plt.yticks(tick_marks, classes)

    # plt.axis("equal")
    ax = plt.gca()
    left, right = plt.xlim()
    ax.spines['left'].set_position(('data', left))
    ax.spines['right'].set_position(('data', right))
    for edge_i in ['top', 'bottom', 'right', 'left']:
        ax.spines[edge_i].set_edgecolor("white")

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        num = float('{:.2f}'.format(cm[i, j])) if normalize else int(cm[i, j])
        plt.text(j, i, num,
                 verticalalignment='center',
                 horizontalalignment="center",
                 color="white" if num > thresh else "black")
    plt.ylabel('ground turth')
    plt.xlabel('predict')
    plt.tight_layout()
    save_p = os.path.join(out_path, './{}_{}.png'.format(title_png, title))
    cm_txt = save_p.replace('.png', '.txt')
    with open(cm_txt, 'a+') as f:
        f.write('{}:\n'.format(title))
        f.write(str(cm))
        f.write('\n')
    # plt.savefig(save_p, transparent=True, dpi=800)
    plt.savefig(save_p, transparent=True, dpi=300)
    # plt.show()


if __name__ == '__main__':
    pass

