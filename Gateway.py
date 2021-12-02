from Raw_data_aq import Raw_data_aq
from Raw_data_archiving import Raw_data_archiving
from Data_Processing import Data_Processing
from IndicatorElements import AnaView, StringView
from opcua import Client
from time import sleep
from PEA_Video_stream import PEA_Video_stream
from OperationElements import AnaServParam,StringServParam,DIntServParam
from threading import Thread
from Illumination import Illuminaton
#from New_image import New_image


address='opc.tcp://localhost:4840'
client = Client(address)
client.connect()

stream=PEA_Video_stream()
stream.start_vid_stream(host_name='192.168.178.69',port=23336)


S_Raw_data_aq_Shutter_speed_setpoint=AnaServParam(node='ns=7;s=Shutter_speed_setpoint',client=client,opc_address=address)
S_Raw_data_aq_Resolution_setpoint=AnaServParam(node='ns=8;s=Resolution_setpoint',client=client,opc_address=address)
S_Raw_data_aq_ROI_x0=AnaServParam(node='ns=9;s=ROI_x0',client=client,opc_address=address)
S_Raw_data_aq_ROI_y0=AnaServParam(node='ns=10;s=ROI_y0',client=client,opc_address=address)
S_Raw_data_aq_ROI_x_delta=AnaServParam(node='ns=11;s=ROI_x_delta',client=client,opc_address=address)
S_Raw_data_aq_ROI_y_delta=AnaServParam(node='ns=12;s=ROI_y_delta',client=client,opc_address=address)
S_Raw_data_aq_Gain_setpoint=AnaServParam(node='ns=13;s=Gain_setpoint',client=client,opc_address=address)
S_Raw_data_aq_Auto_brightness_setpoint=AnaServParam(node='ns=14;s=Auto_brightness_setpoint',client=client,opc_address=address)
S_Raw_data_aq_Time_interval_setpoint=AnaServParam(node='ns=15;s=Time_interval_setpoint',client=client,opc_address=address)
S_Raw_data_aq_Shutter_speed_feedback=AnaView(node='ns=16;s=Shutter_Speed_feedback',client=client)
S_Raw_data_aq_Resolution_feedback=AnaView(node='ns=17;s=Resolution_feedback',client=client)
S_Raw_data_aq_Gain_feedback=AnaView(node='ns=18;s=Gain_feedback',client=client)
S_Raw_data_aq_Auto_Brightness_feedback=AnaView(node='ns=19;s=Auto_Brightness_feedback',client=client)
S_Raw_data_aq_Webserver_endpoint=StringView(node='ns=20;s=Webserver_endpoint',client=client)

