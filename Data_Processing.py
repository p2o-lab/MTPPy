from Service_control import Service_control
from src.Procedure import Procedure
from time import sleep
import cv2


class Regression(Procedure):
    def __init__(self):
        super(Regression,self).__init__()
        self.IsSelfCompleting=False
        self.ProcedureId=0
        self.IsDefault=True

class Classification(Procedure):
    def __init__(self):
        super(Classification,self).__init__()
        self.IsSelfCompleting=False
        self.ProcedureId=1
        self.IsDefault=False

class Test_Model(Procedure):
    def __init__(self):
        super(Test_Model,self).__init__()
        self.IsSelfCompleting=False
        self.ProcedureId=2
        self.IsDefault=False

class Data_Processing(Service_control):

    def __init__(self,node,client,opc_address,VideoStream,Model_ID,Result,Confidence_interval,Status_message):
        super(Data_Processing,self).__init__(node=node,client=client,opc_address=opc_address)
        self.VideoStream=VideoStream
        self.Model_ID=Model_ID
        self.Confidence_interval=Confidence_interval
        self.Status_message=Status_message
        self.Result=Result
        self.Result.VSclMax=307200
        self.client=client
        self.Regression=Regression()
        self.Classification=Classification()
        self.Test_Model=Test_Model()
        self.identifier = self.node.nodeid.Identifier

    def Idle(self):
        pass
    def Starting(self):
        #print('Service 1 is starting')
        self.Service_SM.Start( SC=True)

    def Execute(self):
#Todo generate flga to trigger archivin service
        print(f'Service 1 is Executing')
        if self.ProcedureCur==self.Test_Model.ProcedureId:
            while True:
                if self.VideoStream.new_img_flag_process == True:
                    edge = cv2.Canny(self.VideoStream.frame, 100, 200)
                    edsum=edge.sum()/255
                    self.Result.set_v(edsum)
                    #self.client.get_node(f'ns=1;s=V').set_value(self.Result.V)
                    self.VideoStream.model_frame = edge
                    self.VideoStream.new_img_flag_process = False

                if self.stop_execute:
                    break

    def Completing(self):
        print('Service 1 is completing')
        self.Result.set_v(0)
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

    def Sync_operation_mode(self):
        if self.Model_ID.Sync == True:
            self.Model_ID.StateChannel = self.StateChannel
            self.Model_ID.StateOpAct = self.StateOpAct
            self.Model_ID.StateAutAct = self.StateAutAct
            self.Model_ID.StateOffAct = self.StateOffAct

    def Service_activated(self):
        pass
# S=Data_Processing(AnaView())
# S.Execute()