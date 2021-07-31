import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),'modules'))
import readConfig
import pics_modify
from PIL import Image,ExifTags
# import exifread

class Photo:
    def __init__(self):
        config=readConfig.readConfig(os.path.join(os.path.dirname(__file__),'config','PhotoEdit.config'))
        self.logo_dir=config['logo及二维码文件夹']
        self.wtmk_src=os.path.join(self.logo_dir,'树带熊logo2_white.png')

    def put_mark(self,pic='d:\\temp\\sdx\\003.jpg'):
        bg=Image.open(pic)
        #根据exif信息判断旋转，如无exif信息，则根据图片宽高判断。已写入模块
        pic_judged=pics_modify.judge_rotation_and_export_size(bg)
        bg,w,h=pic_judged['img'],pic_judged['size'][0],pic_judged['size'][1]
        
        bg_2=bg.convert('RGBA')            
        wtmk_img=Image.open(self.wtmk_src)

        #横，正方形
        if w>=h:           
            wtmk_size=[w//12,wtmk_img.size[0]*w//12//wtmk_img.size[1]]
            wtmk=wtmk_img.resize(wtmk_size)    
            wtmk_a=wtmk.split()[3]            
            p_wtmk=(int(w-wtmk.size[0]*1.2),int(h-wtmk.size[1]*1.2))
            
        else:
            wtmk_size=[w//6,wtmk_img.size[0]*w//6//wtmk_img.size[1]]
            wtmk=wtmk_img.resize(wtmk_size)    
            wtmk_a=wtmk.split()[3]            
            p_wtmk=(int(w-wtmk.size[0]*1.2),int(h-wtmk.size[1]*1.2))


        bg_2.paste(wtmk,p_wtmk,mask=wtmk_a)
        img=bg_2.convert('RGB')
        img.show()



if __name__=='__main__':
    p=Photo()
    p.put_mark()