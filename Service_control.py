from DataAssembly import DataAssembly
import State_Machine as SM
from threading import Thread
from opcua import Client

class Service_control(DataAssembly):
    def __init__(self,node,client,opc_address):
        super(Service_control,self).__init__()

        self.Service_SM=SM.Statemachine()
        self.WQC=0
        self.OSLevel=0
        self.CommandOp=0
        self.CommandInt=0
        self.CommandExt=0
        self.ProcedureOp=0
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

        self.client = client
        self.node = self.client.get_node(node)
        self.ns = self.node.nodeid.NamespaceIndex
        self.Init_sync()

        # handler = Handler()
        # handler_client = Client(opc_address)
        # handler_client.connect()
        #
        # ServiceControl_nodes = self.client.get_node(f'ns={self.ns};s=ServiceControl').get_children()
        #
        # sub = handler_client.create_subscription(500, handler)
        # handle = sub.subscribe_data_change(ServiceControl_nodes)

    #TODO runtime in einzelne variablenbasierte eventfunktionen aufsplitten

    #Zustandssteuerung VDI_256_B4 Section 6.5.2
    def State_control(self,SC=False):
        if self.StateOffAct != True:
            if self.StateOpAct==True:
                self.Service_SM.ex_command(self.CommandOp,SC=SC)
            elif self.StateAutAct==True and self.SrcIntAct==True:
                self.Service_SM.ex_command(self.CommandInt,SC=SC)
            elif self.StateAutAct==True and self.SrcExtAct==True:
                self.Service_SM.ex_command(self.CommandExt,SC=SC)


    #Prozedurvorgabe  VDI_256_B4 Section 6.5.3
    #TODO implement procedures as Functions in the individual Service or use the current procedure identifier to communicate only the value

    def Procedure_selection(self):
        if self.StateCur == self.Service_SM.Starting and self.StateOffAct != True:
            if self.StateOpAct == True:
                self.ProcedureCur = self.ProcedureReq

            if self.StateAutAct == True and self.SrcIntAct == True:
                self.ProcedureCur = self.ProcedureReq

            if self.StateAutAct == True and self.SrcExtAct == True:
                self.ProcedureCur = self.ProcedureReq

            self.client.get_node(f'ns={self.ns};s=ProcedureCur').set_value(self.ProcedureCur)

    # Service Operation Mode VDI_256_B4 Section 5.6.1
    def Service_operation_mode(self):
        if self.StateOffAct==True:
            if self.StateAutAut or self.StateOpAut or self.StateAutOp or self.StateOpOp:
                self.Service_activated()
                self.execute_state()

        if self.StateChannel == True:

            if self.StateAutAut == True:
                self.StateOpAct = False
                self.StateAutAct = True
                self.StateOffAct = False
                self.client.get_node(f'ns={self.ns};s=StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s=StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s=StateOffAct').set_value(self.StateOffAct)

            if self.StateOpAut == True:
                self.StateOpAct = True
                self.StateAutAct = False
                self.StateOffAct = False
                self.client.get_node(f'ns={self.ns};s=StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s=StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s=StateOffAct').set_value(self.StateOffAct)

            if self.StateOffAut == True:
                self.StateOpAct = False
                self.StateAutAct = False
                self.StateOffAct = True

                self.client.get_node(f'ns={self.ns};s=StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s=StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s=StateOffAct').set_value(self.StateOffAct)



        elif self.StateChannel==False:

            if self.StateAutOp == True:
                self.StateOpAct = False
                self.StateAutAct = True
                self.StateOffAct = False
                self.StateAutOp = False

                self.client.get_node(f'ns={self.ns};s=StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s=StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s=StateOffAct').set_value(self.StateOffAct)
                self.client.get_node(f'ns={self.ns};s=StateAutOp').set_value(self.StateAutOp)

            if self.StateOpOp==True:
                self.StateOpAct=True
                self.StateAutAct=False
                self.StateOffAct=False
                self.StateOpOp = False

                self.client.get_node(f'ns={self.ns};s=StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s=StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s=StateOffAct').set_value(self.StateOffAct)
                self.client.get_node(f'ns={self.ns};s=StateOpOp').set_value(self.StateOpOp)

            if self.StateOffOp == True:
                self.StateOpAct = False
                self.StateAutAct = False
                self.StateOffAct = True
                self.StateOffOp = False

                self.client.get_node(f'ns={self.ns};s=StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s=StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s=StateOffAct').set_value(self.StateOffAct)
                self.client.get_node(f'ns={self.ns};s=StateOffOp').set_value(self.StateOffOp)



    #TODO Rückmeldung VDI_256_B4 Section 6.5.4
    def Update_feedback(self):
        if self.StateOffAct != True:
            if self.StateOpAct == True:
                self.ProcedureReq = self.ProcedureOp
                self.client.get_node(f'ns={self.ns};s=ProcedureReq').set_value(self.ProcedureReq)

            if self.StateAutAct == True and self.SrcIntAct == True:
                self.ProcedureReq = self.ProcedureInt
                self.client.get_node(f'ns={self.ns};s=ProcedureReq').set_value(self.ProcedureReq)

            if self.StateAutAct == True and self.SrcExtAct == True:
                self.ProcedureReq = self.ProcedureExt
                self.client.get_node(f'ns={self.ns};s=ProcedureReq').set_value(self.ProcedureReq)


        self.StateCur=self.Service_SM.get_current_state()
        self.CommandEn=self.Service_SM.get_command_en()
        self.client.get_node(f'ns={self.ns};s=StateCur').set_value(self.StateCur)
        self.client.get_node(f'ns={self.ns};s=CommandEn').set_value(self.CommandEn)

        #self.PosTextID= self.get_PosTextID()


    #TODO Dienst Bediener Interaktion VDI_256_B4 Section 6.5.6


    #TODO Service Source Mode VDI_256_B4 Section 5.6.2
    def Service_source_mode(self):
        if self.SrcChannel==False and self.StateOffAct != True:

            if self.SrcExtAut == True:
                self.SrcExtAut=False
                self.client.get_node(f'ns={self.ns};s=SrcExtAut').set_value(self.SrcExtAut)

            if self.SrcIntAut == True:
                self.SrcIntAut=False
                self.client.get_node(f'ns={self.ns};s=SrcIntAut').set_value(self.SrcIntAut)

            if self.SrcExtOp==True:
                self.SrcIntAct=False
                self.SrcExtAct=True
                self.SrcExtOp=False

                self.client.get_node(f'ns={self.ns};s=SrcIntAct').set_value(self.SrcIntAct)
                self.client.get_node(f'ns={self.ns};s=SrcExtAct').set_value(self.SrcExtAct)
                self.client.get_node(f'ns={self.ns};s=SrcExtOp').set_value(self.SrcExtOp)

            if self.SrcIntOp==True:
                self.SrcIntAct=True
                self.SrcExtAct=False
                self.SrcIntOp=False

                self.client.get_node(f'ns={self.ns};s=SrcIntAct').set_value(self.SrcIntAct)
                self.client.get_node(f'ns={self.ns};s=SrcExtAct').set_value(self.SrcExtAct)
                self.client.get_node(f'ns={self.ns};s=SrcIntOp').set_value(self.SrcIntOp)

    # SrC Channel True is set PEA intern witch Service_source_mode_Aut_Ext and Service_source_mode_Aut_Int

    def Service_source_mode_Aut_Ext(self):
        if self.SrcChannel==True and self.StateOffAct != True:
            self.SrcExtAut=True
            self.SrcIntAut=False
            self.client.get_node(f'ns={self.ns};s=SrcExtAut').set_value(self.SrcExtAut)
            self.client.get_node(f'ns={self.ns};s=SrcIntAut').set_value(self.SrcIntAut)

    def Service_source_mode_Aut_Int(self):
        if self.SrcChannel==True and self.StateOffAct != True:
            self.SrcExtAut=False
            self.SrcIntAut=True
            self.client.get_node(f'ns={self.ns};s=SrcExtAut').set_value(self.SrcExtAut)
            self.client.get_node(f'ns={self.ns};s=SrcIntAut').set_value(self.SrcIntAut)

    # def get_PosTextID(self):
    #     #Todo Discuss about possible (necessary dialogs)
          #Todo implement dialogs
    #     if self.StateCur==16:
    #         PosTextID=0
    #     else: PosTextID=1
    #     return PosTextID

    def execute_state(self):
        if self.StateOffAct ==False:
            if self.StateCur == self.Service_SM.Idle and self.prev_state != self.Service_SM.Idle:
                self.stop_resetting = True
                self.stop_idle = False
                self.prev_state = self.Service_SM.Idle
                Idle_thread = Thread(target=self.Idle)
                Idle_thread.start()

            if self.StateCur == self.Service_SM.Starting and self.prev_state != self.Service_SM.Starting:
                self.stop_idle = True
                self.stop_execute = True
                self.stop_starting = False
                self.prev_state = self.Service_SM.Starting
                Starting_thread = Thread(target=self.Starting)
                Starting_thread.start()

            if self.StateCur == self.Service_SM.Execute and self.prev_state != self.Service_SM.Execute:
                self.stop_idle = True
                self.stop_execute = False
                self.prev_state = self.Service_SM.Execute
                Execute_thread = Thread(target=self.Execute)
                Execute_thread.start()


            if self.StateCur == self.Service_SM.Completing and self.prev_state != self.Service_SM.Completing:
                self.stop_execute = True
                self.stop_completing = False
                self.prev_state = self.Service_SM.Completing
                Completing_thread = Thread(target=self.Completing)
                Completing_thread.start()


            if self.StateCur == self.Service_SM.Completed and self.prev_state != self.Service_SM.Completed:
                self.stop_completing = True
                self.stop_completed = False
                self.prev_state = self.Service_SM.Completed
                Completed_thread = Thread(target=self.Completed)
                Completed_thread.start()


            if self.StateCur == self.Service_SM.Resuming and self.prev_state != self.Service_SM.Resuming:
                self.stop_paused = True
                self.stop_resuming = False
                self.prev_state = self.Service_SM.Resuming
                Resuming_thread = Thread(target=self.Resuming)
                Resuming_thread.start()


            if self.StateCur == self.Service_SM.Paused and self.prev_state != self.Service_SM.Paused:
                self.stop_pausing = True
                self.stop_paused = False
                self.prev_state = self.Service_SM.Paused
                Paused_thread = Thread(target=self.Paused)
                Paused_thread.start()


            if self.StateCur == self.Service_SM.Pausing and self.prev_state != self.Service_SM.Pausing:
                self.stop_execute = True
                self.stop_pausing = False
                self.prev_state = self.Service_SM.Pausing
                Pausing_thread = Thread(target=self.Pausing)
                Pausing_thread.start()


            if self.StateCur == self.Service_SM.Holding and self.prev_state != self.Service_SM.Holding:
                self.stop_execute = True
                self.stop_starting = True
                self.stop_completing = True
                self.stop_resuming = True
                self.stop_paused = True
                self.stop_pausing = True
                self.stop_unholding = True
                self.stop_holding = False
                self.prev_state = self.Service_SM.Holding
                Holding_thread = Thread(target=self.Holding)
                Holding_thread.start()


            if self.StateCur == self.Service_SM.Held and self.prev_state != self.Service_SM.Held:
                self.stop_holding = True
                self.stop_held = False
                self.prev_state = self.Service_SM.Held
                Held_thread = Thread(target=self.Held)
                Held_thread.start()


            if self.StateCur == self.Service_SM.Unholding and self.prev_state != self.Service_SM.Unholding:
                self.stop_held = True
                self.stop_unholding = False
                self.prev_state = self.Service_SM.Unholding
                Unholding_thread = Thread(target=self.Unholding)
                Unholding_thread.start()

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
                self.prev_state = self.Service_SM.Stopping
                Stopping_thread = Thread(target=self.Stopping)
                Stopping_thread.start()


            if self.StateCur == self.Service_SM.Stopped and self.prev_state != self.Service_SM.Stopped:
                self.stop_stopping = True
                self.stop_stopped = False
                self.prev_state = self.Service_SM.Stopped
                Stopped_thread = Thread(target=self.Stopped)
                Stopped_thread.start()


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
                self.prev_state = self.Service_SM.Aborting
                Aborting_thread = Thread(target=self.Aborting)
                Aborting_thread.start()


            if self.StateCur == self.Service_SM.Aborted and self.prev_state != self.Service_SM.Aborted:
                self.stop_aborting = True
                self.stop_aborted = False
                self.prev_state = self.Service_SM.Aborted
                Aborted_thread = Thread(target=self.Aborted)
                Aborted_thread.start()


            if self.StateCur == self.Service_SM.Resetting and self.prev_state != self.Service_SM.Resetting:
                self.stop_completed = True
                self.stop_stopped = True
                self.stop_aborted = True
                self.stop_resetting = False
                self.prev_state = self.Service_SM.Resetting
                Resetting_thread = Thread(target=self.Resetting)
                Resetting_thread.start()


        # if self.StateOffAct == False:
        #     self.stop_idle = True
        #     self.stop_starting = True
        #     self.stop_execute = True
        #     self.stop_completing = True
        #     self.stop_completed = True
        #     self.stop_resuming = True
        #     self.stop_paused = True
        #     self.stop_pausing = True
        #     self.stop_holding = True
        #     self.stop_held = True
        #     self.stop_unholding = True
        #     self.stop_stopping = True
        #     self.stop_stopped = True
        #     self.stop_aborting = True
        #     self.stop_aborted = True
        #     self.stop_resetting = True

    def Runtime(self):
        self.State_control()
        self.Procedure_selection()
        self.Service_operation_mode()
        self.Update_feedback()
        self.Service_source_mode()
        self.Sync_operation_mode()
        self.execute_state()

    def Init_sync(self):
        self.client.get_node(f'ns={self.ns};s=TagName').set_value(self.TagName)
        self.client.get_node(f'ns={self.ns};s=TagDescription').set_value(self.TagDescription)
        self.client.get_node(f'ns={self.ns};s=OSLevel').set_value(self.OSLevel)
        self.client.get_node(f'ns={self.ns};s=WQC').set_value(self.WQC)
        self.client.get_node(f'ns={self.ns};s=CommandOp').set_value(self.CommandOp)
        self.client.get_node(f'ns={self.ns};s=CommandInt').set_value(self.CommandInt)
        self.client.get_node(f'ns={self.ns};s=CommandExt').set_value(self.CommandExt)
        self.client.get_node(f'ns={self.ns};s=ProcedureOp').set_value(self.ProcedureOp)
        self.client.get_node(f'ns={self.ns};s=ProcedureInt').set_value(self.ProcedureInt)
        self.client.get_node(f'ns={self.ns};s=ProcedureExt').set_value(self.ProcedureExt)
        self.client.get_node(f'ns={self.ns};s=StateCur').set_value(self.StateCur)
        self.client.get_node(f'ns={self.ns};s=CommandEn').set_value(self.CommandEn)
        self.client.get_node(f'ns={self.ns};s=ProcedureCur').set_value(self.ProcedureCur)
        self.client.get_node(f'ns={self.ns};s=ProcedureReq').set_value(self.ProcedureReq)
        self.client.get_node(f'ns={self.ns};s=PosTextID').set_value(self.PosTextID)
        self.client.get_node(f'ns={self.ns};s=InteractQuestionID').set_value(self.InteractQuestionID)
        self.client.get_node(f'ns={self.ns};s=InteractAnswerID').set_value(self.InteractAnswerID)
        self.client.get_node(f'ns={self.ns};s=StateChannel').set_value(self.StateChannel)
        self.client.get_node(f'ns={self.ns};s=StateOffAut').set_value(self.StateOffAut)
        self.client.get_node(f'ns={self.ns};s=StateOpAut').set_value(self.StateOpAut)
        self.client.get_node(f'ns={self.ns};s=StateAutAut').set_value(self.StateAutAut)
        self.client.get_node(f'ns={self.ns};s=StateOffOp').set_value(self.StateOffOp)
        self.client.get_node(f'ns={self.ns};s=StateOpOp').set_value(self.StateOpOp)
        self.client.get_node(f'ns={self.ns};s=StateAutOp').set_value(self.StateAutOp)
        self.client.get_node(f'ns={self.ns};s=StateOpAct').set_value(self.StateOpAct)
        self.client.get_node(f'ns={self.ns};s=StateAutAct').set_value(self.StateAutAct)
        self.client.get_node(f'ns={self.ns};s=StateOffAct').set_value(self.StateOffAct)
        self.client.get_node(f'ns={self.ns};s=SrcChannel').set_value(self.SrcChannel)
        self.client.get_node(f'ns={self.ns};s=SrcExtAut').set_value(self.SrcExtAut)
        self.client.get_node(f'ns={self.ns};s=SrcIntAut').set_value(self.SrcIntAut)
        self.client.get_node(f'ns={self.ns};s=SrcIntOp').set_value(self.SrcIntOp)
        self.client.get_node(f'ns={self.ns};s=SrcExtOp').set_value(self.SrcExtOp)
        self.client.get_node(f'ns={self.ns};s=SrcIntAct').set_value(self.SrcIntAct)
        self.client.get_node(f'ns={self.ns};s=SrcExtAct').set_value(self.SrcExtAct)

    def Handler_sync(self,node,val):
        curr_name = node.nodeid.Identifier
        if curr_name in 'OSLevel': self.OSLevel=val
        if curr_name in 'CommandOp': self.CommandOp=val
        if curr_name in 'CommandExt': self.CommandExt=val
        if curr_name in 'ProcedureOp': self.ProcedureOp=val
        if curr_name in 'ProcedureExt': self.ProcedureExt=val
        if curr_name in 'StateOffOp': self.StateOffOp=val
        if curr_name in 'StateOpOp': self.StateOpOp=val
        if curr_name in 'StateAutOp': self.StateAutOp=val
        if curr_name in 'SrcIntOp': self.SrcIntOp=val
        if curr_name in 'SrcExtOp': self.SrcExtOp=val