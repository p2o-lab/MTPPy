from abc import abstractmethod

from mtppy.suc_data_assembly import SUCServiceControl
from mtppy.thread_control import ThreadControl
from mtppy.operation_source_mode import OperationSourceMode
from mtppy.state_machine import StateMachine
from mtppy.procedure_control import ProcedureControl
from mtppy.state_codes import StateCodes
from mtppy.procedure import Procedure
from mtppy.suc_data_assembly import SUCOperationElement

StateCodes = StateCodes()


class Service(SUCServiceControl):
    def __init__(self, tag_name: str, tag_description: str):
        super().__init__(tag_name, tag_description)

        self.thread_ctrl = ThreadControl()
        self.op_src_mode = OperationSourceMode()

        self.configuration_parameters = {}

        self.procedures = {}
        self.procedure_control = ProcedureControl(self.procedures, self.op_src_mode)

        self.state_machine = StateMachine(operation_source_mode=self.op_src_mode,
                                          procedure_control=self.procedure_control,
                                          execution_routine=self.state_change_callback)

        self.op_src_mode.add_enter_offline_callback(self.state_machine.command_en_ctrl.disable_all)

        self.op_src_mode.add_exit_offline_callback(self.state_machine.command_en_ctrl.set_default)
        self.op_src_mode.add_exit_offline_callback(self.apply_configuration_parameters)
        self.op_src_mode.add_exit_offline_callback(self.init_idle_state)

    def init_idle_state(self):
        self.state_change_callback()

    def state_change_callback(self):
        if self.op_src_mode.attributes['StateOffAct'].value:
            return

        state_str = self.state_machine.get_current_state_str()
        function_to_execute = eval(f'self.{state_str}')
        self.thread_ctrl.request_state(state_str, function_to_execute)
        self.thread_ctrl.reallocate_running_thread()
        if state_str == 'idle':
            self.op_src_mode.allow_switch_to_offline_mode(True)
        else:
            self.op_src_mode.allow_switch_to_offline_mode(False)

    def is_state(self, state_str):
        if state_str is self.state_machine.get_current_state_str():
            return True
        else:
            self.thread_ctrl.reallocate_running_thread()
            return False

    def state_change(self):
        self.state_machine.state_change()

    def add_configuration_parameter(self, configuration_parameter: SUCOperationElement):
        self.configuration_parameters[configuration_parameter.tag_name] = configuration_parameter

    def apply_configuration_parameters(self):
        print('Applying service configuration parameters')
        for configuration_parameter in self.configuration_parameters.values():
            configuration_parameter.set_v_out()

    def add_procedure(self, procedure: Procedure):
        self.procedures[procedure.attributes['ProcedureId'].value] = procedure
        if procedure.attributes['IsDefault'].value:
            self.procedure_control.default_procedure_id = procedure.attributes['ProcedureId'].value
            self.procedure_control.attributes['ProcedureOp'].init_value = self.procedure_control.default_procedure_id
            self.procedure_control.attributes['ProcedureInt'].init_value = self.procedure_control.default_procedure_id
            self.procedure_control.attributes['ProcedureExt'].init_value = self.procedure_control.default_procedure_id

    @abstractmethod
    def idle(self):
        pass

    @abstractmethod
    def starting(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def completing(self):
        pass

    @abstractmethod
    def completed(self):
        pass

    @abstractmethod
    def pausing(self):
        pass

    @abstractmethod
    def paused(self):
        pass

    @abstractmethod
    def resuming(self):
        pass

    @abstractmethod
    def holding(self):
        pass

    @abstractmethod
    def held(self):
        pass

    @abstractmethod
    def unholding(self):
        pass

    @abstractmethod
    def stopping(self):
        pass

    @abstractmethod
    def stopped(self):
        pass

    @abstractmethod
    def aborting(self):
        pass

    @abstractmethod
    def aborted(self):
        pass

    @abstractmethod
    def resetting(self):
        pass
