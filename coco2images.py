import os
import json
import shutil
import cv2

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

filedir = "annotations.json"

trainIds = getDirId("train/")
testIds = getDirId("test/")
otherIds = getDirId("other/")

dir_train = 'images/train'
dir_test = 'images/test'

jsons = 'annotations/test.json'
out = open(jsons, 'r')
outs = json.load(out)
l1 = outs['images']
num = 0
for i in l1:
    num += 1
    if i['id'] in trainIds:
        t1 = 'train/' + i['id'] + '.jpg'
        shutil.copy(t1, dir_test)
    elif i['id'] in testIds:
        t1 = 'test/' + i['id'] + '.jpg'
        shutil.copy(t1, dir_test)
    elif i['id'] in otherIds:
        t1 = 'other/' + i['id'] + '.jpg'
        shutil.copy(t1, dir_test)
    else:
        break

print(num)
