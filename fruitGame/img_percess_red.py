import cv2
import numpy as np
import matplotlib.pyplot as plt

def gamma_trans(img,gamma):#gamma函数处理
    '''修改曝光度'''
    gamma_table=[np.power(x/255.0,gamma)*255.0 for x in range(256)]#建立映射表
    gamma_table=np.round(np.array(gamma_table)).astype(np.uint8)#颜色值为整数
    return cv2.LUT(img,gamma_table)#图片颜色查表。另外可以根据光强（颜色）均匀化原则设计自适应算法。


def contrast_and_light(img,alpha, beta):
    '''
    @:param alpha 调节对比度
    @:param beta调节亮度
    '''
    return np.uint8(np.clip((alpha * img + beta), 0, 255))
    blank = np.zeros(img.shape, img.dtype)
    return cv2.addWeighted(img,blank, 1-alpha, beta)


def getEdge(img):
    '''获取边界'''
    return  cv2.Canny(img,50,200)


# def percess(img):
#     '''加工过程'''
#     blue=np.zeros_like(img)
#     r,g,b=img[:,:,0],img[:,:,1],img[:,:,2]
#     gb=(g+b)/2
#     gray=(r+g+b)/3
#     blue[...,0]=img[...,0]
#     for x,row in enumerate(img):
#         for y,point in enumerate(row):
#             if gray[x][y]>180:
#                 img[x][y] = np.array([0, 0, 0])
#             # if r[x][y]<gb[x][y]+20 and r[x][y]>gb[x][y]-20 and r[x][y]<50:
#             #     img[x][y]=np.array([0,0,0])
#             elif r[x][y]>128:
#                 img[x][y] = np.array([0,0,0])
#             elif gb[x][y]<115:
#                 img[x][y] = np.array([0,0,0])
#             elif gb[x][y] < 115:
#                 img[x][y] = np.array([0, 0, 0])
#             # else:
#             #     img[x][y] = np.array([0,0,0])
#     cv2.imshow('123',img)
#     gray=cv2.cvtColor(blue,cv2.COLOR_BGR2GRAY)
#     dark_gray = gamma_trans(gray, 1.8)
#     dark_gray = contrast_and_light(dark_gray,35,-130)
#     edge=getEdge(dark_gray)
#     dot_pos_x,dot_pos_y=np.where(edge!=0)
#     poly = np.polyfit( dot_pos_x,  dot_pos_y, deg=1)
#     z = np.polyval(poly, dot_pos_x)
#     k=cv2.waitKey()
#
#     l=np.where(z==z.min())[0][0]
#     return (int(z[l]),int(dot_pos_x[l]))

def percess_by_hsv(img,lower=np.array([0,131,180]),uper=np.array([6,255,255])):
    img=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    bin_img=cv2.inRange(img, lower, uper)
    edge = getEdge(bin_img)
    dot_pos_x, dot_pos_y = np.where(edge != 0)
    poly = np.polyfit(dot_pos_x, dot_pos_y, deg=1)
    z = np.polyval(poly, dot_pos_x)
    l = np.where(z == z.min())[0][0]
    return (int(z[l]), int(dot_pos_x[l]))

def get_pen_head_pos(img_path):
    '''获取画笔头的位置'''
    img=cv2.imread(img_path)
    return percess_by_hsv(img)


def nothing(x):
    pass


def createbars():
    """
    实现创建六个滑块的作用，分别控制H、S、V的最高值与最低值
    """
    cv2.createTrackbar("H_l", "image", 0, 180, nothing)
    cv2.createTrackbar("H_h", "image", 0, 180, nothing)
    cv2.createTrackbar("S_l", "image", 0, 255, nothing)
    cv2.createTrackbar("S_h", "image", 0, 255, nothing)
    cv2.createTrackbar("V_l", "image", 0, 255, nothing)
    cv2.createTrackbar("V_h", "image", 0, 255, nothing)



def find_param(img_array):
    '''
    用来找hsv合适的参数
    :param img_array:
    :return:
    '''
    cv2.namedWindow("image")
    createbars()  # 创建六个滑块
    frame = cv2.imread('3.jpg')
    while True:
        lower = np.array([0, 0, 0])  # 设置初始值
        upper = np.array([0, 0, 0])

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 将图片由BGR颜色空间转化成HSV空间，HSV可以更好地分割颜色图形
        lower[0] = cv2.getTrackbarPos("H_l", "image")  # 获取"H_l"滑块的实时值
        upper[0] = cv2.getTrackbarPos("H_h", "image")  # 获取"H_h"滑块的实时值
        lower[1] = cv2.getTrackbarPos("S_l", "image")
        upper[1] = cv2.getTrackbarPos("S_h", "image")
        lower[2] = cv2.getTrackbarPos("V_l", "image")
        upper[2] = cv2.getTrackbarPos("V_h", "image")

        mask = cv2.inRange(hsv_frame, lower, upper)  # cv2.inrange()函数通过设定的最低、最高阈值获得图像的掩膜
        cv2.imshow("img", frame)
        cv2.imshow("mask", mask)
        if cv2.waitKey(1) & 0xff == 27:
            break


if __name__=='__main__':

    print(get_pen_head_pos('3.jpg'))
