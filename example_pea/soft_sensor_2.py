from src.pea import PEA
from service_dummy_2 import ServiceDummy
from src.operation_element import AnaServParam, DIntServParam, BinServParam, StringServParam

import time

module = PEA()
opcua_server = module.get_opcua_server()
opcua_ns = module.get_opcua_ns()

# Service definition
service_1 = ServiceDummy('dummy', 'description')
module.add_service(service_1)

# Configuration parameters
service_parameter_3 = BinServParam('serv_param_bin', v_state_0='state_0', v_state_1='state_1')
service_1.add_configuration_parameter(service_parameter_3)

print('--- Start OPC UA server ---')
module.run_opcua_server()


# Test
time.sleep(1)
print('--- Set parameters of service dummy to Operator mode ---')
opcua_server.get_node('ns=3;s=services.dummy.configuration_parameters.serv_param_bin.op_src_mode.StateOpOp').set_value(True)
time.sleep(1)

print('--- Set parameters VOp of service dummy to different values ---')
opcua_server.get_node('ns=3;s=services.dummy.configuration_parameters.serv_param_bin.control_elements.VOp').set_value(True)
time.sleep(1)

print('--- Set service dummy to Operator mode ---')
opcua_server.get_node('ns=3;s=services.dummy.op_src_mode.StateOpOp').set_value(True)
time.sleep(1)

print('--- Start service dummy ---')
opcua_server.get_node('ns=3;s=services.dummy.state_machine.CommandOp').set_value(4)
time.sleep(5)

print('--- Complete service dummy ---')
opcua_server.get_node('ns=3;s=services.dummy.state_machine.CommandOp').set_value(1024)
time.sleep(1)

print('--- Reset service dummy ---')
opcua_server.get_node('ns=3;s=services.dummy.state_machine.CommandOp').set_value(2)

print('--- Set service dummy to Offline mode ---')
opcua_server.get_node('ns=3;s=services.dummy.op_src_mode.StateOffOp').set_value(True)
time.sleep(1)
