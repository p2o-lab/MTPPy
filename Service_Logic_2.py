from opcua import Client

class Sync_Class():
    def __init__(self,Service,ns,handler,opc_address):
        self.Service=Service
        self.ns=ns
        self.opc_address=opc_address
        client = Client(self.opc_address)
        client.connect()
        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(client.get_node(f'ns={self.ns};s=Service_Control').get_children())


    def Sync_PEA_POL(self):
        client2=Client(self.opc_address)
        client2.connect()
        client2.get_node(f'ns={self.ns};s=WQC').set_value(self.Service.Service.WQC)
        client2.get_node(f'ns={self.ns};s=CommandInt').set_value(self.Service.Service.CommandInt)
        client2.get_node(f'ns={self.ns};s=ProcedureInt').set_value(self.Service.Service.ProcedureInt)
        client2.get_node(f'ns={self.ns};s=StateCur').set_value(self.Service.Service.StateCur)
        client2.get_node(f'ns={self.ns};s=CommandEn').set_value(self.Service.Service.CommandEn)
        client2.get_node(f'ns={self.ns};s=ProcedureCur').set_value(self.Service.Service.ProcedureCur)
        client2.get_node(f'ns={self.ns};s=ProcedureReq').set_value(self.Service.Service.ProcedureReq)
        client2.get_node(f'ns={self.ns};s=PosTextID').set_value(self.Service.Service.PosTextID)
        client2.get_node(f'ns={self.ns};s=InteractQuestionID').set_value(self.Service.Service.InteractQuestionID)
        client2.get_node(f'ns={self.ns};s=StateChannel').set_value(self.Service.Service.StateChannel)
        client2.get_node(f'ns={self.ns};s=StateOffAut').set_value(self.Service.Service.StateOffAut)
        client2.get_node(f'ns={self.ns};s=StateOpAut').set_value(self.Service.Service.StateOpAut)
        client2.get_node(f'ns={self.ns};s=StateAutAut').set_value(self.Service.Service.StateAutAut)
        client2.get_node(f'ns={self.ns};s=StateOpAct').set_value(self.Service.Service.StateOpAct)
        client2.get_node(f'ns={self.ns};s=StateAutAct').set_value(self.Service.Service.StateAutAct)
        client2.get_node(f'ns={self.ns};s=StateOffAct').set_value(self.Service.Service.StateOffAct)
        client2.get_node(f'ns={self.ns};s=SrcChannel').set_value(self.Service.Service.SrcChannel)
        client2.get_node(f'ns={self.ns};s=SrcExtAut').set_value(self.Service.Service.SrcExtAut)
        client2.get_node(f'ns={self.ns};s=SrcIntAut').set_value(self.Service.Service.SrcIntAut)
        client2.get_node(f'ns={self.ns};s=SrcIntAct').set_value(self.Service.Service.SrcIntAct)
        client2.get_node(f'ns={self.ns};s=SrcExtAct').set_value(self.Service.Service.SrcExtAct)

        if client2.get_node(f'ns={self.ns};s=StateOffOp').get_value() == True or\
            client2.get_node(f'ns={self.ns};s=StateOpOp').get_value() == True or\
            client2.get_node(f'ns={self.ns};s=StateAutOp').get_value() == True:

            client2.get_node(f'ns={self.ns};s=StateAutOp').set_value(self.Service.Service.StateAutOp)
            client2.get_node(f'ns={self.ns};s=StateOpOp').set_value(self.Service.Service.StateOpOp)
            client2.get_node(f'ns={self.ns};s=StateOffOp').set_value(self.Service.Service.StateOffOp)

        client2.disconnect()

    def Sync_POL_PEA(self):
        client3=Client(self.opc_address)
        client3.connect()
        self.Service.Service.OSLevel = client3.get_node(f'ns={self.ns};s=OSLevel').get_value()
        self.Service.Service.CommandOP = client3.get_node(f'ns={self.ns};s=CommandOp').get_value()
        self.Service.Service.CommandExt = client3.get_node(f'ns={self.ns};s=CommandExt').get_value()
        self.Service.Service.ProcedureOP = client3.get_node(f'ns={self.ns};s=ProcedureOp').get_value()
        self.Service.Service.ProcedureExt = client3.get_node(f'ns={self.ns};s=ProcedureExt').get_value()
        self.Service.Service.InteractAnswerID = client3.get_node(f'ns={self.ns};s=InteractAnswerID').get_value()

        self.Service.Service.SrcIntOp = client3.get_node(f'ns={self.ns};s=SrcIntOp').get_value()
        self.Service.Service.SrcExtOp = client3.get_node(f'ns={self.ns};s=SrcExtOp').get_value()

        self.Service.Service.StateOffOp = client3.get_node(f'ns={self.ns};s=StateOffOp').get_value()
        self.Service.Service.StateOpOp = client3.get_node(f'ns={self.ns};s=StateOpOp').get_value()
        self.Service.Service.StateAutOp = client3.get_node(f'ns={self.ns};s=StateAutOp').get_value()

        client3.disconnect()

    def Sync_and_execute(self,node,val):

        curr_nsi = self.ns
        curr_name = node.nodeid.Identifier
        print(f'{curr_name}: {val}')

        self.Sync_POL_PEA()

        self.Service.Service.State_control()
        self.Service.Service.Procedure_selection()
        self.Service.Service.Service_operation_mode()
        self.Service.Service.Service_source_mode()
        self.Service.execute_state()
        self.Service.Service.update_feedback()

        self.Sync_PEA_POL()