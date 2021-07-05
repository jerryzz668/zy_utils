"""
@Description:
@Author     : zhangyan
@Time       : 2021/7/1 上午11:28
"""

from preprocessing.zy_utils import *
from preprocessing import modify_xmls
from preprocessing import labelme_from_xml

def data_to_test(input_dir, output_dir):
    make_dir3(output_dir, ['01', '05', '13'], ['images', 'jsons'])

    xml_intermediate_result = os.path.join(os.path.dirname(output_dir), 'xml_modify')  # create
    make_dir3(xml_intermediate_result, ['01', '05', '13'], ['xml', 'xml_save'])

    # copy xml and img to output file
    input_dir_list = os.listdir(input_dir)
    for layer1 in input_dir_list:
        layer1_path = os.path.join(input_dir, layer1)  # 第一层文件路径--biaozhu
        layer2_path_list = os.listdir(layer1_path)  # 第二层list
        for layer2 in layer2_path_list:
            layer2_path = os.path.join(layer1_path, layer2)  # 第二层文件路径--侧面、大面、拐角
            if os.path.isfile(layer2_path): continue
            layer3_path_list = os.listdir(layer2_path)  # 第三层list--侧面里
            if layer2 == '侧面':
                for layer3 in layer3_path_list:
                    layer3_path = os.path.join(layer2_path, layer3)  # img and outputs path
                    if layer3.endswith('.jpg'):
                        shutil.copy(layer3_path, os.path.join(output_dir, '05', 'images'))
                    if layer3 == 'outputs':
                        outputs_xml_list = os.listdir(layer3_path)
                        for xml in outputs_xml_list:
                            shutil.copy(os.path.join(layer3_path, xml), os.path.join(xml_intermediate_result, '05', 'xml'))
            if layer2 == '大面':
                for layer3 in layer3_path_list:
                    layer3_path = os.path.join(layer2_path, layer3)  # img and outputs path
                    if layer3.endswith('.jpg'):
                        shutil.copy(layer3_path, os.path.join(output_dir, '13', 'images'))
                    if layer3 == 'outputs':
                        outputs_xml_list = os.listdir(layer3_path)
                        for xml in outputs_xml_list:
                            shutil.copy(os.path.join(layer3_path, xml), os.path.join(xml_intermediate_result, '13', 'xml'))
            if layer2 == '拐角':
                for layer3 in layer3_path_list:
                    layer3_path = os.path.join(layer2_path, layer3)  # img and outputs path
                    if layer3.endswith('.jpg'):
                        shutil.copy(layer3_path, os.path.join(output_dir, '01', 'images'))
                    if layer3 == 'outputs':
                        outputs_xml_list = os.listdir(layer3_path)
                        for xml in outputs_xml_list:
                            shutil.copy(os.path.join(layer3_path, xml), os.path.join(xml_intermediate_result, '01', 'xml'))

    # xml_modify and xml_to_labelme
    xml_modify_list = os.listdir(xml_intermediate_result)
    for optical_sur in xml_modify_list:
        xml_path = os.path.join(xml_intermediate_result, optical_sur, 'xml')  # 拷贝出来各个光学面的xml_path
        xml_save_path = os.path.join(xml_intermediate_result, optical_sur, 'xml_save')  # xml_modify_save_path
        image_save_path = os.path.join(output_dir, optical_sur, 'images')
        json_save_path = os.path.join(output_dir, optical_sur, 'jsons')

        modify_xmls.modify_xmls(xml_path, xml_save_path)  # modify xmls，delete '-'
        labelme_from_xml.xml_to_labelme(xml_save_path, image_save_path, 'item', None)  # generate labelme

        move_specify_file(image_save_path, '.json', json_save_path)  # 生成的json文件移动到jsons文件夹

if __name__ == '__main__':
    """
    input_dir：
    A件
     |---微软A件-20210619-漏失图标注
     |---微软A件-20210620-漏失图标注
                 |---侧面
                 |---大面
                 |---拐角
                      |---img1
                      |---img2
                      |---outputs
                            |---1.xml
                            |---2.xml
                            
    output_dir:
    data_to_test_output
                |---01                 
                |---05                 
                |---13                 
                    |---images                 
                             |---img1                 
                    |---jsons
                             |---json1              
    """
    input_dir = ''
    output_dir = ''
    data_to_test(input_dir, output_dir)