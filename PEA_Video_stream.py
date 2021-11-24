import numpy as np
from flask import Flask, render_template, Response, request
import cv2
import threading
from time import sleep

class PEA_Video_stream():
    def __init__(self):
        self.frame = cv2.imread('templates/novid.jpg')
        self.model_frame = cv2.imread('templates/novid.jpg')

        self.new_img_flag_archive = False
        self.new_img_flag_process = False
    def start_vid_stream(self,host_name,port):
        self.host_name=host_name
        self.port=port
        app = Flask(__name__)

        @app.route('/video_feed')
        def video_feed():
            return Response(self.disp_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

        @app.route('/model_out')
        def model_out():
            return Response(self.disp_model_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @app.route('/')
        def index():
            """Video streaming home page."""
            return render_template('index.html')

        threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=False, use_reloader=False)).start()

    def disp_frames(self):
        while True:
            ret, buffer = cv2.imencode('.jpeg', self.frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def disp_model_frames(self):
        while True:
            ret, buffer = cv2.imencode('.jpeg', self.model_frame)
            model_frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + model_frame + b'\r\n')