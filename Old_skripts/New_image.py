import cv2
from threading import Thread
from time import sleep
from PIL import Image
import imagehash

class New_image():
    def __init__(self):
        self.cam=cv2.VideoCapture('http://192.168.178.69:23336/video_feed')
        _,self.old_img=self.cam.read()
        self.new_img_av=False
        self.hash0 = self.gen_hsh(self.old_img)
        #self.img_thread=Thread(target=self.check_new_img())
        #self.img_thread.start()



    def check_new_img(self):
        #while True:
        _,self.akt_img=self.cam.read()
        self.hash1 = self.gen_hsh(self.akt_img)

        if self.hash0 != self.hash1 and self.new_img_av == False:
            self.new_img_av=True
            self.old_img=self.akt_img
            self.hash0=self.hash1


    def gen_hsh(self,img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        hash = imagehash.average_hash(im_pil)
        return hash

NI=New_image()
print('im here')


while True:
    NI.check_new_img()
    if NI.new_img_av==True:
         print('New Img av')
         NI.new_img_av=False
    else:
        print('No New Img av')
    sleep(1)