
class StringView_Sync():
    def __init__(self,StringView,ns,client):
        self.StringView=StringView
        self.client = client
        self.ns=ns

    def Sync_PEA_POL(self):

        self.client.get_node(f'ns={self.ns};s=WQC').write_value(self.StringView.WQC)
        self.client.get_node(f'ns={self.ns};s=TagName').write_value(self.StringView.TagName)
        self.client.get_node(f'ns={self.ns};s=TagDescription').write_value(self.StringView.TagDescription)
        self.client.get_node(f'ns={self.ns};s=Text').write_value(self.StringView.Text)

    def sync_and_execute(self):

        self.Sync_PEA_POL()