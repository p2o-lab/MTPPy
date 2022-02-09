from src.service import Service
import time
import random


class ServiceDummy(Service):
    def __init__(self, tag_name, tag_description):
        super().__init__(tag_name, tag_description)

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
