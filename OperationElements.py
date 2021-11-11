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

    def service_source_mode(self):
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
