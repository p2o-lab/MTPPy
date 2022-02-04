from src.service import Service
import time


class ServiceDummy(Service):
    def __init__(self, tag_name, opcua_server, opcua_ns):
        super().__init__(tag_name, opcua_server, opcua_ns)

    def Idle(self):
        pass

    def Starting(self):
        print('Starting')
        self.state_machine.Start()

    def Execute(self):
        print('Execute')
        cycle = 0
        while True:
            if self.state_stop_flags['execute']:
                break

            print('Cycle %i' % cycle)
            print('ServParameter %s has value %f'
                  % (self.configuration_parameters['serv_param_ana'].tag_name,
                     self.configuration_parameters['serv_param_ana'].control_elements.variables['VOut'].value))

            print('ServParameter %s has value %i'
                  % (self.configuration_parameters['serv_param_dint'].tag_name,
                     self.configuration_parameters['serv_param_dint'].control_elements.variables['VOut'].value))

            print('ServParameter %s has value %r'
                  % (self.configuration_parameters['serv_param_bin'].tag_name,
                     self.configuration_parameters['serv_param_bin'].control_elements.variables['VOut'].value))

            print('ServParameter %s has value %s'
                  % (self.configuration_parameters['serv_param_string'].tag_name,
                     self.configuration_parameters['serv_param_string'].control_elements.variables['VOut'].value))
            cycle += 1
            time.sleep(0.5)

    def Completing(self):
        self.state_machine.Complete()

    def Completed(self):
        pass

    def Pausing(self):
        pass

    def Paused(self):
        pass

    def Resuming(self):
        pass

    def Holding(self):
        pass

    def Held(self):
        pass

    def Unholding(self):
        pass

    def Stopping(self):
        pass

    def Stopped(self):
        pass

    def Aborting(self):
        pass

    def Aborted(self):
        pass

    def Resetting(self):
        print('Resetting')
        self.state_machine.Reset()
