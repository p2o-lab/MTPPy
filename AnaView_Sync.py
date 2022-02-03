

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
        self.client.get_node(f'ns={self.ns};s=WQC').write_value(self.AnaView.WQC)
        self.client.get_node(f'ns={self.ns};s=TagName').write_value(self.AnaView.TagName)
        self.client.get_node(f'ns={self.ns};s=TagDescription').write_value(self.AnaView.TagDescription)
        self.client.get_node(f'ns={self.ns};s=V').write_value(self.AnaView.V)
        self.client.get_node(f'ns={self.ns};s=VSclMin').write_value(self.AnaView.VSclMin)
        self.client.get_node(f'ns={self.ns};s=VSclMax').write_value(self.AnaView.VSclMax)
        self.client.get_node(f'ns={self.ns};s=VUnit').write_value(self.AnaView.VUnit)
        #self.client.disconnect()

    def sync_and_execute(self):

        self.AnaView.limit_check()
        self.Sync_PEA_POL()