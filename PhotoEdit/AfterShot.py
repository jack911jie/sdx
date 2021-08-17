import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),'modules'))
import readConfig
import pics_modify
from PIL import Image,ExifTags
import datetime
from tqdm import tqdm
# import numpy as np
# import exifread

class Photo:
    def __init__(self):
        config=readConfig.readConfig(os.path.join(os.path.dirname(__file__),'config','PhotoEdit.config'))
        self.logo_dir=config['logo及二维码文件夹']
        self.wtmk_src=os.path.join(self.logo_dir,'树带熊_logo2_white.png')
        self.wtmk2_src=os.path.join(self.logo_dir,'t_and_b_logo_white.png')
        self.wtmk3_src=os.path.join(self.logo_dir,'xiong_and_zimu.png')
        self.wtmk3_dark_src=os.path.join(self.logo_dir,'xiong_and_zimu_dark.png')


    def put_mark(self,pic='d:\\temp\\sdx\\004.jpg',logo_type='xiong',new_size='',pos='rb',thresh_hold=0.3):
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
            print('logo类型错误：xiong 或 zimu 或 xiong_and_zimu')
            exit()

        #横，正方形
        if w>=h:           
            wtmk_size=[w//18,(wtmk_img.size[1]*w//18)//wtmk_img.size[0]]
            wtmk=wtmk_img.resize(wtmk_size)    
            wtmk_a=wtmk.split()[3]           
            if pos=='rb': 
                p_wtmk=(int(w-wtmk.size[0]*1.4),int(h-wtmk.size[1]*1.4))
            elif pos=='ru':
                p_wtmk=(int(w-wtmk.size[0]*1.4),int(wtmk.size[1]*0.4))
            else:
                print('位置参数错误')
                exit(0)
            
        else:
            wtmk_size=[w//9,(wtmk_img.size[1]*w//9)//wtmk_img.size[0]]
            wtmk=wtmk_img.resize(wtmk_size)    
            wtmk_a=wtmk.split()[3]            
            if pos=='rb':
                p_wtmk=(int(w-wtmk.size[0]*1.4),int(h-wtmk.size[1]*1.4))
            elif pos=='ru':
                p_wtmk=(int(w-wtmk.size[0]*1.4),int(wtmk.size[1]*0.4))
            else:
                print('位置参数错误')
                exit(0)

        logo_img=bg.crop((p_wtmk[0],p_wtmk[1],p_wtmk[0]+wtmk.size[0],p_wtmk[1]+wtmk.size[1]))
        logo_section=pics_modify.evaluate_hsv()
        logo_sec_hsv=logo_section.evaluate(logo_img)
        # print(logo_type,logo_sec_hsv)
        if logo_type=='xiong_and_zimu':
            if logo_sec_hsv[2]>=thresh_hold:
                wtmk_dark_img=Image.open(self.wtmk3_dark_src)
                wtmk=wtmk_dark_img.resize(wtmk_size)

        
        

        bg_2.paste(wtmk,p_wtmk,mask=wtmk_a)
        img=bg_2.convert('RGB')
        # img.show()
        if new_size:
            if w>=h:
                img=img.resize((int(new_size),int(new_size*h/w)))
            else:
                img=img.resize((int(new_size*w/h),int(new_size)))
        return img
    

    def group_mark(self,pic_dir='q:\\temp\\sdx\\to_mark',logo_type='pic',new_size='',pos='ru',thresh_hold=0.3,mode='prgrm',msg_box=''):
        out_dir=os.path.join(os.path.dirname(pic_dir),'mark_'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'_logotype_'+logo_type)
        
        fns_to_mark=[]
        for fn in os.listdir(pic_dir):
            if fn[-3:].lower()=='jpg' or fn[-4:].lower()=='jpeg':
                fns_to_mark.append(fn)

        total_pics=len(fns_to_mark)
        if total_pics>0:
            n=1
            
            for fn_to_mark in fns_to_mark:            
                if mode=='prgrm':
                    print('正在处理第 {}/{} 张照片'.format(n,total_pics),end='\r',flush=True)
                elif mode=='gui':
                    msg_box.delete('1.0','end')
                    print('正在处理第 {}/{} 张照片'.format(n,total_pics),end='')
                else:
                    print('无效的调用模式：prgrm 或 gui')
                out_pic=self.put_mark(pic=os.path.join(pic_dir,fn_to_mark),logo_type=logo_type,new_size=new_size,pos=pos,thresh_hold=thresh_hold)
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
    # logo_type参数：xiong 或 zimu 或 xiong_and_zimu
    p.group_mark(pic_dir='d:\\temp\\sdx\\to_mark',logo_type='xiong_and_zimu',new_size=2400,pos='ru',thresh_hold=0.42,mode='prgrm')