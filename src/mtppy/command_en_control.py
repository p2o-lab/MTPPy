class CommandEnControl:
    def __init__(self):
        self.command_en = {
            'undefined': {'default': False, 'value': False, 'bit_no': 0, 'int': 1},
            'reset': {'default': False, 'value': False, 'bit_no': 1, 'int': 2},
            'start': {'default': False, 'value': False, 'bit_no': 2, 'int': 4},
            'stop': {'default': True, 'value': True, 'bit_no': 3, 'int': 8},
            'hold': {'default': False, 'value': False, 'bit_no': 4, 'int': 16},
            'unhold': {'default': False, 'value': False, 'bit_no': 5, 'int': 32},
            'pause': {'default': False, 'value': False, 'bit_no': 6, 'int': 64},
            'resume': {'default': False, 'value': False, 'bit_no': 7, 'int': 128},
            'abort': {'default': True, 'value': True, 'bit_no': 8, 'int': 256},
            'restart': {'default': False, 'value': False, 'bit_no': 9, 'int': 512},
            'complete': {'default': False, 'value': False, 'bit_no': 10, 'int': 1024},
        }
        self.hold_enabled = True
        self.pause_enabled = True
        self.restart_enabled = True

    def set_default(self):
        for command_en in self.command_en:
            self.command_en[command_en]['value'] = self.command_en[command_en]['default']

    def disable_all(self):
        for command_en in self.command_en:
            self.command_en[command_en]['value'] = False

    def get_command(self, cmd):
        if cmd in self.command_en.keys():
            return self.command_en[cmd]['value']
        else:
            return None

    def get_command_en(self):
        command_en_sum = 0
        for command in self.command_en.values():
            if command['value']:
                command_en_sum += command['int']
        return command_en_sum

    def set_command(self, cmd, value):
        if cmd in self.command_en.keys():
            self.command_en[cmd]['value'] = value

    def enable_hold_loop(self, value: bool):
        self.hold_enabled = value

    def enable_pause_loop(self, value: bool):
        self.pause_enabled = value

    def enable_restart(self, value: bool):
        self.restart_enabled = value

    def execute(self, state):
        print(f'CommandEn changed to correspond {state}')
        exec(f'self._execute_{state}()')

    def _execute_undefined(self):
        self.disable_all()

    def _execute_idle(self):
        self.set_command('reset', False)
        self.set_command('start', True)
        self.set_command('stop', True)
        if self.hold_enabled:
            self.set_command('hold', False)
            self.set_command('unhold', False)
        if self.pause_enabled:
            self.set_command('pause', False)
            self.set_command('resume', False)
        self.set_command('abort', True)
        if self.restart_enabled:
            self.set_command('restart', False)
        self.set_command('complete', False)

    def _execute_starting(self):
        self.set_command('reset', False)
        self.set_command('start', False)
        self.set_command('stop', True)
        if self.hold_enabled:
            self.set_command('hold', True)
            self.set_command('unhold', False)
        if self.pause_enabled:
            self.set_command('pause', False)
            self.set_command('resume', False)
        self.set_command('abort', True)
        if self.restart_enabled:
            self.set_command('restart', False)
        self.set_command('complete', True)

    def _execute_execute(self):
        self.set_command('reset', False)
        self.set_command('start', False)
        self.set_command('stop', True)
        if self.hold_enabled:
            self.set_command('hold', True)
            self.set_command('unhold', False)
        if self.pause_enabled:
            self.set_command('pause', True)
            self.set_command('resume', False)
        self.set_command('abort', True)
        if self.restart_enabled:
            self.set_command('restart', True)
        self.set_command('complete', True)

    def _execute_completing(self):
        self.set_command('reset', False)
        self.set_command('start', False)
        self.set_command('stop', True)
        if self.hold_enabled:
            self.set_command('hold', True)
            self.set_command('unhold', False)
        if self.pause_enabled:
            self.set_command('pause', False)
            self.set_command('resume', False)
        self.set_command('abort', True)
        if self.restart_enabled:
            self.set_command('restart', False)
        self.set_command('complete', False)

    def _execute_completed(self):
        self.set_command('reset', True)
        self.set_command('start', False)
        self.set_command('stop', True)
        if self.hold_enabled:
            self.set_command('hold', False)
            self.set_command('unhold', False)
        if self.pause_enabled:
            self.set_command('pause', False)
            self.set_command('resume', False)
        self.set_command('abort', True)
        if self.restart_enabled:
            self.set_command('restart', False)
        self.set_command('complete', False)

    def _execute_resuming(self):
        self.set_command('reset', False)
        self.set_command('start', False)
        self.set_command('stop', True)
        if self.hold_enabled:
            self.set_command('hold', False)
            self.set_command('unhold', False)
        if self.pause_enabled:
            self.set_command('pause', False)
            self.set_command('resume', False)
        self.set_command('abort', True)
        if self.restart_enabled:
            self.set_command('restart', False)
        self.set_command('complete', True)

    def _execute_paused(self):
        self.set_command('reset', False)
        self.set_command('start', False)
        self.set_command('stop', True)
        if self.hold_enabled:
            self.set_command('hold', False)
            self.set_command('unhold', False)
        if self.pause_enabled:
            self.set_command('pause', False)
            self.set_command('resume', True)
        self.set_command('abort', True)
        if self.restart_enabled:
            self.set_command('restart', False)
        self.set_command('complete', True)

    def _execute_pausing(self):
        self.set_command('reset', False)
        self.set_command('start', False)
        self.set_command('stop', True)
        if self.hold_enabled:
            self.set_command('hold', False)
            self.set_command('unhold', False)
        if self.pause_enabled:
            self.set_command('pause', False)
            self.set_command('resume', False)
        self.set_command('abort', True)
        if self.restart_enabled:
            self.set_command('restart', False)
        self.set_command('complete', True)

    def _execute_holding(self):
        self.set_command('reset', False)
        self.set_command('start', False)
        self.set_command('stop', True)
        if self.hold_enabled:
            self.set_command('hold', False)
            self.set_command('unhold', False)
        if self.pause_enabled:
            self.set_command('pause', False)
            self.set_command('resume', False)
        self.set_command('abort', True)
        if self.restart_enabled:
            self.set_command('restart', False)
        self.set_command('complete', False)

    def _execute_held(self):
        self.set_command('reset', False)
        self.set_command('start', False)
        self.set_command('stop', True)
        if self.hold_enabled:
            self.set_command('hold', False)
            self.set_command('unhold', True)
        if self.pause_enabled:
            self.set_command('pause', False)
            self.set_command('resume', False)
        self.set_command('abort', True)
        if self.restart_enabled:
            self.set_command('restart', False)
        self.set_command('complete', False)

    def _execute_unholding(self):
        self.set_command('reset', False)
        self.set_command('start', False)
        self.set_command('stop', True)
        if self.hold_enabled:
            self.set_command('hold', False)
            self.set_command('unhold', False)
        if self.pause_enabled:
            self.set_command('pause', False)
            self.set_command('resume', False)
        self.set_command('abort', True)
        if self.restart_enabled:
            self.set_command('restart', False)
        self.set_command('complete', True)

    def _execute_stopping(self):
        self.set_command('reset', False)
        self.set_command('start', False)
        self.set_command('stop', False)
        if self.hold_enabled:
            self.set_command('hold', False)
            self.set_command('unhold', False)
        if self.pause_enabled:
            self.set_command('pause', False)
            self.set_command('resume', False)
        self.set_command('abort', True)
        if self.restart_enabled:
            self.set_command('restart', False)
        self.set_command('complete', False)

    def _execute_stopped(self):
        self.set_command('reset', True)
        self.set_command('start', False)
        self.set_command('stop', False)
        if self.hold_enabled:
            self.set_command('hold', False)
            self.set_command('unhold', False)
        if self.pause_enabled:
            self.set_command('pause', False)
            self.set_command('resume', False)
        self.set_command('abort', True)
        if self.restart_enabled:
            self.set_command('restart', False)
        self.set_command('complete', False)

    def _execute_aborting(self):
        self.set_command('reset', False)
        self.set_command('start', False)
        self.set_command('stop', False)
        if self.hold_enabled:
            self.set_command('hold', False)
            self.set_command('unhold', False)
        if self.pause_enabled:
            self.set_command('pause', False)
            self.set_command('resume', False)
        self.set_command('abort', False)
        if self.restart_enabled:
            self.set_command('restart', False)
        self.set_command('complete', False)

    def _execute_aborted(self):
        self.set_command('reset', True)
        self.set_command('start', False)
        self.set_command('stop', False)
        if self.hold_enabled:
            self.set_command('hold', False)
            self.set_command('unhold', False)
        if self.pause_enabled:
            self.set_command('pause', False)
            self.set_command('resume', False)
        self.set_command('abort', False)
        if self.restart_enabled:
            self.set_command('restart', False)
        self.set_command('complete', False)

    def _execute_resetting(self):
        self.set_command('reset', False)
        self.set_command('start', False)
        self.set_command('stop', False)
        if self.hold_enabled:
            self.set_command('hold', False)
            self.set_command('unhold', False)
        if self.pause_enabled:
            self.set_command('pause', False)
            self.set_command('resume', False)
        self.set_command('abort', False)
        if self.restart_enabled:
            self.set_command('restart', False)
        self.set_command('complete', False)
