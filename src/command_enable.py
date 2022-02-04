class CommandEn:
    def __init__(self):
        self.commands = {
            'Undefined': {'default': False, 'value': False, 'bit_no': 0, 'int': 1},
            'Reset': {'default': False, 'value': False, 'bit_no': 1, 'int': 2},
            'Start': {'default': False, 'value': False, 'bit_no': 2, 'int': 4},
            'Stop': {'default': True, 'value': True, 'bit_no': 3, 'int': 8},
            'Hold': {'default': False, 'value': False, 'bit_no': 4, 'int': 16},
            'Unhold': {'default': False, 'value': False, 'bit_no': 5, 'int': 32},
            'Pause': {'default': False, 'value': False, 'bit_no': 6, 'int': 64},
            'Resume': {'default': False, 'value': False, 'bit_no': 7, 'int': 128},
            'Abort': {'default': True, 'value': True, 'bit_no': 8, 'int': 256},
            'Restart': {'default': False, 'value': False, 'bit_no': 9, 'int': 512},
            'Complete': {'default': False, 'value': False, 'bit_no': 10, 'int': 1024},
        }

    def set_command(self, command, value):
        self.commands[command]['value'] = value

    def is_enabled(self, command):
        return self.commands[command]['value']

    def get_command_en(self):
        command_en_sum = 0
        for command in self.commands.values():
            if command['value']:
                command_en_sum = + command['int']
        return command_en_sum

    def reset(self):
        for command in self.commands.values():
            command['value'] = command['default']
