import os
import xml.etree.cElementTree as ET
from collections import Counter


def get_bbox(xml_path):
    tree = ET.ElementTree(file=xml_path)
    root = tree.getroot()
    object_set = root.findall('object')
    object_bbox = list()

    for Object in object_set:
        name = Object.find('name').text
        object_bbox.append(name)
    return object_bbox



if __name__ == '__main__':
    xml_dir = '/home/zhenlianglu/Dataset/tt100k_2021/xmllabel1/annotations/train'
    names = []
    for file in os.listdir(xml_dir):
        file_name = file.split('.')[0]
        xml = file_name + '.xml'
        bndboxes = get_bbox(xml_path=os.path.join(xml_dir, xml))
        for i in bndboxes:
            names.append(i)
    cn = dict(Counter(names))
    r1 = str(cn).replace('{', '').replace('}', '').replace("'", '')
    print(r1)
