from opcua import Client

class AnaView_Sync():
    def __init__(self,AnaView,ns,client):
        self.AnaView=AnaView
        self.client = client
        self.ns=ns
        # self.opc_address = opc_address
        # client = Client(self.opc_address)
        # client.connect()
        # sub = client.create_subscription(500, handler)
        # handle = sub.subscribe_data_change(client.get_node(f'ns={self.ns};s=AnaView').get_children())

    def Sync_PEA_POL(self):
        #client2 = Client(self.opc_address)
        #self.client.connect()
        self.client.get_node(f'ns={self.ns};s=WQC').set_value(self.AnaView.WQC)
        self.client.get_node(f'ns={self.ns};s=TagName').set_value(self.AnaView.TagName)
        self.client.get_node(f'ns={self.ns};s=TagDescription').set_value(self.AnaView.TagDescription)
        self.client.get_node(f'ns={self.ns};s=V').set_value(self.AnaView.V)
        self.client.get_node(f'ns={self.ns};s=VSclMin').set_value(self.AnaView.VSclMin)
        self.client.get_node(f'ns={self.ns};s=VSclMax').set_value(self.AnaView.VSclMax)
        self.client.get_node(f'ns={self.ns};s=VUnit').set_value(self.AnaView.VUnit)
        #self.client.disconnect()

    def Sync_and_execute(self):

        self.AnaView.limit_check()
        self.Sync_PEA_POL()