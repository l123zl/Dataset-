# -*- coding: utf-8 -*-
import os
from PIL import Image
import glob

yolo_img = 'xmllabel1/images/train/'
yolo_txt = 'xmllabel1/txt/train/'
voc_xml = 'xmllabel1/odgtxml/train/'

# 目标类别
labels = ['i2','i4','i5','il100','il60','il80','io','ip','p10','p11','p12',
          'p19','p23','p26','p27','p3','p5','p6','pg','ph4','ph4.5','ph5',
          'pl100','pl120','pl20','pl30','pl40','pl5','pl50','pl60','pl70',
          'pl80','pm20','pm30','pm55','pn','pne','po','pr40','w13','w32',
          'w55','w57','w59','wo']
# 匹配文件路径下的所有jpg文件，并返回列表
img_glob = glob.glob(yolo_img + '*.jpg')

img_base_names = []

for img in img_glob:
    # os.path.basename:取文件的后缀名
    img_base_names.append(os.path.basename(img))

img_pre_name = []
i = 0
for img in img_base_names:
    # os.path.splitext:将文件按照后缀切分为两块
    temp1, temp2 = os.path.splitext(img)
    img_pre_name.append(temp1)
    print('imgpre:{}'.format(img_pre_name))
for img in img_pre_name:
    with open(voc_xml + img + '.xml', 'w') as xml_files:
        image = Image.open(yolo_img + img + '.jpg')
        img_w, img_h = image.size
        xml_files.write('<annotation>\n')
        xml_files.write('   <folder>folder</folder>\n')
        xml_files.write('   <filename>{}.jpg</filename>\n'.format(img))
        xml_files.write('   <source>\n')
        xml_files.write('   <database>Unknown</database>\n')
        xml_files.write('   </source>\n')
        xml_files.write('   <size>\n')
        xml_files.write('     <width>{}</width>\n'.format(img_w))
        xml_files.write('     <height>{}</height>\n'.format(img_h))
        xml_files.write('     <depth>3</depth>\n')
        xml_files.write('   </size>\n')
        xml_files.write('   <segmented>0</segmented>\n')
        with open(yolo_txt + img + '.txt', 'r') as f:
            # 以列表形式返回每一行
            lines = f.read().splitlines()
            for each_line in lines:
                line = each_line.split(' ')
                xml_files.write('   <object>\n')
                xml_files.write('      <id>{}</id>\n'.format(i))
                xml_files.write('      <occ>{}</occ>\n'.format(int(line[0])))
                xml_files.write('      <name>{}</name>\n'.format(labels[int(line[0])]))
                xml_files.write('      <pose>Unspecified</pose>\n')
                xml_files.write('      <truncated>0</truncated>\n')
                xml_files.write('      <difficult>0</difficult>\n')
                xml_files.write('      <bndbox>\n')
                center_x = round(float(line[1]) * img_w)
                center_y = round(float(line[2]) * img_h)
                bbox_w = round(float(line[3]) * img_w)
                bbox_h = round(float(line[4]) * img_h)
                xmin = str(int(center_x - bbox_w / 2))
                ymin = str(int(center_y - bbox_h / 2))
                xmax = str(int(center_x + bbox_w / 2))
                ymax = str(int(center_y + bbox_h / 2))
                xml_files.write('         <xmin>{}</xmin>\n'.format(xmin))
                xml_files.write('         <ymin>{}</ymin>\n'.format(ymin))
                xml_files.write('         <xmax>{}</xmax>\n'.format(xmax))
                xml_files.write('         <ymax>{}</ymax>\n'.format(ymax))
                xml_files.write('      </bndbox>\n')
                xml_files.write('   </object>\n')
                i += 1
        xml_files.write('</annotation>')
        i=0
