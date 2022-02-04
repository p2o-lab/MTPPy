from src.pea import PEA
from src.procedure import Procedure

from service_dummy import ServiceDummy
from src.operation_element import AnaServParam, DIntServParam, BinServParam, StringServParam

import time

module = PEA()
opcua_server = module.get_server_obj()
opcua_ns = module.get_server_ns()

# Service definition
service_1 = ServiceDummy('dummy', opcua_server=opcua_server, opcua_ns=opcua_ns)
module.add_service(service_1)

# Configuration parameters
service_parameter_1 = AnaServParam('serv_param_ana', v_min=0, v_max=10, v_scl_min=0, v_scl_max=10, v_unit=23)
service_1.add_configuration_parameter(service_parameter_1)
service_parameter_2 = DIntServParam('serv_param_dint', v_min=0, v_max=10, v_scl_min=0, v_scl_max=-10, v_unit=10)
service_1.add_configuration_parameter(service_parameter_2)
service_parameter_3 = BinServParam('serv_param_bin', v_state_0='state_0', v_state_1='state_1')
service_1.add_configuration_parameter(service_parameter_3)
service_parameter_4 = StringServParam('serv_param_string')
service_1.add_configuration_parameter(service_parameter_4)

# Procedures definition
procedure_1 = Procedure(0, is_self_completing=True, is_default=True)
procedure_2 = Procedure(1, is_self_completing=False, is_default=False)
service_1.add_procedure(procedure_1)
service_1.add_procedure(procedure_2)

print('--- Start OPC UA server ---')
module.run_opcua_server()


# Test
time.sleep(1)
print('--- Set parameters of service dummy to Operator mode ---')
opcua_server.get_node('ns=2;s=services.dummy.configuration_parameters.serv_param_ana.operation_mode.StateOpOp').set_value(True)
opcua_server.get_node('ns=2;s=services.dummy.configuration_parameters.serv_param_dint.operation_mode.StateOpOp').set_value(True)
opcua_server.get_node('ns=2;s=services.dummy.configuration_parameters.serv_param_bin.operation_mode.StateOpOp').set_value(True)
opcua_server.get_node('ns=2;s=services.dummy.configuration_parameters.serv_param_string.operation_mode.StateOpOp').set_value(True)
time.sleep(1)

print('--- Set parameters VOp of service dummy to different values ---')
opcua_server.get_node('ns=2;s=services.dummy.configuration_parameters.serv_param_ana.control_elements.VOp').set_value(10.54)
opcua_server.get_node('ns=2;s=services.dummy.configuration_parameters.serv_param_dint.control_elements.VOp').set_value(-5)
opcua_server.get_node('ns=2;s=services.dummy.configuration_parameters.serv_param_bin.control_elements.VOp').set_value(True)
opcua_server.get_node('ns=2;s=services.dummy.configuration_parameters.serv_param_string.control_elements.VOp').set_value('hello there')
time.sleep(1)

print('--- Set service dummy to Operator mode ---')
opcua_server.get_node('ns=2;s=services.dummy.operation_mode.StateOpOp').set_value(True)
time.sleep(1)

print('--- Start service dummy ---')
opcua_server.get_node('ns=2;s=services.dummy.state_machine.CommandOp').set_value(4)
time.sleep(5)

print('--- Complete service dummy ---')
opcua_server.get_node('ns=2;s=services.dummy.state_machine.CommandOp').set_value(1024)
time.sleep(1)

print('--- Reset service dummy ---')
opcua_server.get_node('ns=2;s=services.dummy.state_machine.CommandOp').set_value(2)

print('--- Set service dummy to Offline mode ---')
opcua_server.get_node('ns=2;s=services.dummy.operation_mode.StateOffOp').set_value(True)
time.sleep(1)


print('--- Set parameter VOp of service dummy to other values ---')
opcua_server.get_node('ns=2;s=services.dummy.configuration_parameters.serv_param_ana.control_elements.VOp').set_value(14.54)
opcua_server.get_node('ns=2;s=services.dummy.configuration_parameters.serv_param_dint.control_elements.VOp').set_value(6)
opcua_server.get_node('ns=2;s=services.dummy.configuration_parameters.serv_param_bin.control_elements.VOp').set_value(False)
opcua_server.get_node('ns=2;s=services.dummy.configuration_parameters.serv_param_string.control_elements.VOp').set_value('hello there again')
time.sleep(1)

print('--- Set service dummy to Operator mode ---')
opcua_server.get_node('ns=2;s=services.dummy.operation_mode.StateOpOp').set_value(True)
time.sleep(1)

print('--- Start service dummy ---')
opcua_server.get_node('ns=2;s=services.dummy.state_machine.CommandOp').set_value(4)
time.sleep(5)

print('--- Complete service dummy ---')
opcua_server.get_node('ns=2;s=services.dummy.state_machine.CommandOp').set_value(1024)
time.sleep(1)

print('--- Reset service dummy ---')
opcua_server.get_node('ns=2;s=services.dummy.state_machine.CommandOp').set_value(2)

print('--- Set service dummy to Offline mode ---')
opcua_server.get_node('ns=2;s=services.dummy.operation_mode.StateOffOp').set_value(True)
time.sleep(1)
