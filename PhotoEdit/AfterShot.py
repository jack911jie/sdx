import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),'modules'))
import readConfig
from PIL import Image

class Photo:
    def __init__(self):
        config=readConfig.readConfig(os.path.join(os.path.dirname(__file__),'config','PhotoEdit.config'))
        self.logo_dir=config['logo及二维码文件夹']

    def put_mark(self):
        wtmk_src=os.path.join(self.logo_dir,'树带熊logo2.png')
        wtmk_img=Image.open(wtmk_src)
        wtmk_img.show()
        print(self.logo_dir,'OK')

if __name__=='__main__':
    p=Photo()
    p.put_mark()