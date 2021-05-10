import copy
from concurrent.futures.thread import ThreadPoolExecutor
from img_slice_utils import *
import datetime
# dict_label=['bai', 'hongliang', 'hongmie', 'huangliang', 'huangmie', 'luliang', 'lumie']

def imgs_crop_and_fill(img_folder_path, crop_stategy, output_path='outputs', empty_check=True, num_worker=8, iou_thres=0.2):
    '''
    :param img_folder_path: 图片文件夹绝对路径
    :param crop_stategy: 截取策略
    :param empty_check: 是否检查空截框
    :param num_worker: 线程数
    :param output_path: 保存路径
    :param iou_thres: 截图时iou阈值
    :return: 整个文件夹下的图片截图和填充
    '''
    thread_pool = ThreadPoolExecutor(max_workers=num_worker)
    print('Thread Pool is created!')
    # 检查输出路径文件夹是否存在
    if not os.path.exists(output_path): os.makedirs(output_path)
    for img_name in os.listdir(img_folder_path):
        img_file_path = os.path.join(img_folder_path, img_name)
        # 过滤文件夹和非图片文件
        if not os.path.isfile(img_file_path) or img_name[img_name.rindex('.')+1:] not in IMG_TYPES: continue
        thread_pool.submit(img_crop_and_fill, img_file_path, crop_stategy, output_path, empty_check, iou_thres)
    thread_pool.shutdown(wait=True)

# 单张图片的截图和填充，用来作为多线程的输入方法
def img_crop_and_fill(img_file_path, crop_strategy, output_path, empty_check, iou_thres):
    img = cv2.imread(img_file_path)
    try:
        instance = json_to_instance(img_file_path[:img_file_path.rindex('.')]+'.json')
    except FileNotFoundError:
        # 有些图片没有对应的json文件，或表示该图片无目标
        print('\033[1;33m%s has no json file...\033[0m' % (img_file_path))
        instance = create_empty_json_instance(img_file_path)
    instance_clean(instance)
    instance_points_to_polygon(instance)
    crops = crop_strategy(img, instance)
    for crop in crops:
        crop_size, fill_size = crop[0], crop[1]
        try:
            init_crop_and_fill(img, instance, crop_size, fill_size, output_path, empty_check, iou_thres)
        except Exception as e:
            # 有些图片crop报错需要log
            print('\033[1;31m%s fails in cropping %s, due to %s.\033[0m' % (img_file_path, crop_size, e.with_traceback()))

# 单张图片的截图和填充，要求输入已经读取的img和json instance
def init_crop_and_fill(img, instance, crop_size, fill_size, output_path, empty_check, iou_thres):
    if empty_check and crop_is_empty(instance, crop_size, iou_thres): return
    # 新图片名、json文件名，新图片路径，json文件路径
    offset_x, offset_y = crop_size[2]-fill_size[2], crop_size[0]-fill_size[0]
    img_new_name = instance['imagePath'].replace('.', '_%d_%d.' % (offset_x, offset_y))
    img_new_name = merge_img_name(img_new_name)
    json_new_name = img_new_name[:img_new_name.rindex('.')] + '.json'
    img_new_path = os.path.join(output_path, img_new_name)
    json_new_path = os.path.join(output_path, json_new_name)
    instance_new = {'version': '1.0', 'imageData': None,
                    'imageWidth': crop_size[3] - crop_size[2] + fill_size[2] + fill_size[3],
                    'imageHeight': crop_size[1] - crop_size[0] + fill_size[0] + fill_size[1],
                    'imageDepth': img.shape[2],
                    'imagePath': img_new_name, 'shapes': copy.deepcopy(instance['shapes'])}
    # 先截图后填充
    img_crop = img[crop_size[0]: crop_size[1], crop_size[2]: crop_size[3]]
    update_objs_in_crop(instance_new, crop_size, iou_thres)
    img_new = cv2.copyMakeBorder(img_crop, fill_size[0], fill_size[1], fill_size[2], fill_size[3], cv2.BORDER_REPLICATE)
    cv2.imwrite(img_new_path, img_new)
    for obj in instance_new['shapes']:
        for point in obj['points']:
            point[0] -= offset_x
            point[1] -= offset_y
    instance_to_json(instance_new, json_new_path)
    print(img_new_name, ' is done!')

