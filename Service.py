import State_Machine as SM

class Service:
    def __init__(self):
        self.Service_SM=SM()

        self.TagName='Service'
        self.TagDescription='Service Description'
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
        self.IntOp=False
        self.SrcIntAut=False
        self.SrcExtOp=False
        self.SrcIntAct=False
        self.SrcExtAct=False
        self.ExtAct=False


#TODO add eventbased runtime execution perhaps a function with i old != actual gives back TRUE/False for Triggering

    def Service_runtime(self):

#TODO runtime in einzelne variablenbasierte eventfunktionen aufsplitten

        #Zustandssteuerung VDI_256_B4 Section 6.5.2
        if self.StateOpAct==True:
            self.Service_SM.ex_command(self.CommandOP)
        elif self.StateAutAct==True and self.SrcIntAct==True:
            self.Service_SM.ex_command(self.CommandInt)
        elif self.StateAutAct==True and self.SrcExtAct==True:
            self.Service_SM.ex_command(self.CommandExt)


        #Prozedurvorgabe  VDI_256_B4 Section 6.5.3
        #TODO implement procedures as Functions in the individual Service or use the current procedure identifier to communicate only the value
        if self.Service_SM.get_current_state()==0b10000:

            if self.StateOpAct==True:
                self.ProcedureCur=self.ProcedureOP

            if self.StateAutAct==True and self.SrcIntAct==True:
                self.ProcedureCur=self.ProcedureInt

            if self.StateAutAct==True and self.SrcExtAct==True:
                self.ProcedureCur=self.ProcedureExt

        # Service Operation Mode VDI_256_B4 Section 5.6.1

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


        #TODO Rückmeldung VDI_256_B4 Section 6.5.3

        #TODO Dienst Bediener Interaktion VDI_256_B4 Section 6.5.6

        #TODO Service Source Mode VDI_256_B4 Section 5.6.2

