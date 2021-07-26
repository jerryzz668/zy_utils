import os
import shutil
from concurrent.futures.thread import ThreadPoolExecutor

'''
# @Description: 移动一个文件夹下子文件夹内的所有jpg图像到一个新到文件夹
                移动一个文件夹下子文件夹内子文件夹内的所有xml到一个新到文件夹
# @Author     : zhangyan
# @Time       : 2020/11/27 5:32 下午
'''

def imgs_move(input_path: str, output_path='xml', move = None, num_worker=8):
    thread_pool = ThreadPoolExecutor(max_workers=num_worker)
    print('Thread Pool is created!')
    for dir in os.listdir(input_path):
        img_dir_path = os.path.join(input_path, dir)
        thread_pool.submit(img_move, img_dir_path, output_path)  # 多线程img_move
    thread_pool.shutdown(wait=True)

def xmls_move(input_path: str, output_path='xml', move = None, num_worker=8):
    thread_pool = ThreadPoolExecutor(max_workers=num_worker)
    print('Thread Pool is created!')
    for dir in os.listdir(input_path):
        img_dir_path = os.path.join(input_path, dir)
        thread_pool.submit(xml_move, img_dir_path, output_path)  # 多线程xml_move
    thread_pool.shutdown(wait=True)

def img_move(input_path, output_path='img'):
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    filelist = os.listdir(input_path)
    for file in filelist:
        if os.path.splitext(file)[1] == '.jpg':
            shutil.move(os.path.join(input_path, file), output_path)
            print('{} has been moved!'.format(file))

def xml_move(input_path, output_path='xml'):
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    filelist = os.listdir(input_path)
    for file in filelist:
        if file == 'outputs':
            xml_path = os.path.join(input_path, file)
            xml_list = os.listdir(xml_path)
            for xml in xml_list:
                shutil.move(os.path.join(xml_path, xml), output_path)
                print('{} has been moved!'.format(xml))

if __name__ == '__main__':
    input_path = '/Users/zhangyan/Desktop/0830damian'  # 修改input
    img_output_path = '/Users/zhangyan/Desktop/img'  # 修改img_output
    xml_output_path = '/Users/zhangyan/Desktop/xml'  # 修改xml_output
    imgs_move(input_path, img_output_path)
    xmls_move(input_path, xml_output_path)