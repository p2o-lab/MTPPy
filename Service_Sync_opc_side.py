from opcua import Client

class Service_Sync():
    #def __init__(self,Service,ns,handler,opc_address):
    def __init__(self,Service,ns,client):
        self.Service=Service
        self.ns=ns
        self.client=client
        #self.opc_address=opc_address
        # client = Client(self.opc_address)
        # client.connect()
        # sub = client.create_subscription(500, handler)
        # handle = sub.subscribe_data_change(client.get_node(f'ns={self.ns};s=ServiceControl').get_children())


    def Sync_PEA_POL(self):
        #self.client=Client(self.opc_address)
        #self.client.connect()
        self.client.get_node(f'ns={self.ns};s=WQC').set_value(self.Service.WQC)
        self.client.get_node(f'ns={self.ns};s=CommandInt').set_value(self.Service.CommandInt)
        self.client.get_node(f'ns={self.ns};s=ProcedureInt').set_value(self.Service.ProcedureInt)
        self.client.get_node(f'ns={self.ns};s=StateCur').set_value(self.Service.StateCur)
        self.client.get_node(f'ns={self.ns};s=CommandEn').set_value(self.Service.CommandEn)
        self.client.get_node(f'ns={self.ns};s=ProcedureCur').set_value(self.Service.ProcedureCur)
        self.client.get_node(f'ns={self.ns};s=ProcedureReq').set_value(self.Service.ProcedureReq)
        self.client.get_node(f'ns={self.ns};s=PosTextID').set_value(self.Service.PosTextID)
        self.client.get_node(f'ns={self.ns};s=InteractQuestionID').set_value(self.Service.InteractQuestionID)
        self.client.get_node(f'ns={self.ns};s=StateChannel').set_value(self.Service.StateChannel)
        self.client.get_node(f'ns={self.ns};s=StateOffAut').set_value(self.Service.StateOffAut)
        self.client.get_node(f'ns={self.ns};s=StateOpAut').set_value(self.Service.StateOpAut)
        self.client.get_node(f'ns={self.ns};s=StateAutAut').set_value(self.Service.StateAutAut)
        self.client.get_node(f'ns={self.ns};s=StateOpAct').set_value(self.Service.StateOpAct)
        self.client.get_node(f'ns={self.ns};s=StateAutAct').set_value(self.Service.StateAutAct)
        self.client.get_node(f'ns={self.ns};s=StateOffAct').set_value(self.Service.StateOffAct)
        self.client.get_node(f'ns={self.ns};s=SrcChannel').set_value(self.Service.SrcChannel)
        self.client.get_node(f'ns={self.ns};s=SrcExtAut').set_value(self.Service.SrcExtAut)
        self.client.get_node(f'ns={self.ns};s=SrcIntAut').set_value(self.Service.SrcIntAut)
        self.client.get_node(f'ns={self.ns};s=SrcIntAct').set_value(self.Service.SrcIntAct)
        self.client.get_node(f'ns={self.ns};s=SrcExtAct').set_value(self.Service.SrcExtAct)

        if self.client.get_node(f'ns={self.ns};s=StateOffOp').get_value() == True or\
            self.client.get_node(f'ns={self.ns};s=StateOpOp').get_value() == True or\
            self.client.get_node(f'ns={self.ns};s=StateAutOp').get_value() == True:

            self.client.get_node(f'ns={self.ns};s=StateAutOp').set_value(self.Service.StateAutOp)
            self.client.get_node(f'ns={self.ns};s=StateOpOp').set_value(self.Service.StateOpOp)
            self.client.get_node(f'ns={self.ns};s=StateOffOp').set_value(self.Service.StateOffOp)

        #self.client.disconnect()

    def Sync_POL_PEA(self):
        #client3=Client(self.opc_address)
        #self.client.connect()
        self.Service.OSLevel = self.client.get_node(f'ns={self.ns};s=OSLevel').get_value()
        self.Service.CommandOP = self.client.get_node(f'ns={self.ns};s=CommandOp').get_value()
        self.Service.CommandExt = self.client.get_node(f'ns={self.ns};s=CommandExt').get_value()
        self.Service.ProcedureOP = self.client.get_node(f'ns={self.ns};s=ProcedureOp').get_value()
        self.Service.ProcedureExt = self.client.get_node(f'ns={self.ns};s=ProcedureExt').get_value()
        self.Service.InteractAnswerID = self.client.get_node(f'ns={self.ns};s=InteractAnswerID').get_value()

        self.Service.SrcIntOp = self.client.get_node(f'ns={self.ns};s=SrcIntOp').get_value()
        self.Service.SrcExtOp = self.client.get_node(f'ns={self.ns};s=SrcExtOp').get_value()

        self.Service.StateOffOp = self.client.get_node(f'ns={self.ns};s=StateOffOp').get_value()
        self.Service.StateOpOp = self.client.get_node(f'ns={self.ns};s=StateOpOp').get_value()
        self.Service.StateAutOp = self.client.get_node(f'ns={self.ns};s=StateAutOp').get_value()

        #self.client.disconnect()

    def Sync_and_execute(self):
    #def Sync_and_execute(self,node,val):

        self.Sync_POL_PEA()
        self.Service.State_control()
        self.Service.Procedure_selection()
        self.Service.Service_operation_mode()
        self.Service.Service_source_mode()
        self.Service.execute_state()
        self.Service.update_feedback()

        self.Sync_PEA_POL()