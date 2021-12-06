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

class Raw_data_archiving(Service_control):
    def __init__(self,node,client,opc_address,Model_Result,VideoStream,Data_sink,Data_format,Status_Message):
        super(Raw_data_archiving,self).__init__(node=node,client=client,opc_address=opc_address)
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
        if os.path.exists(self.save_path) == False:
            os.mkdir(self.save_path)

        self.meta_dict={'Img_name':'0','Date':'0','Model_Result':0}
        self.Service_SM.Start(SC=True)

    def Execute(self):
        self.Status_Message.set_text(f'Saving results to {self.save_path} as {self.save_format}')
        while self.ProcedureCur==self.P_Trigger_based.ProcedureId:
            if self.VideoStream.new_img_flag_archive == True:
                time=datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
                time=time[:-5]
                self.meta_dict['Model_Result'] = self.Model_Result.V
                cv2.imwrite(self.save_path+time+'_img'+self.save_format,self.VideoStream.frame)
                self.meta_dict['Img_name']=time+'_img'+self.save_format
                self.meta_dict['Date']=time
                out_json=open(self.save_path+time+'.json','w+')
                json.dump(self.meta_dict,out_json)
                self.VideoStream.new_img_flag_archive = False
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
        self.Status_Message.set_text(' ')
        self.Service_SM.Reset(SC=True)

    def Sync_operation_mode(self):
        if self.Data_sink.Sync == True:
            self.Data_sink.StateChannel = self.StateChannel
            self.Data_sink.StateOpAct = self.StateOpAct
            self.Data_sink.StateAutAct = self.StateAutAct
            self.Data_sink.StateOffAct = self.StateOffAct

        if self.Data_format.Sync == True:
            self.Data_format.StateChannel=self.StateChannel
            self.Data_format.StateOpAct=self.StateOpAct
            self.Data_format.StateAutAct=self.StateAutAct
            self.Data_format.StateOffAct=self.StateOffAct


    def Service_activated(self):
        self.Data_sink.set_VOut()
        self.Data_format.set_VOut()
        if self.Data_sink.VOut[-1]!='/': self.Data_sink.VOut=self.Data_sink.VOut+'/'
        if self.Data_format.VOut[0]!='.':self.Data_format.VOut='.'+self.Data_format.VOut
        self.save_path=self.Data_sink.VOut
        self.save_format=self.Data_format.VOut


