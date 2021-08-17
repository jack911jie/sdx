import os
from PIL import Image,ImageDraw
import colorsys
import numpy as np

def circle_corner(img,radii=150):
    radii=int(img.size[0]*radii/4032)
    # 画圆（用于分离4个角）  
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建黑色方形
    # circle.save('1.jpg','JPEG',qulity=100)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 黑色方形内切白色圆形
    # circle.save('2.jpg','JPEG',qulity=100)

    # 原图转为带有alpha通道（表示透明程度）
    img = img.convert("RGBA")
    w, h = img.size

    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', img.size, 255)	#与img同大小的白色矩形，L 表示黑白图
    # alpha.save('3.jpg','JPEG',qulity=100)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
    # alpha.save('4.jpg','JPEG',qulity=100)

    img.putalpha(alpha)		# 白色区域透明可见，黑色区域不可见
    # img.save('e:\\temp\\5555.png','PNG',qulity=100)

    # img.show()
    return img

def round_pic(img,method='in'):
    if img.mode!='RGBA':
        img=img.convert('RGBA')

    if method=='out':
        w,h=img.size
        r=int(np.sqrt(w*w/4+h*h/4))
        d=int(r*2)
        bg=Image.new('RGBA',(d,d),'#FFFFFF')
        scale=3
        alpha_layer = Image.new('L', (d*scale, d*scale), 0)
        draw=ImageDraw.Draw(alpha_layer)
        draw.ellipse((0,0,d*scale,d*scale),fill='#FFFFFF')
        alpha_layer=alpha_layer.resize((d,d))
        
        # bg.paste(alpha_layer,(0,0),mask=alpha_layer)
        bg.paste(img,((d-w)//2,(d-h)//2),mask=img)
        bg.putalpha(alpha_layer)
        # bg.save('e:/temp/dq.png')
    elif method=='in':        
        w,h=img.size
        d=min(w,h)
        scale=3
        alpha_layer=Image.new('L',(w*scale,h*scale),0)
        draw=ImageDraw.Draw(alpha_layer)
        if h>=w:
            draw.ellipse((0,(h*scale-d*scale)//2,w*scale,(h*scale-d*scale)//2+d*scale),fill='#FFFFFF')
            alpha_layer=alpha_layer.resize((w,h))
            img.putalpha(alpha_layer)
        else:
            draw.ellipse(((w*scale-d*scale)//2,0,(w*scale-d*scale)//2+d*scale,h*scale),fill='#FFFFFF')
            alpha_layer=alpha_layer.resize((w,h))
            img.putalpha(alpha_layer)
        bg=img

        # alpha_layer.show()
        # img.show()
        # bg.show()
    return bg

def judge_rotation_and_export_size(img):
        #根据exif信息判断旋转，如无exif信息，则根据图片宽高判断。
        #参考文档：https://mercurial-bandicoot-c34.notion.site/PIL-7891e4c4cbb6419182c4e222b5a97b18
        #274是exif信息里判断旋转的标签ID
        exif_orientation_tag=274
        if hasattr(img, "_getexif") and isinstance(img._getexif(), dict) and exif_orientation_tag in img._getexif():
            exif_data=img._getexif()            
            orientation = exif_data[exif_orientation_tag]        
            if  orientation==6:
                img=img.rotate(-90, expand=True)        
            if orientation==8:
                img=img.rotate(90, expand=True)
        else:
            pass
        
        w,h=img.size[0],img.size[1]

        return {'img':img,'size':[w,h]}

class evaluate_hsv:
    def evaluate(self,img):
        img_arr=np.array(img).tolist()
        hsv=[]
        for rgbs in img_arr:
            hsv_h=[]
            hsv_s=[]
            hsv_v=[]
            for rgb in rgbs:
                hsv_h.append(self.rgb_hsv(rgb)[0])
                hsv_s.append(self.rgb_hsv(rgb)[1])
                hsv_v.append(self.rgb_hsv(rgb)[2])
            hsv.append([hsv_h,hsv_s,hsv_v])
        # print(hsv)
        # return 
        # print(hsv[2])
        return [np.mean(hsv[0]),np.mean(hsv[1]),np.mean(hsv[2])]


    def rgb_hsv(self,rgb):
        # img_arr=np.array(img).tolist()
        h,s,v=colorsys.rgb_to_hsv(rgb[0]/255,rgb[1]/255,rgb[2]/255)
        return [h,s,v]