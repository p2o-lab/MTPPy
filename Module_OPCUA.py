from opcua import Server
class Module_OPCUA_class:
    def __init__(self):

        Service_control_dict={
                    'TagName':{'init':'TagName','datatype':12},
                    'TagDescription':{'init':'TagDescription','datatype':12},
                    'WQC':{'init':0,'datatype':6},
                    'OSLevel':{'init':0,'datatype':6},
                    'CommandOp':{'init':0,'datatype':6},
                    'CommandInt':{'init':0,'datatype':6},
                    'CommandExt':{'init':0,'datatype':6},
                    'ProcedureOp':{'init':1,'datatype':6},
                    'ProcedureInt':{'init':0,'datatype':6},
                    'ProcedureExt':{'init':0,'datatype':6},
                    'StateCur':{'init':0,'datatype':6},
                    'CommandEn':{'init':0,'datatype':6},
                    'ProcedureCur':{'init':0,'datatype':6},
                    'ProcedureReq':{'init':0,'datatype':6},
                    'PosTextID':{'init':0,'datatype':6},
                    'InteractQuestionID':{'init':0,'datatype':6},
                    'InteractAnswerID':{'init':0,'datatype':6},
                    'StateChannel':{'init':False,'datatype':1},
                    'StateOffAut':{'init':False,'datatype':1},
                    'StateOpAut':{'init':False,'datatype':1},
                    'StateAutAut':{'init':False,'datatype':1},
                    'StateOffOp':{'init':False,'datatype':1},
                    'StateOpOp':{'init':False,'datatype':1},
                    'StateAutOp':{'init':False,'datatype':1},
                    'StateOpAct':{'init':True,'datatype':1},
                    'StateAutAct':{'init':False,'datatype':1},
                    'StateOffAct':{'init':False,'datatype':1},
                    'SrcChannel':{'init':False,'datatype':1},
                    'SrcExtAut':{'init':False,'datatype':1},
                    'SrcIntOp':{'init':False,'datatype':1},
                    'SrcExtOp':{'init':False,'datatype':1},
                    'SrcIntAct':{'init':False,'datatype':1},
                    'SrcExtAct':{'init':False,'datatype':1},
                    'SrcIntAut':{'init':False,'datatype':1},
                }
        AnaView_dict={'TagName': {'init': 'TagName','datatype':12},
                     'TagDescription': {'init': 'TagDescription','datatype':12},
                     'WQC':{'init':0,'datatype':6},
                     'V':{'init':0,'datatype':10},
                     'VSclMin':{'init':0,'datatype':10},
                     'VSclMax':{'init':100,'datatype':10},
                     'VUnit':{'init':0,'datatype':6}}

        StringView_dict={'TagName': {'init': 'TagName','datatype':12},
                    'TagDescription': {'init': 'TagDescription','datatype':12},
                     'WQC':{'init':0,'datatype':6},
                     'Text':{'init':0,'datatype':12}}

        AnaServ_dict={'TagName': {'init': 'TagName','datatype':12},
                      'TagDescription': {'init': 'TagDescription','datatype':12},
                      'OSLevel':{'init':0,'datatype':6},
                      'WQC':{'init':0,'datatype':6},
                      'VExt':{'init':0,'datatype':10},
                      'VOp':{'init':0,'datatype':10},
                      'VInt':{'init':0,'datatype':10},
                      'VReq':{'init':0,'datatype':10},
                      'VOut':{'init':0,'datatype':10},
                      'VFbk':{'init':0,'datatype':10},
                      'VSclMin':{'init':0,'datatype':10},
                      'VSclMax':{'init':100,'datatype':10},
                      'VUnit':{'init':0,'datatype':10},
                      'VMin':{'init':0,'datatype':10},
                      'VMax':{'init':0,'datatype':10},
                      'Sync':{'init':True,'datatype':1},
                      'StateChannel': {'init': False, 'datatype': 1},
                      'StateOffAut': {'init': False, 'datatype': 1},
                      'StateOpAut': {'init': False, 'datatype': 1},
                      'StateAutAut': {'init': False, 'datatype': 1},
                      'StateOffOp': {'init': False, 'datatype': 1},
                      'StateOpOp': {'init': False, 'datatype': 1},
                      'StateAutOp': {'init': False, 'datatype': 1},
                      'StateOpAct': {'init': True, 'datatype': 1},
                      'StateAutAct': {'init': False, 'datatype': 1},
                      'StateOffAct': {'init': False, 'datatype': 1},
                      'SrcChannel': {'init': False, 'datatype': 1},
                      'SrcExtAut': {'init': False, 'datatype': 1},
                      'SrcIntOp': {'init': False, 'datatype': 1},
                      'SrcExtOp': {'init': False, 'datatype': 1},
                      'SrcIntAct': {'init': False, 'datatype': 1},
                      'SrcExtAct': {'init': False, 'datatype': 1},
                      'SrcIntAut': {'init': False, 'datatype': 1},
                      }

        DIntServ_dict={'TagName': {'init': 'TagName','datatype':12},
                      'TagDescription': {'init': 'TagDescription','datatype':12},
                      'OSLevel':{'init':0,'datatype':6},
                      'WQC':{'init':0,'datatype':6},
                      'VExt':{'init':0,'datatype':6},
                      'VOp':{'init':0,'datatype':6},
                      'VInt':{'init':0,'datatype':6},
                      'VReq':{'init':0,'datatype':6},
                      'VOut':{'init':0,'datatype':6},
                      'VFbk':{'init':0,'datatype':6},
                      'VSclMin':{'init':0,'datatype':6},
                      'VSclMax':{'init':100,'datatype':6},
                      'VUnit':{'init':0,'datatype':6},
                      'VMin':{'init':0,'datatype':6},
                      'VMax':{'init':0,'datatype':6},
                      'Sync':{'init':False,'datatype':1},
                      'StateChannel': {'init': False, 'datatype': 1},
                      'StateOffAut': {'init': False, 'datatype': 1},
                      'StateOpAut': {'init': False, 'datatype': 1},
                      'StateAutAut': {'init': False, 'datatype': 1},
                      'StateOffOp': {'init': False, 'datatype': 1},
                      'StateOpOp': {'init': False, 'datatype': 1},
                      'StateAutOp': {'init': False, 'datatype': 1},
                      'StateOpAct': {'init': True, 'datatype': 1},
                      'StateAutAct': {'init': False, 'datatype': 1},
                      'StateOffAct': {'init': False, 'datatype': 1},
                      'SrcChannel': {'init': False, 'datatype': 1},
                      'SrcExtAut': {'init': False, 'datatype': 1},
                      'SrcIntOp': {'init': False, 'datatype': 1},
                      'SrcExtOp': {'init': False, 'datatype': 1},
                      'SrcIntAct': {'init': False, 'datatype': 1},
                      'SrcExtAct': {'init': False, 'datatype': 1},
                      'SrcIntAut': {'init': False, 'datatype': 1},
                      }

        StringServ_dict={'TagName': {'init': 'TagName','datatype':12},
                         'TagDescription': {'init': 'TagDescription','datatype':12},
                         'OSLevel':{'init':0,'datatype':6},
                         'WQC':{'init':0,'datatype':6},
                         'VExt':{'init': 'VExt_string','datatype':12},
                         'VOp':{'init': 'VOp_string','datatype':12},
                         'VInt':{'init': 'VInt_string','datatype':12},
                         'VReq':{'init': 'VReq_string','datatype':12},
                         'VOut':{'init': 'VOut_string','datatype':12},
                         'VFbk':{'init': 'VFbk_string','datatype':12},
                         'Sync': {'init': False, 'datatype': 1},
                         'StateChannel': {'init': False, 'datatype': 1},
                         'StateOffAut': {'init': False, 'datatype': 1},
                         'StateOpAut': {'init': False, 'datatype': 1},
                         'StateAutAut': {'init': False, 'datatype': 1},
                         'StateOffOp': {'init': False, 'datatype': 1},
                         'StateOpOp': {'init': False, 'datatype': 1},
                         'StateAutOp': {'init': False, 'datatype': 1},
                         'StateOpAct': {'init': True, 'datatype': 1},
                         'StateAutAct': {'init': False, 'datatype': 1},
                         'StateOffAct': {'init': False, 'datatype': 1},
                         'SrcChannel': {'init': False, 'datatype': 1},
                         'SrcExtAut': {'init': False, 'datatype': 1},
                         'SrcIntOp': {'init': False, 'datatype': 1},
                         'SrcExtOp': {'init': False, 'datatype': 1},
                         'SrcIntAct': {'init': False, 'datatype': 1},
                         'SrcExtAct': {'init': False, 'datatype': 1},
                         'SrcIntAut': {'init': False, 'datatype': 1},
                         }

        DintView_dict={'TagName': {'init': 'TagName','datatype':12},
                    'TagDescription': {'init': 'TagDescription','datatype':12},
                     'WQC':{'init':0,'datatype':6},
                     'V':{'init':0,'datatype':6},
                     'VSclMin':{'init':0,'datatype':6},
                     'VSclMax':{'init':100,'datatype':6},
                     'VUnit':{'init':0,'datatype':6}}

        BinProcessValueIn_dict={'TagName': {'init': 'TagName','datatype':12},
                                'TagDescription': {'init': 'TagDescription','datatype':12},
                                'WQC':{'init':0,'datatype':6},
                                'VExt': {'init': False, 'datatype': 1},
                                'VState0':{'init':'VState0','datatype':1},
                                'VState1':{'init':'VState1','datatype':1}}

        self.structure_dict={
            'Data_processing':{'ServiceControl': Service_control_dict,
                               'Model_ID': DIntServ_dict,

                               'Result':AnaView_dict,
                               'Confidence_interval':AnaView_dict,
                                'Status_message_data_processing':StringView_dict
                   },
            'Raw_data_aquisitoion':{'ServiceControl': Service_control_dict,
                                    'Shutter_speed_setpoint':AnaServ_dict,
                                    'Resolution_setpoint':AnaServ_dict,
                                    'ROI_x0':AnaServ_dict,
                                    'ROI_y0':AnaServ_dict,
                                    'ROI_x_delta':AnaServ_dict,
                                    'ROI_y_delta':AnaServ_dict,
                                    'Gain_setpoint':AnaServ_dict,
                                    'Auto_brightness_setpoint':AnaServ_dict,
                                    'Time_interval_setpoint':AnaServ_dict,

                                    'Shutter_speed_feedback':AnaView_dict,
                                    'Resolution_feedback':AnaView_dict,
                                    'Gain_feedback':AnaView_dict,
                                    'Auto_brightness_feedback':AnaView_dict,
                                    'Webserver_endpoint':StringView_dict,

                                    'Data_aq_trigger':BinProcessValueIn_dict,
                                    },

            'Raw_data_archiving':{'ServiceControl':Service_control_dict,
                                'Data_sink':StringServ_dict,
                                'Data_format':StringServ_dict,

                                'Status_message_data_archiving':StringView_dict,
                                },

            'Configuration_Mode':{'ServiceControl': Service_control_dict,
                                  'Configuration_ID': DIntServ_dict,
                                  'Current_configuration_ID': DintView_dict,
                                  },

            'Camera_positioning':{'ServiceControl':Service_control_dict,
                                  'Absolute_X_setpoint_camera_pos':AnaServ_dict,
                                  'Absolute_Y_setpoint_camera_pos':AnaServ_dict,
                                  'Absolute_Z_setpoint_camera_pos':AnaServ_dict,
                                  'Absolute_angle_X_Y_setpoint_camera_pos':AnaServ_dict,
                                  'Absolute_angle_X_Z_setpoint_camera_pos':AnaServ_dict,
                                  'Absolute_angle_Y_Z_setpoint_camera_pos':AnaServ_dict,

                                  'Absolute_X_camera_pos': AnaView_dict,
                                  'Absolute_Y_camera_pos': AnaView_dict,
                                  'Absolute_Z_camera_pos': AnaView_dict,
                                  'Absolute_angle_X_Y_camera_pos': AnaView_dict,
                                  'Absolute_angle_X_Z_camera_pos': AnaView_dict,
                                  'Absolute_angle_Y_Z_camera_pos': AnaView_dict,
                                  'Position_ID_camera_pos':DIntServ_dict
                                  },

            'Camera_position_update':{'ServiceControl': Service_control_dict,
                                       'Absolute_X_camera_upd': AnaView_dict,
                                       'Absolute_Y_camera_upd': AnaView_dict,
                                       'Absolute_Z_camera_upd': AnaView_dict,
                                       'Absolute_angle_X_Y_camera_upd': AnaView_dict,
                                       'Absolute_angle_X_Z_camera_upd': AnaView_dict,
                                       'Absolute_angle_Y_Z_camera_upd': AnaView_dict,
                                       'Position_ID_camera_upd':DIntServ_dict,
                                       'Position_ID_camera_upd1':DintView_dict

                                       },

            'Illumination':{'ServiceControl':Service_control_dict,
                            'Wavelength_setpoint':AnaServ_dict,
                            'Intensity_setpoint':AnaServ_dict,
                            'Frequency_setpoint':AnaServ_dict,
                            'Duration_setpoint':AnaServ_dict,

                            'Intensity_feedback': AnaView_dict,

                            'Light_trigger':BinProcessValueIn_dict,
                            },

            'Lens':{'ServiceControl':Service_control_dict,
                    'Absolute_focus_setpoint':AnaServ_dict,
                    'Absolute_iris_setpoint':AnaServ_dict,
                    'Auto_focus_setpoint':AnaServ_dict,
                    'Auto_iris_setpoint':AnaServ_dict,

                    'Absolute_focus_feedback': AnaView_dict,
                    'Absolute_iris_feedback': AnaView_dict,
                    'Auto_focus_feedback': AnaView_dict,
                    'Auto_iris_feedback': AnaView_dict,
                    },
        }
    def start_OPCUA(self):
        server=Server()
        server.set_endpoint("opc.tcp://0.0.0.0:4840")
        server.set_server_name("Test_PEA_OPCUA_Server")
        root=server.get_objects_node()
        ns=1
        for key_1 in self.structure_dict.keys():

            obj_1=root.add_folder(f'ns={ns};s={key_1}',key_1)
            #print(key_1)
            for key_2 in self.structure_dict[key_1].keys():
                #print(key_2)
                obj_2=obj_1.add_folder(f'ns={ns};s={key_1}.{key_2}',key_2)
                for key_3 in self.structure_dict[key_1][key_2].keys():
                    #print(key_3)
                    obj_3=obj_2.add_variable(f'ns={ns};s={key_1}.{key_2}.{key_3}',key_3,self.structure_dict[key_1][key_2][key_3]['init']
                                             ,datatype=self.structure_dict[key_1][key_2][key_3]['datatype'])
                    obj_3.set_writable()
                #ns=ns+1


        server.start()
        print('\nOPCUA server started')

