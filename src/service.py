from abc import abstractmethod

from src.attribute import Attribute
from src.thread_control import ThreadControl
from src.operation_source_mode import OperationSourceMode
from src.state_machine import StateMachine
from src.procedure_control import ProcedureControl
from src.state_codes import StateCodes
StateCodes = StateCodes()


class Service:
    def __init__(self, tag_name, tag_description):
        self.tag_name = tag_name
        self.tag_description = tag_description

        self.thread_ctrl = ThreadControl()
        self.op_src_mode = OperationSourceMode()
        self.op_src_mode.add_exit_offline_callback(self.set_configuration_parameters)

        self.state_machine = StateMachine(operation_source_mode=self.op_src_mode,
                                          execution_routine=self.execute_state)

        self.procedure_control = ProcedureControl(self.op_src_mode)
        self.op_src_mode.add_exit_offline_callback(self.procedure_control.set_procedure_cur)

        self._init_attributes()
        self.configuration_parameters = {}

        self.op_src_mode.add_exit_offline_callback(self.init_idle_state)

    def _init_attributes(self):
        self.attributes = {
            'PosTextID': Attribute('StateChannel', bool, init_value=0),
            'InteractQuestionID': Attribute('StateOffAut', bool, init_value=0),
            'InteractAnswerID': Attribute('StateOpAut', bool, init_value=0),
            'WQC': Attribute('WQC', int, init_value=255),
            'OSLevel': Attribute('OSLevel', int, init_value=0),
        }

    def init_idle_state(self):
        self.execute_state(forced=True)

    def execute_state(self, forced=False):
        #if self.op_src_mode.attributes['StateOffAct']:
        #    return
        if not self.state_machine.is_state(self.state_machine.prev_state) or forced:
            state_str = self.state_machine.get_current_state_str()
            self.state_machine.command_en_ctrl.execute(state_str)
            self.thread_ctrl.execute(state_str, eval(f'self.{state_str}'))
            self.state_machine.update_prev_state()

    def add_configuration_parameter(self, configuration_parameter):
        self.configuration_parameters[configuration_parameter.tag_name] = configuration_parameter

    def set_configuration_parameters(self):
        print('Applying service configuration parameters')
        for configuration_parameter in self.configuration_parameters.values():
            configuration_parameter.control_elements.set_v_out()

    def add_procedure(self, procedure):
        self.procedure_control.add_procedure(procedure)

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
