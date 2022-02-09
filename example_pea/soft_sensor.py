from src.opcua_server_pea import OPCUAServerPEA
from service_dummy import ServiceDummy

import time

module = OPCUAServerPEA()
opcua_server = module.get_opcua_server()
opcua_ns = module.get_opcua_ns()

# Service definition
service_1 = ServiceDummy('dummy', 'description')
module.add_service(service_1)

# Start server
print('--- Start OPC UA server ---')
module.run_opcua_server()

# Test
time.sleep(1)
print('--- Set parameters of service dummy to Operator mode ---')
opcua_server.get_node('ns=3;s=services.dummy.configuration_parameters.serv_param_ana.op_src_mode.StateOpOp').set_value(True)
opcua_server.get_node('ns=3;s=services.dummy.configuration_parameters.serv_param_dint.op_src_mode.StateOpOp').set_value(True)
opcua_server.get_node('ns=3;s=services.dummy.configuration_parameters.serv_param_bin.op_src_mode.StateOpOp').set_value(True)
opcua_server.get_node('ns=3;s=services.dummy.configuration_parameters.serv_param_str.op_src_mode.StateOpOp').set_value(True)

time.sleep(1)

print('--- Set parameters VOp of service dummy to different values ---')
opcua_server.get_node('ns=3;s=services.dummy.configuration_parameters.serv_param_ana.VOp').set_value(10.54)
opcua_server.get_node('ns=3;s=services.dummy.configuration_parameters.serv_param_dint.VOp').set_value(-5)
opcua_server.get_node('ns=3;s=services.dummy.configuration_parameters.serv_param_bin.VOp').set_value(True)
opcua_server.get_node('ns=3;s=services.dummy.configuration_parameters.serv_param_str.VOp').set_value('hello there')

time.sleep(1)

print('--- Change procedure to 2 ---')
opcua_server.get_node('ns=3;s=services.dummy.procedure_control.ProcedureOp').set_value(2)
time.sleep(1)

print('--- Set service dummy to Operator mode ---')
opcua_server.get_node('ns=3;s=services.dummy.op_src_mode.StateOpOp').set_value(True)
time.sleep(2)

print('--- Start service dummy ---')
opcua_server.get_node('ns=3;s=services.dummy.state_machine.CommandOp').set_value(4)
time.sleep(5)

print('--- Try to unhold service dummy ---')
opcua_server.get_node('ns=3;s=services.dummy.state_machine.CommandOp').set_value(32)
time.sleep(2)

print('--- Complete service dummy ---')
opcua_server.get_node('ns=3;s=services.dummy.state_machine.CommandOp').set_value(1024)
time.sleep(1)

print('--- Reset service dummy ---')
opcua_server.get_node('ns=3;s=services.dummy.state_machine.CommandOp').set_value(2)

print('--- Set service dummy to Offline mode ---')
opcua_server.get_node('ns=3;s=services.dummy.op_src_mode.StateOffOp').set_value(True)
time.sleep(1)
