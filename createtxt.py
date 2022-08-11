import  json

with open("TT100K_VOC_classes.json", 'r', encoding='UTF-8') as f:
    data = json.loads(f.read())
    key_list = list(data.keys())

    label_f = open("label_list.txt", "x")
    for i in range(len(key_list)):

        label_f.write('{}\n'.format(key_list[i]))

