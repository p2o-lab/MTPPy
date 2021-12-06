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

Serv_previx_rda='Raw_data_aquisitoion'
S_Raw_data_aq_Shutter_speed_setpoint=AnaServParam(node=f'ns=1;s={Serv_previx_rda}.Shutter_speed_setpoint',client=client,opc_address=address)
S_Raw_data_aq_Resolution_setpoint=AnaServParam(node=f'ns=1;s={Serv_previx_rda}.Resolution_setpoint',client=client,opc_address=address)
S_Raw_data_aq_ROI_x0=AnaServParam(node=f'ns=1;s={Serv_previx_rda}.ROI_x0',client=client,opc_address=address)
S_Raw_data_aq_ROI_y0=AnaServParam(node=f'ns=1;s={Serv_previx_rda}.ROI_y0',client=client,opc_address=address)
S_Raw_data_aq_ROI_x_delta=AnaServParam(node=f'ns=1;s={Serv_previx_rda}.ROI_x_delta',client=client,opc_address=address)
S_Raw_data_aq_ROI_y_delta=AnaServParam(node=f'ns=1;s={Serv_previx_rda}.ROI_y_delta',client=client,opc_address=address)
S_Raw_data_aq_Gain_setpoint=AnaServParam(node=f'ns=1;s={Serv_previx_rda}.Gain_setpoint',client=client,opc_address=address)
S_Raw_data_aq_Auto_brightness_setpoint=AnaServParam(node=f'ns=1;s={Serv_previx_rda}.Auto_brightness_setpoint',client=client,opc_address=address)
S_Raw_data_aq_Time_interval_setpoint=AnaServParam(node=f'ns=1;s={Serv_previx_rda}.Time_interval_setpoint',client=client,opc_address=address)
S_Raw_data_aq_Shutter_speed_feedback=AnaView(node=f'ns=1;s={Serv_previx_rda}.Shutter_Speed_feedback',client=client)
S_Raw_data_aq_Resolution_feedback=AnaView(node=f'ns=1;s={Serv_previx_rda}.Resolution_feedback',client=client)
S_Raw_data_aq_Gain_feedback=AnaView(node=f'ns=1;s={Serv_previx_rda}.Gain_feedback',client=client)
S_Raw_data_aq_Auto_Brightness_feedback=AnaView(node=f'ns=1;s={Serv_previx_rda}.Auto_Brightness_feedback',client=client)
S_Raw_data_aq_Webserver_endpoint=StringView(node=f'ns=1;s={Serv_previx_rda}.Webserver_endpoint',client=client)

