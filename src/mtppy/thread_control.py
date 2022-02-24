from threading import Thread


class ThreadControl:
    def __init__(self):
        self.thread_stop_flags = {
            'idle': {'default': False, 'value': False},
            'starting': {'default': False, 'value': False},
            'execute': {'default': False, 'value': False},
            'completing': {'default': True, 'value': True},
            'complete': {'default': False, 'value': False},
            'completed': {'default': False, 'value': False},
            'resuming': {'default': False, 'value': False},
            'pause': {'default': False, 'value': False},
            'pausing': {'default': False, 'value': False},
            'paused': {'default': False, 'value': False},
            'holding': {'default': True, 'value': True},
            'held': {'default': False, 'value': False},
            'unholding': {'default': False, 'value': False},
            'stopping': {'default': False, 'value': False},
            'stopped': {'default': False, 'value': False},
            'aborting': {'default': False, 'value': False},
            'aborted': {'default': False, 'value': False},
            'resetting': {'default': False, 'value': False},
        }

    def set_flag(self, flag: str, value: bool):
        self.thread_stop_flags[flag]['value'] = value

    def set_all_true_except(self, flag_exc: str):
        print(f'Flag {flag_exc} set to False (rest are True)')
        for flag_key in self.thread_stop_flags:
            if flag_key == flag_exc:
                continue
            self.set_flag(flag_key, True)

    def get_flag(self, flag: str):
        return self.thread_stop_flags[flag]['value']

    def execute_mod(self, state: str, function: callable):
        print(f'Execute thread control of state {state}')
        self.set_all_true_except(state)
        Thread(target=function).start()

    def execute(self, state:str, function: callable):
        print(f'Execute thread control of state {state}')
        exec(f'self.execute_{state}()')
        Thread(target=function).start()

    def execute_idle(self):
        self.set_flag('resetting', True)
        self.set_flag('idle', False)

    def execute_starting(self):
        self.set_flag('idle', True)
        self.set_flag('execute', True)
        self.set_flag('starting', False)

    def execute_execute(self):
        self.set_flag('idle', True)
        self.set_flag('execute', False)

    def execute_completing(self):
        self.set_flag('execute', True)
        self.set_flag('completing', False)

    def execute_completed(self):
        self.set_flag('completing', True)
        self.set_flag('completed', False)

    def execute_resuming(self):
        self.set_flag('paused', True)
        self.set_flag('resuming', False)

    def execute_paused(self):
        self.set_flag('pausing', True)
        self.set_flag('paused', False)

    def execute_pausing(self):
        self.set_flag('execute', True)
        self.set_flag('pausing', False)

    def execute_holding(self):
        self.set_flag('execute', True)
        self.set_flag('starting', True)
        self.set_flag('completing', True)
        self.set_flag('resuming', True)
        self.set_flag('paused', True)
        self.set_flag('pausing', True)
        self.set_flag('unholding', True)
        self.set_flag('holding', False)

    def execute_held(self):
        self.set_flag('holding', True)
        self.set_flag('held', False)

    def execute_unholding(self):
        self.set_flag('held', True)
        self.set_flag('unholding', False)

    def execute_stopping(self):
        self.set_flag('execute', True)
        self.set_flag('starting', True)
        self.set_flag('completing', True)
        self.set_flag('resuming', True)
        self.set_flag('paused', True)
        self.set_flag('pausing', True)
        self.set_flag('holding', True)
        self.set_flag('held', True)
        self.set_flag('unholding', True)
        self.set_flag('completed', True)
        self.set_flag('resetting', True)
        self.set_flag('idle', True)
        self.set_flag('stopping', False)

    def execute_stopped(self):
        self.set_flag('stopping', True)
        self.set_flag('stopped', False)

    def execute_aborting(self):
        self.set_flag('execute', True)
        self.set_flag('starting', True)
        self.set_flag('completing', True)
        self.set_flag('resuming', True)
        self.set_flag('paused', True)
        self.set_flag('pausing', True)
        self.set_flag('holding', True)
        self.set_flag('held', True)
        self.set_flag('unholding', True)
        self.set_flag('completed', True)
        self.set_flag('resetting', True)
        self.set_flag('idle', True)
        self.set_flag('stopping', True)
        self.set_flag('stopped', True)
        self.set_flag('aborting', False)

    def execute_aborted(self):
        self.set_flag('aborting', True)
        self.set_flag('aborted', False)

    def execute_resetting(self):
        self.set_flag('completed', True)
        self.set_flag('stopped', True)
        self.set_flag('aborted', True)
        self.set_flag('resetting', False)
        