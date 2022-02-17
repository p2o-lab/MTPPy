from mtppy.service import Service
from mtppy.procedure import Procedure
from mtppy.operation_elements import *
from mtppy.indicator_elements import *
import time
import random


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
        while True:
            if self.thread_ctrl.get_flag('idle'):
                break
            print('Cycle %i' % cycle)
            cycle += 1
            time.sleep(1)

    def starting(self):
        print('- Starting -')
        self.state_machine.start()

    def execute(self):
        print('- Execute -')
        cycle = 0
        while True:
            if self.thread_ctrl.get_flag('execute'):
                break
            print('Cycle %i' % cycle)
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
                self.procedures[2].report_values['proc_rv_bin'].set_v(not self.procedures[2].report_values['proc_rv_bin'].attributes['V'].value)
                self.procedures[2].report_values['proc_rv_dint'].set_v(random.randint(-100, 100))
                self.procedures[2].report_values['proc_rv_str'].set_v(str(random.random()))

            cycle += 1
            time.sleep(1)

    def completing(self):
        self.state_machine.complete()

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
        self.state_machine.reset()
