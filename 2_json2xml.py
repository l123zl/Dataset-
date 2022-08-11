import os
import json
from lxml import etree as ET
from xml.dom import minidom


# 找出训练集和测试集中的不在45类的标注图片的id
def edit_xml(objects, id, dir):
    save_xml_path = os.path.join(dir, "%s.xml" % id)  # xml

    root = ET.Element("annotation")
    # root.set("version", "1.0")
    folder = ET.SubElement(root, "folder")
    folder.text = "images"
    filename = ET.SubElement(root, "filename")
    filename.text = id + ".jpg"
    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    width.text = str(2048)
    height = ET.SubElement(size, "height")
    height.text = str(2048)
    depth = ET.SubElement(size, "depth")
    depth.text = "3"
    segmented = ET.SubElement(root, "segmented")
    segmented.text = "0"
    for obj in objects:  #
        object = ET.SubElement(root, "object")
        name = ET.SubElement(object, "name")  # number
        name.text = obj["category"]

        # meaning = ET.SubElement(object, "meaning")  # name
        # meaning.text = inf_value[0]
        pose = ET.SubElement(object, "pose")
        pose.text = "Unspecified"
        truncated = ET.SubElement(object, "truncated")
        truncated.text = "0"
        occluded = ET.SubElement(object, "occluded")
        occluded.text = "0"
        difficult = ET.SubElement(object, "difficult")
        difficult.text = "0"
        bndbox = ET.SubElement(object, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        xmin.text = (obj["bbox"]["xmin"])
        ymin = ET.SubElement(bndbox, "ymin")
        ymin.text = str(int(obj["bbox"]["ymin"]))
        xmax = ET.SubElement(bndbox, "xmax")
        xmax.text = str(int(obj["bbox"]["xmax"]))
        ymax = ET.SubElement(bndbox, "ymax")
        ymax.text = str(int(obj["bbox"]["ymax"]))
    tree = ET.ElementTree(root)
    tree.write(save_xml_path, encoding="UTF-8", xml_declaration=True)
    root = ET.parse(save_xml_path)
    file_lines = minidom.parseString(ET.tostring(root, encoding="Utf-8")).toprettyxml(
        indent="\t")
    file_line = open(save_xml_path, "w", encoding="utf-8")
    file_line.write(file_lines)
    file_line.close()


def getDirId(dir):  # get the  id list  of id.png
    names = os.listdir(dir)
    ids = []
    for name in names:
        # path = os.path.join(dir, name)
        # img  = cv2.imread(path)
        # w, h, c = img.shape
        # if name.endswith(".jpg") or name.endswith(".png"):
        # ids["%s" % name.split(".")[0]] = [w, h, c]
        ids.append(name.split(".")[0])
    return ids


def is_tt45(objects):
    flag = True
    json_file = open('./TT100K_VOC_classes.json', 'r')
    results = json.load(json_file)
    for obj in objects:
        text = obj["category"]
        for key in results.keys():
            flag1 = False
            if key == text:
                flag1 = True
                break
        if flag1 == False:
            flag = False
            break
    return flag


filedir = "annotations.json"
annos = json.loads(open(filedir).read())

trainIds = getDirId("train/")
testIds = getDirId("test/")
otherIds = getDirId("other/")

ids = annos["imgs"].keys()  # all img ids in .json

dirt = "annotations"
if not os.path.exists(dirt):
    os.makedirs(dirt)

Not_TT45_list = []
for id in ids:
    #  json 中的ID图片有待检测目标，且该id图片在 train文件夹中
    if len(annos["imgs"][id]["objects"]) > 0 and (id in trainIds):
        objects = annos["imgs"][id]["objects"]
        flag = is_tt45(objects)
        if flag is False:
            Not_TT45_list.append(id + '\n')
        edit_xml(objects, id, dir=dirt)

    elif len(annos["imgs"][id]["objects"]) > 0 and (id in testIds):
        objects = annos["imgs"][id]["objects"]
        flag = is_tt45(objects)
        if flag is False:
            Not_TT45_list.append(id + '\n')
        edit_xml(objects, id, dir=dirt)
    elif len(annos["imgs"][id]["objects"]) > 0 and (id in otherIds):
        objects = annos["imgs"][id]["objects"]
        flag = is_tt45(objects)
        if flag is False:
            Not_TT45_list.append(id + '\n')
        edit_xml(objects, id, dir=dirt)
with open("Not_TT45_list_train.txt", "a") as f:
    f.writelines(Not_TT45_list)

