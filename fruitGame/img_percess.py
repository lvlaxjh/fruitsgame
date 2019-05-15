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


def percess(img):
    '''加工过程'''
    blue=np.zeros_like(img)
    blue[...,0]=img[...,0]
    gray=cv2.cvtColor(blue,cv2.COLOR_BGR2GRAY)
    dark_gray = gamma_trans(gray, 1.8)
    dark_gray = contrast_and_light(dark_gray,35,-130)
    edge=getEdge(dark_gray)
    dot_pos_x,dot_pos_y=np.where(edge!=0)
    poly = np.polyfit( dot_pos_x,  dot_pos_y, deg=1)
    z = np.polyval(poly, dot_pos_x)
    l=np.where(z==z.max())[0][0]
    return (int(z[l]),int(dot_pos_x[l]))



def get_pen_head_pos(img_path):
    '''获取画笔头的位置'''
    img=cv2.imread(img_path)
    return percess(img)


if __name__=='__main__':
    print(get_pen_head_pos('1.jpg'))
