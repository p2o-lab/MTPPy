
from flask import Flask, render_template, Response
import cv2
import threading
from time import sleep
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
from LoadSpectrum import read_spa

class PEA_Video_stream():
    def __init__(self):
        self.frame = cv2.imread('templates/novid.jpg')
        self.model_frame = cv2.imread('templates/novid.jpg')

        self.new_img_flag_archive = False
        self.new_img_flag_process = False
        self.N=1

    def start_vid_stream(self,host_name,port):
        self.host_name=host_name
        self.port=port
        app = Flask(__name__)

        @app.route('/video_feed')
        def video_feed():
            return Response(self.disp_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

        @app.route('/graph')
        def graph():
            #bar = self.create_plot()
            #return render_template('index2.html', plot=bar)
            plot=self.create_plot()
            return render_template('index2.html', plot=plot)


        @app.route('/model_out')
        def model_out():
            return Response(self.disp_model_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @app.route('/')
        def index():
            """Video streaming home page."""
            return render_template('index.html')


        #threading.Thread(target=self.create_plot).start()
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

    def create_plot(self):

        #path = 'templates/cy785lo.SPA'
        #path2='templates/naph785lo.SPA'
        path2='templates/Acetominophen Caffeine Acetylsalicylic acid.SPA'
        spectra_tmp, wavelength_tmp, title_tmp = read_spa(path2)
        #spectra_tmp2, _, _ = read_spa(path2)

        data = [go.Line(
            x=1/wavelength_tmp,
            y=spectra_tmp)]

        #z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')

        #graph = [1 / wavelength_tmp, spectra_tmp, spectra_tmp, spectra_tmp, spectra_tmp]
        #df = pd.DataFrame(graph)
        #data = [go.Surface(z=df.values)]

        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

        #return graphJSON

# source video stream https://towardsdatascience.com/video-streaming-in-web-browsers-with-opencv-flask-93a38846fe00
# source graph https://blog.heptanalytics.com/flask-plotly-dashboard/

