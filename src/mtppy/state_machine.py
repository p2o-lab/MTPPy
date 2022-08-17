import logging

from mtppy.attribute import Attribute
from mtppy.state_codes import StateCodes
from mtppy.command_codes import CommandCodes
from mtppy.command_en_control import CommandEnControl
from mtppy.operation_source_mode import OperationSourceMode
from mtppy.procedure_control import ProcedureControl
StateCodes = StateCodes()
CommandCodes = CommandCodes()


class StateMachine:
    def __init__(self, operation_source_mode: OperationSourceMode,
                 procedure_control: ProcedureControl,
                 execution_routine: callable):
        """
        Represents a state machine for a service.
        :param operation_source_mode: Operation and source mode control.
        :param procedure_control: Procedure control.
        :param execution_routine: Execution routine for state changing.
        """

        self.attributes = {
            'CommandOp': Attribute('CommandOp', int, init_value=0, sub_cb=self.set_command_op),
            'CommandInt': Attribute('CommandInt', int, init_value=0, sub_cb=self.set_command_int),
            'CommandExt': Attribute('CommandExt', int, init_value=0, sub_cb=self.set_command_ext),

            'StateCur': Attribute('StateCur', int, init_value=16),
            'CommandEn': Attribute('CommandEn', int, init_value=0),
        }

        self.op_src_mode = operation_source_mode
        self.procedure_control = procedure_control
        self.execution_routine = execution_routine
        self.command_en_ctrl = CommandEnControl()

        self.act_state = StateCodes.idle
        self.prev_state = StateCodes.idle

    def set_command_op(self, value: int):
        if self.op_src_mode.attributes['StateOpAct'].value:
            self.command_execution(value)

    def set_command_int(self, value: int):
        if self.op_src_mode.attributes['StateAutAct'].value and self.op_src_mode.attributes['SrcIntAct'].value:
            self.command_execution(value)

    def set_command_ext(self, value: int):
        if self.op_src_mode.attributes['StateAutAct'].value and self.op_src_mode.attributes['SrcExtAct'].value:
            self.command_execution(value)

    def command_execution(self, com_var: int):
        if com_var not in CommandCodes.get_list_int():
            logging.debug(f'Command Code {com_var} does not exist')
            return

        cmd_str = CommandCodes.int_code[com_var]
        if not self.command_en_ctrl.is_enabled(cmd_str):
            logging.debug(f'CommandEn does not permit to execute {cmd_str} from state {self.get_current_state_str()}')
            return
        else:
            logging.debug(f'CommandEn permits to execute {cmd_str}')

        eval(f'self.{CommandCodes.int_code[com_var]}()')

    def start(self):
        if self.command_en_ctrl.is_enabled('start'):
            self.procedure_control.set_procedure_cur()
            self.procedure_control.apply_procedure_parameters()
            self._change_state_to(StateCodes.starting)

    def restart(self):
        if self.command_en_ctrl.is_enabled('restart'):
            self._change_state_to(StateCodes.starting)

    def complete(self):
        if self.command_en_ctrl.is_enabled('complete'):
            self._change_state_to(StateCodes.completing)

    def pause(self):
        if self.command_en_ctrl.is_enabled('pause'):
            self._change_state_to(StateCodes.pausing)

    def resume(self):
        if self.command_en_ctrl.is_enabled('resume'):
            self._change_state_to(StateCodes.resuming)

    def reset(self):
        if self.command_en_ctrl.is_enabled('reset'):
            self._change_state_to(StateCodes.resetting)

    def hold(self):
        if self.command_en_ctrl.is_enabled('hold'):
            self._change_state_to(StateCodes.holding)

    def unhold(self):
        if self.command_en_ctrl.is_enabled('unhold'):
            self._change_state_to(StateCodes.unholding)

    def stop(self):
        if self.command_en_ctrl.is_enabled('stop'):
            self._change_state_to(StateCodes.stopping)

    def abort(self):
        if self.command_en_ctrl.is_enabled('abort'):
            self._change_state_to(StateCodes.aborting)

    def state_change(self):
        if self.act_state == StateCodes.starting:
            self._change_state_to(StateCodes.execute)
        elif self.act_state == StateCodes.starting:
            self._change_state_to(StateCodes.execute)
        elif self.act_state == StateCodes.completing:
            self._change_state_to(StateCodes.completed)
        elif self.act_state == StateCodes.pausing:
            self._change_state_to(StateCodes.paused)
        elif self.act_state == StateCodes.resuming:
            self._change_state_to(StateCodes.execute)
        elif self.act_state == StateCodes.resetting:
            self._change_state_to(StateCodes.idle)
        elif self.act_state == StateCodes.holding:
            self._change_state_to(StateCodes.held)
        elif self.act_state == StateCodes.unholding:
            self._change_state_to(StateCodes.execute)
        elif self.act_state == StateCodes.stopping:
            self._change_state_to(StateCodes.stopped)
        elif self.act_state == StateCodes.aborting:
            self._change_state_to(StateCodes.aborted)

    def _change_state_to(self, new_state: int):
        self.act_state = new_state
        self.attributes['StateCur'].set_value(new_state)
        new_state_str = StateCodes.int_code[new_state]
        self.command_en_ctrl.execute(new_state_str)
        self.attributes['CommandEn'].set_value(self.command_en_ctrl.get_command_en())
        self.execution_routine()
        logging.debug(f'Service state changed to {new_state}')

    def get_current_state_str(self):
        return StateCodes.int_code[self.act_state]
