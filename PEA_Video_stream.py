import numpy as np
from flask import Flask, render_template, Response, request
import cv2
import threading
from time import sleep

class PEA_Video_stream():
    def __init__(self):
        self.new_img_flag_archive=False
        self.new_img_flag_process=False
        self.data_aq_active=False
        self.mode='Snapshot'
        self.mode_sleep=0
        self.break_var=False
        self.Trigger=False
        self.frame2 = cv2.imread('templates/novid.jpg')

    def start_vid_stream(self,host_name,port):
        #self.camera = cv2.VideoCapture(0)
        self.host_name=host_name
        self.port=port

        app = Flask(__name__)

        @app.route('/video_feed')
        def video_feed():
            # Video streaming route. Put this in the src attribute of an img tag
            return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @app.route('/')
        def index():
            """Video streaming home page."""
            return render_template('index.html')

        threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=False, use_reloader=False)).start()
        #app.run(host=host_name, port=port, debug=False, use_reloader=False)

    def gen_frames(self):  # generate frame by frame from camera
        while True:
            if self.data_aq_active:
                #_,frame=self.camera.read()
                frame=self.frame
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            else:
                ret, buffer = cv2.imencode('.jpg',  self.frame2)
                frame2 = buffer.tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n')
                while self.data_aq_active!=True:
                    sleep(1)
