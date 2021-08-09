import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'PhotoEdit'))
import AfterShot


def put_mark_to_photo(pic_dir='q:\\temp\\sdx\\to_mark',logo_type='xiong_and_zimu',new_size=2400):
    photo=AfterShot.Photo()
    photo.group_mark(pic_dir=pic_dir,logo_type=logo_type,new_size=new_size)


if __name__=='__main__':
    put_mark_to_photo(pic_dir='q:\\temp\\sdx\\to_mark',logo_type='xiong_and_zimu',new_size=2400)