class ThreadStopFlags:
    def __init__(self):
        self.flags = {
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

    def set_flag(self, flag, value):
        print(f'Flag {flag} set to {value}')
        self.flags[flag]['value'] = value

    def get_flag(self, flag):
        return self.flags[flag]['value']

    def reset(self):
        for flag in self.flags.values():
            flag['value'] = flag['default']