# 合并name的后缀信息
def merge_img_name(img_name: str):
    info = img_name[img_name.index('_')+1:img_name.rindex('.')].split('_')
    if len(info) == 2: return img_name
    offset_x = int(info[0]) + int(info[2])
    offset_y = int(info[1]) + int(info[3])
    return img_name[:img_name.index('_')] + '_%d_%d'%(offset_x, offset_y) + img_name[img_name.rindex('.'):]

# instance中的shapes字段为原instance中shapes字段的深拷贝
# 此方法更新instance中的shapes字段
def update_objs_in_crop(instance, crop_size, iou_thres=0.2):
    shapes_new = []
    shapes = instance['shapes']
    # 遍历shapes中的目标objs
    for obj in shapes:
        points = obj['points']
        shape_type = obj['shape_type']
        # 目标不在crop区域，continue
        if not obj_in_crop(obj, crop_size, iou_thres):
            continue
        # 目标在crop区域，开始更新坐标
        points_new = []
        # 四条截边
        bounds = [[crop_size[2], crop_size[0], crop_size[3], crop_size[0]],  # (xmin, ymin, xmax, ymin)
                  [crop_size[3], crop_size[0], crop_size[3], crop_size[1]],  # (xmax, ymin, xmax, ymax)
                  [crop_size[3], crop_size[1], crop_size[2], crop_size[1]],  # (xmax, ymax, xmin, ymax)
                  [crop_size[2], crop_size[1], crop_size[2], crop_size[0]]]  # (xmin, ymax, xmin, ymin)
        # four_points = [[crop_size[2], crop_size[0]], [crop_size[3], crop_size[0]], [crop_size[3], crop_size[1]], [crop_size[2], crop_size[1]]]
        # xywh = points_to_xywh(obj)
        for i, point in enumerate(points):
            if point_in_crop(point, crop_size):
                if (i != 0 or shape_type == 'polygon') and (not point_in_crop(points[i-1], crop_size)):
                    for bound in bounds:
                        cross_point = get_cross_point(point[0], point[1], points[i-1][0], points[i-1][1], *bound)
                        if cross_point != None:
                            points_new.append(cross_point)
                            break
                points_new.append(point)
            elif (i != 0 or shape_type == 'polygon') and point_in_crop(points[i-1], crop_size):
                for bound in bounds:
                    cross_point = get_cross_point(point[0], point[1], points[i-1][0], points[i-1][1], *bound)
                    if cross_point != None:
                        points_new.append(cross_point)
                        break
            elif (i != 0 or shape_type == 'polygon') and (not point_in_crop(points[i-1], crop_size)):
                temp = []
                for bound in bounds:
                    cross_point = get_cross_point(point[0], point[1], points[i-1][0], points[i-1][1], *bound)
                    if cross_point != None:
                        temp.append(cross_point)
                if len(temp) == 0: continue
                if (temp[0][0]-point[0])**2+(temp[0][1]-point[1])**2 > (temp[1][0]-point[0])**2+(temp[1][1]-point[1])**2:
                    points_new.append(temp[0])
                    points_new.append(temp[1])
                else:
                    points_new.append(temp[1])
                    points_new.append(temp[0])
        obj['points'] = points_new
        shapes_new.append(obj)
    instance['shapes'] = shapes_new
def imgs_crop_class(imgs_folder_path,output_path,crop_namber=1,rd=False,crop_size=512):

    if not os.path.exists(output_path): os.makedirs(output_path)
    for img_name in os.listdir(imgs_folder_path):
        img_file_path = os.path.join(imgs_folder_path, img_name)

        # 过滤文件夹和非图片文件
        print(img_name.split(".")[-1])
        if img_name.split(".")[-1] not in IMG_TYPES:
            continue
        print("img_file_path::", img_file_path)
        img = cv2.imread(img_file_path)
        if img is None:
            continue
        json_path=img_file_path.split(".")[0]+".json"
        # print("json_path::", json_path)
        if not os.path.exists(json_path):
            continue

        instance = json_to_instance(json_path)
        print("instance::", instance)
        crop_img(output_path,img,instance,crop_namber=crop_namber,rd=rd,crop_size=crop_size)
