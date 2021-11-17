from Service_control import Service_control
from Procedure import Procedure


class Prod_Template(Procedure):
    def __init__(self):
        super(Prod_Template,self).__init__()

class Service_template(Service_control):
    def __init__(self,Prod_Template):
        super(Service_template,self).__init__()

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




