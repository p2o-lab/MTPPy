from Service_control import Service_control
from Procedure import Procedure


class Prod_Template(Procedure):
    def __init__(self):
        super(Prod_Template,self).__init__()

class Service_template():
    def __init__(self,Service_control,node,client,opc_address,Handler,Prod_Template):
        super(Service_template,self).__init__(client,node,opc_address,Handler)

    def Idle(self):
       pass

    def Starting(self):
        self.Service_SM.Start(SC=True)

    def Execute(self):
        pass

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
        pass
