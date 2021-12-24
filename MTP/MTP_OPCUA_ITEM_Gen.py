import xmltodict
import copy
import json

from dict2xml import dict2xml


with open('manifest.aml', 'r', encoding='utf-8') as xml_file:
    data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()

InstanceList=data_dict['CAEXFile']['InstanceHierarchy'][0]['InternalElement']['InternalElement'][0]['InternalElement'][0]['InternalElement']
SourceList=data_dict['CAEXFile']['InstanceHierarchy'][0]['InternalElement']['InternalElement'][0]['InternalElement'][1]['InternalElement']
OPCUA_Item=data_dict['CAEXFile']['InstanceHierarchy'][0]['InternalElement']['InternalElement'][0]['InternalElement'][1]['InternalElement']['ExternalInterface']
SourceList_intel_new=[]
ID=10000
Service=''
for Param in InstanceList:
    Attribute=Param['Attribute']
    if Param['@RefBaseSystemUnitPath']!='MTPDataObjectSUCLib/DataAssembly/DiagnosticElement/HealthStateView':
        if Param['@Name'] in ['Shutter_speed_setpoint','Resolution_setpoint','ROI_x0','ROI_y0','ROI_x_delta','ROI_y_delta','Gain_setpoint','Auto_brightness_setpoint','Time_interval_setpoint','Shutter_Speed_feedback',
                              'Resolution_feedback','Gain_feedback''Auto_brightness_feedback','Webserver_endpoint']:
            Service ='Raw_data_aquisitoion'
        elif Param['@Name'] in ['Model_ID','Result','Confidence_interval','Status_message_data_processing']:
            Service = 'Data_processing'

        elif Param['@Name'] in ['Raw_data_archiving','Data_sink','Data_format','Status_message_data_archiving']:
            Service = 'Raw_data_archiving'

        elif Param['@Name'] in ['Configuration_Mode','Configuration_ID','Current_configuration_ID']:
            Service = 'Configuration_Mode'

        elif Param['@Name'] in ['Camera_positioning','Absolute_X_setpoint_camera_pos','Absolute_Y_setpoint_camera_pos','Absolute_Z_setpoint_camera_pos',
                                'Absolute_angle_X_Y_setpoint_camera_pos','Absolute_angle_X_Z_setpoint_camera_pos',
                                'Absolute_angle_Y_Z_setpoint_camera_pos','Absolute_X_camera_pos','Absolute_Y_camera_pos'
                                ,'Absolute_Z_camera_pos','Absolute_angle_X_Y_camera_pos','Absolute_angle_X_Z_camera_pos'
                                ,'Absolute_angle_Y_Z_camera_pos','Position_ID_camera_pos']:
            Service = 'Camera_positioning'

        elif Param['@Name'] in ['Camera_position_Zeroing','Absolute_X_camera_upd','Absolute_Y_camera_upd','Absolute_Z_camera_upd',
                                'Absolute_angle_X_Y_camera_upd','Absolute_angle_X_Z_camera_upd','Absolute_angle_Y_Z_camera_upd',
                                'Position_ID_camera_upd1','Position_ID_camera_upd']:
            Service = 'Camera_position_update'

        elif Param['@Name'] in ['Illumination','Wavelength_setpoint','Intensity_setpoint','Frequenzy_setpoint','Duration_setpoint','Intensity_feedback','Light_trigger']:
            Service = 'Illumination'

        elif Param['@Name'] in ['Lens','Absolute_focus_setpoint','Absolute_iris_setpoint','Auto_focus_setpoint','Absolute_focus_feedback','Absolute_iris_feedback','Auto_focus_feedback','Auto_iris_feedback']:
            Service = 'Lens'

        Name = Param['@Name']

        if Param['@Name'] in ['Raw_data_aquisition', 'Data_processing', 'Raw_data_archiving', 'Configuration_mode',
                    'Camera_positioning', 'Camera_position_update', 'Illumination', 'Lens']:
            #print(Param['@Name'])
            Name = 'ServiceControl'
            #print(Name)


        for Att in Attribute:
            if Att['@Name'] not in ['RefID','TagName','TagDescription']:
                Att['@AttributeDataType']='xs:IDREF'
                Att['Value']=ID
                Att['DefaultValue']=0
                OPCUA_Item_new=copy.deepcopy(OPCUA_Item)
                OPCUA_Item_new['@ID']=ID
                OPCUA_Item_new['@Name']=Param['@Name']+'.'+Att['@Name']
                OPCUA_Item_new['Attribute'][0]['Value']=3
                OPCUA_Item_new['Attribute'][1]['Value']=str(Service+'.'+Name+'.'+Att['@Name'])
                OPCUA_Item_new['Attribute'][2]['Value']='urn:freeopcua:python:server'
                SourceList_intel_new.append(copy.deepcopy(OPCUA_Item_new))
                ID+=1
            #print(Att)
data_dict['CAEXFile']['InstanceHierarchy'][0]['InternalElement']['InternalElement'][0]['InternalElement'][0]['InternalElement']=InstanceList
data_dict['CAEXFile']['InstanceHierarchy'][0]['InternalElement']['InternalElement'][0]['InternalElement'][1]['InternalElement']['ExternalInterface']=SourceList_intel_new

#print(InstanceList)

xml_format= xmltodict.unparse(data_dict,pretty=True)
xmlfile=open('manifest_2.aml','w')
xmlfile.write(xml_format)
xmlfile.close()
