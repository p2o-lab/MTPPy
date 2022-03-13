from src.mtppy.command_en_control import CommandEnControl
import itertools


hold_enabled = True
pause_enabled = True
restart_enabled = True

test_cases = {
    'undefined': {'undefined': False,
                  'reset': False,
                  'start': False,
                  'stop': False,
                  'hold': False,
                  'unhold': False,
                  'pause': False,
                  'resume': False,
                  'abort': False,
                  'restart': False,
                  'complete': False},

    'idle': {'undefined': False,
                  'reset': False,
                  'start': True,
                  'stop': True,
                  'hold': False,
                  'unhold': False,
                  'pause': False,
                  'resume': False,
                  'abort': True,
                  'restart': False,
                  'complete': False},

    'starting': {'undefined': False,
                 'reset': False,
                 'start': False,
                 'stop': True,
                 'hold': hold_enabled,
                 'unhold': False,
                 'pause': False,
                 'resume': False,
                 'abort': True,
                 'restart': False,
                 'complete': True},

    'execute': {'undefined': False,
                'reset': False,
                'start': False,
                'stop': True,
                'hold': hold_enabled,
                'unhold': False,
                'pause': pause_enabled,
                'resume': False,
                'abort': True,
                'restart': restart_enabled,
                'complete': True},

    'completing': {'undefined': False,
                   'reset': False,
                   'start': False,
                   'stop': True,
                   'hold': hold_enabled,
                   'unhold': False,
                   'pause': False,
                   'resume': False,
                   'abort': True,
                   'restart': False,
                   'complete': False},

    'completed': {'undefined': False,
                  'reset': True,
                  'start': False,
                  'stop': True,
                  'hold': False,
                  'unhold': False,
                  'pause': False,
                  'resume': False,
                  'abort': True,
                  'restart': False,
                  'complete': False},

    'resuming': {'undefined': False,
                 'reset': False,
                 'start': False,
                 'stop': True,
                 'hold': hold_enabled,
                 'unhold': False,
                 'pause': False,
                 'resume': False,
                 'abort': True,
                 'restart': False,
                 'complete': True},

    'paused': {'undefined': False,
               'reset': False,
               'start': False,
               'stop': True,
               'hold': hold_enabled,
               'unhold': False,
               'pause': False,
               'resume': True,
               'abort': True,
               'restart': False,
               'complete': True},

    'pausing': {'undefined': False,
                'reset': False,
                'start': False,
                'stop': True,
                'hold': hold_enabled,
                'unhold': False,
                'pause': False,
                'resume': False,
                'abort': True,
                'restart': False,
                'complete': True},

    'holding': {'undefined': False,
                'reset': False,
                'start': False,
                'stop': True,
                'hold': False,
                'unhold': False,
                'pause': False,
                'resume': False,
                'abort': True,
                'restart': False,
                'complete': False},

    'held': {'undefined': False,
             'reset': False,
             'start': False,
             'stop': True,
             'hold': False,
             'unhold': True,
             'pause': False,
             'resume': False,
             'abort': True,
             'restart': False,
             'complete': False},

    'unholding': {'undefined': False,
                  'reset': False,
                  'start': False,
                  'stop': True,
                  'hold': hold_enabled,
                  'unhold': False,
                  'pause': False,
                  'resume': False,
                  'abort': True,
                  'restart': False,
                  'complete': True},

    'stopping': {'undefined': False,
                 'reset': False,
                 'start': False,
                 'stop': False,
                 'hold': False,
                 'unhold': False,
                 'pause': False,
                 'resume': False,
                 'abort': True,
                 'restart': False,
                 'complete': False},

    'stopped': {'undefined': False,
                'reset': True,
                'start': False,
                'stop': False,
                'hold': False,
                'unhold': False,
                'pause': False,
                'resume': False,
                'abort': True,
                'restart': False,
                'complete': False},

    'aborting': {'undefined': False,
                 'reset': False,
                 'start': False,
                 'stop': False,
                 'hold': False,
                 'unhold': False,
                 'pause': False,
                 'resume': False,
                 'abort': False,
                 'restart': False,
                 'complete': False},

    'aborted': {'undefined': False,
                'reset': True,
                'start': False,
                'stop': False,
                'hold': False,
                'unhold': False,
                'pause': False,
                'resume': False,
                'abort': False,
                'restart': False,
                'complete': False},

    'resetting': {'undefined': False,
                  'reset': False,
                  'start': False,
                  'stop': True,
                  'hold': False,
                  'unhold': False,
                  'pause': False,
                  'resume': False,
                  'abort': True,
                  'restart': False,
                  'complete': False},
}


def init_state(state='idle', hold_en=True, pause_en=True, restart_en=True):
    command_en_ctrl = CommandEnControl()
    command_en_ctrl.execute(state)
    command_en_ctrl.enable_hold_loop(hold_en)
    command_en_ctrl.enable_pause_loop(pause_en)
    command_en_ctrl.enable_restart(restart_en)
    return command_en_ctrl


def test_states():
    for state in test_cases:
        for loop_en_flags in itertools.product([False, True], repeat=3):
            hold_en = loop_en_flags[0]
            pause_en = loop_en_flags[0]
            restart_en = loop_en_flags[0]
            command_en_ctrl = init_state(state=state, hold_en=hold_en, pause_en=pause_en, restart_en=restart_en)
            command_en_ctrl.execute(state)
            for command, command_en in test_cases[state].items():
                response = command_en_ctrl.command_en[command]['value']
                print(f'State: {state}, command: {command}, hold_en: {hold_en}, pause_en: {pause_en}, restart_en: {restart_en}, expected: {command_en}, received: {response}')
                assert response == command_en


def test_set_default():
    command_en_ctrl = init_state()
    command_en_ctrl.set_default()
    for command_en in command_en_ctrl.command_en:
        assert command_en_ctrl.command_en[command_en]['value'] == command_en_ctrl.command_en[command_en]['default']


def test_disable_all():
    command_en_ctrl = init_state()
    command_en_ctrl.disable_all()
    for command_en in command_en_ctrl.command_en:
        assert command_en_ctrl.command_en[command_en]['value'] == False


def test_get_command():
    command_en_ctrl = init_state()
    for command_en in command_en_ctrl.command_en:
        assert command_en_ctrl.get_command(command_en) == command_en_ctrl.command_en[command_en]['value']

    assert command_en_ctrl.get_command('not_exist') == None


def test_set_command():
    command_en_ctrl = init_state()
    for command_en in command_en_ctrl.command_en:
        command_en_ctrl._set_command(command_en, True)
        command_en_ctrl._set_command('not_exist', False)
        assert command_en_ctrl.command_en[command_en]['value'] == True

        command_en_ctrl._set_command(command_en, False)
        command_en_ctrl._set_command('not_exist', True)
        assert command_en_ctrl.command_en[command_en]['value'] == False
