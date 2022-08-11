import os
import cv2
import json
import shutil
from sklearn.model_selection import train_test_split

def oo(dataset, obj_id, ids):
    for anno_dic in obj_list:
        if anno_dic["category"] not in classes:
            continue
        x = anno_dic['bbox']['xmin']
        y = anno_dic['bbox']['ymin']
        width = anno_dic['bbox']['xmax'] - anno_dic['bbox']['xmin']
        height = anno_dic['bbox']['ymax'] - anno_dic['bbox']['ymin']
        label_key = anno_dic['category']

        dataset['annotations'].append({
            'area': width * height,
            'bbox': [x, y, width, height],
            'category_id': results[label_key],
            'id': obj_id,
            'image_id': ids,
            'iscrowd': 0,
            # mask, 矩形是从左上角点按顺时针的四个顶点
            'segmentation': [[x, y, x + width, y, x + width, y + height, x, y + height]]
        })
        # 每个标注的对象id唯一

        obj_id += 1
        print(obj_id)
    # ids += 1
    # 用opencv读取图片，得到图像的宽和高
    im = cv2.imread(os.path.join('images', image_name))
    H, W, _ = im.shape
    # 添加图像的信息到dataset中
    dataset['images'].append({'file_name': image_name,
                              'id': ids,
                              'width': W,
                              'height': H})
    # return obj_id, ids
    return obj_id
# 存放数据的父路径
parent_path = '/home/zhenlianglu/Dataset/tt100k_2021/'
if not os.path.exists('images'):
    os.makedirs('images')

# 读TT100K原始数据集标注文件
with open(os.path.join(parent_path, 'annotations.json')) as origin_json:
    origin_dict = json.load(origin_json)

with open(os.path.join(parent_path, 'annotations/statistics.json')) as select_json:
    select_dict = json.load(select_json)
if len(os.listdir('images')) != len(select_dict):
    os.remove('images')
    os.makedirs('images')
    for i in ['train', 'test', 'other']:
        files = os.listdir(i)
        for j in files:
            if j in select_dict:
                shutil.copy(os.path.join(i, j), 'images')
print(len(os.listdir('images')))
train_dataset = {'categories': [], 'annotations': [], 'images': []}
test_dataset = {'categories': [], 'annotations': [], 'images': []}
json_file = open('./TT100K_VOC_classes.json', 'r')
results = json.load(json_file)
classes = []
for k,v in enumerate(results):
    classes.append(v)
# 建立类别和id的关系
for i, cls in enumerate(classes, 1):
    train_dataset['categories'].append({'id': i, 'name': cls, 'supercategory': 'mark'})
    test_dataset['categories'].append({'id': i, 'name': cls, 'supercategory': 'mark'})

images_dic = origin_dict['imgs']

train_id = 0
train_ld = 0
test_id = 0
test_ld = 0
# TT100K的annotation转换成coco的
for image_id in images_dic:

    image_element = images_dic[image_id]
    image_path = image_element['path']
    image_name = image_path.split('/')[-1]
    # 在所选的类别图片中
    if image_name not in select_dict:
        continue
    # shutil.copy(os.path.join(parent_path,image_path),os.path.join(parent_path,"dataset/JPEGImages"))

    # 处理TT100K中的标注信息
    obj_list = image_element['objects']

    # 切换dataset的引用对象，从而划分数据集
    train, test = train_test_split(select_dict, test_size=0.2, random_state=42)
    if image_name in train:
        # train_id, train_ld = oo(train_dataset, train_id, train_ld)
        train_id = oo(train_dataset, train_id, image_id)
    elif image_name in test:
        # test_id, test_ld = oo(test_dataset, test_id, test_ld)
        test_id = oo(test_dataset, test_id, image_id)

# 保存结果
for phase in ['train', 'test']:
    json_name = os.path.join(parent_path, 'annotation/{}.json'.format(phase))
    with open(json_name, 'w', encoding="utf-8") as f:
        if phase == 'train':
            json.dump(train_dataset, f, ensure_ascii=False)
        if phase == 'test':
            json.dump(test_dataset, f, ensure_ascii=False)

