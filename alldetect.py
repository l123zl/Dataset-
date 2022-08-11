import os
import xml.etree.ElementTree as ET
import tqdm
class_names = ['i2', 'i4', 'i5', 'il100', 'il60', 'il80', 'io', 'ip', 'p10', 'p11', 'p12',
               'p19', 'p23', 'p26', 'p27', 'p3', 'p5', 'p6', 'pg', 'ph4', 'ph4.5', 'ph5',
               'pl100', 'pl120', 'pl20', 'pl30', 'pl40', 'pl5', 'pl50', 'pl60', 'pl70',
               'pl80', 'pm20', 'pm30', 'pm55', 'pn', 'pne', 'po', 'pr40', 'w13', 'w32',
               'w55', 'w57', 'w59', 'wo']

def del_delete_eq_1(xml_path):
    # 从xml文件中读取，使用getroot()获取根节点，得到的是一个Element对象
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for object in root.findall('object'):
        deleted = str(object.find('name').text)

        if (deleted not in class_names):
            root.remove(object)

    tree.write(xml_path)


def main():
    root_dir = "annotations"
    xml_path_list = [os.path.join(root_dir, x) for x in os.listdir(root_dir)]

    # 使用tqdm显示进程
    for xml in tqdm.tqdm(xml_path_list):
        del_delete_eq_1(xml)


if __name__ == '__main__':
    main()
