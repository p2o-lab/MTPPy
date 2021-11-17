import numpy as np
from flask import Flask, render_template, Response, request
import cv2
import threading
from time import sleep

class PEA_Video_stream():
    def __init__(self):
        pass

    def start_vid_stream(self,host_name,port):
        app = Flask(__name__)
        self.camera = cv2.VideoCapture(0)
        #host_name = "0.0.0.0"
        #port = 23336
        app = Flask(__name__)

        @app.route('/video_feed_canny')
        def video_feed_canny():
            # Video streaming route. Put this in the src attribute of an img tag
            return Response(self.gen_frames_canny(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @app.route('/video_feed')
        def video_feed():
            # Video streaming route. Put this in the src attribute of an img tag
            return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @app.route('/shutdown')
        def shutdown():
            self.shutdown_server()
            return 'Server shutting down...'

        @app.route('/')
        def index():
            """Video streaming home page."""
            return render_template('index.html')

        # app.debug=False
        # app.run()

        #threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=False, use_reloader=False)).start()
        app.run(host=host_name, port=port, debug=False, use_reloader=False)

    def gen_frames(self):  # generate frame by frame from camera
        while True:
            # Capture frame-by-frame
            success, frame = self.camera.read()  # read the camera frame

            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    def gen_frames_canny(self):  # generate frame by frame from camera
        while True:
            # Capture frame-by-frame
            success, frame = self.camera.read()  # read the camera frame
            edge = cv2.Canny(frame, 100, 200)

            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', edge)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            #sleep(1)
    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()