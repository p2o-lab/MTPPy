from Service_control import Service_control
from Procedure import Procedure
import os
import json
import datetime
import cv2
from time import sleep

class Trigger_based(Procedure):
    def __init__(self):
        super(Trigger_based,self).__init__()
        self.IsSelfCompleting=False
        self.ProcedureId=0
        self.IsDefault=True

class Rawdataarchiving(Service_control):
    def __init__(self,Model_Result,VideoStream,Data_sink,Data_format,Status_Message):
        super(Rawdataarchiving,self).__init__()
        self.P_Trigger_based=Trigger_based()
        self.Model_Result=Model_Result
        self.VideoStream=VideoStream
        self.Data_sink=Data_sink
        self.Data_format=Data_format
        self.Status_Message=Status_Message
        self.Data_sink.VOut='Archive/'
        self.Data_format.Vout='.jpeg'

    def Idle(self):
       pass

    def Starting(self):
        if self.save_path=='Archive/':
            if os.path.exists('Archive') == False:
                os.mkdir('Archive')

        self.meta_dict={'Img_name':'0','Img_canny_name':'0','Date':'0','Num_white_pix':0}
        self.Service_SM.Start(SC=True)

    def Execute(self):
        self.Status_Message.Text=f'Saving results to {self.save_path} as {self.save_format}'
        while self.ProcedureCur==self.P_Trigger_based.ProcedureId:
            if self.VideoStream.new_img_flag_archive == True:
                time=datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                self.VideoStream.new_img_flag_archive = False
                #if time[-1] in ['0','5']:
                self.meta_dict['Num_white_pix'] = self.Model_Result.V
                cv2.imwrite(self.save_path+time+'_img'+self.save_format,self.VideoStream.frame)
                self.meta_dict['Img_name']=time+'_img'+self.save_format
                self.meta_dict['Date']=time
                self.meta_dict['Img_canny_name']=time+'_canny'+self.save_format
                out_json=open(self.save_path+time+'.json','w+')
                json.dump(self.meta_dict,out_json)
            if self.stop_execute:
                break


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

    def Sync_operation_mode(self):
        pass

    def Service_activated(self):
        self.save_path=self.Data_sink.VOut
        self.save_format=self.Data_format.Vout


