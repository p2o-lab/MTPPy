from opcua import Server

Service_control_dict={
            'TagName':{'init':'TagName'},
            'TagDescription':{'init':'TagDescription'},
            'WQC':{'ns':'ns=1;s=WQC','Name':'WQC','Type':'byte','init':0},
            'OSLevel':{'ns':'ns=1;s=Os_Level','Name':'Os_Level','Type':'byte','init':0},
            'CommandOp':{'ns':'ns=1;s=CommandOp','Name':'CommandOp','Type':'int','init':0},
            'CommandInt':{'init':0},
            'CommandExt':{'init':0},
            'ProcedureOp':{'init':1},
            'ProcedureInt':{'init':0},
            'ProcedureExt':{'init':0},
            'StateCur':{'init':0},
            'CommandEn':{'init':0},
            'ProcedureCur':{'init':0},
            'ProcedureReq':{'init':0},
            'PosTextID':{'init':0},
            'InteractQuestionID':{'init':0},
            'InteractAnswerID':{'init':0},
            'StateChannel':{'init':False},
            'StateOffAut':{'init':False},
            'StateOpAut':{'init':False},
            'StateAutAut':{'init':False},
            'StateOffOp':{'init':False},
            'StateOpOp':{'init':False},
            'StateAutOp':{'init':False},
            'StateOpAct':{'init':True},
            'StateAutAct':{'init':False},
            'StateOffAct':{'init':False},
            'SrcChannel':{'init':False},
            'SrcExtAut':{'init':False},
            'SrcIntOp':{'init':False},
            'SrcExtOp':{'init':False},
            'SrcIntAct':{'init':False},
            'SrcExtAct':{'init':False},
            'SrcIntAut':{'init':False},
        }
AnaView_dict={'TagName': {'init': 'TagName'},
            'TagDescription': {'init': 'TagDescription'},
             'WQC':{'init':0},
             'V':{'init':0},
             'VSclMin':{'init':0},
             'VSclMax':{'init':100},
             'VUnit':{'init':0}}

structure_dict={
    'Data_Processing':{'ServiceControl':
        Service_control_dict,
         'AnaView':AnaView_dict
           },
    'Raw_data_aquisitoion':{'ServiceControl':
        Service_control_dict},

    'Rawdataarchiving':{'ServiceControl':
        Service_control_dict},

    'Configuration_Mode':{'ServiceControl':
        Service_control_dict},

    'Camera_Positioning':{'ServiceControl':
        Service_control_dict},

    'Camera_Position_Zeroing':{'ServiceControl':
        Service_control_dict},

    'Illumination':{'ServiceControl':
        Service_control_dict},

    'Lens':{'ServiceControl':
        Service_control_dict},
}

server=Server()
server.set_endpoint("opc.tcp://localhost:4840")
server.set_server_name("Test_PEA_OPCUA_Server")
root=server.get_objects_node()
ns=1
for key_1 in structure_dict.keys():

    obj_1=root.add_folder(f'ns={ns};s={key_1}',key_1)
    #print(key_1)
    for key_2 in structure_dict[key_1].keys():
        #print(key_2)
        obj_2=obj_1.add_folder(f'ns={ns};s={key_2}',key_2)
        for key_3 in structure_dict[key_1][key_2].keys():
            #print(key_3)
            obj_3=obj_2.add_variable(f'ns={ns};s={key_3}',key_3,structure_dict[key_1][key_2][key_3]['init'])
            obj_3.set_writable()
        ns=ns+1

print('Server started')
server.start()