S_Raw_data_aq=Raw_data_aq(node='ns=6;s=Raw_data_aquisitoion',client=client,opc_address=address,VideoStream=stream,
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

def Raw_data_aq_sync():
    while True:
        S_Raw_data_aq_Shutter_speed_setpoint.Runtime()
        S_Raw_data_aq_Resolution_setpoint.Runtime()
        S_Raw_data_aq_ROI_x0.Runtime()
        S_Raw_data_aq_ROI_y0.Runtime()
        S_Raw_data_aq_ROI_x_delta.Runtime()
        S_Raw_data_aq_ROI_y_delta.Runtime()
        S_Raw_data_aq_Gain_setpoint.Runtime()
        S_Raw_data_aq_Auto_brightness_setpoint.Runtime()
        S_Raw_data_aq_Time_interval_setpoint.Runtime()
        S_Raw_data_aq_Shutter_speed_feedback.Runtime()
        S_Raw_data_aq_Resolution_feedback.Runtime()
        S_Raw_data_aq_Gain_feedback.Runtime()
        S_Raw_data_aq_Auto_Brightness_feedback.Runtime()
        S_Raw_data_aq_Webserver_endpoint.Runtime()
        S_Raw_data_aq.Runtime()
        sleep(1)




S_Data_processing_Model_ID=DIntServParam(node='ns=2;s=Model_ID',client=client,opc_address=address)
S_Data_processing_Result=AnaView(node='ns=3;s=Result',client=client)
S_Data_processing_Confidence_interval=AnaView(node='ns=4;s=Confidence_interval',client=client)
S_Data_processing_Status_message=StringView(node='ns=5;s=Status_message',client=client)
S_Data_processing=Data_Processing(node='ns=1;s=Data_Processing',client=client,opc_address=address,VideoStream=stream,
                                  Result=S_Data_processing_Result,
                                  Model_ID=S_Data_processing_Model_ID,
                                  Confidence_interval=S_Data_processing_Confidence_interval,
                                  Status_message=S_Data_processing_Status_message)

def Data_processing_sync():
    while True:
        S_Data_processing_Model_ID.Runtime()
        S_Data_processing_Result.Runtime()
        S_Data_processing_Confidence_interval.Runtime()
        S_Data_processing_Status_message.Runtime()
        S_Data_processing.Runtime()
        sleep(1)

S_Raw_data_arch_Data_sink=StringServParam(node='ns=22;s=Data_sink',client=client,opc_address=address)
S_Raw_data_arch_Data_format=StringServParam(node='ns=23;s=Data_format',client=client,opc_address=address)
S_Raw_data_arch_Status_message=StringView(node='ns=24;s=Status_message',client=client)
S_Raw_data_archiving=Raw_data_archiving(node='ns=21;s=Rawdataarchiving',client=client,opc_address=address,VideoStream=stream,
                                        Model_Result=S_Data_processing_Result,
                                        Data_sink=S_Raw_data_arch_Data_sink,
                                        Data_format=S_Raw_data_arch_Data_format,
                                        Status_Message=S_Raw_data_arch_Status_message)

def Raw_data_archiving_sync():
    while True:
        S_Raw_data_arch_Data_sink.Runtime()
        S_Raw_data_arch_Data_format.Runtime()
        S_Raw_data_arch_Status_message.Runtime()
        S_Raw_data_archiving.Runtime()
        sleep(1)


S_Illumination_Wavelength=AnaServParam(node='ns=49;s=Wavelength_setpoint',client=client,opc_address=address)
S_Illumination_Intensity_setpoint=AnaServParam(node='ns=50;s=Intensity_setpoint',client=client,opc_address=address)
S_Illumination_Frequency_setpoint=AnaServParam(node='ns=51;s=Frequenzy_setpoint',client=client,opc_address=address)
S_Illumination_Duration_setpoint=AnaServParam(node='ns=52;s=Duration_setpoint',client=client,opc_address=address)
S_Illumination_Intensity_feedback=AnaView(node='ns=53;s=Intensity_feedback',client=client)
#S_Illumination_Light_trigger=BinProcessValueIn(node=,client=client,opc_address=address)

S_Illumination=Illuminaton(node='ns=48;s=ServiceControl',client=client,opc_address=address,
                           Wavelength=S_Illumination_Wavelength,
                           Intensity_setpoint=S_Illumination_Intensity_setpoint,
                           Frequency_setpoint=S_Illumination_Frequency_setpoint,
                           Duration_setpoint=S_Illumination_Duration_setpoint,
                           Intensity_feedback=S_Illumination_Intensity_feedback,
                           )

def Illumination_sync():
    while True:
        S_Illumination_Wavelength.Runtime()
        S_Illumination_Intensity_setpoint.Runtime()
        S_Illumination_Frequency_setpoint.Runtime()
        S_Illumination_Duration_setpoint.Runtime()
        S_Illumination_Intensity_feedback.Runtime()
        S_Illumination.Runtime()
        #print('running')
        sleep(1)

class Module_handler(object):
    def datachange_notification(self, node, val, data):
        print(f'{node} {val}')
        ns=node.nodeid.NamespaceIndex

        if ns == 1: S_Data_processing.Handler_sync(node, val)
        if ns == 2: S_Data_processing_Model_ID.Handler_sync(node, val)

        if ns==6: S_Raw_data_aq.Handler_sync(node, val)
        if ns==7: S_Raw_data_aq_Shutter_speed_setpoint.Handler_sync(node, val)
        if ns==8: S_Raw_data_aq_Resolution_setpoint.Handler_sync(node, val)
        if ns==9: S_Raw_data_aq_ROI_x0.Handler_sync(node, val)
        if ns==10: S_Raw_data_aq_ROI_y0.Handler_sync(node, val)
        if ns==11: S_Raw_data_aq_ROI_x_delta.Handler_sync(node, val)
        if ns==12: S_Raw_data_aq_ROI_y_delta.Handler_sync(node, val)
        if ns==13: S_Raw_data_aq_Gain_setpoint.Handler_sync(node, val)
        if ns==14: S_Raw_data_aq_Auto_brightness_setpoint.Handler_sync(node, val)
        if ns==15: S_Raw_data_aq_Time_interval_setpoint.Handler_sync(node, val)

        if ns==21: S_Raw_data_archiving.Handler_sync(node, val)
        if ns==22: S_Raw_data_arch_Data_sink.Handler_sync(node, val)
        if ns==23: S_Raw_data_arch_Data_format.Handler_sync(node, val)

        if ns==48: S_Illumination.Handler_sync(node, val)
        if ns==49: S_Illumination_Wavelength.Handler_sync(node, val)
        if ns==50: S_Illumination_Intensity_setpoint.Handler_sync(node, val)
        if ns==51: S_Illumination_Frequency_setpoint.Handler_sync(node, val)
        if ns==52: S_Illumination_Duration_setpoint.Handler_sync(node, val)





Module_Nodes=[]
for node_1 in client.get_objects_node().get_children()[1:]:
    for node_2 in client.get_node(node_1).get_children():
        for node_3 in client.get_node(node_2).get_children(): Module_Nodes.append(node_3)

handler = Module_handler()
handler_client = Client(address)
handler_client.connect()
sub = handler_client.create_subscription(500, handler)
handle = sub.subscribe_data_change(Module_Nodes)


Raw_data_aq_thread=Thread(target=Raw_data_aq_sync)
Raw_data_aq_thread.start()


Data_processing_thread=Thread(target=Data_processing_sync)
Data_processing_thread.start()


Raw_data_archiving_thread=Thread(target=Raw_data_archiving_sync)
Raw_data_archiving_thread.start()


Illumination_thread=Thread(target=Illumination_sync)
Illumination_thread.start()

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