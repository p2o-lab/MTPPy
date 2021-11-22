from DataAssembly import DataAssembly

class OperationElement(DataAssembly):
    def __init__(self):
        super(OperationElement,self).__init__()
        self.OSLevel=0

class AnaMan(OperationElement):
    def __init__(self):
        super(AnaMan,self).__init__()

        self.VOut=0
        self.VSclMin=0
        self.VSclMax=100
        self.VUnit=0
        self.VMan=0
        self.VMin=0
        self.VMax=100
        self.VRbk=0
        self.VFbk=0

    def scale_check(self):
        if self.V < self.VSclMin: self.V = self.VSclMin
        if self.V > self.VSclMax: self.V = self.VSclMax

    def limit_check(self):
        if self.V < self.VMin: self.V = self.VMin
        if self.V > self.VMax: self.V = self.VMax

    ## Todo Readback und Feedback implementieren

class AnaManInt(AnaMan):
    def __init__(self):
        super(AnaMan,self).__init__()
        self.WQC=0
        self.VMan=0
        self.VInt=0

        self.SrcChannel=False
        self.SrcManAut=False
        self.SrcManOp=False
        self.SrcIntAut=False
        self.SrcIntOp=False
        self.SrcIntAct=False
        self.SrcManAct=False

    def service_source_mode(self):
        if self.SrcChannel==True :

            if self.SrcManAut == True:
                self.SrcManAct=True
                self.SrcIntAct=False

            if self.SrcIntAut == True:
                self.SrcManAct=False
                self.SrcIntAct=True

        if self.SrcChannel==False:

            if self.SrcIntOp==True:
                self.SrcManAct=False
                self.SrcIntAct=True
                self.SrcIntOp=False

            if self.SrcManOp==True:
                self.SrcManAct=True
                self.SrcIntAct=False
                self.SrcManOp=False

    def set_act_value(self):
        if self.SrcManAct==True:
            self.V=self.VMan
        if self.SrcIntAct==True:
            self.V=self.VInt

class DIntMan(OperationElement):
    def __init__(self):
        super(DIntMan,self).__init__()
        self.VOut = 0
        self.VSclMin = 0
        self.VSclMax = 100
        self.VUnit = 0
        self.VMan = 0
        self.VMin = 0
        self.VMax = 100
        self.VRbk = 0
        self.VFbk = 0

    def scale_check(self):
        if self.V < self.VSclMin: self.V = self.VSclMin
        if self.V > self.VSclMax: self.V = self.VSclMax

    def limit_check(self):
        if self.V < self.VMin: self.V = self.VMin
        if self.V > self.VMax: self.V = self.VMax

    ## Todo Readback und Feedback implementieren
    ## Todo limitierung auf DInt forcen ?

class DIntManInt(DIntMan):
    def __init__(self):
        super(DIntManInt,self).__init__()
        self.WQC=0
        self.VMan=0
        self.VInt=0

        self.SrcChannel=False
        self.SrcManAut=False
        self.SrcManOp=False
        self.SrcIntAut=False
        self.SrcIntOp=False
        self.SrcIntAct=False
        self.SrcManAct=False

    def source_mode(self):
        if self.SrcChannel==True :

            if self.SrcManAut == True:
                self.SrcManAct=True
                self.SrcIntAct=False

            if self.SrcIntAut == True:
                self.SrcManAct=False
                self.SrcIntAct=True

        if self.SrcChannel==False:

            if self.SrcIntOp==True:
                self.SrcManAct=False
                self.SrcIntAct=True
                self.SrcIntOp=False

            if self.SrcManOp==True:
                self.SrcManAct=True
                self.SrcIntAct=False
                self.SrcManOp=False

    def set_act_value(self):
        if self.SrcManAct==True:
            self.V=self.VMan
        if self.SrcIntAct==True:
            self.V=self.VInt

    ##Todo force DInt ?

class BinMan(OperationElement):
    def __init__(self):
        super(BinMan,self).__init__()
        self.VOut=False
        self.VState0='VState0'
        self.VState1='VState1'
        self.VMan=False
        self.VRbk=False
        self.VFbk=False

class BinManInt(BinMan):
    def __init__(self):
        super(BinMan,self).__init__()

        self.WQC = 0
        self.VMan = False
        self.VInt = False

        self.SrcChannel = False
        self.SrcManAut = False
        self.SrcManOp = False
        self.SrcIntAut = False
        self.SrcIntOp = False
        self.SrcIntAct = False
        self.SrcManAct = False

    def source_mode(self):
        if self.SrcChannel == True:

            if self.SrcManAut == True:
                self.SrcManAct = True
                self.SrcIntAct = False

            if self.SrcIntAut == True:
                self.SrcManAct = False
                self.SrcIntAct = True

        if self.SrcChannel == False:

            if self.SrcIntOp == True:
                self.SrcManAct = False
                self.SrcIntAct = True
                self.SrcIntOp = False

            if self.SrcManOp == True:
                self.SrcManAct = True
                self.SrcIntAct = False
                self.SrcManOp = False

    def set_act_value(self):
        if self.SrcManAct == True:
            self.V = self.VMan
        if self.SrcIntAct == True:
            self.V = self.VInt

