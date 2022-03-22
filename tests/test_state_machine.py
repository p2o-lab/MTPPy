from test_procedure_control import init_procedure_control
from mtppy.state_machine import StateMachine
from mtppy.state_codes import StateCodes
from mtppy.command_codes import CommandCodes

StateCodes = StateCodes()
CommandCodes = CommandCodes()

valid_commands = {
    'stopped': {
        'reset': 'resetting',
        'abort': 'aborting'},
    'starting': {
        'complete': 'completing',
        'hold': 'holding',
        'stop': 'stopping',
        'abort': 'aborting'},
    'idle': {
        'start': 'starting',
        'stop': 'stopping',
        'abort': 'aborting'},
    'paused': {
        'resume': 'resuming',
        'complete': 'completing',
        'hold': 'holding',
        'stop': 'stopping',
        'abort': 'aborting'},
    'execute': {'complete': 'completing',
                'restart': 'starting',
                'pause': 'pausing',
                'hold': 'holding',
                'stop': 'stopping',
                'abort': 'aborting'},
    'stopping': {'abort': 'aborting'},
    'aborting': {},
    'aborted': {
        'reset': 'resetting'},
    'holding': {
        'stop': 'stopping',
        'abort': 'aborting'},
    'held': {
        'unhold': 'unholding',
        'stop': 'stopping',
        'abort': 'aborting'},
    'unholding': {
        'complete': 'completing',
        'hold': 'holding',
        'stop': 'stopping',
        'abort': 'aborting'},
    'pausing': {
        'complete': 'completing',
        'hold': 'holding',
        'stop': 'stopping',
        'abort': 'aborting'},
    'resuming': {
        'complete': 'completing',
        'hold': 'holding',
        'stop': 'stopping',
        'abort': 'aborting'},
    'resetting': {
        'stop': 'stopping',
        'abort': 'aborting'},
    'completing': {
        'hold': 'holding',
        'stop': 'stopping',
        'abort': 'aborting'},
    'completed': {
        'reset': 'resetting',
        'stop': 'stopping',
        'abort': 'aborting'}
}


class CallbackObject:
    def __init__(self):
        self.value = 0

    def value_callback(self):
        self.value = 10


def init_state_machine(state='idle', op_mode='off', src_mode='int'):
    callback_object = CallbackObject()
    procedure_control = init_procedure_control(op_mode=op_mode, src_mode=src_mode)
    op_src_mode = procedure_control.op_src_mode
    state_machine = StateMachine(operation_source_mode=op_src_mode,
                                 procedure_control=procedure_control,
                                 execution_routine=callback_object.value_callback)

    if state == 'stopped':
        state_machine.command_execution(CommandCodes.stop)
        state_machine.state_change()
    elif state == 'starting':
        state_machine.command_execution(CommandCodes.start)
    elif state == 'idle':
        pass
    elif state == 'paused':
        state_machine.command_execution(CommandCodes.start)
        state_machine.state_change()
        state_machine.command_execution(CommandCodes.pause)
        state_machine.state_change()
    elif state == 'execute':
        state_machine.command_execution(CommandCodes.start)
        state_machine.state_change()
    elif state == 'stopping':
        state_machine.command_execution(CommandCodes.stop)
    elif state == 'aborting':
        state_machine.command_execution(CommandCodes.abort)
    elif state == 'aborted':
        state_machine.command_execution(CommandCodes.abort)
        state_machine.state_change()
    elif state == 'holding':
        state_machine.command_execution(CommandCodes.start)
        state_machine.command_execution(CommandCodes.hold)
    elif state == 'held':
        state_machine.command_execution(CommandCodes.start)
        state_machine.command_execution(CommandCodes.hold)
        state_machine.state_change()
    elif state == 'unholding':
        state_machine.command_execution(CommandCodes.start)
        state_machine.command_execution(CommandCodes.hold)
        state_machine.state_change()
        state_machine.command_execution(CommandCodes.unhold)
    elif state == 'pausing':
        state_machine.command_execution(CommandCodes.start)
        state_machine.state_change()
        state_machine.command_execution(CommandCodes.pause)
    elif state == 'resuming':
        state_machine.command_execution(CommandCodes.start)
        state_machine.state_change()
        state_machine.command_execution(CommandCodes.pause)
        state_machine.state_change()
        state_machine.command_execution(CommandCodes.resume)
    elif state == 'resetting':
        state_machine.command_execution(CommandCodes.stop)
        state_machine.state_change()
        state_machine.command_execution(CommandCodes.reset)
    elif state == 'completing':
        state_machine.command_execution(CommandCodes.start)
        state_machine.command_execution(CommandCodes.complete)
    elif state == 'completed':
        state_machine.command_execution(CommandCodes.start)
        state_machine.command_execution(CommandCodes.complete)
        state_machine.state_change()
    print(f'Transition to {state} ', end='')
    if state_machine.get_current_state_str() == state:
        print(f'completed')
    else:
        print(f'failed')
    return state_machine, callback_object


def test_set_command():
    test_scenario = [('off', 'int', 'set_command_op', False),
                     ('off', 'ext', 'set_command_op', False),
                     ('op', 'int', 'set_command_op', True),
                     ('op', 'ext', 'set_command_op', True),
                     ('aut', 'int', 'set_command_op', False),
                     ('aut', 'ext', 'set_command_op', False),

                     ('off', 'int', 'set_command_int', False),
                     ('off', 'ext', 'set_command_int', False),
                     ('op', 'int', 'set_command_int', False),
                     ('op', 'ext', 'set_command_int', False),
                     ('aut', 'int', 'set_command_int', True),
                     ('aut', 'ext', 'set_command_int', False),

                     ('off', 'int', 'set_command_ext', False),
                     ('off', 'ext', 'set_command_ext', False),
                     ('op', 'int', 'set_command_ext', False),
                     ('op', 'ext', 'set_command_ext', False),
                     ('aut', 'int', 'set_command_ext', False),
                     ('aut', 'ext', 'set_command_ext', True)]

    for op_mode, src_mode, set_command, change_allowed in test_scenario:
        for state in StateCodes.get_list_str():
            for command in CommandCodes.get_list_int():
                state_machine, callback_object = init_state_machine(state=state, op_mode=op_mode, src_mode=src_mode)
                eval(f'state_machine.{set_command}({command})')
                command_str = CommandCodes.int_code[command]
                # eval(f'state_machine.{command_str}()')
                if command_str in valid_commands[state].keys() and change_allowed:
                    expected_state = valid_commands[state][command_str]
                else:
                    expected_state = state
                final_state = state_machine.get_current_state_str()
                print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, validity is {change_allowed},', end=' ')
                print(f'transition {state}->({command_str})->{final_state} (expected {expected_state})')
                assert final_state == expected_state
