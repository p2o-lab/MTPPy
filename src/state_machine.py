from src.variable import Variable
from src.command_enable import CommandEn
from opcua import ua


class StateMachine:
    def __init__(self, opcua_server, opcua_ns, opcua_prefix, source_mode, operation_mode, execution_routine):

        self.command_en = CommandEn()

        self.Pause_disabled = False
        self.Hold_disabled = False
        self.Pause_Hold_disabled = False

        self.Idle = 16
        self.Starting = 8
        self.Execute = 64
        self.Completing = 65536
        self.Completed = 131072
        self.Resuming = 16384
        self.Paused = 32
        self.Pausing = 8192
        self.Holding = 1024
        self.Held = 2048
        self.Unholding = 4096
        self.Stopping = 128
        self.Stopped = 4
        self.Aborting = 256
        self.Aborted = 512
        self.Resetting = 32678

        self.act_state = self.Idle

        self.source_mode = source_mode
        self.operation_mode = operation_mode

        self.variables = {}

        self.opcua_server = opcua_server
        self.opcua_ns = opcua_ns
        self.opcua_prefix = f'{opcua_prefix}.state_machine'

        self.execution_routine = execution_routine

        self._attach_opcua_nodes()

    def _attach_opcua_nodes(self):

        variables = {
            'CommandOp': {'type': ua.VariantType.UInt32, 'init_value': 0, 'callback': self.set_CommandOp, 'writable': True},
            'CommandInt': {'type': ua.VariantType.UInt32, 'init_value': 0, 'callback': self.set_CommandInt, 'writable': True},
            'CommandExt': {'type': ua.VariantType.UInt32, 'init_value': 0, 'callback': self.set_CommandExt, 'writable': True},
            'StateCur': {'type': ua.VariantType.UInt32, 'init_value': self.Idle, 'callback': None, 'writable': False},
            'CommandEn': {'type': ua.VariantType.UInt32, 'init_value': self.command_en.get_command_en(), 'callback': None, 'writable': False},
        }

        for var_name, var_dict in variables.items():
            var_opcua_node_obj = self.opcua_server.get_node(f'ns={self.opcua_ns};s={self.opcua_prefix}.{var_name}')
            self.variables[var_name] = Variable(var_name,
                                                opcua_type=var_dict['type'],
                                                init_value=var_dict['init_value'],
                                                opcua_node_obj=var_opcua_node_obj,
                                                writable=var_dict['writable'],
                                                callback=var_dict['callback'])

    # TODO implement error messages if not valid state changes are blocked
    def change_state_to(self, new_state):
        print('Service state changed to %i' % new_state)
        self.act_state = new_state
        self.write_cur_state()
        self.write_command_en()
        self.execution_routine()

    def Start(self, SC=True):
        if self.act_state == self.Starting and SC == True:
            self.change_state_to(self.Execute)
        elif self.act_state == self.Idle:
            self.change_state_to(self.Starting)

    def Restart(self, SC=True):
        if self.act_state == self.Starting and SC == True:
            self.change_state_to(self.Execute)
        elif self.act_state == self.Execute:
            self.change_state_to(self.Starting)

    def Complete(self, SC=True):
        if self.act_state == self.Completing and SC == True:
            self.change_state_to(self.Completed)
        elif self.act_state == self.Execute:
            self.change_state_to(self.Completing)

    def Pause(self, SC=True):
        if self.act_state == self.Pausing and SC == True:
            self.change_state_to(self.Paused)
        elif self.act_state == self.Execute and self.Pause_disabled == False and self.Pause_Hold_disabled == False:
            self.change_state_to(self.Pausing)

    def Resume(self, SC=True):
        if self.act_state == self.Resuming and SC == True:
            self.change_state_to(self.Execute)
        elif self.act_state == self.Paused:
            self.change_state_to(self.Resuming)

    def Reset(self, SC=True):
        if self.act_state == self.Resetting and SC == True:
            self.change_state_to(self.Idle)
        elif self.act_state in [self.Completed, self.Stopped, self.Aborted]:
            self.change_state_to(self.Resetting)

    def Hold(self, SC=True):
        if self.act_state == self.Holding and SC == True:
            self.change_state_to(self.Held)
        elif self.act_state in [self.Starting, self.Execute, self.Completing,
                                self.Resuming, self.Paused, self.Pausing, self.Unholding] \
                and self.Hold_disabled == False and self.Pause_Hold_disabled == False:
            self.change_state_to(self.Holding)

    def Unhold(self, SC=True):
        if self.act_state == self.Unholding and SC == True:
            self.change_state_to(self.Execute)
        elif self.act_state == self.Held:
            self.change_state_to(self.Unholding)

    def Stop(self, SC=True):
        if self.act_state == self.Stopping and SC == True:
            self.change_state_to(self.Stopped)
        elif self.act_state in [self.Idle, self.Starting, self.Execute, self.Completing,
                                self.Completed, self.Resuming, self.Paused, self.Pausing,
                                self.Holding, self.Held, self.Unholding, self.Resetting]:
            self.change_state_to(self.Stopping)

    def Abort(self, SC=True):
        if self.act_state == self.Aborting and SC == True:
            self.change_state_to(self.Aborted)
        elif self.act_state in [self.Idle, self.Starting, self.Execute, self.Completing,
                                self.Completed, self.Resuming, self.Paused, self.Pausing,
                                self.Holding, self.Held, self.Unholding, self.Stopping, self.Stopped, self.Resetting]:
            self.change_state_to(self.Aborting)

    def write_cur_state(self):
        self.variables['StateCur'].write_value(self.act_state)

    def write_command_en(self):
        self.variables['CommandEn'].write_value(self.command_en.get_command_en())

    def set_CommandOp(self, value):
        if self.source_mode != 'off':
            if self.operation_mode.variables['StateOpAct']:
                self.ex_command(value, SC=False)

    def set_CommandInt(self, value):
        if self.source_mode != 'off':
            if self.operation_mode.variables['StateAutAct'] and self.source_mode.variables['SrcIntAct']:
                self.ex_command(value, SC=False)

    def set_CommandExt(self, value):
        if self.source_mode != 'off':
            if self.operation_mode.variables['StateAutAct'] and self.source_mode.variables['SrcExtAct']:
                self.ex_command(value, SC=False)

    def ex_command(self, com_var, SC=True):
        if com_var == 2:
            self.Reset(SC)
        elif com_var == 4:
            self.Start(SC)
        elif com_var == 8:
            self.Stop(SC)
        elif com_var == 16:
            self.Hold(SC)
        elif com_var == 32:
            self.Unhold(SC)
        elif com_var == 64:
            self.Pause(SC)
        elif com_var == 128:
            self.Resume(SC)
        elif com_var == 256:
            self.Abort(SC)
        elif com_var == 512:
            self.Restart(SC)
        elif com_var == 1024:
            self.Complete(SC)

    def get_current_state(self):
        return self.act_state

    def is_state_str(self, state_str):
        return self.act_state == eval(f'self.{state_str}')

    def is_state_int(self, state_int):
        return self.act_state == state_int

    def is_state(self, state):
        if type(state) == int:
            return self.is_state_int(state)
        elif type(state) == str:
            return self.is_state_str(state)
