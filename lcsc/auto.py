from PIL import Image, ImageEnhance, ImageFilter
import os
from io import BytesIO
import requests

import urllib, random


url = 'https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1535866637&di=d7d6ec0481db08c4c89057469a12192b&src=http://c.hiphotos.baidu.com/zhidao/pic/item/d1a20cf431adcbefc4b8f4e5aeaf2edda2cc9f41.jpg'
response = requests.get(url)
img = Image.open(BytesIO(response.content))
print(img)
exit()

# import hashlib

def getGray(image_file):
    tmpls = []
    for h in range(0, image_file.size[1]):  # h
        for w in range(0, image_file.size[0]):  # w
            tmpls.append(image_file.getpixel((w, h)))

    return tmpls


def getAvg(ls):  # 获取平均灰度值
    return sum(ls) / len(ls)


def getMH(a, b):  # 比较100个字符有几个字符相同
    dist = 0;
    for i in range(0, len(a)):
        if a[i] == b[i]:
            dist = dist + 1
    return dist


def getImgHash(fne):
    image_file = Image.open(fne)  # 打开
    image_file = image_file.resize((12, 12))  # 重置图片大小我12px X 12px
    image_file = image_file.convert("L")  # 转256灰度图
    Grayls = getGray(image_file)  # 灰度集合
    avg = getAvg(Grayls)  # 灰度平均值
    bitls = ''  # 接收获取0或1
    # 除去变宽1px遍历像素
    for h in range(1, image_file.size[1] - 1):  # h
        for w in range(1, image_file.size[0] - 1):  # w
            if image_file.getpixel((w, h)) >= avg:  # 像素的值比较平均值 大于记为1 小于记为0
                bitls = bitls + '1'
            else:
                bitls = bitls + '0'
    return bitls


def compare_images(img1, img2):

    pass


a = getImgHash(".//testpic//001n.bmp")  # 图片地址自行替换
files = os.listdir(".//testpic")  # 图片文件夹地址自行替换
for file in files:
    b = getImgHash(".//testpic//" + str(file))
    compare = getMH(a, b)
    print
    file, u'相似度', str(compare) + '%'
