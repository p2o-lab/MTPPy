from Raw_data_aq import Raw_data_aq
from IndicatorElements import AnaView, StringView
from opcua import Client
from time import sleep
from PEA_Video_stream import PEA_Video_stream
from OperationElements import AnaServParam
from threading import Thread
#from New_image import New_image

# class Test_Handler(object):
#     def datachange_notification(self, node, val, data):
#         print(f'{node} {val}')
# #         S_Data_Processing_Sync.Sync_and_execute(node, val)


# class S_Data_Processing_AnaView_Handler(object):
#     def datachange_notification(self,node,val,data):

address='opc.tcp://localhost:4840'
client = Client(address)
client.connect()

# client2=Client(address)
# client2.connect()
#
# Server_node=client2.get_node('ns=6;s=ServiceControl').get_children()
#
# handler=Test_Handler()
# sub=client2.create_subscription(500,handler)
#
# handle=sub.subscribe_data_change(Server_node)

stream=PEA_Video_stream()
stream.start_vid_stream(host_name='192.168.178.69',port=23336)

S_Raw_data_aq_Shutter_speed_setpoint=AnaServParam()
S_Raw_data_aq_Resolution_setpoint=AnaServParam()
S_Raw_data_aq_ROI_x0=AnaServParam()
S_Raw_data_aq_ROI_y0=AnaServParam()
S_Raw_data_aq_ROI_x_delta=AnaServParam()
S_Raw_data_aq_ROI_y_delta=AnaServParam()
S_Raw_data_aq_Gain_setpoint=AnaServParam()
S_Raw_data_aq_Auto_brightness_setpoint=AnaServParam()
S_Raw_data_aq_Time_interval_setpoint=AnaServParam()
S_Raw_data_aq_Shutter_speed_feedback=AnaView()
S_Raw_data_aq_Resolution_feedback=AnaView()
S_Raw_data_aq_Gain_feedback=AnaView()
S_Raw_data_aq_Auto_Brightness_feedback=AnaView()
S_Raw_data_aq_Webserver_endpoint=StringView()

class Raw_data_aq_handler(object):
    def datachange_notification(self, node, val, data):
        #print(f'{node} {val}')
        S_Raw_data_aq.Handler_sync(node, val)

S_Raw_data_aq=Raw_data_aq(ns=6,client=client,opc_address=address,Handler=Raw_data_aq_handler,VideoStream=stream,
                          Shutter_speed_setpoint=S_Raw_data_aq_Shutter_speed_setpoint,
                          Resolution_setpoint=S_Raw_data_aq_Resolution_setpoint,
                          ROI_x0=S_Raw_data_aq_ROI_x0,
                          ROI_y0=S_Raw_data_aq_ROI_y0,
                          ROI_x_delta=S_Raw_data_aq_ROI_x_delta,
                          ROI_y_delta=S_Raw_data_aq_ROI_y_delta,
                          Gain_setpoint=S_Raw_data_aq_Gain_setpoint,
                          Auto_brightness_setpoint=S_Raw_data_aq_Auto_brightness_setpoint,
                          Time_interval_setpoint=S_Raw_data_aq_Time_interval_setpoint,
                          Shutter_speed_feedback=S_Raw_data_aq_Shutter_speed_feedback,
                          Resolution_feedback=S_Raw_data_aq_Resolution_feedback,
                          Gain_feedback=S_Raw_data_aq_Gain_feedback,
                          Auto_Brightness_feedback=S_Raw_data_aq_Auto_Brightness_feedback,
                          Webserver_endpoint=S_Raw_data_aq_Webserver_endpoint)

def Raw_data_aq_snc():
    while True:

        S_Raw_data_aq.Runtime()
        sleep(1)

Raw_data_aq_thread=Thread(target=Raw_data_aq_snc())
Raw_data_aq_thread.start()

#
#
#
# S_Data_Processing_AnaView=AnaView()
# S_Data_Processing=Data_Processing(S_Data_Processing_AnaView,stream)
#
# S_Rawdataarchiving=Rawdataarchiving(S_Data_Processing_AnaView,stream)
#
# S_Data_Processing_Sync=ServiceControl_Sync(S_Data_Processing,1,client)
# S_Data_Processing_AnaView_Sync=AnaView_Sync(S_Data_Processing_AnaView,3,client)
# S_Rawdataarchiving_Sync=ServiceControl_Sync(S_Rawdataarchiving,21,client)
# S_Raw_data_aq_Sync=ServiceControl_Sync(S_Raw_data_aq,6,client)

# while True:
#     S_Raw_data_aq_Sync.Sync_and_execute()
#     S_Data_Processing_Sync.Sync_and_execute()
#     S_Data_Processing_AnaView_Sync.Sync_and_execute()
#     S_Rawdataarchiving_Sync.Sync_and_execute()
    #sleep(0.5)