from Service_control import Service_control
from Procedure import Procedure
from PEA_Video_stream import PEA_Video_stream
import requests


class Continuous(Procedure):
    def __init__(self):
        super(Continuous,self).__init__()
        self.IsSelfCompleting=False
        self.ProcedureId=0
        self.IsDefault=True

class Raw_data_aq(Service_control):
    def __init__(self):
        super(Raw_data_aq,self).__init__()
        self.P_Continuous=Continuous()

    def Idle(self):
       pass

    def Starting(self):
        self.Service_SM.Start( SC=True)

    def Execute(self):
        #if self.ProcedureCur==self.P_Continuous.ProcedureId:
        if self.ProcedureCur==0:
            stream=PEA_Video_stream()
            stream.start_vid_stream(host_name='192.168.178.69',port=23336)

    def Completing(self):
        requests.get(' http://192.168.178.69:23336/shutdown')
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

#i=Raw_data_aq()
