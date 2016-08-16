#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: Gaomin Wu
@contact: pattywgm@163.com
@file: img_code_identify.py
@time: 16/8/4  下午11:17
@desc: Reference --> http://blog.csdn.net/nwpulei/article/details/8457738
"""
from PIL import Image, ImageFilter
from pytesseract import *

# 二值化
threshold = 30
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(220)


def getverify1(path, name):

    #打开图片
    im = Image.open(path)
    print "Img's format:" + im.format + " size: " + str(im.size) + " mode: " +im.mode
    #转化到黑白色
    imgry = im.convert('L')
    # imgry = imgry.rotate(15)
    imgry.save('g'+name)
    #二值化
    out = imgry.point(table,'1')
    out.save('b'+name)
    #识别
    text = image_to_string(out)
    #识别对吗
    text = text.strip()
    text = text.lower()

    #out.save(text+'.jpg')
    print 'text:', text
    return text
# getverify1('/Users/pattywgm/SelfProject/DouBanMovieProVenv/captcha2.jpeg', 'captcha1.jpeg')