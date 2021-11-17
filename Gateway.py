from Service_Sync_opc_side import Service_Sync
from Data_Processing import Data_Processing
from Raw_data_aq import Raw_data_aq
from Rawdataarchiving import Rawdataarchiving
from IndicatorElements import AnaView
from AnaView_Sync_opc_side import AnaView_Sync
from opcua import Client
from time import sleep
from PEA_Video_stream import PEA_Video_stream


# class S_Data_Processing_Handler(object):
#     def datachange_notification(self, node, val, data):
#         S_Data_Processing_Sync.Sync_and_execute(node, val)

# class S_Data_Processing_AnaView_Handler(object):
#     def datachange_notification(self,node,val,data):

#start video stream
# Vid_stream=PEA_Video_stream()
# Vid_stream.start_vid_stream(host_name='192.168.178.69',port=23336)

address='opc.tcp://localhost:4840'
client = Client(address)
client.connect()

S_Data_Processing_AnaView=AnaView()
S_Data_Processing=Data_Processing(S_Data_Processing_AnaView)
S_Raw_data_aq=Raw_data_aq()
S_Rawdataarchiving=Rawdataarchiving(S_Data_Processing_AnaView)

S_Data_Processing_Sync=Service_Sync(S_Data_Processing,1,client)
S_Data_Processing_AnaView_Sync=AnaView_Sync(S_Data_Processing_AnaView,2,client)
S_Rawdataarchiving_Sync=Service_Sync(S_Rawdataarchiving,4,client)
S_Raw_data_aq_Sync=Service_Sync(S_Raw_data_aq,3,client)

while True:
    S_Raw_data_aq_Sync.Sync_and_execute()
    S_Data_Processing_Sync.Sync_and_execute()
    S_Data_Processing_AnaView_Sync.Sync_and_execute()
    S_Rawdataarchiving_Sync.Sync_and_execute()
    sleep(0.5)