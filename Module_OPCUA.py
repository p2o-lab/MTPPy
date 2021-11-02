from opcua import Server

structure_dict={
    'D_Service':
        {'Service_Control':{
            'WQC':{'ns':'ns=1;s=WQC','Name':'WQC','Type':'byte','init':0},
            'OsLevel':{'ns':'ns=1;s=Os_Level','Name':'Os_Level','Type':'byte','init':0},
            'CommandOp':{'ns':'ns=1;s=CommandOp','Name':'CommandOp','Type':'int','init':0},
            'CommandInt':{'init':0},
            'CommandExt':{'init':0},
            'ProcedureOp':{'init':0},
            'ProcedureInt':{'init':0},
            'ProcedureExt':{'init':0},
            'StateCur':{'init':16},
            'CommandEn':{'init':268},
            'ProcedureCur':{'init':0},
            'ProcedureReq':{'init':0},
            'PosTextID':{'init':0},
            'InteractQuestionID':{'init':0},
            'InteractAnswerID':{'init':0},
            'StateChannel':{'init':False,'Type':'byte'},
            'StateOffAut':{'init':False,'Type':'byte'},
            'StateOpAut':{'init':False,'Type':'byte'},
            'StateAutAut':{'init':False,'Type':'byte'},
            'StateOffOp':{'init':False,'Type':'byte'},
            'StateOpOp':{'init':False,'Type':'byte'},
            'StateAutOp':{'init':False,'Type':'byte'},
            'StateOpAct':{'init':True,'Type':'byte'},
            'StateAutAct':{'init':False,'Type':'byte'},
            'StateOffAct':{'init':False,'Type':'byte'},
            'SrcChannel':{'init':False,'Type':'byte'},
            'SrcExtAut':{'init':False,'Type':'byte'},
            'SrcIntOp':{'init':False,'Type':'byte'},
            'SrcExtOp':{'init':False,'Type':'byte'},
            'SrcIntAct':{'init':False,'Type':'byte'},
            'SrcExtAct':{'init':False,'Type':'byte'}}},
    'D_Service_2':
        {'Service_Control': {
            'WQC': {'ns': 'ns=1;s=WQC', 'Name': 'WQC', 'Type': 'byte', 'init': 0},
            'OsLevel': {'ns': 'ns=1;s=Os_Level', 'Name': 'Os_Level', 'Type': 'byte', 'init': 0},
            'CommandOp': {'ns': 'ns=1;s=CommandOp', 'Name': 'CommandOp', 'Type': 'int', 'init': 0},
            'CommandInt': {'init': 0},
            'CommandExt': {'init': 0},
            'ProcedureOp': {'init': 0},
            'ProcedureInt': {'init': 0},
            'ProcedureExt': {'init': 0},
            'StateCur': {'init': 0},
            'CommandEn': {'init': 0},
            'ProcedureCur': {'init': 0},
            'ProcedureReq': {'init': 0},
            'PosTextID': {'init': 0},
            'InteractQuestionID': {'init': 0},
            'InteractAnswerID': {'init': 0},
            'StateChannel': {'init': 0},
            'StateOffAut': {'init': 0},
            'StateOpAut': {'init': 0},
            'StateAutAut': {'init': 0},
            'StateOffOp': {'init': 0},
            'StateOpOp': {'init': 0},
            'StateAutOp': {'init': 0},
            'StateOpAct': {'init': 0},
            'StateAutAct': {'init': 0},
            'StateOffAct': {'init': 0},
            'SrcChannel': {'init': 0},
            'SrcExtAut': {'init': 0},
            'SrcIntOp': {'init': 0},
            'SrcExtOp': {'init': 0},
            'SrcIntAct': {'init': 0},
            'SrcExtAct': {'init': 0},

        }}}

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
