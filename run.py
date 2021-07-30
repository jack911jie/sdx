import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'PhotoEdit'))
import AfterShot

def put_mark_to_photo():
    p=AfterShot.Photo()
    p.put_mark()


if __name__=='__main__':
    put_mark_to_photo()