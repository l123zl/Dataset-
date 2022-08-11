import json

with open('annotations/test.json') as f:
    Json = json.load(f)
    annotations = Json['annotations']
    images = Json['images']
    image_id_name_dict = {}
    image_id_width_dict = {}
    image_id_height_dict = {}
    for image in images:
        image_id_name_dict[image['id']] = image['file_name']
        image_id_height_dict[image['id']] = image['height']
        image_id_width_dict[image['id']] = image['width']
    # print(image_id_name_dict)
    for i in range(1909):
        for annotation in annotations:
            if annotation['image_id'] != i:  # i表示第i张照片，数据集共2476张
                continue
            bbox = annotation['bbox']
            x, y, w, h = bbox
            x = x + w / 2
            y = y + h / 2
            width = image_id_width_dict[i]
            height = image_id_height_dict[i]
            x = str(x / width)
            y = str(y / height)
            w = str(w / width)
            h = str(h / height)
            with open('annotation/labels/test/{}.txt'.format(
                    image_id_name_dict[i].split('.')[0]), 'a') as f:
                annotation['category_id'] = annotation['category_id'] - 1
                category = str(annotation['category_id'])
                print(category)
                f.write(category + ' ' + x + ' ' + y + ' ' + w + ' ' + h + '\n')
