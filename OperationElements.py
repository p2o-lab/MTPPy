from opcua import Client
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
    def __init__(self,node,client,opc_address):
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

        self.client = client
        self.node = self.client.get_node(node)
        self.ns = self.node.nodeid.NamespaceIndex
        self.identifier = self.node.nodeid.Identifier
        self.Init_sync()

    def operation_mode(self):
        if self.StateChannel == True:

            if self.StateAutAut == True:
                self.StateOpAct = False
                self.StateAutAct = True
                self.StateOffAct = False
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)

            if self.StateOpAut == True:
                self.StateOpAct = True
                self.StateAutAct = False
                self.StateOffAct = False
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)

            if self.StateOffAut == True:
                self.StateOpAct = False
                self.StateAutAct = False
                self.StateOffAct = True
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)

        elif self.StateChannel==False:

            if self.StateAutOp == True:
                self.StateOpAct = False
                self.StateAutAct = True
                self.StateOffAct = False
                self.StateAutOp = False

                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutOp').set_value(self.StateAutOp)

            if self.StateOpOp==True:
                self.StateOpAct=True
                self.StateAutAct=False
                self.StateOffAct=False
                self.StateOpOp = False

                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpOp').set_value(self.StateOpOp)

            if self.StateOffOp == True:
                self.StateOpAct = False
                self.StateAutAct = False
                self.StateOffAct = True
                self.StateOffOp = False

                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffOp').set_value(self.StateOffOp)


    def source_mode(self):
        if self.SrcChannel == False and self.StateOffAct != True and self.Sync == False:

            if self.SrcExtAut == True:
                self.SrcExtAut = False
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtAut').set_value(self.SrcExtAut)

            if self.SrcIntAut == True:
                self.SrcIntAut = False
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntAut').set_value(self.SrcIntAut)

            if self.SrcExtOp == True:
                self.SrcIntAct = False
                self.SrcExtAct = True
                self.SrcExtOp = False

                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntAct').set_value(self.SrcIntAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtAct').set_value(self.SrcExtAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtOp').set_value(self.SrcExtOp)

            if self.SrcIntOp == True:
                self.SrcIntAct = True
                self.SrcExtAct = False
                self.SrcIntOp = False

                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntAct').set_value(self.SrcIntAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtAct').set_value(self.SrcExtAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntOp').set_value(self.SrcIntOp)

        if self.Sync==True:
            self.client.get_node(f'ns={self.ns};s={self.identifier}.StateChannel').set_value(self.StateChannel)
            self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
            self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
            self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)


    def scale_check(self):
        if self.VReq < self.VSclMin: self.VReq = self.VSclMin
        if self.VReq > self.VSclMax: self.VReq = self.VSclMax

    def limit_check(self):
        if self.VReq < self.VMin: self.VReq = self.VMin
        if self.VReq > self.VMax: self.VReq = self.VMax


    def set_VReq(self):
        if self.StateOffAct != True:
            if self.StateOpAct==True:
                self.VReq=self.VOp
                self.client.get_node(f'ns={self.ns};s={self.identifier}.VReq').set_value(self.VReq)
            if self.StateAutAct ==True and self.SrcExtAct == True :
                self.VReq=self.VExt
                self.client.get_node(f'ns={self.ns};s={self.identifier}.VReq').set_value(self.VReq)
            if self.StateAutAct == True and self.SrcIntAct == True:
                self.VReq=self.VInt
                self.client.get_node(f'ns={self.ns};s={self.identifier}.VReq').set_value(self.VReq)

    def set_VOut(self):
        self.VOut=self.VReq
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VOut').set_value(self.VOut)

    def Init_sync(self):
        self.client.get_node(f'ns={self.ns};s={self.identifier}.TagName').set_value(self.TagName)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.TagDescription').set_value(self.TagDescription)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.OSLevel').set_value(self.OSLevel)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.WQC').set_value(self.WQC)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VExt').set_value(self.VExt)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VOp').set_value(self.VOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VInt').set_value(self.VInt)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VReq').set_value(self.VReq)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VOut').set_value(self.VOut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VFbk').set_value(self.VFbk)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VSclMin').set_value(self.VSclMin)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VSclMax').set_value(self.VSclMax)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VUnit').set_value(self.VUnit)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VMin').set_value(self.VMin)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VMax').set_value(self.VMax)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.Sync').set_value(self.Sync)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateChannel').set_value(self.StateChannel)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAut').set_value(self.StateOffAut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAut').set_value(self.StateOpAut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAut').set_value(self.StateAutAut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffOp').set_value(self.StateOffOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpOp').set_value(self.StateOpOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutOp').set_value(self.StateAutOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcChannel').set_value(self.SrcChannel)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtAut').set_value(self.SrcExtAut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntAut').set_value(self.SrcIntAut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntOp').set_value(self.SrcIntOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtOp').set_value(self.SrcExtOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntAct').set_value(self.SrcIntAct)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtAct').set_value(self.SrcExtAct)

    def Handler_sync(self, node, val,ident):
        #curr_name = node.nodeid.Identifier
        if 'OSLevel' in ident: self.OSLevel = val
        if 'VExt' in ident:
            self.VExt = val
            self.scale_check()
            self.limit_check()
            self.set_VReq()

        if 'VOp' in ident:
            self.VOp = val
            self.scale_check()
            self.limit_check()
            self.set_VReq()

        if 'Sync' in ident: self.Sync = val
        if 'StateOffOp' in ident:
            self.StateOffOp = val
            self.operation_mode()
        if 'StateOpOp' in ident:
            self.StateOpOp = val
            self.operation_mode()
        if 'StateAutOp' in ident:
            self.StateAutOp = val
            self.operation_mode()
        if 'SrcIntOp' in ident:
            self.SrcIntOp = val
            self.source_mode()
        if 'SrcExtOp' in ident:
            self.SrcExtOp = val
            self.source_mode()

    # def Runtime(self):
    #     self.operation_mode()
    #     self.source_mode()
    #     self.scale_check()
    #     self.limit_check()
    #     self.set_VReq()

