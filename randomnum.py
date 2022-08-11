# -*- coding:utf-8 -*-

import os
import random

def rename(paths, path):
    filelist = os.listdir(paths)
    for i in filelist:
        txt = os.path.join(os.path.abspath(paths), i)
        lable = os.path.join(os.path.abspath(path), i.split('.')[0] + '.txt')
        stxt = os.path.join(os.path.abspath(paths), i.split('.')[0] + '_train.jpg')
        slable = os.path.join(os.path.abspath(path), i.split('.')[0] + '_train.txt')
        os.rename(txt, stxt)
        os.rename(lable, slable)
    print(filelist)
    random.shuffle(filelist)
    print(filelist)
    total_num = len(filelist)
    for i, j in enumerate(os.listdir(paths)):
        src = os.path.join(os.path.abspath(paths), j)
        txtsrc = os.path.join(os.path.abspath(path), j.split('.')[0] + '.txt')
        dst = os.path.join(os.path.abspath(paths), str(i+1) + '.jpg')
        txtdst = os.path.join(os.path.abspath(path), str(i+1) + '.txt')
        os.rename(src, dst)
        os.rename(txtsrc, txtdst)
    print("total %d to rename & converted jpgs" % total_num)

if __name__ == '__main__':
    newname = "/home/zhenlianglu/Dataset/tt100k_2021/xmllabel1/images/train"
    path = "/home/zhenlianglu/Dataset/tt100k_2021/xmllabel1/labels/train"
    rename(newname, path)
