from Service_Sync_opc_side import Service_Sync
from Data_Processing import Data_Processing
from IndicatorElements import AnaView
from AnaView_Sync_opc_side import AnaView_Sync
from opcua import Client
from time import sleep


class S_Data_Processing_Handler(object):
    def datachange_notification(self, node, val, data):
        S_Data_Processing_Sync.Sync_and_execute(node, val)

# class S_Data_Processing_AnaView_Handler(object):
#     def datachange_notification(self,node,val,data):



address='opc.tcp://localhost:4840'
client = Client(address)
client.connect()

S_Data_Processing_AnaView=AnaView()
S_Data_Processing=Data_Processing(S_Data_Processing_AnaView)

S_Data_Processing_Sync=Service_Sync(S_Data_Processing,1,client)
S_Data_Processing_AnaView_Sync=AnaView_Sync(S_Data_Processing_AnaView,2,client)

while True:
    S_Data_Processing_Sync.Sync_and_execute()
    S_Data_Processing_AnaView_Sync.Sync_and_execute()
    sleep(0.5)