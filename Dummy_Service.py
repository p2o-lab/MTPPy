import Service
import Procedure
from time import sleep
from threading import Thread
import threading

class D_Service():

    def __init__(self):
        self.Service=Service.Service()
        self.Prod_def=Procedure.Procedure(1,False,False)


    def Idle(self):
        if self.Service.ProcedureCur==1:
            print('Procedure 1 is Idle')

    def Starting(self):
        #if self.Service.ProcedureCur==1:
        print('Procedure 1 is starting')
        #self.Service.StateCur=8
        self.Service.update_feedback()
        sleep(4)
        #self.Service.Service_SM.Start(True)
        #self.Service.update_feedback()


    def Execute(self):
        #while self.Service.ProcedureCur==1:
            #if self.Service.ProcedureCur==1:
        i=0
        while True:
            print(f'Procedure 1 is Executing {i} s')
            sleep(1)
            i+=1
            #global stop_threads
            if self.stop_threads:
                break

    def Completing(self):
        #if self.Service.ProcedureCur==1:
        print('Procedure 1 is completing')
        sleep(4)
        self.Service.Service_SM.Complete(True)
        self.Service.update_feedback()

    def Completed(self):
        #if self.Service.ProcedureCur==1:
        sleep(1)
        print('Procedure 1 is completed')

    def execute_state(self):
        if self.Service.Service_SM.get_current_state()==16:
            self.Idle()

        if self.Service.Service_SM.get_current_state()==8:
            self.Starting()


        if self.Service.Service_SM.get_current_state()==64:
            self.stop_threads=False
            Ex_thread=Thread(target=self.Execute)
            Ex_thread.start()
            #self.Execute()

        if self.Service.Service_SM.get_current_state()==65536:
            self.stop_threads = True
            self.Completing()
            #Ex_thread.join()

        if self.Service.Service_SM.get_current_state()==131072:
            self.stop_threads = True
            self.Completed()



# S=D_Service()
# S.Service.Service_SM.act_state=64
# #S.Execute()
# S.execute_state()
