from src.variable import Variable
from src.source_mode import SourceMode
from src.operation_mode import OperationMode
from src.procedure_control import ProcedureControl
from src.state_machine import StateMachine
from threading import Thread
from abc import abstractmethod
from opcua import ua


class Service:
    def __init__(self, tag_name, opcua_server, opcua_ns):
        self.tag_name = tag_name
        self.opcua_prefix = f'services.{tag_name}'
        self.opcua_server = opcua_server
        self.opcua_ns = opcua_ns

        self.operation_mode = OperationMode(opcua_server=opcua_server,
                                            opcua_ns=opcua_ns,
                                            opcua_prefix=self.opcua_prefix)

        self.source_mode = SourceMode(opcua_server=opcua_server,
                                      opcua_ns=opcua_ns,
                                      opcua_prefix=self.opcua_prefix,
                                      operation_mode=self.operation_mode
                                      )
        self.operation_mode.attach_source_mode(self.source_mode)

        self.procedures = []

        self.procedure_control = ProcedureControl(opcua_server=opcua_server,
                                                  opcua_ns=opcua_ns,
                                                  opcua_prefix=self.opcua_prefix,
                                                  source_mode=self.source_mode,
                                                  operation_mode=self.operation_mode)

        self.state_machine = StateMachine(opcua_server=opcua_server,
                                          opcua_ns=opcua_ns,
                                          opcua_prefix=self.opcua_prefix,
                                          source_mode=self.source_mode,
                                          operation_mode=self.operation_mode,
                                          execution_routine=self.execute_state)

        self.restart_enabled = True
        self.pause_enabled = True
        self.hold_enabled = True

        self.state_stop_flags = {
            'idle': False,
            'starting': False,
            'execute': False,
            'completing': False,
            'complete': False,
            'resuming': False,
            'paused': False,
            'pausing': False,
            'holding': False,
            'held': False,
            'unholding': False,
            'stopping': False,
            'stopped': False,
            'aborting': False,
            'aborted': False,
            'resetting': False,
        }

        self.prev_state = 0

        self.configuration_parameters = {}

        self.WQC = 255
        self.OSLevel = 0

        self.operation_mode.add_cb_exit_offline_mode(self.set_configuration_parameters)

        self.variables = {}

        serv_variables = {
            'PosTextID': {'type': ua.VariantType.UInt32, 'init_value': 0, 'callback': None, 'writable': False},
            'InteractQuestionID': {'type': ua.VariantType.UInt32, 'init_value': 0, 'callback': None, 'writable': False},
            'InteractAnswerID': {'type': ua.VariantType.UInt32, 'init_value': 0, 'callback': None, 'writable': False},
        }

        for var_name, var_dict in serv_variables.items():
            var_opcua_node_obj = self.opcua_server.get_node(f'ns={self.opcua_ns};s={self.opcua_prefix}.{var_name}')
            self.variables[var_name] = Variable(var_name, init_value=var_dict['init_value'],
                                                opcua_type=var_dict['type'],
                                                opcua_node_obj=var_opcua_node_obj,
                                                writable=var_dict['writable'],
                                                callback=var_dict['callback'])

    def add_configuration_parameter(self, configuration_parameter):
        self.configuration_parameters[configuration_parameter.tag_name] = configuration_parameter
        opcua_prefix = f'{self.opcua_prefix}.configuration_parameters'
        configuration_parameter.attach(opcua_prefix, self.opcua_server, self.opcua_ns)

    def add_procedure(self, procedure):
        self.procedures.append(procedure)

    def execute_idle(self):
        self.state_machine.command_en.set_command('Reset', False)
        self.state_machine.command_en.set_command('Start', True)
        self.state_machine.command_en.set_command('Stop', True)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', False)
            self.state_machine.command_en.set_command('Unhold', False)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', False)
            self.state_machine.command_en.set_command('Resume', False)
        self.state_machine.command_en.set_command('Abort', True)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', False)
        self.state_machine.command_en.set_command('Complete', False)

        self.state_stop_flags['resetting'] = True
        self.state_stop_flags['idle'] = False

        Thread(target=self.Idle).start()

    def execute_starting(self):
        self.state_machine.command_en.set_command('Reset', False)
        self.state_machine.command_en.set_command('Start', False)
        self.state_machine.command_en.set_command('Stop', True)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', True)
            self.state_machine.command_en.set_command('Unhold', False)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', False)
            self.state_machine.command_en.set_command('Resume', False)
        self.state_machine.command_en.set_command('Abort', True)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', False)
        self.state_machine.command_en.set_command('Complete', True)

        self.state_stop_flags['idle'] = True
        self.state_stop_flags['execute'] = True
        self.state_stop_flags['starting'] = False

        Thread(target=self.Starting).start()

    def execute_execute(self):
        self.state_machine.command_en.set_command('Reset', False)
        self.state_machine.command_en.set_command('Start', False)
        self.state_machine.command_en.set_command('Stop', True)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', True)
            self.state_machine.command_en.set_command('Unhold', False)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', True)
            self.state_machine.command_en.set_command('Resume', False)
        self.state_machine.command_en.set_command('Abort', True)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', True)
        self.state_machine.command_en.set_command('Complete', True)

        self.state_stop_flags['idle'] = True
        self.state_stop_flags['execute'] = False

        Thread(target=self.Execute).start()

    def execute_completing(self):
        self.state_machine.command_en.set_command('Reset', False)
        self.state_machine.command_en.set_command('Start', False)
        self.state_machine.command_en.set_command('Stop', True)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', True)
            self.state_machine.command_en.set_command('Unhold', False)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', False)
            self.state_machine.command_en.set_command('Resume', False)
        self.state_machine.command_en.set_command('Abort', True)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', False)
        self.state_machine.command_en.set_command('Complete', True)

        self.state_stop_flags['execute'] = True
        self.state_stop_flags['completing'] = False

        Thread(target=self.Completing).start()

    def execute_completed(self):
        self.state_machine.command_en.set_command('Reset', True)
        self.state_machine.command_en.set_command('Start', False)
        self.state_machine.command_en.set_command('Stop', True)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', False)
            self.state_machine.command_en.set_command('Unhold', False)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', False)
            self.state_machine.command_en.set_command('Resume', False)
        self.state_machine.command_en.set_command('Abort', True)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', False)
        self.state_machine.command_en.set_command('Complete', True)

        self.state_stop_flags['completing'] = True
        self.state_stop_flags['completed'] = False

        Thread(target=self.Completed).start()

    def execute_resuming(self):
        self.state_machine.command_en.set_command('Reset', False)
        self.state_machine.command_en.set_command('Start', False)
        self.state_machine.command_en.set_command('Stop', True)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', False)
            self.state_machine.command_en.set_command('Unhold', False)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', False)
            self.state_machine.command_en.set_command('Resume', False)
        self.state_machine.command_en.set_command('Abort', True)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', False)
        self.state_machine.command_en.set_command('Complete', True)

        self.state_stop_flags['paused'] = True
        self.state_stop_flags['resuming'] = False

        Thread(target=self.Resuming).start()

    def execute_paused(self):
        self.state_machine.command_en.set_command('Reset', False)
        self.state_machine.command_en.set_command('Start', False)
        self.state_machine.command_en.set_command('Stop', True)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', False)
            self.state_machine.command_en.set_command('Unhold', False)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', False)
            self.state_machine.command_en.set_command('Resume', True)
        self.state_machine.command_en.set_command('Abort', True)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', False)
        self.state_machine.command_en.set_command('Complete', True)

        self.state_stop_flags['pausing'] = True
        self.state_stop_flags['paused'] = False

        Thread(target=self.Paused).start()

    def execute_pausing(self):
        self.state_machine.command_en.set_command('Reset', False)
        self.state_machine.command_en.set_command('Start', False)
        self.state_machine.command_en.set_command('Stop', True)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', False)
            self.state_machine.command_en.set_command('Unhold', False)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', False)
            self.state_machine.command_en.set_command('Resume', False)
        self.state_machine.command_en.set_command('Abort', True)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', False)
        self.state_machine.command_en.set_command('Complete', True)

        self.state_stop_flags['execute'] = True
        self.state_stop_flags['pausing'] = False

        Thread(target=self.Pausing).start()

    def execute_holding(self):
        self.state_machine.command_en.set_command('Reset', False)
        self.state_machine.command_en.set_command('Start', False)
        self.state_machine.command_en.set_command('Stop', True)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', False)
            self.state_machine.command_en.set_command('Unhold', False)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', False)
            self.state_machine.command_en.set_command('Resume', False)
        self.state_machine.command_en.set_command('Abort', True)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', False)
        self.state_machine.command_en.set_command('Complete', True)

        self.state_stop_flags['execute'] = True
        self.state_stop_flags['starting'] = True
        self.state_stop_flags['completing'] = True
        self.state_stop_flags['resuming'] = True
        self.state_stop_flags['paused'] = True
        self.state_stop_flags['pausing'] = True
        self.state_stop_flags['unholding'] = True
        self.state_stop_flags['holding'] = False

        Thread(target=self.Holding).start()

    def execute_held(self):
        self.state_machine.command_en.set_command('Reset', False)
        self.state_machine.command_en.set_command('Start', False)
        self.state_machine.command_en.set_command('Stop', True)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', False)
            self.state_machine.command_en.set_command('Unhold', True)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', False)
            self.state_machine.command_en.set_command('Resume', False)
        self.state_machine.command_en.set_command('Abort', True)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', False)
        self.state_machine.command_en.set_command('Complete', False)

        self.state_stop_flags['holding'] = True
        self.state_stop_flags['held'] = False

        Thread(target=self.Held).start()

    def execute_unholding(self):
        self.state_machine.command_en.set_command('Reset', False)
        self.state_machine.command_en.set_command('Start', False)
        self.state_machine.command_en.set_command('Stop', True)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', False)
            self.state_machine.command_en.set_command('Unhold', False)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', False)
            self.state_machine.command_en.set_command('Resume', False)
        self.state_machine.command_en.set_command('Abort', True)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', False)
        self.state_machine.command_en.set_command('Complete', False)

        self.state_stop_flags['held'] = True
        self.state_stop_flags['unholding'] = False

        Thread(target=self.Unholding).start()

    def execute_stopping(self):
        self.state_machine.command_en.set_command('Reset', False)
        self.state_machine.command_en.set_command('Start', False)
        self.state_machine.command_en.set_command('Stop', False)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', False)
            self.state_machine.command_en.set_command('Unhold', False)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', False)
            self.state_machine.command_en.set_command('Resume', False)
        self.state_machine.command_en.set_command('Abort', True)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', False)
        self.state_machine.command_en.set_command('Complete', False)

        self.state_stop_flags['execute'] = True
        self.state_stop_flags['starting'] = True
        self.state_stop_flags['completing'] = True
        self.state_stop_flags['resuming'] = True
        self.state_stop_flags['paused'] = True
        self.state_stop_flags['pausing'] = True
        self.state_stop_flags['holding'] = True
        self.state_stop_flags['held'] = True
        self.state_stop_flags['unholding'] = True
        self.state_stop_flags['completed'] = True
        self.state_stop_flags['resetting'] = True
        self.state_stop_flags['idle'] = True
        self.state_stop_flags['stopping'] = False

        Thread(target=self.Stopping).start()

    def execute_stopped(self):
        self.state_machine.command_en.set_command('Reset', True)
        self.state_machine.command_en.set_command('Start', False)
        self.state_machine.command_en.set_command('Stop', False)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', False)
            self.state_machine.command_en.set_command('Unhold', False)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', False)
            self.state_machine.command_en.set_command('Resume', False)
        self.state_machine.command_en.set_command('Abort', True)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', False)
        self.state_machine.command_en.set_command('Complete', False)

        self.state_stop_flags['stopping'] = True
        self.state_stop_flags['stopped'] = False

        Thread(target=self.Stopped).start()

    def execute_aborting(self):
        self.state_machine.command_en.set_command('Reset', False)
        self.state_machine.command_en.set_command('Start', False)
        self.state_machine.command_en.set_command('Stop', False)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', False)
            self.state_machine.command_en.set_command('Unhold', False)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', False)
            self.state_machine.command_en.set_command('Resume', False)
        self.state_machine.command_en.set_command('Abort', False)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', False)
        self.state_machine.command_en.set_command('Complete', False)

        self.state_stop_flags['execute'] = True
        self.state_stop_flags['starting'] = True
        self.state_stop_flags['completing'] = True
        self.state_stop_flags['resuming'] = True
        self.state_stop_flags['paused'] = True
        self.state_stop_flags['pausing'] = True
        self.state_stop_flags['holding'] = True
        self.state_stop_flags['held'] = True
        self.state_stop_flags['unholding'] = True
        self.state_stop_flags['completed'] = True
        self.state_stop_flags['resetting'] = True
        self.state_stop_flags['idle'] = True
        self.state_stop_flags['stopping'] = True
        self.state_stop_flags['stopped'] = True
        self.state_stop_flags['aborting'] = False

        Thread(target=self.Aborting).start()

    def execute_aborted(self):
        self.state_machine.command_en.set_command('Reset', True)
        self.state_machine.command_en.set_command('Start', False)
        self.state_machine.command_en.set_command('Stop', False)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', False)
            self.state_machine.command_en.set_command('Unhold', False)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', False)
            self.state_machine.command_en.set_command('Resume', False)
        self.state_machine.command_en.set_command('Abort', False)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', False)
        self.state_machine.command_en.set_command('Complete', False)

        self.state_stop_flags['aborting'] = True
        self.state_stop_flags['aborted'] = False

        Thread(target=self.Aborted).start()

    def execute_resetting(self):
        self.state_machine.command_en.set_command('Reset', False)
        self.state_machine.command_en.set_command('Start', False)
        self.state_machine.command_en.set_command('Stop', False)
        if self.hold_enabled:
            self.state_machine.command_en.set_command('Hold', False)
            self.state_machine.command_en.set_command('Unhold', False)
        if self.pause_enabled:
            self.state_machine.command_en.set_command('Pause', False)
            self.state_machine.command_en.set_command('Resume', False)
        self.state_machine.command_en.set_command('Abort', False)
        if self.restart_enabled:
            self.state_machine.command_en.set_command('Restart', False)
        self.state_machine.command_en.set_command('Complete', False)

        self.state_stop_flags['completed'] = True
        self.state_stop_flags['stopped'] = True
        self.state_stop_flags['aborted'] = True
        self.state_stop_flags['resetting'] = False
        Thread(target=self.Resetting).start()

    def execute_state(self):
        #if self.operation_mode.mode == 'off':
        #    return

        if self.state_machine.is_state(self.prev_state):
            return

        if self.state_machine.is_state('Idle'):
            self.execute_idle()

        if self.state_machine.is_state('Starting'):
            self.execute_starting()

        if self.state_machine.is_state('Execute'):
            self.execute_execute()

        if self.state_machine.is_state('Completing'):
            self.execute_completing()

        if self.state_machine.is_state('Completed'):
            self.execute_completed()

        if self.state_machine.is_state('Resuming'):
            self.execute_resuming()

        if self.state_machine.is_state('Paused'):
            self.execute_paused()

        if self.state_machine.is_state('Pausing'):
            self.execute_pausing()

        if self.state_machine.is_state('Holding'):
            self.execute_holding()

        if self.state_machine.is_state('Held'):
            self.execute_held()

        if self.state_machine.is_state('Unholding'):
            self.execute_unholding()

        if self.state_machine.is_state('Stopping'):
            self.execute_stopping()

        if self.state_machine.is_state('Stopped'):
            self.execute_stopped()

        if self.state_machine.is_state('Aborting'):
            self.execute_aborting()

        if self.state_machine.is_state('Aborted'):
            self.execute_aborted()

        if self.state_machine.is_state('Resetting'):
            self.execute_resetting()

        self.prev_state = self.state_machine.get_current_state()

    def set_configuration_parameters(self):
        print('Applying service configuration parameters')
        for configuration_parameter in self.configuration_parameters.values():
            configuration_parameter.control_elements.set_VOut()

    @abstractmethod
    def Idle(self):
        pass

    @abstractmethod
    def Starting(self):
        pass

    @abstractmethod
    def Execute(self):
        pass

    @abstractmethod
    def Completing(self):
        pass

    @abstractmethod
    def Completed(self):
        pass

    @abstractmethod
    def Pausing(self):
        pass

    @abstractmethod
    def Paused(self):
        pass

    @abstractmethod
    def Resuming(self):
        pass

    @abstractmethod
    def Holding(self):
        pass

    @abstractmethod
    def Held(self):
        pass

    @abstractmethod
    def Unholding(self):
        pass

    @abstractmethod
    def Stopping(self):
        pass

    @abstractmethod
    def Stopped(self):
        pass

    @abstractmethod
    def Aborting(self):
        pass

    @abstractmethod
    def Aborted(self):
        pass

    @abstractmethod
    def Resetting(self):
        pass
