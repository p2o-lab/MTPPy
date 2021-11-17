from Service_control import Service_control
import Procedure
from time import sleep
import cv2
from IndicatorElements import AnaView

class Data_Processing(Service_control):

    def __init__(self,AnaView):
        super(Data_Processing,self).__init__()
        self.AnaView=AnaView
        self.AnaView.VSclMax=307200

    def Idle(self):

        print(f'Service 1 is Idle')
        while True:
            sleep(1)

            if self.stop_idle:
                break

    def Starting(self):
        print('Service 1 is starting')
        for i in range (0,4):
            print(i)
            sleep(1)
        self.Service_SM.Start( SC=True)

    def Execute(self):
        cam = cv2.VideoCapture('http://192.168.178.69:23336/video_feed')
        print(f'Service 1 is Executing')

        while True:
            _,img=cam.read()
            edge = cv2.Canny(img, 100, 200)
            sum=edge.sum()/255
            self.AnaView.V=sum
            sleep(1)
            if self.stop_execute:
                break


    def Completing(self):
        print('Service 1 is completing')
        self.Service_SM.Complete(SC=True)


    def Completed(self):
        sleep(1)
        print('Service 1 is completed')

    def Resuming(self):
        print(f'Service 1 is Resuming')
        self.Service_SM.Resume(SC=True)

    def Paused(self):
        print(f'Service 1 is Paused')

    def Pausing(self):
        print(f'Service 1 is Pausing')
        self.Service_SM.Pause(SC=True)

    def Holding(self):
        print(f'Service 1 is Holding')
        self.Service_SM.Hold(SC=True)

    def Held(self):
        print(f'Service 1 is Held')

    def Unholding(self):
        print(f'Service 1 is Unholding')
        self.Service_SM.Unhold(SC=True)

    def Stopping(self):
        print(f'Service 1 is Stopping')
        self.Service_SM.Stop(SC=True)

    def Stopped(self):
        print(f'Service 1 is Stopped')

    def Aborting(self):
        print(f'Service 1 is Abborting')
        self.Service_SM.Abort(SC=True)

    def Aborted(self):
        print(f'Service 1 is Aborted')

    def Resetting(self):
        print(f'Service 1 is Resetting')
        self.Service_SM.Reset(SC=True)

#S=Data_Processing(AnaView())