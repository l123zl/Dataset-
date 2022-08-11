import os
import json

os.makedirs('annotations', exist_ok=True)
# 存放数据的父路径
parent_path = '/home/zhenlianglu/Dataset/tt100k_2021'

# 读TT100K原始数据集标注文件
with open(os.path.join(parent_path, 'annotations.json')) as origin_json:
    origin_dict = json.load(origin_json)
# 建立统计每个类别包含的图片的字典

images_dic = origin_dict['imgs']
json_file = open('./TT100K_VOC_classes.json', 'r')
results = json.load(json_file)
classes = []
for k,v in enumerate(results):
    classes.append(v)

sta = {}
for i in classes:
    sta[i] = []
# 记录所有保留的图片
saved_images = []
# 遍历TT100K的imgs
for image_id in images_dic:
    image_element = images_dic[image_id]
    image_path = image_element['path']

    # 添加图像的信息到dataset中
    image_path = image_path.split('/')[-1]
    obj_list = image_element['objects']

    # 遍历每张图片的标注信息
    for anno_dic in obj_list:
        label_key = anno_dic['category']
        if label_key in classes:
            # 防止一个图片多次加入一个标签类别
            sta[label_key].append(image_path)
# 只保留包含图片数超过100的类别
result = {k: v for k, v in sta.items()}

for i in result:
    print("the type of {} includes {} images".format(i, len(result[i])))
    saved_images.extend(result[i])

saved_images = list(set(saved_images))
print("total types is {}".format(len(result)))
print(len(saved_images))
# 保存结果
json_name = os.path.join(parent_path, 'annotations/statistics.json')
with open(json_name, 'w', encoding="utf-8") as f:
    json.dump(saved_images, f, ensure_ascii=False, indent=1)

