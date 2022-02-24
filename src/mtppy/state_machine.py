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
        if self.op_src_mode.attributes['StateOpAct']:
            self._exec_command(value, sc=False)

    def set_command_int(self, value: int):
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcIntAct']:
            self._exec_command(value, sc=False)

    def set_command_ext(self, value: int):
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcExtAct']:
            self._exec_command(value, sc=False)

    def _exec_command(self, com_var: int, sc=True):
        if com_var not in CommandCodes.get_list_int():
            print(f'Command Code {com_var} does not exist')
            return

        cmd_str = CommandCodes.int_code[com_var]
        if not self.command_en_ctrl.get_command(cmd_str):
            print(f'CommandEn does not permit to execute {cmd_str}')
            return
        else:
            print(f'CommandEn permits to execute {cmd_str}')

        eval(f'self.{CommandCodes.int_code[com_var]}(sc)')
        return

    def _change_state_to(self, new_state: int):
        self.act_state = new_state
        self.attributes['StateCur'].set_value(new_state)
        self.attributes['CommandEn'].set_value(self.command_en_ctrl.get_command_en())
        self.execution_routine()
        print(f'Service state changed to {new_state}')

    def start(self, sc=True):
        if self.act_state == StateCodes.idle:
            self.procedure_control.set_procedure_cur()
            self.procedure_control.apply_procedure_parameters()
            self._change_state_to(StateCodes.starting)
        elif self.act_state == StateCodes.starting and sc:
            self._change_state_to(StateCodes.execute)

    def restart(self, sc=True):
        if self.act_state == StateCodes.execute:
            self._change_state_to(StateCodes.starting)
        elif self.act_state == StateCodes.starting and sc:
            self._change_state_to(StateCodes.execute)

    def complete(self, sc=True):
        if self.act_state == StateCodes.execute:
            self._change_state_to(StateCodes.completing)
        elif self.act_state == StateCodes.completing and sc:
            self._change_state_to(StateCodes.completed)

    def pause(self, sc=True):
        if self.act_state == StateCodes.execute:
            self._change_state_to(StateCodes.pausing)
        elif self.act_state == StateCodes.pausing and sc:
            self._change_state_to(StateCodes.paused)

    def resume(self, sc=True):
        if self.act_state == StateCodes.paused:
            self._change_state_to(StateCodes.resuming)
        elif self.act_state == StateCodes.resuming and sc:
            self._change_state_to(StateCodes.execute)

    def reset(self, sc=True):
        if self.act_state in [StateCodes.completed, StateCodes.stopped, StateCodes.aborted]:
            self._change_state_to(StateCodes.resetting)
        elif self.act_state == StateCodes.resetting and sc:
            self._change_state_to(StateCodes.idle)

    def hold(self, sc=True):
        if self.act_state in [StateCodes.starting, StateCodes.execute, StateCodes.completing,
                              StateCodes.resuming, StateCodes.paused, StateCodes.pausing, StateCodes.unholding]:
            self._change_state_to(StateCodes.holding)
        elif self.act_state == StateCodes.holding and sc:
            self._change_state_to(StateCodes.held)

    def unhold(self, sc=True):
        if self.act_state == StateCodes.held:
            self._change_state_to(StateCodes.unholding)
        elif self.act_state == StateCodes.unholding and sc:
            self._change_state_to(StateCodes.execute)

    def stop(self, sc=True):
        if self.act_state in [StateCodes.idle, StateCodes.starting, StateCodes.execute, StateCodes.completing,
                              StateCodes.completed, StateCodes.resuming, StateCodes.paused, StateCodes.pausing,
                              StateCodes.holding, StateCodes.held, StateCodes.unholding, StateCodes.resetting]:
            self._change_state_to(StateCodes.stopping)
        elif self.act_state == StateCodes.stopping and sc:
            self._change_state_to(StateCodes.stopped)

    def abort(self, sc=True):
        if self.act_state in [StateCodes.idle, StateCodes.starting, StateCodes.execute, StateCodes.completing,
                              StateCodes.completed, StateCodes.resuming, StateCodes.paused, StateCodes.pausing,
                              StateCodes.holding, StateCodes.held, StateCodes.unholding, StateCodes.stopping,
                              StateCodes.stopped, StateCodes.resetting]:
            self._change_state_to(StateCodes.aborting)
        elif self.act_state == StateCodes.aborting and sc:
            self._change_state_to(StateCodes.aborted)

    def get_current_state_int(self):
        return self.act_state

    def get_current_state_str(self):
        return StateCodes.int_code[self.act_state]

    def update_prev_state(self):
        self.prev_state = self.act_state
