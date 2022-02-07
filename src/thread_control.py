from src.thread_stop_flags import ThreadStopFlags
from threading import Thread


class ThreadControl:
    def __init__(self):
        self.thread_stop_flags = ThreadStopFlags()

    def set_flag(self, flag, value):
        self.thread_stop_flags.set_flag(flag, value)

    def get_flag(self, flag):
        return self.thread_stop_flags.get_flag(flag)

    def execute(self, state, function):
        print(f'Execute thread control of state {state}')
        exec(f'self.execute_{state}()')
        Thread(target=function).start()

    def execute_idle(self):
        self.thread_stop_flags.set_flag('resetting', True)
        self.thread_stop_flags.set_flag('idle', False)

    def execute_starting(self):
        self.thread_stop_flags.set_flag('idle', True)
        self.thread_stop_flags.set_flag('execute', True)
        self.thread_stop_flags.set_flag('starting', False)

    def execute_execute(self):
        self.thread_stop_flags.set_flag('idle', True)
        self.thread_stop_flags.set_flag('execute', False)

    def execute_completing(self):
        self.thread_stop_flags.set_flag('execute', True)
        self.thread_stop_flags.set_flag('completing', False)

    def execute_completed(self):
        self.thread_stop_flags.set_flag('completing', True)
        self.thread_stop_flags.set_flag('completed', False)

    def execute_resuming(self):
        self.thread_stop_flags.set_flag('paused', True)
        self.thread_stop_flags.set_flag('resuming', False)

    def execute_paused(self):
        self.thread_stop_flags.set_flag('pausing', True)
        self.thread_stop_flags.set_flag('paused', False)

    def execute_pausing(self):
        self.thread_stop_flags.set_flag('execute', True)
        self.thread_stop_flags.set_flag('pausing', False)

    def execute_holding(self):
        self.thread_stop_flags.set_flag('execute', True)
        self.thread_stop_flags.set_flag('starting', True)
        self.thread_stop_flags.set_flag('completing', True)
        self.thread_stop_flags.set_flag('resuming', True)
        self.thread_stop_flags.set_flag('paused', True)
        self.thread_stop_flags.set_flag('pausing', True)
        self.thread_stop_flags.set_flag('unholding', True)
        self.thread_stop_flags.set_flag('holding', False)

    def execute_held(self):
        self.thread_stop_flags.set_flag('holding', True)
        self.thread_stop_flags.set_flag('held', False)

    def execute_unholding(self):
        self.thread_stop_flags.set_flag('held', True)
        self.thread_stop_flags.set_flag('unholding', False)

    def execute_stopping(self):
        self.thread_stop_flags.set_flag('execute', True)
        self.thread_stop_flags.set_flag('starting', True)
        self.thread_stop_flags.set_flag('completing', True)
        self.thread_stop_flags.set_flag('resuming', True)
        self.thread_stop_flags.set_flag('paused', True)
        self.thread_stop_flags.set_flag('pausing', True)
        self.thread_stop_flags.set_flag('holding', True)
        self.thread_stop_flags.set_flag('held', True)
        self.thread_stop_flags.set_flag('unholding', True)
        self.thread_stop_flags.set_flag('completed', True)
        self.thread_stop_flags.set_flag('resetting', True)
        self.thread_stop_flags.set_flag('idle', True)
        self.thread_stop_flags.set_flag('stopping', False)

    def execute_stopped(self):
        self.thread_stop_flags.set_flag('stopping', True)
        self.thread_stop_flags.set_flag('stopped', False)

    def execute_aborting(self):
        self.thread_stop_flags.set_flag('execute', True)
        self.thread_stop_flags.set_flag('starting', True)
        self.thread_stop_flags.set_flag('completing', True)
        self.thread_stop_flags.set_flag('resuming', True)
        self.thread_stop_flags.set_flag('paused', True)
        self.thread_stop_flags.set_flag('pausing', True)
        self.thread_stop_flags.set_flag('holding', True)
        self.thread_stop_flags.set_flag('held', True)
        self.thread_stop_flags.set_flag('unholding', True)
        self.thread_stop_flags.set_flag('completed', True)
        self.thread_stop_flags.set_flag('resetting', True)
        self.thread_stop_flags.set_flag('idle', True)
        self.thread_stop_flags.set_flag('stopping', True)
        self.thread_stop_flags.set_flag('stopped', True)
        self.thread_stop_flags.set_flag('aborting', False)

    def execute_aborted(self):
        self.thread_stop_flags.set_flag('aborting', True)
        self.thread_stop_flags.set_flag('aborted', False)

    def execute_resetting(self):
        self.thread_stop_flags.set_flag('completed', True)
        self.thread_stop_flags.set_flag('stopped', True)
        self.thread_stop_flags.set_flag('aborted', True)
        self.thread_stop_flags.set_flag('resetting', False)
        