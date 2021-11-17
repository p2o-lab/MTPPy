from Service_control import Service_control
from Procedure import Procedure
import os
import json
import datetime
import cv2
from time import sleep

class Prod_Template(Procedure):
    def __init__(self):
        super(Prod_Template,self).__init__()

class Rawdataarchiving(Service_control):
    def __init__(self,AnaView):
        super(Rawdataarchiving,self).__init__()
        self.AnaView=AnaView


    def Idle(self):
       pass

    def Starting(self):
        if os.path.exists('Archive') == False:
            os.mkdir('Archive')

        self.meta_dict={'Img_name':'0','Img_canny_name':'0','Date':'0','Num_white_pix':0}
        self.Service_SM.Start(SC=True)

    def Execute(self):
        cam = cv2.VideoCapture('http://192.168.178.69:23336/video_feed')
        cam2 = cv2.VideoCapture('http://192.168.178.69:23336/video_feed_canny')

        while True:
            time=datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            self.meta_dict['Num_white_pix']=self.AnaView.V
            _,image=cam.read()
            _,image2=cam2.read()
            cv2.imwrite('Archive/'+time+'_img'+'.jpeg',image)
            cv2.imwrite('Archive/'+time+'_canny'+'.jpeg',image2)
            self.meta_dict['Img_name']=time+'_img'+'.jpeg'
            self.meta_dict['Date']=time
            self.meta_dict['Img_canny_name']=time+'_canny'+'.jpeg'
            out_json=open('Archive/'+time+'.json','w+')
            json.dump(self.meta_dict,out_json)
            if self.stop_execute:
                break
            sleep(1)

    def Completing(self):
        self.Service_SM.Complete(SC=True)

    def Completed(self):
        pass

    def Resuming(self):
        self.Service_SM.Resume(SC=True)

    def Paused(self):
        pass

    def Pausing(self):
        self.Service_SM.Pause(SC=True)

    def Holding(self):
        self.Service_SM.Hold(SC=True)

    def Held(self):
        pass

    def Unholding(self):
        self.Service_SM.Unhold(SC=True)

    def Stopping(self):
        self.Service_SM.Stop(SC=True)

    def Stopped(self):
        pass

    def Aborting(self):
        self.Service_SM.Abort(SC=True)

    def Aborted(self):
        pass

    def Resetting(self):
        self.Service_SM.Reset(SC=True)




