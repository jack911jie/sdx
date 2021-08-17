import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'modules'))
sys.path.append(os.path.join(os.path.dirname(__file__),'PhotoEdit'))
import readConfig
import AfterShot
import output_redirect
import tkinter as tk
from PIL import Image,ImageTk


class SdxGui:
    def __init__(self):
        config=readConfig.readConfig(os.path.join(os.path.dirname(__file__),'PhotoEdit','config','PhotoEdit.config'))
        self.logo_dir=config['logo及二维码文件夹']

    def go(self,pic_dir='e:\\temp\\sdx\\to_mark',logo_type='xiong_and_zimu',thresh_hold=0.42,new_size=2400,mode='gui'):
        window=tk.Tk()
        window.title('树带熊给照片打标')
        window.geometry('300x300')

        logo=Image.open(os.path.join(self.logo_dir,'xiong_and_zimu.jpg'))
        logo=logo.resize((100,100))
        logo_cover=ImageTk.PhotoImage(logo)
        lb_logo=tk.Label(window,image=logo_cover)
        lb_logo.pack()

        lb_pos=tk.Label(window,text='logo位置',bg='#FFFFEE',font=('黑体',12),width=500,height=2)
        lb_pos.pack()

        pos = tk.StringVar()    # 定义一个var用来将radiobutton的值和Label的值联系在一起.
        pos.set('ru')
        pos1= tk.Radiobutton(window, text='右上角', variable=pos, value='ru')
        pos1.pack()
        pos2 = tk.Radiobutton(window, text='右下角', variable=pos, value='rb')
        pos2.pack()


        msg_box=tk.Text(window)  
        def put_mark():
            p=AfterShot.Photo()
            # p.put_mark(pic='q:\\temp\\sdx\\DSC_0659.jpg',logo_type='txt')
            # logo_type参数：xiong 或 zimu 或 xiong_and_zimu
            my_out=output_redirect.myStdout(msg_box)
            p.group_mark(pic_dir=pic_dir,logo_type=logo_type,new_size=new_size,pos=pos.get(),thresh_hold=thresh_hold,mode=mode,msg_box=msg_box)
            my_out.restoreStd()

        btn=tk.Button(window,text='给照片添加水印',font=('楷体',12),command=put_mark)      
        btn.pack()
        msg_box.pack()

        window.mainloop()




if __name__=='__main__':
    gui=SdxGui()
    gui.go(pic_dir='d:\\temp\\sdx\\to_mark',logo_type='xiong_and_zimu',thresh_hold=0.42,new_size=2400,mode='gui')
