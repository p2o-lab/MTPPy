from Service_control import Service_control
import Procedure
from time import sleep
from threading import Thread
from random import randint
import threading
from flask import Flask, render_template, Response
import cv2
from IndicatorElements import AnaView
import numpy as np



class Data_Processing(Service_control):

    def __init__(self,AnaView):
        super(Data_Processing,self).__init__()

        self.AnaView=AnaView
        self.AnaView.VSclMax=1000000000
        self.Prod_def=Procedure.Procedure(1,False,False)
        self.stop_idle=False
        self.stop_starting=False
        self.stop_execute=False
        self.stop_completing=False
        self.stop_completed=False
        self.stop_resuming=False
        self.stop_paused=False
        self.stop_pausing=False
        self.stop_holding=False
        self.stop_held=False
        self.stop_unholding=False
        self.stop_stopping=False
        self.stop_stopped=False
        self.stop_aborting=False
        self.stop_aborted=False
        self.stop_resetting=False
        self.prev_state=0

        #Ex_thread = Thread(target=self.vid_stream)
        self.vid_stream()

    def vid_stream(self):

        self.camera = cv2.VideoCapture(0)
        host_name = "0.0.0.0"
        port = 23336
        app = Flask(__name__)

        @app.route('/video_feed')
        def video_feed():
            # Video streaming route. Put this in the src attribute of an img tag
            return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @app.route('/')
        def index():
            """Video streaming home page."""
            return render_template('index.html')
        # app.debug=False
        # app.run()

        threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=False, use_reloader=False)).start()

    def gen_frames(self):  # generate frame by frame from camera
        while True:
            # Capture frame-by-frame
            success, frame = self.camera.read()  # read the camera frame
            self.edge = cv2.Canny(frame, 100, 200)
            self.pixels = np.asarray(self.edge)

            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', self.edge)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    def Idle(self):
        i=0
        while True:
            print(f'Service 1 is Idle {i} s')
            sleep(1)
            i+=1

            if self.stop_idle:
                break


    def Starting(self):
        #if self.Service.ProcedureCur==1:
        print('Service 1 is starting')
        #self.Service.StateCur=8
        self.update_feedback()
        sleep(4)

    def Execute(self):
        #while self.Service.ProcedureCur==1:
            #if self.Service.ProcedureCur==1:
        i=0

        while True:
            sum=0
            print(f'Service 1 is Executing {i} s')
            #self.pixels=np.asarray(self.edge)
            #print(self.pixels)
            for el in self.pixels:
                for el2 in el:
                    if el2==255: sum+=1
            #print(self.pixels.sum())
            self.AnaView.V=sum
            sleep(1)
            i+=1
            #global stop_threads
            if self.stop_execute:
                break

    def Completing(self):
        #if self.Service.ProcedureCur==1:
        print('Service 1 is completing')
        sleep(4)
        self.Service_SM.Complete(True)
        self.update_feedback()

    def Completed(self):
        #if self.Service.ProcedureCur==1:
        sleep(1)
        print('Service 1 is completed')

################################################################################

    def execute_state(self):

        if self.Service_SM.get_current_state()==16 and self.prev_state!=16:
            self.stop_resetting=True
            self.stop_idle=False
            Idle_thread=Thread(target=self.Idle)
            Idle_thread.start()
            self.prev_state=16
##TODO hier weitermachen
        if self.Service_SM.get_current_state()==8 and self.prev_state!=8:

            self.Starting()
            self.prev_state = 8

        if self.Service_SM.get_current_state()==64 and self.prev_state!=64:
            self.stop_idle=True
            self.stop_execute=False
            Ex_thread=Thread(target=self.Execute)
            Ex_thread.start()
            self.prev_state = 64
            #self.Execute()

        if self.Service_SM.get_current_state()==65536 and self.prev_state!=65536:
            self.stop_execute = True
            self.Completing()
            self.prev_state =65536
            #Ex_thread.join()

        if self.Service_SM.get_current_state()==131072and self.prev_state!=131072:
            self.stop_execute = True
            self.Completed()
            self.prev_state = 131072



#S=Data_Processing(AnaView())
# S.vid_stream()

# while True:
#     print(S.pixels)
#     sleep(5)
# S.Service.Service_SM.act_state=64
# #S.Execute()
# S.execute_state()
