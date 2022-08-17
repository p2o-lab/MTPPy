from mtppy.opcua_server_pea import OPCUAServerPEA
from mtppy.mtp_generator import MTPGenerator
from mtppy.service import Service
from mtppy.procedure import Procedure
from mtppy.operation_elements import *
from mtppy.indicator_elements import *
from mtppy.active_elements import *

import time
import random
from datetime import datetime

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] %(module)s.%(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


class RandomNumberGenerator(Service):
    def __init__(self, tag_name, tag_description):
        super().__init__(tag_name, tag_description)

        # Procedure definition
        proc_0 = Procedure(0, 'cont', is_self_completing=False, is_default=True)

        # Adding two procedure parameters
        proc_0.add_procedure_parameter(
            DIntServParam('lower_bound', v_min=0, v_max=100, v_scl_min=0, v_scl_max=100, v_unit=23))
        proc_0.add_procedure_parameter(
            DIntServParam('upper_bound', v_min=0, v_max=100, v_scl_min=0, v_scl_max=100, v_unit=23))

        # Adding procedure report value
        proc_0.add_report_value(
            AnaView('generated_value', v_scl_min=0, v_scl_max=100, v_unit=23),
        )

        # Allocating procedure to the service
        self.add_procedure(proc_0)

    def idle(self):
        print('- Idle -')
        cycle = 0
        while self.is_state('idle'):
            print(f'Idle cycle {cycle}')
            print('Doing nothing...')
            cycle += 1
            time.sleep(1)

    def starting(self):
        print('- Starting -')
        print('Applying procedure parameters...')
        self.state_change()

    def execute(self):
        print('- Execute -')
        cycle = 0
        while self.is_state('execute'):
            print('Execute cycle %i' % cycle)

            # Read procedure parameters
            lower_bound = self.procedures[0].procedure_parameters['lower_bound'].get_v_out()
            upper_bound = self.procedures[0].procedure_parameters['upper_bound'].get_v_out()

            # Execute random number generation
            generated_number = random.randint(lower_bound, upper_bound)

            # Return report value
            self.procedures[0].report_values['generated_value'].set_v(generated_number)

            cycle += 1
            time.sleep(0.1)

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
    export_manifest_path = '../manifest_files/example_minimal_manifest.aml'
    manifest_template_path = '../manifest_files/manifest_template.xml'
    mtp_generator = MTPGenerator(writer_info_dict, export_manifest_path, manifest_template_path)

    module = OPCUAServerPEA(mtp_generator)

    # Service definition
    service_1 = RandomNumberGenerator('rand_num_gen', 'This services generates random number')
    module.add_service(service_1)

    # Active element
    pid_ctrl = PIDCtrl('pid_ctrl')
    module.add_active_element(pid_ctrl)

    # Start server
    print('--- Start OPC UA server ---')
    module.run_opcua_server()

    # Test
    opcua_server = module.get_opcua_server()
    opcua_ns = module.get_opcua_ns()
    time.sleep(1)

    print('--- Set procedure parameters to Operator mode ---')
    opcua_server.get_node('ns=3;s=services.rand_num_gen.procedures.cont.procedure_parameters.lower_bound.op_src_mode.StateOpOp').set_value(True)
    opcua_server.get_node('ns=3;s=services.rand_num_gen.procedures.cont.procedure_parameters.upper_bound.op_src_mode.StateOpOp').set_value(True)
    time.sleep(1)

    print('--- Set procedure parameter values ---')
    opcua_server.get_node('ns=3;s=services.rand_num_gen.procedures.cont.procedure_parameters.lower_bound.VOp').set_value(40)
    opcua_server.get_node('ns=3;s=services.rand_num_gen.procedures.cont.procedure_parameters.upper_bound.VOp').set_value(60)
    time.sleep(1)

    print('--- Set service to Operator mode ---')
    opcua_server.get_node('ns=3;s=services.rand_num_gen.op_src_mode.StateOpOp').set_value(True)
    time.sleep(1)

    print('--- Start service ---')
    opcua_server.get_node('ns=3;s=services.rand_num_gen.state_machine.CommandOp').set_value(4)
    time.sleep(10)

    print('--- Complete service ---')
    opcua_server.get_node('ns=3;s=services.rand_num_gen.state_machine.CommandOp').set_value(1024)
    time.sleep(1)

    print('--- Reset service ---')
    opcua_server.get_node('ns=3;s=services.rand_num_gen.state_machine.CommandOp').set_value(2)

    print('--- Set service dummy to Offline mode ---')
    opcua_server.get_node('ns=3;s=services.rand_num_gen.op_src_mode.StateOffOp').set_value(True)
    time.sleep(1)
