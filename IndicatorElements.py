from opcua import Client
from DataAssembly import DataAssembly

class IndicatorElement(DataAssembly):
    def __init__(self):
        super(IndicatorElement,self).__init__()
        self.WQC=0

class AnaView(IndicatorElement):
    def __init__(self,node,client):
        super(AnaView,self).__init__()
        self.V=0
        self.VSclMin=0
        self.VSclMax=100
        self.VUnit=0
        self.V_old= self.V
        self.client=client
        self.node = self.client.get_node(node)
        self.ns = self.node.nodeid.NamespaceIndex
        self.Init_sync()

    def limit_check(self):
        if self.V != self.V_old:
            if self.V < self.VSclMin: self.V = self.VSclMin
            elif self.V > self.VSclMax: self.V = self.VSclMax
            self.V_old=self.V
            self.client.get_node(f'ns={self.ns};s=V').set_value(self.V)

    def Init_sync(self):
        self.client.get_node(f'ns={self.ns};s=TagName').set_value(self.TagName)
        self.client.get_node(f'ns={self.ns};s=TagDescription').set_value(self.TagDescription)
        self.client.get_node(f'ns={self.ns};s=WQC').set_value(self.WQC)
        self.client.get_node(f'ns={self.ns};s=V').set_value(self.V)
        self.client.get_node(f'ns={self.ns};s=VSclMin').set_value(self.VSclMin)
        self.client.get_node(f'ns={self.ns};s=VSclMax').set_value(self.VSclMax)
        self.client.get_node(f'ns={self.ns};s=VUnit').set_value(self.VUnit)

    def Runtime(self):
        self.limit_check()

class AnaMon(AnaView):
    def __init__(self):
        super(AnaMon,self).__init__()

        self.OSLevel=0
        self.VAHEn=False
        self.VAHLim=0
        self.VAHAct=False
        self.VWHEn=False
        self.VWHLim=0
        self.VWHAct=False
        self.VTHEn=False
        self.VTHLim=0
        self.VTHAct=False
        self.VTLEn=False
        self.VTLLim=0
        self.VTLAct=False
        self.VWLEn=False
        self.VWLLim=0
        self.VWLAct=False
        self.VALEn=False
        self.VALLim=0
        self.VALAct=False

    def limit_monitoring(self):

        if self.VAHEn==True and self.V >= self.VAHLim: self.VAHAct=True
        else: self.VAHAct=False

        if self.VALEn==True and self.V <= self.VALLim: self.VALAct=True
        else: self.VALAct=False

        if self.VWHEn==True and self.V >= self.VWHLim: self.VWHAct=True
        else: self.VWHAct=False

        if self.VWLEn==True and self.V <= self.VWLLim: self.VWLAct=True
        else: self.VWLAct=False

        if self.VTHEn==True and self.V >= self.VTHLim: self.VTHAct=True
        else: self.VTHAct=False

        if self.VTLEn==True and self.V <= self.VTLLim: self.VTLAct=True
        else: self.VTLAct=False

class DintView(IndicatorElement):
    def __init__(self):
        super(DintView, self).__init__()
        self.V=0
        self.VSclMin=0
        self.VSclMax=100
        self.VUnit=0

    def scale_check(self):
        if self.V < self.VSclMin: self.V = self.VSclMin
        if self.V > self.VSclMax: self.V = self.VSclMax

class DintMon(DintView):
    def __init__(self):
        super(DintMon,self).__init__()

        self.OSLevel=0
        self.VAHEn=False
        self.VAHLim=0
        self.VAHAct=False
        self.VWHEN=False
        self.VWHLim=0
        self.VWHAct=False
        self.VTHEn=False
        self.VTHLim=0
        self.VTHAct=False
        self.VTLEn=False
        self.VTLLim=0
        self.VTLAct=False
        self.VWLEn=False
        self.VWLLim=0
        self.VWLAct=False
        self.VALEn=False
        self.VALLim=0
        self.VALAct=False

        def limit_monitoring(self):

            if self.VAHEn == True and self.V >= self.VAHLim:
                self.VAHAct = True
            else:
                self.VAHAct = False

            if self.VALEn == True and self.V <= self.VALLim:
                self.VALAct = True
            else:
                self.VALAct = False

            if self.VWHEn == True and self.V >= self.VWHLim:
                self.VWHAct = True
            else:
                self.VWHAct = False

            if self.VWLEn == True and self.V <= self.VWLLim:
                self.VWLAct = True
            else:
                self.VWLAct = False

            if self.VTHEn == True and self.V >= self.VTHLim:
                self.VTHAct = True
            else:
                self.VTHAct = False

            if self.VTLEn == True and self.V <= self.VTLLim:
                self.VTLAct = True
            else:
                self.VTLAct = False

class BinView(IndicatorElement):
    def __init__(self):
        super(BinView,self).__init__()
        self.V=False
        self.VState0='text replacement for false'
        self.VState1='text replacement for true'

class BinMon(BinView):
    def __init__(self):
        super(BinMon,self).__init__()
        self.OSLevel=0
        self.VFlutEn=False
        self.VFlutTi=0
        self.VFlutCnt=0
        self.VFlutAct=False

##TODO    def fluttering_detection(self):


class StringView(IndicatorElement):
    def __init__(self,node,client):
        super(StringView,self).__init__()
        self.Text='Text_Value'
        self.Text_old=self.Text
        self.client=client
        self.node = self.client.get_node(node)
        self.ns = self.node.nodeid.NamespaceIndex
        self.Init_sync()

    def Init_sync(self):
        self.client.get_node(f'ns={self.ns};s=TagName').set_value(self.TagName)
        self.client.get_node(f'ns={self.ns};s=TagDescription').set_value(self.TagDescription)
        self.client.get_node(f'ns={self.ns};s=WQC').set_value(self.WQC)
        self.client.get_node(f'ns={self.ns};s=Text').set_value(self.Text)

    def Runtime(self):
        if self.Text != self.Text_old:
            self.Text_old=self.Text
            self.client.get_node(f'ns={self.ns};s=Text').set_value(self.Text)