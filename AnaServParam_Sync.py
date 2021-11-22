from opcua import Client

class AnaServParam_Sync():
    def __init__(self,AnaServParam,ns,client):
        self.AnaServParam=AnaServParam
        self.ns=ns
        self.client=client

    def Sync_POL_PEA(self):

        self.AnaServParam.OSLevel = self.client.get_node(f'ns={self.ns};s=OSLevel').get_value()
        self.AnaServParam.VExt = self.client.get_node(f'ns={self.ns};s=VExt').get_value()
        self.AnaServParam.VOp = self.client.get_node(f'ns={self.ns};s=VOp').get_value()

        self.AnaServParam.SrcIntOp = self.client.get_node(f'ns={self.ns};s=SrcIntOp').get_value()
        self.AnaServParam.SrcExtOp = self.client.get_node(f'ns={self.ns};s=SrcExtOp').get_value()

        self.AnaServParam.StateAutOp = self.client.get_node(f'ns={self.ns};s=StateAutOp').get_value()
        self.AnaServParam.StateOpOp = self.client.get_node(f'ns={self.ns};s=StateOpOp').get_value()
        self.AnaServParam.StateOffOp = self.client.get_node(f'ns={self.ns};s=StateOffOp').get_value()

    def Sync_PEA_POL(self):

        self.client.get_node(f'ns={self.ns};s=TagName').set_value(self.AnaServParam.TagName)
        self.client.get_node(f'ns={self.ns};s=TagDescription').set_value(self.AnaServParam.TagDescription)
        self.client.get_node(f'ns={self.ns};s=OSLevel').set_value(self.AnaServParam.OSLevel)
        self.client.get_node(f'ns={self.ns};s=WQC').set_value(self.AnaServParam.WQC)
        self.client.get_node(f'ns={self.ns};s=VInt').set_value(self.AnaServParam.VInt)
        self.client.get_node(f'ns={self.ns};s=VReq').set_value(self.AnaServParam.VReq)
        self.client.get_node(f'ns={self.ns};s=VOut').set_value(self.AnaServParam.VOut)
        self.client.get_node(f'ns={self.ns};s=VFbk').set_value(self.AnaServParam.VFbk)
        self.client.get_node(f'ns={self.ns};s=VSclMin').set_value(self.AnaServParam.VSclMin)
        self.client.get_node(f'ns={self.ns};s=VSclMax').set_value(self.AnaServParam.VSclMax)
        self.client.get_node(f'ns={self.ns};s=VUnit').set_value(self.AnaServParam.VUnit)
        self.client.get_node(f'ns={self.ns};s=VMin').set_value(self.AnaServParam.VMin)
        self.client.get_node(f'ns={self.ns};s=VMax').set_value(self.AnaServParam.VMax)
        self.client.get_node(f'ns={self.ns};s=StateChannel').set_value(self.AnaServParam.StateChannel)
        self.client.get_node(f'ns={self.ns};s=StateOffAut').set_value(self.AnaServParam.StateOffAut)
        self.client.get_node(f'ns={self.ns};s=StateOpAut').set_value(self.AnaServParam.StateOpAut)
        self.client.get_node(f'ns={self.ns};s=StateAutAut').set_value(self.AnaServParam.StateAutAut)
        self.client.get_node(f'ns={self.ns};s=StateOpAct').set_value(self.AnaServParam.StateOpAct)
        self.client.get_node(f'ns={self.ns};s=StateAutAct').set_value(self.AnaServParam.StateAutAct)
        self.client.get_node(f'ns={self.ns};s=StateOffAct').set_value(self.AnaServParam.StateOffAct)
        self.client.get_node(f'ns={self.ns};s=SrcChannel').set_value(self.AnaServParam.SrcChannel)
        self.client.get_node(f'ns={self.ns};s=SrcExtAut').set_value(self.AnaServParam.SrcExtAut)
        self.client.get_node(f'ns={self.ns};s=SrcIntAut').set_value(self.AnaServParam.SrcIntAut)
        self.client.get_node(f'ns={self.ns};s=SrcIntAct').set_value(self.AnaServParam.SrcIntAct)
        self.client.get_node(f'ns={self.ns};s=SrcExtAct').set_value(self.AnaServParam.SrcExtAct)

        if self.client.get_node(f'ns={self.ns};s=StateOffOp').get_value() == True or\
            self.client.get_node(f'ns={self.ns};s=StateOpOp').get_value() == True or\
            self.client.get_node(f'ns={self.ns};s=StateAutOp').get_value() == True:

            self.client.get_node(f'ns={self.ns};s=StateAutOp').set_value(self.AnaServParam.StateAutOp)
            self.client.get_node(f'ns={self.ns};s=StateOpOp').set_value(self.AnaServParam.StateOpOp)
            self.client.get_node(f'ns={self.ns};s=StateOffOp').set_value(self.AnaServParam.StateOffOp)


    def sync_and_execute(self):
        self.Sync_POL_PEA()
        self.AnaServParam.operation_mode()
        self.AnaServParam.source_mode()
        self.AnaServParam.scale_check()
        self.AnaServParam.limit_check()
        self.AnaServParam.set_req_value()
        self.Sync_PEA_POL()