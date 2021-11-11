import Service
import Procedure
from time import sleep
from threading import Thread
import threading

class D_Service():

    def __init__(self):
        self.Service=Service.Service()
        self.Prod_def=Procedure.Procedure(1,False,False)
        self.stop_idle=False
        self.stop_starting=False
        self.stop_execute=False
        self.stop_completing=False
        self.stop_completed=False
        self.stop_resuming=False
        self.stop_paused=False
        self.stop_pausing=False
        self.stop_holding=False
        self.stop_held=False
        self.stop_unholding=False
        self.stop_stopping=False
        self.stop_stopped=False
        self.stop_aborting=False
        self.stop_aborted=False
        self.stop_resetting=False
        self.prev_state=0

    def Idle(self):
        i=0
        while True:
            print(f'Service 1 is Idle {i} s')
            sleep(1)
            i+=1

            if self.stop_idle:
                break


    def Starting(self):
        #if self.Service.ProcedureCur==1:
        print('Service 1 is starting')
        #self.Service.StateCur=8
        self.Service.update_feedback()
        sleep(4)

    def Execute(self):
        #while self.Service.ProcedureCur==1:
            #if self.Service.ProcedureCur==1:
        i=0
        while True:
            print(f'Service 1 is Executing {i} s')
            sleep(1)
            i+=1
            #global stop_threads
            if self.stop_execute:
                break

    def Completing(self):
        #if self.Service.ProcedureCur==1:
        print('Service 1 is completing')
        sleep(4)
        self.Service.Service_SM.Complete(True)
        self.Service.update_feedback()

    def Completed(self):
        #if self.Service.ProcedureCur==1:
        sleep(1)
        print('Service 1 is completed')

################################################################################

    def execute_state(self):

        if self.Service.Service_SM.get_current_state()==16 and self.prev_state!=16:
            self.stop_resetting=True
            self.stop_idle=False
            Idle_thread=Thread(target=self.Idle)
            Idle_thread.start()
            self.prev_state=16
##TODO hier weitermachen
        if self.Service.Service_SM.get_current_state()==8 and self.prev_state!=8:

            self.Starting()
            self.prev_state = 8

        if self.Service.Service_SM.get_current_state()==64 and self.prev_state!=64:
            self.stop_idle=True
            self.stop_execute=False
            Ex_thread=Thread(target=self.Execute)
            Ex_thread.start()
            self.prev_state = 64
            #self.Execute()

        if self.Service.Service_SM.get_current_state()==65536 and self.prev_state!=65536:
            self.stop_execute = True
            self.Completing()
            self.prev_state =65536
            #Ex_thread.join()

        if self.Service.Service_SM.get_current_state()==131072and self.prev_state!=131072:
            self.stop_execute = True
            self.Completed()
            self.prev_state = 131072



# S=D_Service()
# S.Service.Service_SM.act_state=64
# #S.Execute()
# S.execute_state()
