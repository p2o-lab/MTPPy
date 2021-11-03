import Service
import Procedure
from time import sleep

class D_Service():
    def __init__(self):
        self.Service=Service.Service()
        self.Prod_def=Procedure.Procedure(1,False,False)

    def Idle(self):
        if self.Service.ProcedureCur==1:
            print('Procedure 1 is Idle')

    def Starting(self):
        if self.Service.ProcedureCur==1:
            print('Procedure 1 is starting')
            sleep(1)
            self.Service.Service_SM.Start(True)


    def Execute(self):
        while self.Service.ProcedureCur==32:
            if self.Service.ProcedureCur==1:
                print('Procedure 1 is Executing')
                sleep(1)

    def Completing(self):
        if self.Service.ProcedureCur==1:
            print('Procedure 1 is completing')
            sleep(1)
            self.Service.Service_SM.Complete(True)

    def Completed(self):
        if self.Service.ProcedureCur==1:
            print('Procedure 1 is completed')
            sleep(1)

    def execute_state(self):
        if self.Service.Service_SM.get_current_state()==16:
            self.Idle()
        if self.Service.Service_SM.get_current_state()==8:
            self.Starting()
        if self.Service.Service_SM.get_current_state()==64:
            self.Execute()
        if self.Service.Service_SM.get_current_state()==65536:
            self.Completing()
        if self.Service.Service_SM.get_current_state()==131072:
            self.Completed()

#S=D_Service()