S_Raw_data_aq=Raw_data_aq(node=f'ns=1;s={Serv_previx_rda}.ServiceControl',client=client,opc_address=address,VideoStream=stream,
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

Serv_previx_dp='Data_Processing'
S_Data_processing_Model_ID=DIntServParam(node=f'ns=1;s={Serv_previx_dp}.Model_ID',client=client,opc_address=address)
S_Data_processing_Result=AnaView(node=f'ns=1;s={Serv_previx_dp}.Result',client=client)
S_Data_processing_Confidence_interval=AnaView(node=f'ns=1;s={Serv_previx_dp}.Confidence_interval',client=client)
S_Data_processing_Status_message=StringView(node=f'ns=1;s={Serv_previx_dp}.Status_message',client=client)
S_Data_processing=Data_Processing(node=f'ns=1;s={Serv_previx_dp}.ServiceControl',client=client,opc_address=address,VideoStream=stream,
                                  Result=S_Data_processing_Result,
                                  Model_ID=S_Data_processing_Model_ID,
                                  Confidence_interval=S_Data_processing_Confidence_interval,
                                  Status_message=S_Data_processing_Status_message)

Serv_previx_da='Raw_data_archiving'
S_Raw_data_arch_Data_sink=StringServParam(node=f'ns=1;s={Serv_previx_da}.Data_sink',client=client,opc_address=address)
S_Raw_data_arch_Data_format=StringServParam(node=f'ns=1;s={Serv_previx_da}.Data_format',client=client,opc_address=address)
S_Raw_data_arch_Status_message=StringView(node=f'ns=1;s={Serv_previx_da}.Status_message',client=client)
S_Raw_data_archiving=Raw_data_archiving(node=f'ns=1;s={Serv_previx_da}.ServiceControl',client=client,opc_address=address,VideoStream=stream,
                                        Model_Result=S_Data_processing_Result,
                                        Data_sink=S_Raw_data_arch_Data_sink,
                                        Data_format=S_Raw_data_arch_Data_format,
                                        Status_Message=S_Raw_data_arch_Status_message)

Serv_previx_i='Illumination'
S_Illumination_Wavelength=AnaServParam(node=f'ns=1;s={Serv_previx_i}.Wavelength_setpoint',client=client,opc_address=address)
S_Illumination_Intensity_setpoint=AnaServParam(node=f'ns=1;s={Serv_previx_i}.Intensity_setpoint',client=client,opc_address=address)
S_Illumination_Frequency_setpoint=AnaServParam(node=f'ns=1;s={Serv_previx_i}.Frequenzy_setpoint',client=client,opc_address=address)
S_Illumination_Duration_setpoint=AnaServParam(node=f'ns=1;s={Serv_previx_i}.Duration_setpoint',client=client,opc_address=address)
S_Illumination_Intensity_feedback=AnaView(node=f'ns=1;s={Serv_previx_i}.Intensity_feedback',client=client)
#S_Illumination_Light_trigger=BinProcessValueIn(node=,client=client,opc_address=address)

S_Illumination=Illuminaton(node=f'ns=1;s={Serv_previx_i}.ServiceControl',client=client,opc_address=address,
                           Wavelength=S_Illumination_Wavelength,
                           Intensity_setpoint=S_Illumination_Intensity_setpoint,
                           Frequency_setpoint=S_Illumination_Frequency_setpoint,
                           Duration_setpoint=S_Illumination_Duration_setpoint,
                           Intensity_feedback=S_Illumination_Intensity_feedback,
                           )


class Module_handler(object):
    def datachange_notification(self, node, val, data):
        print(f'{node} {val}')
        ns=node.nodeid.NamespaceIndex
        identifier = node.nodeid.Identifier

        if f'{Serv_previx_dp}.ServiceControl' in identifier: S_Data_processing.Handler_sync(node, val, identifier)
        if f'{Serv_previx_dp}.Model_ID' in identifier: S_Data_processing_Model_ID.Handler_sync(node, val, identifier)

        if f'{Serv_previx_rda}.ServiceControl' in identifier: S_Raw_data_aq.Handler_sync(node, val, identifier)
        if f'{Serv_previx_rda}.Shutter_speed_setpoint' in identifier: S_Raw_data_aq_Shutter_speed_setpoint.Handler_sync(node, val, identifier)
        if f'{Serv_previx_rda}.Resolution_setpoint' in identifier: S_Raw_data_aq_Resolution_setpoint.Handler_sync(node, val, identifier)
        if f'{Serv_previx_rda}.ROI_x0' in identifier: S_Raw_data_aq_ROI_x0.Handler_sync(node, val, identifier)
        if f'{Serv_previx_rda}.ROI_y0' in identifier: S_Raw_data_aq_ROI_y0.Handler_sync(node, val, identifier)
        if f'{Serv_previx_rda}.ROI_x_delta' in identifier: S_Raw_data_aq_ROI_x_delta.Handler_sync(node, val, identifier)
        if f'{Serv_previx_rda}.ROI_y_delta' in identifier: S_Raw_data_aq_ROI_y_delta.Handler_sync(node, val, identifier)
        if f'{Serv_previx_rda}.Gain_setpoint' in identifier: S_Raw_data_aq_Gain_setpoint.Handler_sync(node, val, identifier)
        if f'{Serv_previx_rda}.Auto_brightness_setpoint' in identifier: S_Raw_data_aq_Auto_brightness_setpoint.Handler_sync(node, val, identifier)
        if f'{Serv_previx_rda}.Time_interval_setpoint' in identifier: S_Raw_data_aq_Time_interval_setpoint.Handler_sync(node, val, identifier)

        if f'{Serv_previx_da}.ServiceControl' in identifier: S_Raw_data_archiving.Handler_sync(node, val, identifier)
        if f'{Serv_previx_da}.Data_sink' in identifier: S_Raw_data_arch_Data_sink.Handler_sync(node, val, identifier)
        if f'{Serv_previx_da}.Data_format' in identifier: S_Raw_data_arch_Data_format.Handler_sync(node, val, identifier)

        if f'{Serv_previx_i}.ServiceControl' in identifier: S_Illumination.Handler_sync(node, val, identifier)
        if f'{Serv_previx_i}.Wavelength' in identifier: S_Illumination_Wavelength.Handler_sync(node, val, identifier)
        if f'{Serv_previx_i}.Intensity_setpoint' in identifier: S_Illumination_Intensity_setpoint.Handler_sync(node, val, identifier)
        if f'{Serv_previx_i}.Frequency_setpoint' in identifier: S_Illumination_Frequency_setpoint.Handler_sync(node, val, identifier)
        if f'{Serv_previx_i}.Duration_setpoint' in identifier: S_Illumination_Duration_setpoint.Handler_sync(node, val, identifier)





Module_Nodes=[]
for node_1 in client.get_objects_node().get_children()[1:]:
    for node_2 in client.get_node(node_1).get_children():
        for node_3 in client.get_node(node_2).get_children(): Module_Nodes.append(node_3)

handler = Module_handler()
handler_client = Client(address)
handler_client.connect()
sub = handler_client.create_subscription(500, handler)
handle = sub.subscribe_data_change(Module_Nodes)


