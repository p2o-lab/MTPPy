import logging


class CommandEnControl:
    def __init__(self):
        """
        Command enable control.
        """
        self.command_en = {
            'undefined': {'default': False, 'value': False, 'bit_no': 0, 'int': 1},
            'reset': {'default': False, 'value': False, 'bit_no': 1, 'int': 2},
            'start': {'default': True, 'value': True, 'bit_no': 2, 'int': 4},
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
        """
        Applies default values to all command enable flags.
        :return:
        """
        for command_en in self.command_en:
            self.command_en[command_en]['value'] = self.command_en[command_en]['default']

    def disable_all(self):
        """
        Sets False to all command enable flags.
        :return:
        """
        for command_en in self.command_en:
            self.command_en[command_en]['value'] = False

    def is_enabled(self, cmd: str):
        """
        Checks if a given command is enabled right now.
        :param cmd: Command to check.
        :return: Command enable flag state.
        """
        if cmd in self.command_en.keys():
            return self.command_en[cmd]['value']
        else:
            return None

    def get_command_en(self):
        """
        Calculates a sum of all command enable flags.
        :return: Sum of all command enable flags.
        """
        command_en_sum = 0
        for command in self.command_en.values():
            if command['value']:
                command_en_sum += command['int']
        return command_en_sum

    def set_command_en(self, cmd: str, value: bool):
        """
        Sets a specific command enable to a given value.
        :param cmd: Command enable flag.
        :param value: Value to be set.
        :return:
        """
        if cmd in self.command_en.keys():
            self.command_en[cmd]['value'] = value

    def enable_hold_loop(self, value: bool):
        """
        Enables hold loop.
        :param value: True if the hold loop is to active and False if to disable.
        :return:
        """
        self.hold_enabled = value

    def enable_pause_loop(self, value: bool):
        """
        Enables pause loop.
        :param value: True if the pause loop is to active and False if to disable.
        :return:
        """
        self.pause_enabled = value

    def enable_restart(self, value: bool):
        """
        Enables restart loop.
        :param value: True if the restart command is to active and False if to disable.
        :return:
        """
        self.restart_enabled = value

    def execute(self, state: str):
        """
        Executes command enable changes required for a certain state.
        :param state: Given state.
        :return:
        """
        logging.debug(f'CommandEn changed to correspond {state}')
        exec(f'self._execute_{state}()')

    def _execute_undefined(self):
        self.disable_all()

    def _execute_idle(self):
        self.set_command_en('reset', False)
        self.set_command_en('start', True)
        self.set_command_en('stop', True)
        if self.hold_enabled:
            self.set_command_en('hold', False)
            self.set_command_en('unhold', False)
        if self.pause_enabled:
            self.set_command_en('pause', False)
            self.set_command_en('resume', False)
        self.set_command_en('abort', True)
        if self.restart_enabled:
            self.set_command_en('restart', False)
        self.set_command_en('complete', False)

    def _execute_starting(self):
        self.set_command_en('reset', False)
        self.set_command_en('start', False)
        self.set_command_en('stop', True)
        if self.hold_enabled:
            self.set_command_en('hold', True)
            self.set_command_en('unhold', False)
        if self.pause_enabled:
            self.set_command_en('pause', False)
            self.set_command_en('resume', False)
        self.set_command_en('abort', True)
        if self.restart_enabled:
            self.set_command_en('restart', False)
        self.set_command_en('complete', True)

    def _execute_execute(self):
        self.set_command_en('reset', False)
        self.set_command_en('start', False)
        self.set_command_en('stop', True)
        if self.hold_enabled:
            self.set_command_en('hold', True)
            self.set_command_en('unhold', False)
        if self.pause_enabled:
            self.set_command_en('pause', True)
            self.set_command_en('resume', False)
        self.set_command_en('abort', True)
        if self.restart_enabled:
            self.set_command_en('restart', True)
        self.set_command_en('complete', True)

    def _execute_completing(self):
        self.set_command_en('reset', False)
        self.set_command_en('start', False)
        self.set_command_en('stop', True)
        if self.hold_enabled:
            self.set_command_en('hold', True)
            self.set_command_en('unhold', False)
        if self.pause_enabled:
            self.set_command_en('pause', False)
            self.set_command_en('resume', False)
        self.set_command_en('abort', True)
        if self.restart_enabled:
            self.set_command_en('restart', False)
        self.set_command_en('complete', False)

    def _execute_completed(self):
        self.set_command_en('reset', True)
        self.set_command_en('start', False)
        self.set_command_en('stop', True)
        if self.hold_enabled:
            self.set_command_en('hold', False)
            self.set_command_en('unhold', False)
        if self.pause_enabled:
            self.set_command_en('pause', False)
            self.set_command_en('resume', False)
        self.set_command_en('abort', True)
        if self.restart_enabled:
            self.set_command_en('restart', False)
        self.set_command_en('complete', False)

    def _execute_resuming(self):
        self.set_command_en('reset', False)
        self.set_command_en('start', False)
        self.set_command_en('stop', True)
        if self.hold_enabled:
            self.set_command_en('hold', True)
            self.set_command_en('unhold', False)
        if self.pause_enabled:
            self.set_command_en('pause', False)
            self.set_command_en('resume', False)
        self.set_command_en('abort', True)
        if self.restart_enabled:
            self.set_command_en('restart', False)
        self.set_command_en('complete', True)

    def _execute_paused(self):
        self.set_command_en('reset', False)
        self.set_command_en('start', False)
        self.set_command_en('stop', True)
        if self.hold_enabled:
            self.set_command_en('hold', True)
            self.set_command_en('unhold', False)
        if self.pause_enabled:
            self.set_command_en('pause', False)
            self.set_command_en('resume', True)
        self.set_command_en('abort', True)
        if self.restart_enabled:
            self.set_command_en('restart', False)
        self.set_command_en('complete', True)

    def _execute_pausing(self):
        self.set_command_en('reset', False)
        self.set_command_en('start', False)
        self.set_command_en('stop', True)
        if self.hold_enabled:
            self.set_command_en('hold', True)
            self.set_command_en('unhold', False)
        if self.pause_enabled:
            self.set_command_en('pause', False)
            self.set_command_en('resume', False)
        self.set_command_en('abort', True)
        if self.restart_enabled:
            self.set_command_en('restart', False)
        self.set_command_en('complete', True)

    def _execute_holding(self):
        self.set_command_en('reset', False)
        self.set_command_en('start', False)
        self.set_command_en('stop', True)
        if self.hold_enabled:
            self.set_command_en('hold', False)
            self.set_command_en('unhold', False)
        if self.pause_enabled:
            self.set_command_en('pause', False)
            self.set_command_en('resume', False)
        self.set_command_en('abort', True)
        if self.restart_enabled:
            self.set_command_en('restart', False)
        self.set_command_en('complete', False)

    def _execute_held(self):
        self.set_command_en('reset', False)
        self.set_command_en('start', False)
        self.set_command_en('stop', True)
        if self.hold_enabled:
            self.set_command_en('hold', False)
            self.set_command_en('unhold', True)
        if self.pause_enabled:
            self.set_command_en('pause', False)
            self.set_command_en('resume', False)
        self.set_command_en('abort', True)
        if self.restart_enabled:
            self.set_command_en('restart', False)
        self.set_command_en('complete', False)

    def _execute_unholding(self):
        self.set_command_en('reset', False)
        self.set_command_en('start', False)
        self.set_command_en('stop', True)
        if self.hold_enabled:
            self.set_command_en('hold', True)
            self.set_command_en('unhold', False)
        if self.pause_enabled:
            self.set_command_en('pause', False)
            self.set_command_en('resume', False)
        self.set_command_en('abort', True)
        if self.restart_enabled:
            self.set_command_en('restart', False)
        self.set_command_en('complete', True)

    def _execute_stopping(self):
        self.set_command_en('reset', False)
        self.set_command_en('start', False)
        self.set_command_en('stop', False)
        if self.hold_enabled:
            self.set_command_en('hold', False)
            self.set_command_en('unhold', False)
        if self.pause_enabled:
            self.set_command_en('pause', False)
            self.set_command_en('resume', False)
        self.set_command_en('abort', True)
        if self.restart_enabled:
            self.set_command_en('restart', False)
        self.set_command_en('complete', False)

    def _execute_stopped(self):
        self.set_command_en('reset', True)
        self.set_command_en('start', False)
        self.set_command_en('stop', False)
        if self.hold_enabled:
            self.set_command_en('hold', False)
            self.set_command_en('unhold', False)
        if self.pause_enabled:
            self.set_command_en('pause', False)
            self.set_command_en('resume', False)
        self.set_command_en('abort', True)
        if self.restart_enabled:
            self.set_command_en('restart', False)
        self.set_command_en('complete', False)

    def _execute_aborting(self):
        self.set_command_en('reset', False)
        self.set_command_en('start', False)
        self.set_command_en('stop', False)
        if self.hold_enabled:
            self.set_command_en('hold', False)
            self.set_command_en('unhold', False)
        if self.pause_enabled:
            self.set_command_en('pause', False)
            self.set_command_en('resume', False)
        self.set_command_en('abort', False)
        if self.restart_enabled:
            self.set_command_en('restart', False)
        self.set_command_en('complete', False)

    def _execute_aborted(self):
        self.set_command_en('reset', True)
        self.set_command_en('start', False)
        self.set_command_en('stop', False)
        if self.hold_enabled:
            self.set_command_en('hold', False)
            self.set_command_en('unhold', False)
        if self.pause_enabled:
            self.set_command_en('pause', False)
            self.set_command_en('resume', False)
        self.set_command_en('abort', False)
        if self.restart_enabled:
            self.set_command_en('restart', False)
        self.set_command_en('complete', False)

    def _execute_resetting(self):
        self.set_command_en('reset', False)
        self.set_command_en('start', False)
        self.set_command_en('stop', True)
        if self.hold_enabled:
            self.set_command_en('hold', False)
            self.set_command_en('unhold', False)
        if self.pause_enabled:
            self.set_command_en('pause', False)
            self.set_command_en('resume', False)
        self.set_command_en('abort', True)
        if self.restart_enabled:
            self.set_command_en('restart', False)
        self.set_command_en('complete', False)