def center_random_size_crop(width,height,points,shape_type,rd):
    a=10
    if rd:
        k = random.randrange(0, a)
    else:
        k=a

    if shape_type == 'rectangle' or shape_type == 'polygon' :
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        min_x, min_y = int(min(xs)), int(min(ys))
        max_x, max_y = int(max(xs)), int(max(ys))


        if int(min_x) - k < 0:
            left_x = 0
        else:
            left_x = int(min_x) - k
        if int(max_x) + k > width:
            left_x = width - (int(max_x) - int(min_x)) - 2 * k

        return min_y, max_y, left_x,left_x + (int(max_x) - int(min_x)) + 2 * k
    elif shape_type == 'circle':
        center = [points[0][0], points[0][1]]
        radius = math.sqrt((points[1][0] - center[0]) ** 2 + (points[1][1] - center[1]) ** 2)
        min_y=int(center[1] - radius)
        max_y= int(center[1] + radius)
        min_x= int(center[0] - radius)
        max_x=int(center[0] + radius)

        if int(min_x) - k < 0:
            left_x = 0
        else:
            left_x = int(min_x) - k
        if int(max_x) + k > width:
            left_x = width - (int(max_x) - int(min_x)) - 2 * k
        return min_y, max_y, left_x,left_x + (int(max_x) - int(min_x)) + 2 * k

def random_crop(width,height,points,shape_type):
    a=10
    k = random.randrange(0, a)
    if shape_type == 'rectangle' or shape_type == 'polygon' :
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        min_x, min_y = int(min(xs)), int(min(ys))
        max_x, max_y = int(max(xs)), int(max(ys))


        if int(min_x) - k < 0:
            left_x = 0
            right_x = left_x + (int(max_x) - int(min_x)) + 2 * a
        else:
            left_x = int(min_x) - k
            right_x=left_x + (int(max_x) - int(min_x)) + 2 * a
        if int(max_x) + 2*a > width:
            left_x =  int(min_x)-k
            right_x=width
        return min_y, max_y, left_x,right_x
    elif shape_type == 'circle':
        center = [points[0][0], points[0][1]]
        radius = math.sqrt((points[1][0] - center[0]) ** 2 + (points[1][1] - center[1]) ** 2)
        min_y=int(center[1] - radius)
        max_y= int(center[1] + radius)
        min_x= int(center[0] - radius)
        max_x=int(center[0] + radius)

        if int(min_x) - k < 0:
            left_x = 0
            right_x = left_x + (int(max_x) - int(min_x)) + 2 * a
        else:
            left_x = int(min_x) - k
            right_x=left_x + (int(max_x) - int(min_x)) + 2 * a
        if int(max_x) + 2*a > width:
            left_x =  int(min_x)-k
            right_x=width
        return min_y, max_y, left_x,right_x

def random_fixed_size_crop(width,height,points,shape_type,crop_size=224):
    # crop_size=224
    a=20
    k = random.randrange(-a, a)
    if shape_type == 'rectangle' or shape_type == 'polygon' or shape_type=='linestrip'or shape_type=='line' :
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        min_x, min_y = int(min(xs)), int(min(ys))
        max_x, max_y = int(max(xs)), int(max(ys))
        center_x=int((max_x+min_x)/2)
        center_y=int((max_y+min_y)/2)


        if center_x - k-crop_size/2 < 0:
            left_x = 0
            right_x = crop_size
        else:
            left_x = center_x - k-crop_size/2
            right_x=left_x + crop_size
        if center_x + crop_size/2+k > width:
            left_x =  width-crop_size-abs(k)
            right_x=left_x+crop_size

        if center_y - k-crop_size/2 < 0:
            min_y = 0
            max_y = crop_size
        else:
            min_y = center_y - k-crop_size/2
            max_y=min_y + crop_size
        if center_y + crop_size/2+k > height:
            min_y =  height-crop_size-abs(k)
            max_y=min_y+crop_size
        return int(min_y), int(max_y), int(left_x),int(right_x)
    elif shape_type == 'circle':
        center = [points[0][0], points[0][1]]
        radius = math.sqrt((points[1][0] - center[0]) ** 2 + (points[1][1] - center[1]) ** 2)
        min_y=int(center[1] - radius)
        max_y= int(center[1] + radius)
        min_x= int(center[0] - radius)
        max_x=int(center[0] + radius)

        if int(min_x) - k < 0:
            left_x = 0
            right_x = left_x + (int(max_x) - int(min_x)) + 2 * a
        else:
            left_x = int(min_x) - k
            right_x=left_x + (int(max_x) - int(min_x)) + 2 * a
        if int(max_x) + 2*a > width:
            left_x =  int(min_x)-k
            right_x=width
        return min_y, max_y, left_x,right_x
    elif shape_type == 'point':
        center = [points[0][0], points[0][1]]
        radius = 10
        min_y=int(center[1] - radius)
        max_y= int(center[1] + radius)
        min_x= int(center[0] - radius)
        max_x=int(center[0] + radius)

        if int(min_x) - k < 0:
            left_x = 0
            right_x = left_x + (int(max_x) - int(min_x)) + 2 * a
        else:
            left_x = int(min_x) - k
            right_x=left_x + (int(max_x) - int(min_x)) + 2 * a
        if int(max_x) + 2*a > width:
            left_x =  int(min_x)-k
            right_x=width
        return min_y, max_y, left_x,right_x

