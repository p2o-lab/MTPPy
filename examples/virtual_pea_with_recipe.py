from mtppy.opcua_server_pea import OPCUAServerPEA
from mtppy.mtp_generator import MTPGenerator
from mtppy.service import Service
from mtppy.procedure import Procedure
from mtppy.operation_elements import *
from mtppy.indicator_elements import *

import time
import random
from datetime import datetime


class ServiceDummy(Service):
    def __init__(self, tag_name, tag_description):
        super().__init__(tag_name, tag_description)
        self.add_service_parameters()
        self.add_procedures()

    def add_service_parameters(self):
        serv_parameters = [AnaServParam('serv_param_ana', v_min=0, v_max=50, v_scl_min=0, v_scl_max=10, v_unit=23),
                           DIntServParam('serv_param_dint', v_min=-10, v_max=10, v_scl_min=0, v_scl_max=-10, v_unit=23),
                           BinServParam('serv_param_bin', v_state_0='state_0', v_state_1='state_1'),
                           StringServParam('serv_param_str')
                           ]
        [self.add_configuration_parameter(serv_param) for serv_param in serv_parameters]

    def add_procedures(self):
        # Procedure 1
        proc_1 = Procedure(0, 'proc_1', is_self_completing=False, is_default=False)

        # Procedure 2
        proc_2 = Procedure(1, 'proc_2', is_self_completing=True, is_default=True)

        # Procedure 3
        proc_3 = Procedure(2, 'proc_3', is_self_completing=True, is_default=False)
        proc_parameters = [AnaServParam('proc_param_ana', v_min=0, v_max=50, v_scl_min=0, v_scl_max=10, v_unit=23),
                           DIntServParam('proc_param_dint', v_min=-10, v_max=10, v_scl_min=0, v_scl_max=-10, v_unit=23),
                           BinServParam('proc_param_bin', v_state_0='state_0', v_state_1='state_1'),
                           StringServParam('proc_param_str'),
                           ]
        [proc_3.add_procedure_parameter(proc_param) for proc_param in proc_parameters]

        report_values = [AnaView('proc_rv_ana', v_scl_min=0, v_scl_max=10, v_unit=23),
                         DIntView('proc_rv_dint', v_scl_min=0, v_scl_max=-10, v_unit=23),
                         BinView('proc_rv_bin', v_state_0='state_0', v_state_1='state_1'),
                         StringView('proc_rv_str'),
                         ]
        [proc_3.add_report_value(report_value) for report_value in report_values]

        self.add_procedure(proc_1)
        self.add_procedure(proc_2)
        self.add_procedure(proc_3)

    def idle(self):
        print('- Idle -')
        cycle = 0
        while self.is_state('idle'):
            print('Idle cycle %i' % cycle)
            cycle += 1
            time.sleep(1)

    def starting(self):
        print('- Starting -')
        self.state_change()

    def execute(self):
        print('- Execute -')
        cycle = 0
        while self.is_state('execute'):
            print('Execute cycle %i' % cycle)
            print(f'ProcedureCur is {self.procedure_control.get_procedure_cur()}')
            print('ServParameter %s has value %r'
                  % (self.configuration_parameters['serv_param_ana'].tag_name,
                     self.configuration_parameters['serv_param_ana'].get_v_out()))
            print('ServParameter %s has value %r'
                  % (self.configuration_parameters['serv_param_dint'].tag_name,
                     self.configuration_parameters['serv_param_dint'].get_v_out()))
            print('ServParameter %s has value %r'
                  % (self.configuration_parameters['serv_param_bin'].tag_name,
                     self.configuration_parameters['serv_param_bin'].get_v_out()))
            print('ServParameter %s has value %r'
                  % (self.configuration_parameters['serv_param_str'].tag_name,
                     self.configuration_parameters['serv_param_str'].get_v_out()))

            if self.procedure_control.get_procedure_cur() == 2:
                self.procedures[2].report_values['proc_rv_ana'].set_v(random.random())
                self.procedures[2].report_values['proc_rv_bin'].set_v(
                    not self.procedures[2].report_values['proc_rv_bin'].attributes['V'].value)
                self.procedures[2].report_values['proc_rv_dint'].set_v(random.randint(-100, 100))
                self.procedures[2].report_values['proc_rv_str'].set_v(str(random.random()))

            cycle += 1
            time.sleep(1)

    def completing(self):
        self.state_change()

    def completed(self):
        pass

    def pausing(self):
        pass

    def paused(self):
        pass

    def resuming(self):
        pass

    def holding(self):
        pass

    def held(self):
        pass

    def unholding(self):
        pass

    def stopping(self):
        pass

    def stopped(self):
        pass

    def aborting(self):
        pass

    def aborted(self):
        pass

    def resetting(self):
        print('- Resetting -')
        self.state_change()


if __name__ == '__main__':

    writer_info_dict = {'WriterName': 'tud/plt', 'WriterID': 'tud/plt', 'WriterVendor': 'tud',
                        'WriterVendorURL': 'www.tud.de',
                        'WriterVersion': '1.0.0', 'WriterRelease': '', 'LastWritingDateTime': str(datetime.now()),
                        'WriterProjectTitle': 'tu/plt/mtp', 'WriterProjectID': ''}
    export_manifest_path = '../manifest_files/example_recipe_manifest.aml'
    mtp_generator = MTPGenerator(writer_info_dict, export_manifest_path)

    module = OPCUAServerPEA(mtp_generator)

    # Service definition
    service_1 = ServiceDummy('dummy', 'description')
    module.add_service(service_1)

    # Start server
    print('--- Start OPC UA server ---')
    module.run_opcua_server()

    # Test
    opcua_server = module.get_opcua_server()
    opcua_ns = module.get_opcua_ns()
    time.sleep(1)
    print('--- Set parameters of service dummy to Operator mode ---')
    opcua_server.get_node(
        'ns=3;s=services.dummy.configuration_parameters.serv_param_ana.op_src_mode.StateOpOp').set_value(True)
    opcua_server.get_node(
        'ns=3;s=services.dummy.configuration_parameters.serv_param_dint.op_src_mode.StateOpOp').set_value(True)
    opcua_server.get_node(
        'ns=3;s=services.dummy.configuration_parameters.serv_param_bin.op_src_mode.StateOpOp').set_value(True)
    opcua_server.get_node(
        'ns=3;s=services.dummy.configuration_parameters.serv_param_str.op_src_mode.StateOpOp').set_value(True)

    time.sleep(1)

    print('--- Set parameters VOp of service dummy to different values ---')
    opcua_server.get_node('ns=3;s=services.dummy.configuration_parameters.serv_param_ana.VOp').set_value(10.54)
    opcua_server.get_node('ns=3;s=services.dummy.configuration_parameters.serv_param_dint.VOp').set_value(-5.11)
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
    time.sleep(500)

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