class DIntServParam(OperationElement):
    def __init__(self,node,client,opc_address):
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

        self.client = client
        self.node = self.client.get_node(node)
        self.ns = self.node.nodeid.NamespaceIndex
        self.identifier= self.node.nodeid.Identifier
        self.Init_sync()

    def operation_mode(self):
        if self.StateChannel == True:

            if self.StateAutAut == True:
                self.StateOpAct = False
                self.StateAutAct = True
                self.StateOffAct = False
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)

            if self.StateOpAut == True:
                self.StateOpAct = True
                self.StateAutAct = False
                self.StateOffAct = False
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)

            if self.StateOffAut == True:
                self.StateOpAct = False
                self.StateAutAct = False
                self.StateOffAct = True
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)

        elif self.StateChannel==False:

            if self.StateAutOp == True:
                self.StateOpAct = False
                self.StateAutAct = True
                self.StateOffAct = False
                self.StateAutOp = False

                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutOp').set_value(self.StateAutOp)

            if self.StateOpOp==True:
                self.StateOpAct=True
                self.StateAutAct=False
                self.StateOffAct=False
                self.StateOpOp = False

                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpOp').set_value(self.StateOpOp)

            if self.StateOffOp == True:
                self.StateOpAct = False
                self.StateAutAct = False
                self.StateOffAct = True
                self.StateOffOp = False

                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffOp').set_value(self.StateOffOp)


    def source_mode(self):
        if self.SrcChannel == False and self.StateOffAct != True and self.Sync == False:

            if self.SrcExtAut == True:
                self.SrcExtAut = False
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtAut').set_value(self.SrcExtAut)

            if self.SrcIntAut == True:
                self.SrcIntAut = False
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntAut').set_value(self.SrcIntAut)

            if self.SrcExtOp == True:
                self.SrcIntAct = False
                self.SrcExtAct = True
                self.SrcExtOp = False

                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntAct').set_value(self.SrcIntAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtAct').set_value(self.SrcExtAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtOp').set_value(self.SrcExtOp)

            if self.SrcIntOp == True:
                self.SrcIntAct = True
                self.SrcExtAct = False
                self.SrcIntOp = False

                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntAct').set_value(self.SrcIntAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtAct').set_value(self.SrcExtAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntOp').set_value(self.SrcIntOp)

        if self.Sync==True:
            self.client.get_node(f'ns={self.ns};s={self.identifier}.StateChannel').set_value(self.StateChannel)
            self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
            self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
            self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)


    def scale_check(self):
        if self.VReq < self.VSclMin: self.VReq = self.VSclMin
        if self.VReq > self.VSclMax: self.VReq = self.VSclMax

    def limit_check(self):
        if self.VReq < self.VMin: self.VReq = self.VMin
        if self.VReq > self.VMax: self.VReq = self.VMax


    def set_VReq(self):
        if self.StateOffAct != True:
            if self.StateOpAct==True:
                self.VReq=self.VOp
                self.client.get_node(f'ns={self.ns};s={self.identifier}.VReq').set_value(self.VReq)
            if self.StateAutAct ==True and self.SrcExtAct == True :
                self.VReq=self.VExt
                self.client.get_node(f'ns={self.ns};s={self.identifier}.VReq').set_value(self.VReq)
            if self.StateAutAct == True and self.SrcIntAct == True:
                self.VReq=self.VInt
                self.client.get_node(f'ns={self.ns};s={self.identifier}.VReq').set_value(self.VReq)

    def set_VOut(self):
        self.VOut=self.VReq
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VOut').set_value(self.VOut)

    def Init_sync(self):
        self.client.get_node(f'ns={self.ns};s={self.identifier}.TagName').set_value(self.TagName)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.TagDescription').set_value(self.TagDescription)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.OSLevel').set_value(self.OSLevel)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.WQC').set_value(self.WQC)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VExt').set_value(self.VExt)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VOp').set_value(self.VOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VInt').set_value(self.VInt)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VReq').set_value(self.VReq)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VOut').set_value(self.VOut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VFbk').set_value(self.VFbk)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VSclMin').set_value(self.VSclMin)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VSclMax').set_value(self.VSclMax)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VUnit').set_value(self.VUnit)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VMin').set_value(self.VMin)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VMax').set_value(self.VMax)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.Sync').set_value(self.Sync)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateChannel').set_value(self.StateChannel)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAut').set_value(self.StateOffAut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAut').set_value(self.StateOpAut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAut').set_value(self.StateAutAut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffOp').set_value(self.StateOffOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpOp').set_value(self.StateOpOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutOp').set_value(self.StateAutOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcChannel').set_value(self.SrcChannel)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtAut').set_value(self.SrcExtAut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntAut').set_value(self.SrcIntAut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntOp').set_value(self.SrcIntOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtOp').set_value(self.SrcExtOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntAct').set_value(self.SrcIntAct)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtAct').set_value(self.SrcExtAct)

    def Handler_sync(self, node, val, ident):
        # curr_name = node.nodeid.Identifier
        if 'OSLevel' in ident: self.OSLevel = val
        if 'VExt' in ident:
            self.VExt = val
            self.scale_check()
            self.limit_check()
            self.set_VReq()

        if 'VOp' in ident:
            self.VOp = val
            self.scale_check()
            self.limit_check()
            self.set_VReq()

        if 'Sync' in ident: self.Sync = val
        if 'StateOffOp' in ident:
            self.StateOffOp = val
            self.operation_mode()
        if 'StateOpOp' in ident:
            self.StateOpOp = val
            self.operation_mode()
        if 'StateAutOp' in ident:
            self.StateAutOp = val
            self.operation_mode()
        if 'SrcIntOp' in ident:
            self.SrcIntOp = val
            self.source_mode()
        if 'SrcExtOp' in ident:
            self.SrcExtOp = val
            self.source_mode()

    # def Runtime(self):
    #     self.operation_mode()
    #     self.source_mode()
    #     self.scale_check()
    #     self.limit_check()
    #     self.set_VReq()

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
    def __init__(self,node,client,opc_address):
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

        self.client = client
        self.node = self.client.get_node(node)
        self.ns = self.node.nodeid.NamespaceIndex
        self.identifier= self.node.nodeid.Identifier
        self.Init_sync()

    def operation_mode(self):
        if self.StateChannel == True:

            if self.StateAutAut == True:
                self.StateOpAct = False
                self.StateAutAct = True
                self.StateOffAct = False
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)

            if self.StateOpAut == True:
                self.StateOpAct = True
                self.StateAutAct = False
                self.StateOffAct = False
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)

            if self.StateOffAut == True:
                self.StateOpAct = False
                self.StateAutAct = False
                self.StateOffAct = True
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)

        elif self.StateChannel == False:

            if self.StateAutOp == True:
                self.StateOpAct = False
                self.StateAutAct = True
                self.StateOffAct = False
                self.StateAutOp = False

                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutOp').set_value(self.StateAutOp)

            if self.StateOpOp == True:
                self.StateOpAct = True
                self.StateAutAct = False
                self.StateOffAct = False
                self.StateOpOp = False

                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpOp').set_value(self.StateOpOp)

            if self.StateOffOp == True:
                self.StateOpAct = False
                self.StateAutAct = False
                self.StateOffAct = True
                self.StateOffOp = False

                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffOp').set_value(self.StateOffOp)

    def source_mode(self):
        if self.SrcChannel == False and self.StateOffAct != True and self.Sync == False:

            if self.SrcExtAut == True:
                self.SrcExtAut = False
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtAut').set_value(self.SrcExtAut)

            if self.SrcIntAut == True:
                self.SrcIntAut = False
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntAut').set_value(self.SrcIntAut)

            if self.SrcExtOp == True:
                self.SrcIntAct = False
                self.SrcExtAct = True
                self.SrcExtOp = False

                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntAct').set_value(self.SrcIntAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtAct').set_value(self.SrcExtAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtOp').set_value(self.SrcExtOp)

            if self.SrcIntOp == True:
                self.SrcIntAct = True
                self.SrcExtAct = False
                self.SrcIntOp = False

                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntAct').set_value(self.SrcIntAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtAct').set_value(self.SrcExtAct)
                self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntOp').set_value(self.SrcIntOp)

        if self.Sync == True:
            self.client.get_node(f'ns={self.ns};s={self.identifier}.StateChannel').set_value(self.StateChannel)
            self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
            self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
            self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)

    def set_VReq(self):
        if self.StateOffAct != True:
            if self.StateOpAct == True:
                self.VReq = self.VOp
                self.client.get_node(f'ns={self.ns};s={self.identifier}.VReq').set_value(self.VReq)
            if self.StateAutAct == True and self.SrcExtAct == True:
                self.VReq = self.VExt
                self.client.get_node(f'ns={self.ns};s={self.identifier}.VReq').set_value(self.VReq)
            if self.StateAutAct == True and self.SrcIntAct == True:
                self.VReq = self.VInt
                self.client.get_node(f'ns={self.ns};s={self.identifier}.VReq').set_value(self.VReq)

    def set_VOut(self):
        self.VOut = self.VReq
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VOut').set_value(self.VOut)

    def Init_sync(self):
        self.client.get_node(f'ns={self.ns};s={self.identifier}.TagName').set_value(self.TagName)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.TagDescription').set_value(self.TagDescription)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.OSLevel').set_value(self.OSLevel)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.WQC').set_value(self.WQC)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VExt').set_value(self.VExt)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VOp').set_value(self.VOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VInt').set_value(self.VInt)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VReq').set_value(self.VReq)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VOut').set_value(self.VOut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.VFbk').set_value(self.VFbk)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.Sync').set_value(self.Sync)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateChannel').set_value(self.StateChannel)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAut').set_value(self.StateOffAut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAut').set_value(self.StateOpAut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAut').set_value(self.StateAutAut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffOp').set_value(self.StateOffOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpOp').set_value(self.StateOpOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutOp').set_value(self.StateAutOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOpAct').set_value(self.StateOpAct)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateAutAct').set_value(self.StateAutAct)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.StateOffAct').set_value(self.StateOffAct)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcChannel').set_value(self.SrcChannel)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtAut').set_value(self.SrcExtAut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntAut').set_value(self.SrcIntAut)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntOp').set_value(self.SrcIntOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtOp').set_value(self.SrcExtOp)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcIntAct').set_value(self.SrcIntAct)
        self.client.get_node(f'ns={self.ns};s={self.identifier}.SrcExtAct').set_value(self.SrcExtAct)


    def Handler_sync(self, node, val, ident):

        if  'OSLevel'in ident: self.OSLevel = val

        if 'VExt' in ident:
            self.VExt = val
            self.set_VReq()

        if 'VOp' in ident:
            self.VOp = val
            self.set_VReq()

        if 'Sync' in ident: self.Sync = val

        if 'StateOffOp' in ident:
            self.StateOffOp = val
            self.operation_mode()

        if 'StateOpOp' in ident:
            self.StateOpOp = val
            self.operation_mode()

        if 'StateAutOp' in ident:
            self.StateAutOp = val
            self.operation_mode()

        if 'SrcIntOp' in ident:
            self.SrcIntOp = val
            self.source_mode()

        if 'SrcExtOp' in ident:
            self.SrcExtOp = val
            self.source_mode()