def crop_img(output_path,img,instance,crop_namber=1,rd=False,crop_size=512):
    objs = instance['shapes']
    width=instance['imageWidth']
    height=instance['imageHeight']
    
    count=0
    for obj in objs:
        shape_type = obj['shape_type']
        label = obj['label']
        points = obj['points']
        if label not in dict_label:
            continue
        for i in range(crop_namber):
            

            output_label_path=os.path.join(output_path,label)

            if not os.path.exists(output_label_path):
                os.makedirs(output_label_path)
            curr_time=datetime.datetime.now()
            time_str=datetime.datetime.strftime(curr_time,'%Y_%m_%d_%H_%M_%S_%f')
            print("time_str::",time_str)
            output_label_name_path=os.path.join(output_label_path,instance['imagePath'].split(".")[0])+"_"+str(count)+"_"+str(time_str)+".jpg"
            # min_y, max_y, left_x,right_x=center_random_size_crop(width, height, points, shape_type,rd=rd)
            print('points::::', shape_type)
            min_y, max_y, left_x, right_x=random_fixed_size_crop(width, height, points, shape_type,crop_size=crop_size)
            print('min_y::::',min_y)
            img_crop = img[min_y: max_y, left_x: right_x]
            cv2.imwrite(output_label_name_path, img_crop)
            count=count+1
def no_json_crop(imgs_folder_path,output_path,crop_namber=1,rd=False,crop_size=128):
    if not os.path.exists(output_path): os.makedirs(output_path)
    for img_name in os.listdir(imgs_folder_path):
        img_file_path = os.path.join(imgs_folder_path, img_name)
        print(img_name.split(".")[-1])
        if img_name.split(".")[-1] not in IMG_TYPES:
            continue
        print("img_file_path::", img_file_path)
        img = cv2.imread(img_file_path)
        if img is None:
            continue
        if img.shape[0]>crop_size and img.shape[1]>crop_size:
            left_y=int(img.shape[0]/2)-int(crop_size/2)
            left_x=int(img.shape[1]/2)-int(crop_size/2)
            img_crop=img[left_y: left_y+crop_size, left_x: left_x+crop_size]
        elif img.shape[0]>crop_size and img.shape[1]<=crop_size:
            left_y = int(img.shape[0] / 2) - int(crop_size / 2)
            img_crop = img[left_y: left_y+crop_size,:]
        elif img.shape[0]<=crop_size and img.shape[1]>crop_size:
            left_x = int(img.shape[1] / 2) - int(crop_size / 2)
            img_crop=img[:, left_x: left_x+crop_size]
        output_path_name=os.path.join(output_path,img_name)
        cv2.imwrite(output_path_name, img_crop)
dict_label=['heidian','loushi_heidian']
if __name__ == '__main__':
    # 在这里定义自己的crop和fill的strategy
    # crop_strategy方法：根据img对象和json instance，给出crop和fill的范围，遵循上下左右
    # return [[crop1, fill1], [crop2, fill2],...]
    # crop: [top, bottom, left, right]   fill: [top, bottom, left, right]
    # img为opencv读取的图片对象，instance为json对象
    # 内置的crop_strategy方法在img_slice_utils.py中
    # def define_my_crop_strategy(img, instance):
    #     pass
    # # 截图并保存
    # imgs_crop_and_fill(img_folder_path='/home/adt/data/data/weiruan/weiruan_a/cemian_guaijiao/cemian/pr',
    #                    # 自定义的截图策略
    #                    crop_stategy=aug_crop_strategy,
    #                    # 截图输出路径
    #                    output_path='/home/adt/data/data/weiruan/weiruan_a/cemian_guaijiao/cemian/pr/crop',
    #                    # 自动滤去不含检测目标的截图框
    #                    empty_check=True,
    #                    # 被截断的检测目标的面积比阈值，低于阈值将不计入截图框中
    #                    iou_thres=0.5)
    imgs_crop_class(imgs_folder_path=r"/home/adt/Desktop/json",
                    output_path=r"/home/adt/Desktop/json/crop",
                    crop_namber=2,
                    rd=True,
                    crop_size=64
                    )
































