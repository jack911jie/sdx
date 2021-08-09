import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),'modules'))
import readConfig
import pics_modify
from PIL import Image,ExifTags
import datetime
# import exifread

class Photo:
    def __init__(self):
        config=readConfig.readConfig(os.path.join(os.path.dirname(__file__),'config','PhotoEdit.config'))
        self.logo_dir=config['logo及二维码文件夹']
        self.wtmk_src=os.path.join(self.logo_dir,'树带熊_logo2_white.png')
        self.wtmk2_src=os.path.join(self.logo_dir,'t_and_b_logo_white.png')
        self.wtmk3_src=os.path.join(self.logo_dir,'xiong_and_zimu.png')


    def put_mark(self,pic='d:\\temp\\sdx\\004.jpg',logo_type='xiong',new_size=''):
        bg=Image.open(pic)
        #根据exif信息判断旋转，如无exif信息，则根据图片宽高判断。已写入模块
        pic_judged=pics_modify.judge_rotation_and_export_size(bg)
        bg,w,h=pic_judged['img'],pic_judged['size'][0],pic_judged['size'][1]

        

        bg_2=bg.convert('RGBA')      
        
        if logo_type=='xiong':
            wtmk_img=Image.open(self.wtmk_src)
        elif logo_type=='zimu':
            wtmk_img=Image.open(self.wtmk2_src)
        elif logo_type=='xiong_and_zimu':
            wtmk_img=Image.open(self.wtmk3_src)
        else:
            print('logo类型错误：xiong 或 zimu')
            exit()

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
        # img.show()
        if new_size:
            img=img.resize((int(new_size),int(2400*h/w)))
        return img

    def group_mark(self,pic_dir='q:\\temp\\sdx\\to_mark',logo_type='pic',new_size=''):
        out_dir=os.path.join(os.path.dirname(pic_dir),'mark_'+datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        
        fns_to_mark=[]
        for fn in os.listdir(pic_dir):
            if fn[-3:].lower()=='jpg' or fn[-4:].lower()=='jpeg':
                fns_to_mark.append(fn)

        total_pics=len(fns_to_mark)
        if total_pics>0:
            n=1
            for fn_to_mark in fns_to_mark:            
                print('正在处理第 {}/{} 张照片'.format(n,total_pics),end='\r',flush=True)
                out_pic=self.put_mark(pic=os.path.join(pic_dir,fn_to_mark),logo_type=logo_type,new_size=new_size)
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
                out_pic.save(os.path.join(out_dir,fn_to_mark))
                n+=1
            print('\n完成')
            os.startfile(out_dir)
        else:
            print('源文件夹为空')

                 

if __name__=='__main__':
    p=Photo()
    # p.put_mark(pic='q:\\temp\\sdx\\DSC_0659.jpg',logo_type='txt')
    p.group_mark(pic_dir='q:\\temp\\sdx\\to_mark',logo_type='zimu',new_size=2400)