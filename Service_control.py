from DataAssembly import DataAssembly
import State_Machine as SM
from threading import Thread

class Service_control(DataAssembly):
    def __init__(self):
        super(Service_control,self).__init__()
        self.Service_SM=SM.Statemachine()
        self.WQC=0
        self.OSLevel=0
        self.CommandOP=0
        self.CommandInt=0
        self.CommandExt=0
        self.ProcedureOP=0
        self.ProcedureInt=0
        self.ProcedureExt=0

        self.StateCur=self.Service_SM.get_current_state()
        self.CommandEn=self.Service_SM.get_command_en()

        self.ProcedureCur=0
        self.ProcedureReq=0
        self.PosTextID=0
        self.InteractQuestionID=0
        self.InteractAnswerID=0

        self.StateChannel=False
        self.StateOffAut=False
        self.StateOpAut=False
        self.StateAutAut=False
        self.StateOffOp=False
        self.StateOpOp=False
        self.StateAutOp=False
        self.StateOpAct=False
        self.StateAutAct=False
        self.StateOffAct=True

        self.SrcChannel=False
        self.SrcExtAut=False
        self.SrcIntAut=False
        self.SrcIntOp=False
        self.SrcIntAut=False
        self.SrcExtOp=False
        self.SrcIntAct=False
        self.SrcExtAct=False
        self.ExtAct=False

        self.stop_idle = False
        self.stop_starting = False
        self.stop_execute = False
        self.stop_completing = False
        self.stop_completed = False
        self.stop_resuming = False
        self.stop_paused = False
        self.stop_pausing = False
        self.stop_holding = False
        self.stop_held = False
        self.stop_unholding = False
        self.stop_stopping = False
        self.stop_stopped = False
        self.stop_aborting = False
        self.stop_aborted = False
        self.stop_resetting = False
        self.prev_state = 0

    #TODO runtime in einzelne variablenbasierte eventfunktionen aufsplitten

    #Zustandssteuerung VDI_256_B4 Section 6.5.2
    def State_control(self,SC=False):
        if self.StateOffAct != True:
            if self.StateOpAct==True:
                self.Service_SM.ex_command(self.CommandOP,SC=SC)
            elif self.StateAutAct==True and self.SrcIntAct==True:
                self.Service_SM.ex_command(self.CommandInt,SC=SC)
            elif self.StateAutAct==True and self.SrcExtAct==True:
                self.Service_SM.ex_command(self.CommandExt,SC=SC)


    #Prozedurvorgabe  VDI_256_B4 Section 6.5.3
    #TODO implement procedures as Functions in the individual Service or use the current procedure identifier to communicate only the value
    def Procedure_selection(self):
        if self.Service_SM.get_current_state()==16 and self.StateOffAct != True:

            if self.StateOpAct==True:
                self.ProcedureCur=self.ProcedureOP

            if self.StateAutAct==True and self.SrcIntAct==True:
                self.ProcedureCur=self.ProcedureInt

            if self.StateAutAct==True and self.SrcExtAct==True:
                self.ProcedureCur=self.ProcedureExt

    # Service Operation Mode VDI_256_B4 Section 5.6.1
    def Service_operation_mode(self):
        if self.StateChannel == True:

            if self.StateAutAut == True:
                self.StateOpAct = False
                self.StateAutAct = True
                self.StateOffAct = False

            if self.StateOpAut == True:
                self.StateOpAct = True
                self.StateAutAct = False
                self.StateOffAct = False

            if self.StateOffAut == True:
                self.StateOpAct = False
                self.StateAutAct = False
                self.StateOffAct = True

        elif self.StateChannel==False:

            if self.StateAutOp == True:
                self.StateOpAct = False
                self.StateAutAct = True
                self.StateOffAct = False
                self.StateAutOp = False

            if self.StateOpOp==True:
                self.StateOpAct=True
                self.StateAutAct=False
                self.StateOffAct=False
                self.StateOpOp = False

            if self.StateOffOp == True:
                self.StateOpAct = False
                self.StateAutAct = False
                self.StateOffAct = True
                self.StateOffOp = False


    #TODO Rückmeldung VDI_256_B4 Section 6.5.4
    def update_feedback(self):
        if self.StateOffAct != True:
            if self.StateOpAct == True:
                self.ProcedureReq = self.ProcedureOP

            if self.StateAutAct == True and self.SrcIntAct == True:
                self.ProcedureReq = self.ProcedureInt

            if self.StateAutAct == True and self.SrcExtAct == True:
                self.ProcedureReq = self.ProcedureExt

        self.StateCur=self.Service_SM.get_current_state()
        self.CommandEn=self.Service_SM.get_command_en()

        #self.PosTextID= self.get_PosTextID()

    def procedure_selection(self):
        if self.StateCur ==self.Service_SM.Starting and self.StateOffAct != True:
            if self.StateOpAct == True:
                self.ProcedureCur = self.ProcedureReq

            if self.StateAutAct == True and self.SrcIntAct == True:
                self.ProcedureCur = self.ProcedureReq

            if self.StateAutAct == True and self.SrcExtAct == True:
                self.ProcedureCur = self.ProcedureReq


    #TODO Dienst Bediener Interaktion VDI_256_B4 Section 6.5.6


    #TODO Service Source Mode VDI_256_B4 Section 5.6.2
    def Service_source_mode(self):
        if self.SrcChannel==False and self.StateOffAct != True:
            self.SrcExtAut=False
            self.SrcIntAut=False

            if self.SrcExtOp==True:
                self.SrcIntAct=False
                self.SrcExtAct=True
                self.SrcExtOp=False

            if self.SrcIntOp==True:
                self.SrcIntAct=True
                self.SrcExtAct=False
                self.SrcIntOp=False

    # SrC Channel True is set PEA intern witch Service_source_mode_Aut_Ext and Service_source_mode_Aut_Int

    def Service_source_mode_Aut_Ext(self):
        if self.SrcChannel==True and self.StateOffAct != True:
            self.SrcExtAut=True
            self.SrcIntAut=False

    def Service_source_mode_Aut_Int(self):
        if self.SrcChannel==True and self.StateOffAct != True:
            self.SrcExtAut=False
            self.SrcIntAut=True

    def get_PosTextID(self):
        #Todo Discuss about possible (necessary dialogs)
        if self.StateCur==16:
            PosTextID=0
        else: PosTextID=1
        return PosTextID

    def execute_state(self):
        if self.StateOffAct ==False:
            if self.StateCur == self.Service_SM.Idle and self.prev_state != self.Service_SM.Idle:
                self.stop_resetting = True
                self.stop_idle = False
                Idle_thread = Thread(target=self.Idle)
                Idle_thread.start()
                self.prev_state = self.Service_SM.Idle

            if self.StateCur == self.Service_SM.Starting and self.prev_state != self.Service_SM.Starting:
                self.stop_idle = True
                self.stop_execute = True
                self.stop_starting = False
                Starting_thread = Thread(target=self.Starting)
                Starting_thread.start()
                self.prev_state = self.Service_SM.Starting

            if self.StateCur == self.Service_SM.Execute and self.prev_state != self.Service_SM.Execute:
                self.stop_idle = True
                self.stop_execute = False
                Execute_thread = Thread(target=self.Execute)
                Execute_thread.start()
                self.prev_state = self.Service_SM.Execute

            if self.StateCur == self.Service_SM.Completing and self.prev_state != self.Service_SM.Completing:
                self.stop_execute = True
                self.stop_completing = False
                Completing_thread = Thread(target=self.Completing())
                Completing_thread.start()
                self.prev_state = self.Service_SM.Completing

            if self.StateCur == self.Service_SM.Completed and self.prev_state != self.Service_SM.Completed:
                self.stop_completing = True
                self.stop_completed = False
                Completed_thread = Thread(target=self.Completed)
                Completed_thread.start()
                self.prev_state = self.Service_SM.Completed

            if self.StateCur == self.Service_SM.Resuming and self.prev_state != self.Service_SM.Resuming:
                self.stop_paused = True
                self.stop_resuming = False
                Resuming_thread = Thread(target=self.Resuming())
                Resuming_thread.start()
                self.prev_state = self.Service_SM.Resuming

            if self.StateCur == self.Service_SM.Paused and self.prev_state != self.Service_SM.Paused:
                self.stop_pausing = True
                self.stop_paused = False
                Paused_thread = Thread(target=self.Paused)
                Paused_thread.start()
                self.prev_state = self.Service_SM.Paused

            if self.StateCur == self.Service_SM.Pausing and self.prev_state != self.Service_SM.Pausing:
                self.stop_execute = True
                self.stop_pausing = False
                Pausing_thread = Thread(target=self.Pausing)
                Pausing_thread.start()
                self.prev_state = self.Service_SM.Pausing

            if self.StateCur == self.Service_SM.Holding and self.prev_state != self.Service_SM.Holding:
                self.stop_execute = True
                self.stop_starting = True
                self.stop_completing = True
                self.stop_resuming = True
                self.stop_paused = True
                self.stop_pausing = True
                self.stop_unholding = True
                self.stop_holding = False
                Holding_thread = Thread(target=self.Holding)
                Holding_thread.start()
                self.prev_state = self.Service_SM.Holding

            if self.StateCur == self.Service_SM.Held and self.prev_state != self.Service_SM.Held:
                self.stop_holding = True
                self.stop_held = False
                Held_thread = Thread(target=self.Held)
                Held_thread.start()
                self.prev_state = self.Service_SM.Held

            if self.StateCur == self.Service_SM.Unholding and self.prev_state != self.Service_SM.Unholding:
                self.stop_held = True
                self.stop_unholding = False
                Unholding_thread = Thread(target=self.Unholding)
                Unholding_thread.start()
                self.prev_state = self.Service_SM.Unholding

            if self.StateCur == self.Service_SM.Stopping and self.prev_state != self.Service_SM.Stopping:
                self.stop_execute = True
                self.stop_starting = True
                self.stop_completing = True
                self.stop_resuming = True
                self.stop_paused = True
                self.stop_pausing = True
                self.stop_unholding = True
                self.stop_completed = True
                self.stop_holding = True
                self.stop_held = True
                self.stop_resetting = True
                self.stop_idle = True
                self.stop_stopping = False
                Stopping_thread = Thread(target=self.Stopping)
                Stopping_thread.start()
                self.prev_state = self.Service_SM.Stopping

            if self.StateCur == self.Service_SM.Stopped and self.prev_state != self.Service_SM.Stopped:
                self.stop_stopping = True
                self.stop_stopped = False
                Stopped_thread = Thread(target=self.Stopped)
                Stopped_thread.start()
                self.prev_state = self.Service_SM.Stopped

            if self.StateCur == self.Service_SM.Aborting and self.prev_state != self.Service_SM.Aborting:
                self.stop_execute = True
                self.stop_starting = True
                self.stop_completing = True
                self.stop_resuming = True
                self.stop_paused = True
                self.stop_pausing = True
                self.stop_unholding = True
                self.stop_completed = True
                self.stop_holding = True
                self.stop_held = True
                self.stop_resetting = True
                self.stop_idle = True
                self.stop_stopping = True
                self.stop_stopped = True
                self.stop_aborting = False
                Aborting_thread = Thread(target=self.Aborting)
                Aborting_thread.start()
                self.prev_state = self.Service_SM.Aborting

            if self.StateCur == self.Service_SM.Aborted and self.prev_state != self.Service_SM.Aborted:
                self.stop_aborting = True
                self.stop_aborted = False
                Aborted_thread = Thread(target=self.Aborted)
                Aborted_thread.start()
                self.prev_state = self.Service_SM.Aborted

            if self.StateCur == self.Service_SM.Resetting and self.prev_state != self.Service_SM.Resetting:
                self.stop_completed = True
                self.stop_stopped = True
                self.stop_aborted = True
                self.stop_resetting = False
                Resetting_thread = Thread(target=self.Resetting)
                Resetting_thread.start()
                self.prev_state = self.Service_SM.Resetting
