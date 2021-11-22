from Service_control import Service_control
from Procedure import Procedure
from PEA_Video_stream import PEA_Video_stream
import requests
import cv2
from time import sleep

class Free_run(Procedure):
    def __init__(self):
        super(Free_run,self).__init__()
        self.IsSelfCompleting=False
        self.ProcedureId=0
        self.IsDefault=True

class Snapshot(Procedure):
    def __init__(self):
        super(Snapshot,self).__init__()
        self.IsSelfCompleting=True
        self.ProcedureId=1
        self.IsDefault=False

class Hardware_trigger(Procedure):
    def __init__(self):
        super(Hardware_trigger, self).__init__()
        self.IsSelfCompleting = False
        self.ProcedureId = 2
        self.IsDefault = False


class Raw_data_aq(Service_control):
    def __init__(self,ns,client,opc_address,Handler,VideoStream,Shutter_speed_setpoint,Resolution_setpoint,
                 ROI_x0,ROI_y0,ROI_x_delta,ROI_y_delta,Gain_setpoint,Auto_brightness_setpoint,
                 Time_interval_setpoint,Shutter_speed_feedback,Resolution_feedback,Gain_feedback,Auto_Brightness_feedback,
                 Webserver_endpoint):
        super(Raw_data_aq,self).__init__(client,ns,opc_address,Handler)

        #self.client=client
        self.opc_address=opc_address
        self.Free_run=Free_run()
        self.Snapshot=Snapshot()
        self.Hardware_trigger=Hardware_trigger()

        self.Video_stream=VideoStream
        self.Shutter_speed_setpoint=Shutter_speed_setpoint
        self.Resolution_setpoint=Resolution_setpoint
        self.ROI_x0=ROI_x0
        self.ROI_y0=ROI_y0
        self.ROI_x_delta=ROI_x_delta
        self.ROI_y_delta=ROI_y_delta
        self.Gain_setpoint=Gain_setpoint
        self.Auto_brightness_setpoint=Auto_brightness_setpoint
        self.Time_interval_setpoint=Time_interval_setpoint
        self.Shutter_speed_feedback=Shutter_speed_feedback
        self.Resolution_feedback=Resolution_feedback
        self.Gain_feedback=Gain_feedback
        self.Auto_Brightness_feedback=Auto_Brightness_feedback
        self.Webserver_endpoint=Webserver_endpoint

        self.Shutter_speed_setpoint.Sync=True
        self.Resolution_setpoint.Sync=True
        self.ROI_x0.Sync=True
        self.ROI_y0.Sync=True
        self.ROI_x_delta.Sync=True
        self.ROI_y_delta.Sync=True
        self.Gain_setpoint.Sync=True
        self.Auto_brightness_setpoint.Sync=True
        self.Time_interval_setpoint.Sync=True

        self.Video_stream.frame = cv2.imread('templates/novid.jpg')

    def Idle(self):
       self.Webserver_endpoint=f'{self.Video_stream.host_name}:{self.Video_stream.port}'

    def Starting(self):
        self.Time_interval_setpoint.set_Vout()

        if self.ProcedureCur==self.Free_run.ProcedureId:
            self.Video_stream.mode='Free_run'


        elif self.ProcedureCur == self.Snapshot.ProcedureId:
            self.Video_stream.mode = 'Snapshot'

        elif self.ProcedureCur == self.Hardware_trigger.ProcedureId:
            self.Video_stream.mode = 'Hardware_trigger'

        else:
            self.Video_stream.mode = 'Snapshot'

        self.Service_SM.Start( SC=True)

    def Execute(self):
        self.Video_stream.data_aq_active=True
        self.camera = cv2.VideoCapture(0)

        if self.ProcedureCur == self.Free_run.ProcedureId:
            while True:
                _, frame3 = self.camera.read()
                self.Video_stream.frame = frame3
                self.Video_stream.new_img_flag_archive = True
                self.Video_stream.new_img_flag_process = True
                sleep(abs(self.Time_interval_setpoint.VOut))
                if self.stop_execute:
                    break

        if self.ProcedureCur == self.Snapshot.ProcedureId:
            _, frame3 = self.camera.read()
            self.Video_stream.frame = frame3
            self.Video_stream.new_img_flag_archive = True
            self.Video_stream.new_img_flag_process = True
            self.Service_SM.Complete()


        if self.ProcedureCur == self.Hardware_trigger.ProcedureId:
            Trigger=False
            while True:
                if Trigger:
                    _, frame3 = self.camera.read()
                    self.Video_stream.frame = frame3
                    self.Video_stream.new_img_flag_archive = True
                    self.Video_stream.new_img_flag_process = True
                if self.stop_execute:
                        break


    def Completing(self):
        self.Video_stream.data_aq_active = False
        _,frame2=self.camera.read()
        self.Video_stream.frame2 = frame2

        #requests.get(' http://192.168.178.69:23336/shutdown')
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

    def Sync_operation_mode(self):

        if self.Shutter_speed_setpoint.Sync == True:
            self.Shutter_speed_setpoint.StateChannel=self.StateChannel
            self.Shutter_speed_setpoint.StateOpAct=self.StateOpAct
            self.Shutter_speed_setpoint.StateAutAct=self.StateAutAct
            self.Shutter_speed_setpoint.StateOffAct=self.StateOffAct


        if self.Resolution_setpoint.Sync == True:
            self.Resolution_setpoint.StateChannel = self.StateChannel
            self.Resolution_setpoint.StateOpAct = self.StateOpAct
            self.Resolution_setpoint.StateAutAct = self.StateAutAct
            self.Resolution_setpoint.StateOffAct = self.StateOffAct

        if self.ROI_x0.Sync == True:
            self.ROI_x0.StateChannel = self.StateChannel
            self.ROI_x0.StateOpAct = self.StateOpAct
            self.ROI_x0.StateAutAct = self.StateAutAct
            self.ROI_x0.StateOffAct = self.StateOffAct

        if self.ROI_y0.Sync == True:
            self.ROI_y0.StateChannel = self.StateChannel
            self.ROI_y0.StateOpAct = self.StateOpAct
            self.ROI_y0.StateAutAct = self.StateAutAct
            self.ROI_y0.StateOffAct = self.StateOffAct

        if self.ROI_x_delta.Sync == True:
            self.ROI_x_delta.StateChannel = self.StateChannel
            self.ROI_x_delta.StateOpAct = self.StateOpAct
            self.ROI_x_delta.StateAutAct = self.StateAutAct
            self.ROI_x_delta.StateOffAct = self.StateOffAct

        if self.ROI_y_delta.Sync == True:
            self.ROI_y_delta.StateChannel = self.StateChannel
            self.ROI_y_delta.StateOpAct = self.StateOpAct
            self.ROI_y_delta.StateAutAct = self.StateAutAct
            self.ROI_y_delta.StateOffAct = self.StateOffAct

        if self.Gain_setpoint.Sync == True:
            self.Gain_setpoint.StateChannel = self.StateChannel
            self.Gain_setpoint.StateOpAct = self.StateOpAct
            self.Gain_setpoint.StateAutAct = self.StateAutAct
            self.Gain_setpoint.StateOffAct = self.StateOffAct

        if self.Auto_brightness_setpoint.Sync == True:
            self.Auto_brightness_setpoint.StateChannel = self.StateChannel
            self.Auto_brightness_setpoint.StateOpAct = self.StateOpAct
            self.Auto_brightness_setpoint.StateAutAct = self.StateAutAct
            self.Auto_brightness_setpoint.StateOffAct = self.StateOffAct

        if self.Time_interval_setpoint.Sync == True:
            self.Time_interval_setpoint.StateChannel = self.StateChannel
            self.Time_interval_setpoint.StateOpAct = self.StateOpAct
            self.Time_interval_setpoint.StateAutAct = self.StateAutAct
            self.Time_interval_setpoint.StateOffAct = self.StateOffAct

    def Service_activated(self):
        pass

#i=Raw_data_aq()
