from src.command_enable import CommandEn


class CommandEnControl:
    def __init__(self):
        self.command_en = CommandEn()
        self.hold_enabled = True
        self.pause_enabled = True
        self.restart_enabled = True

    def set_command(self, cmd, value):
        self.command_en.set_command(cmd, value)

    def enable_hold_loop(self, value: bool):
        self.hold_enabled = value

    def enable_pause_loop(self, value: bool):
        self.pause_enabled = value

    def enable_restart(self, value: bool):
        self.restart_enabled = value

    def execute(self, state):
        exec(f'self.execute_{state}')

    def execute_idle(self):
        self.command_en.set_command('reset', False)
        self.command_en.set_command('start', True)
        self.command_en.set_command('stop', True)
        if self.hold_enabled:
            self.command_en.set_command('hold', False)
            self.command_en.set_command('unhold', False)
        if self.pause_enabled:
            self.command_en.set_command('pause', False)
            self.command_en.set_command('resume', False)
        self.command_en.set_command('abort', True)
        if self.restart_enabled:
            self.command_en.set_command('restart', False)
        self.command_en.set_command('complete', False)

    def execute_starting(self):
        self.command_en.set_command('reset', False)
        self.command_en.set_command('start', False)
        self.command_en.set_command('stop', True)
        if self.hold_enabled:
            self.command_en.set_command('hold', True)
            self.command_en.set_command('unhold', False)
        if self.pause_enabled:
            self.command_en.set_command('pause', False)
            self.command_en.set_command('resume', False)
        self.command_en.set_command('abort', True)
        if self.restart_enabled:
            self.command_en.set_command('restart', False)
        self.command_en.set_command('complete', True)

    def execute_execute(self):
        self.command_en.set_command('reset', False)
        self.command_en.set_command('start', False)
        self.command_en.set_command('stop', True)
        if self.hold_enabled:
            self.command_en.set_command('hold', True)
            self.command_en.set_command('unhold', False)
        if self.pause_enabled:
            self.command_en.set_command('pause', True)
            self.command_en.set_command('resume', False)
        self.command_en.set_command('abort', True)
        if self.restart_enabled:
            self.command_en.set_command('restart', True)
        self.command_en.set_command('complete', True)

    def execute_completing(self):
        self.command_en.set_command('reset', False)
        self.command_en.set_command('start', False)
        self.command_en.set_command('stop', True)
        if self.hold_enabled:
            self.command_en.set_command('hold', True)
            self.command_en.set_command('unhold', False)
        if self.pause_enabled:
            self.command_en.set_command('pause', False)
            self.command_en.set_command('resume', False)
        self.command_en.set_command('abort', True)
        if self.restart_enabled:
            self.command_en.set_command('restart', False)
        self.command_en.set_command('complete', True)

    def execute_completed(self):
        self.command_en.set_command('reset', True)
        self.command_en.set_command('start', False)
        self.command_en.set_command('stop', True)
        if self.hold_enabled:
            self.command_en.set_command('hold', False)
            self.command_en.set_command('unhold', False)
        if self.pause_enabled:
            self.command_en.set_command('pause', False)
            self.command_en.set_command('resume', False)
        self.command_en.set_command('abort', True)
        if self.restart_enabled:
            self.command_en.set_command('restart', False)
        self.command_en.set_command('complete', True)

    def execute_resuming(self):
        self.command_en.set_command('reset', False)
        self.command_en.set_command('start', False)
        self.command_en.set_command('stop', True)
        if self.hold_enabled:
            self.command_en.set_command('hold', False)
            self.command_en.set_command('unhold', False)
        if self.pause_enabled:
            self.command_en.set_command('pause', False)
            self.command_en.set_command('resume', False)
        self.command_en.set_command('abort', True)
        if self.restart_enabled:
            self.command_en.set_command('restart', False)
        self.command_en.set_command('complete', True)

    def execute_paused(self):
        self.command_en.set_command('reset', False)
        self.command_en.set_command('start', False)
        self.command_en.set_command('stop', True)
        if self.hold_enabled:
            self.command_en.set_command('hold', False)
            self.command_en.set_command('unhold', False)
        if self.pause_enabled:
            self.command_en.set_command('pause', False)
            self.command_en.set_command('resume', True)
        self.command_en.set_command('abort', True)
        if self.restart_enabled:
            self.command_en.set_command('restart', False)
        self.command_en.set_command('complete', True)

    def execute_pausing(self):
        self.command_en.set_command('reset', False)
        self.command_en.set_command('start', False)
        self.command_en.set_command('stop', True)
        if self.hold_enabled:
            self.command_en.set_command('hold', False)
            self.command_en.set_command('unhold', False)
        if self.pause_enabled:
            self.command_en.set_command('pause', False)
            self.command_en.set_command('resume', False)
        self.command_en.set_command('abort', True)
        if self.restart_enabled:
            self.command_en.set_command('restart', False)
        self.command_en.set_command('complete', True)

    def execute_holding(self):
        self.command_en.set_command('reset', False)
        self.command_en.set_command('start', False)
        self.command_en.set_command('stop', True)
        if self.hold_enabled:
            self.command_en.set_command('hold', False)
            self.command_en.set_command('unhold', False)
        if self.pause_enabled:
            self.command_en.set_command('pause', False)
            self.command_en.set_command('resume', False)
        self.command_en.set_command('abort', True)
        if self.restart_enabled:
            self.command_en.set_command('restart', False)
        self.command_en.set_command('complete', True)

    def execute_held(self):
        self.command_en.set_command('reset', False)
        self.command_en.set_command('start', False)
        self.command_en.set_command('stop', True)
        if self.hold_enabled:
            self.command_en.set_command('hold', False)
            self.command_en.set_command('unhold', True)
        if self.pause_enabled:
            self.command_en.set_command('pause', False)
            self.command_en.set_command('resume', False)
        self.command_en.set_command('abort', True)
        if self.restart_enabled:
            self.command_en.set_command('restart', False)
        self.command_en.set_command('complete', False)

    def execute_unholding(self):
        self.command_en.set_command('reset', False)
        self.command_en.set_command('start', False)
        self.command_en.set_command('stop', True)
        if self.hold_enabled:
            self.command_en.set_command('hold', False)
            self.command_en.set_command('unhold', False)
        if self.pause_enabled:
            self.command_en.set_command('pause', False)
            self.command_en.set_command('resume', False)
        self.command_en.set_command('abort', True)
        if self.restart_enabled:
            self.command_en.set_command('restart', False)
        self.command_en.set_command('complete', False)

    def execute_stopping(self):
        self.command_en.set_command('reset', False)
        self.command_en.set_command('start', False)
        self.command_en.set_command('stop', False)
        if self.hold_enabled:
            self.command_en.set_command('hold', False)
            self.command_en.set_command('unhold', False)
        if self.pause_enabled:
            self.command_en.set_command('pause', False)
            self.command_en.set_command('resume', False)
        self.command_en.set_command('abort', True)
        if self.restart_enabled:
            self.command_en.set_command('restart', False)
        self.command_en.set_command('complete', False)

    def execute_stopped(self):
        self.command_en.set_command('reset', True)
        self.command_en.set_command('start', False)
        self.command_en.set_command('stop', False)
        if self.hold_enabled:
            self.command_en.set_command('hold', False)
            self.command_en.set_command('unhold', False)
        if self.pause_enabled:
            self.command_en.set_command('pause', False)
            self.command_en.set_command('resume', False)
        self.command_en.set_command('abort', True)
        if self.restart_enabled:
            self.command_en.set_command('restart', False)
        self.command_en.set_command('complete', False)

    def execute_aborting(self):
        self.command_en.set_command('reset', False)
        self.command_en.set_command('start', False)
        self.command_en.set_command('stop', False)
        if self.hold_enabled:
            self.command_en.set_command('hold', False)
            self.command_en.set_command('unhold', False)
        if self.pause_enabled:
            self.command_en.set_command('pause', False)
            self.command_en.set_command('resume', False)
        self.command_en.set_command('abort', False)
        if self.restart_enabled:
            self.command_en.set_command('restart', False)
        self.command_en.set_command('complete', False)

    def execute_aborted(self):
        self.command_en.set_command('reset', True)
        self.command_en.set_command('start', False)
        self.command_en.set_command('stop', False)
        if self.hold_enabled:
            self.command_en.set_command('hold', False)
            self.command_en.set_command('unhold', False)
        if self.pause_enabled:
            self.command_en.set_command('pause', False)
            self.command_en.set_command('resume', False)
        self.command_en.set_command('abort', False)
        if self.restart_enabled:
            self.command_en.set_command('restart', False)
        self.command_en.set_command('complete', False)

    def execute_resetting(self):
        self.command_en.set_command('reset', False)
        self.command_en.set_command('start', False)
        self.command_en.set_command('stop', False)
        if self.hold_enabled:
            self.command_en.set_command('hold', False)
            self.command_en.set_command('unhold', False)
        if self.pause_enabled:
            self.command_en.set_command('pause', False)
            self.command_en.set_command('resume', False)
        self.command_en.set_command('abort', False)
        if self.restart_enabled:
            self.command_en.set_command('restart', False)
        self.command_en.set_command('complete', False)