class AnaServParam(OperationElement):
    def __init__(self):
        super(AnaServParam,self).__init__()
        self.WQC = 0
        self.VExt=0
        self.VOp=0
        self.VInt=0
        self.VReq=0
        self.VOut=0
        self.VFbk=0
        self.VSclMin=0
        self.VSclMax=100
        self.VUnit=0
        self.VMin=0
        self.VMax=100
        self.Sync=False
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
        self.SrcExtOp=False
        self.SrcIntAct=False
        self.SrcExtAct=False

    def operation_mode(self):
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
                self.StateOffAct=True
                self.StateOpOp = False

            if self.StateOffOp == True:
                self.StateOpAct = False
                self.StateAutAct = False
                self.StateOffAct = True
                self.StateOffOp = False

    def source_mode(self):
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

    def scale_check(self):
        if self.VReq < self.VSclMin: self.VReq = self.VSclMin
        if self.VReq > self.VSclMax: self.VReq = self.VSclMax

    def limit_check(self):
        if self.VReq < self.VMin: self.VReq = self.VMin
        if self.VReq > self.VMax: self.VReq = self.VMax


    def set_req_value(self):
        if self.StateOffAct != True:
            if self.StateOpAct==True:
                self.VReq=self.VOp
            if self.StateAutAct ==True and self.SrcExtAct == True :
                self.VReq=self.VExt
            if self.StateAutAct == True and self.SrcIntAct == True:
                self.VReq=self.VInt
    def set_Vout(self):
        self.VOut=self.VReq

class DIntServParam(OperationElement):
    def __init__(self):
        super(DIntServParam,self).__init__()
        self.WQC=0
        self.VExt=0
        self.VOp=0
        self.VInt=0
        self.VReq=0
        self.VOut=0
        self.VFbk=0
        self.VSclMin=0
        self.VSclMax=100
        self.VUnit=0
        self.VMin=0
        self.VMax=100
        self.Sync=False
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
        self.SrcExtOp=False
        self.SrcIntAct=False
        self.SrcExtAct=False

    def operation_mode(self):
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
                self.StateOffAct=True
                self.StateOpOp = False

            if self.StateOffOp == True:
                self.StateOpAct = False
                self.StateAutAct = False
                self.StateOffAct = True
                self.StateOffOp = False

    def source_mode(self):
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

    def scale_check(self):
        if self.VReq < self.VSclMin: self.VReq = self.VSclMin
        if self.VReq > self.VSclMax: self.VReq = self.VSclMax

    def limit_check(self):
        if self.VReq < self.VMin: self.VReq = self.VMin
        if self.VReq > self.VMax: self.VReq = self.VMax


    def set_req_value(self):
        if self.StateOffAct != True:
            if self.StateOpAct==True:
                self.VReq=self.VOp
            if self.StateAutAct ==True and self.SrcExtAct == True :
                self.VReq=self.VExt
            if self.StateAutAct == True and self.SrcIntAct == True:
                self.VReq=self.VInt

class BinServParam(OperationElement):
    def __init__(self):
        super(BinServParam,self).__init__()
        self.WQC = 0
        self.VExt=False
        self.VOp=False
        self.VInt=False
        self.VReq=False
        self.VOut=False
        self.VFbk=False
        self.VState0='text replacement for false'
        self.VState1='text replacement for True'
        self.Sync=False
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
        self.SrcExtOp=False
        self.SrcIntAct=False
        self.SrcExtAct=False

    def operation_mode(self):
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
                self.StateOffAct=True
                self.StateOpOp = False

            if self.StateOffOp == True:
                self.StateOpAct = False
                self.StateAutAct = False
                self.StateOffAct = True
                self.StateOffOp = False

    def source_mode(self):
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

    def set_req_value(self):
        if self.StateOffAct != True:
            if self.StateOpAct==True:
                self.VReq=self.VOp
            if self.StateAutAct ==True and self.SrcExtAct == True :
                self.VReq=self.VExt
            if self.StateAutAct == True and self.SrcIntAct == True:
                self.VReq=self.VInt

class StringServParam(OperationElement):
    def __init__(self):
        super(StringServParam,self).__init__()
        self.WQC = 0
        self.VExt='VExt_string'
        self.VOp='VOp_string'
        self.VInt='VInt_string'
        self.VReq='VReq_string'
        self.VOut='VOut_string'
        self.VFbk='VFbk_string'
        self.Sync=False
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
        self.SrcExtOp=False
        self.SrcIntAct=False
        self.SrcExtAct=False

    def operation_mode(self):
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
                self.StateOffAct=True
                self.StateOpOp = False

            if self.StateOffOp == True:
                self.StateOpAct = False
                self.StateAutAct = False
                self.StateOffAct = True
                self.StateOffOp = False

    def source_mode(self):
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

    def set_req_value(self):
        if self.StateOffAct != True:
            if self.StateOpAct==True:
                self.VReq=self.VOp
            if self.StateAutAct ==True and self.SrcExtAct == True :
                self.VReq=self.VExt
            if self.StateAutAct == True and self.SrcIntAct == True:
                self.VReq=self.VInt








