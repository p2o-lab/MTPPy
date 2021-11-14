from DataAssembly import DataAssembly
import State_Machine as SM

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
        self.StateOffAct=False

        self.SrcChannel=False
        self.SrcExtAut=False
        self.SrcIntAut=False
        self.SrcIntOp=False
        self.SrcIntAut=False
        self.SrcExtOp=False
        self.SrcIntAct=False
        self.SrcExtAct=False
        self.ExtAct=False





#TODO runtime in einzelne variablenbasierte eventfunktionen aufsplitten

    #Zustandssteuerung VDI_256_B4 Section 6.5.2
    def State_control(self):
        if self.StateOffAct != True:
            if self.StateOpAct==True:
                self.Service_SM.ex_command(self.CommandOP)
            elif self.StateAutAct==True and self.SrcIntAct==True:
                self.Service_SM.ex_command(self.CommandInt)
            elif self.StateAutAct==True and self.SrcExtAct==True:
                self.Service_SM.ex_command(self.CommandExt)


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

        if self.StateOpAct == True:
            self.ProcedureReq = self.ProcedureOP

        if self.StateAutAct == True and self.SrcIntAct == True:
            self.ProcedureReq = self.ProcedureInt

        if self.StateAutAct == True and self.SrcExtAct == True:
            self.ProcedureReq = self.ProcedureExt

        self.StateCur=self.Service_SM.get_current_state()
        self.CommandEn=self.Service_SM.get_command_en()

        #self.PosTextID= self.get_PosTextID()


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