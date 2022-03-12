from threading import Thread


class ThreadControl:
    def __init__(self):
        self.thread_stop_flags = {
            'idle': {'default': False, 'value': False},
            'starting': {'default': False, 'value': False},
            'execute': {'default': False, 'value': False},
            'completing': {'default': False, 'value': False},
            'complete': {'default': False, 'value': False},
            'completed': {'default': False, 'value': False},
            'resuming': {'default': False, 'value': False},
            'pause': {'default': False, 'value': False},
            'pausing': {'default': False, 'value': False},
            'paused': {'default': False, 'value': False},
            'holding': {'default': False, 'value': False},
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

    def get_flag(self, flag: str):
        return self.thread_stop_flags[flag]['value']

    def execute(self, state: str, function: callable):
        print(f'Execute thread control of state {state}')
        [self.set_flag(flag, True) for flag in self.thread_stop_flags]
        self.set_flag(state, False)
        Thread(target=function).start()
        