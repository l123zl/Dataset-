# -*- coding:utf-8 -*-
##功能：将xml文件夹下的xml文件转换为json格式文件

import xml.etree.ElementTree as ET
import os
import json

coco = dict()
def parseXmlFiles(xml_path):
    l1 = []
    l2 = []
    for i in os.listdir(xml_path):
        i = i.split('.')[0]
        l1.append(i)
    l1 = sorted(l1)
    for i in l1:
        i = str(i) + '.xml'
        l2.append(i)
    for f in l2:
        if not f.endswith('.xml'):
            continue
        coco['ID'] = ''
        coco['gtboxes'] = []
        xmlname = f.split('.xml')[0]
        xml_file = os.path.join(xml_path, f)
        print(xml_file)

        tree = ET.parse(xml_file)
        root = tree.getroot()
        if root.tag != 'annotation':
            raise Exception('pascal voc xml root element should be annotation, rather than {}'.format(root.tag))

        # elem is <folder>, <filename>, <size>, <object>
        for elem in root:
            if elem.tag == 'folder' or elem.tag == 'source' or elem.tag == 'size' or elem.tag == 'segmented':
                continue

            if elem.tag == 'filename':
                file_name = xmlname
                coco['ID'] = file_name

            # add img item only after parse <size> tag
            if elem.tag == 'object':
                gb = dict()
                gb['fbox'] = []
                gb['tag'] = ''
                gb['extra'] = ''
                et = dict()
                et['box_id'] = 0
                et['occ'] = 0
                bndbox = dict()
                for subelem in elem:

                    bndbox['xmin'] = None
                    bndbox['xmax'] = None
                    bndbox['ymin'] = None
                    bndbox['ymax'] = None

                    current_sub = subelem.tag
                    if subelem.tag == 'id':
                        et['box_id'] = subelem.text
                    elif subelem.tag == 'occ':
                        et['occ'] = subelem.text
                        gb['extra'] = et
                    elif subelem.tag == 'name':
                        tag = subelem.text
                        gb['tag'] = tag
                    elif subelem.tag == 'pose' or subelem.tag == 'truncated' or subelem.tag == 'difficult':
                        continue
                    elif subelem.tag == 'bndbox':
                # option is <xmin>, <ymin>, <xmax>, <ymax>, when subelem is <bndbox>
                        for option in subelem:

                            if current_sub == 'bndbox':
                                if bndbox[option.tag] is not None:
                                    raise Exception('xml structure corrupted at bndbox tag.')
                                bndbox[option.tag] = int(float(option.text))

                    # only after parse the <object> tag
                        if bndbox['xmin'] is not None:
                            # x
                            gb['fbox'].append(bndbox['xmin'])
                            # y
                            gb['fbox'].append(bndbox['ymin'])
                            # w
                            gb['fbox'].append(bndbox['xmax'] - bndbox['xmin'])
                            # h
                            gb['fbox'].append(bndbox['ymax'] - bndbox['ymin'])
                            coco['gtboxes'].append(gb)
        with open(json_file, 'a+') as f:
            js = json.dumps(coco)
            f.write(js + '\n')
        f.close()
        print(coco)
        print(len(l2))

if __name__ == '__main__':
    xml_path = 'xmllabel1/odgtxml/train'
    json_file = 'xmllabel1/json/train.odgt'
    parseXmlFiles(xml_path)

