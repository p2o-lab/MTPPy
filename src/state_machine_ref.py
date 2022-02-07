from src.attribute import Attribute
from src.state_codes import StateCodes
from src.command_enable import CommandEn

StateCodes = StateCodes()


class StateMachine:
    def __init__(self, operation_source_mode, execution_routine):
        self.attributes = {}
        self._init_attributes()
        self.op_src_mode = operation_source_mode
        self.act_state = StateCodes.idle
        self.prev_state = StateCodes.idle
        self.execution_routine = execution_routine

        self.command_en = CommandEn()

    def _init_attributes(self):
        self.attributes = {
            'CommandOp': Attribute('CommandOp', int, init_value=0, cb_value_change=self.set_command_op),
            'CommandInt': Attribute('CommandInt', int, init_value=0, cb_value_change=self.set_command_int),
            'CommandExt': Attribute('CommandExt', int, init_value=0, cb_value_change=self.set_command_ext),

            'StateCur': Attribute('StateCur', int, init_value=0),
            'CommandEn': Attribute('CommandEn', int, init_value=0),
        }

    def set_command_op(self, value):
        if self.op_src_mode.attributes['StateOpAct']:
            self.exec_command(value, sc=False)

    def set_command_int(self, value):
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcIntAct']:
            self.exec_command(value, sc=False)

    def set_command_ext(self, value):
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcExtAct']:
            self.exec_command(value, sc=False)

    def exec_command(self, com_var, sc=True):
        if com_var == 2:
            self.reset(sc)
        elif com_var == 4:
            self.start(sc)
        elif com_var == 8:
            self.stop(sc)
        elif com_var == 16:
            self.hold(sc)
        elif com_var == 32:
            self.unhold(sc)
        elif com_var == 64:
            self.pause(sc)
        elif com_var == 128:
            self.resume(sc)
        elif com_var == 256:
            self.abort(sc)
        elif com_var == 512:
            self.restart(sc)
        elif com_var == 1024:
            self.complete(sc)

    def change_state_to(self, new_state):
        print('Service state changed to %i' % new_state)
        self.act_state = new_state
        self.write_cur_state()
        self.write_command_en()
        self.execution_routine()

    def write_cur_state(self):
        self.attributes['StateCur'].set_value(self.act_state)

    def write_command_en(self):
        self.attributes['CommandEn'].set_value(self.command_en.get_command_en())

    def start(self, sc=True):
        if self.act_state == StateCodes.idle:
            self.change_state_to(StateCodes.starting)
        elif self.act_state == StateCodes.starting and sc:
            self.change_state_to(StateCodes.execute)

    def restart(self, sc=True):
        if self.act_state == StateCodes.execute:
            self.change_state_to(StateCodes.starting)
        elif self.act_state == StateCodes.starting and sc:
            self.change_state_to(StateCodes.execute)

    def complete(self, sc=True):
        if self.act_state == StateCodes.execute:
            self.change_state_to(StateCodes.completing)
        elif self.act_state == StateCodes.completing and sc:
            self.change_state_to(StateCodes.completed)

    def pause(self, sc=True):
        if self.act_state == StateCodes.execute:
            self.change_state_to(StateCodes.pausing)
        elif self.act_state == StateCodes.pausing and sc:
            self.change_state_to(StateCodes.paused)

    def resume(self, sc=True):
        if self.act_state == StateCodes.paused:
            self.change_state_to(StateCodes.resuming)
        elif self.act_state == StateCodes.resuming and sc:
            self.change_state_to(StateCodes.execute)

    def reset(self, sc=True):
        if self.act_state in [StateCodes.completed, StateCodes.stopped, StateCodes.aborted]:
            self.change_state_to(StateCodes.resetting)
        elif self.act_state == StateCodes.resetting and sc:
            self.change_state_to(StateCodes.idle)

    def hold(self, sc=True):
        if self.act_state in [StateCodes.starting, StateCodes.execute, StateCodes.completing,
                              StateCodes.resuming, StateCodes.paused, StateCodes.pausing, StateCodes.unholding]:
            self.change_state_to(StateCodes.holding)
        elif self.act_state == StateCodes.holding and sc:
            self.change_state_to(StateCodes.held)

    def unhold(self, sc=True):
        if self.act_state == StateCodes.held:
            self.change_state_to(StateCodes.unholding)
        elif self.act_state == StateCodes.unholding and sc:
            self.change_state_to(StateCodes.execute)

    def stop(self, sc=True):
        if self.act_state in [StateCodes.idle, StateCodes.starting, StateCodes.execute, StateCodes.completing,
                              StateCodes.completed, StateCodes.resuming, StateCodes.paused, StateCodes.pausing,
                              StateCodes.holding, StateCodes.held, StateCodes.unholding, StateCodes.resetting]:
            self.change_state_to(StateCodes.stopping)
        elif self.act_state == StateCodes.stopping and sc:
            self.change_state_to(StateCodes.stopped)

    def abort(self, sc=True):
        if self.act_state in [StateCodes.idle, StateCodes.starting, StateCodes.execute, StateCodes.completing,
                              StateCodes.completed, StateCodes.resuming, StateCodes.paused, StateCodes.pausing,
                              StateCodes.holding, StateCodes.held, StateCodes.unholding, StateCodes.stopping,
                              StateCodes.stopped, StateCodes.resetting]:
            self.change_state_to(StateCodes.aborting)
        elif self.act_state == StateCodes.aborting and sc:
            self.change_state_to(StateCodes.aborted)

    def get_current_state_int(self):
        return self.act_state

    def get_current_state_str(self):
        return StateCodes.int_code[self.act_state]

    def is_state_str(self, state_str):
        return self.act_state == eval(f'self.{state_str}')

    def is_state_int(self, state_int):
        return self.act_state == state_int

    def is_state(self, state):
        if type(state) == int:
            return self.is_state_int(state)
        elif type(state) == str:
            return self.is_state_str(state)

    def update_prev_state(self):
        self.prev_state = self.act_state
