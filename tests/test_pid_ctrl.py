from mtppy.active_elements import PIDCtrl
from time import sleep


def init_pid_ctrl(op_mode='off', src_mode='int'):
    pid_ctrl = PIDCtrl('tag', tag_description='',
                       pv_scl_min=0, pv_scl_max=100, pv_unit=0,
                       sp_scl_min=0, sp_scl_max=100, sp_unit=0,
                       sp_int_min=-10, sp_int_max=1000, sp_man_min=-10, sp_man_max=1000,
                       mv_min=-10, mv_max=1000, mv_unit=0, mv_scl_min=0, mv_scl_max=100,
                       P=1, Ti=10, Td=1)

    if op_mode == 'op':
        pid_ctrl.op_src_mode.attributes['StateOpOp'].set_value(True)
    elif op_mode == 'aut':
        pid_ctrl.op_src_mode.attributes['StateAutOp'].set_value(True)
    elif op_mode == 'off':
        pass
    else:
        raise ValueError(f'Operation mode {op_mode} is unknown')

    if src_mode == 'man':
        pid_ctrl.op_src_mode.attributes['SrcManOp'].set_value(True)
    elif src_mode == 'int':
        pid_ctrl.op_src_mode.attributes['SrcIntOp'].set_value(True)
    else:
        raise ValueError(f'Source mode {src_mode} is unknown')
    return pid_ctrl


test_scenario_sp = [('off', 'int', 'set_sp_man', False),
                    ('off', 'man', 'set_sp_man', False),
                    ('op', 'int', 'set_sp_man', False),
                    ('op', 'man', 'set_sp_man', False),
                    ('aut', 'int', 'set_sp_man', False),
                    ('aut', 'man', 'set_sp_man', True),

                    ('off', 'int', 'set_sp_int', False),
                    ('off', 'man', 'set_sp_int', False),
                    ('op', 'int', 'set_sp_int', False),
                    ('op', 'man', 'set_sp_int', False),
                    ('aut', 'int', 'set_sp_int', True),
                    ('aut', 'man', 'set_sp_int', False)]


def test_set_sp():
    for op_mode, src_mode, set_command, changes_expected in test_scenario_sp:
        for command in [-500, -10, 500, 1000, 10000]:
            pid_ctrl = init_pid_ctrl(op_mode=op_mode, src_mode=src_mode)
            eval(f'pid_ctrl.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, changes expected: {changes_expected}')
            if changes_expected:
                if -10 <= command <= 1000:
                    assert pid_ctrl.get_sp() == command
                else:
                    assert pid_ctrl.get_sp() == -10
            else:
                assert pid_ctrl.get_sp() == -10
            pid_ctrl.op_src_mode._opmode_to_off()


test_scenario_mv = [('off', 'int', 'set_mv_man', False),
                    ('off', 'man', 'set_mv_man', False),
                    ('op', 'int', 'set_mv_man', True),
                    ('op', 'man', 'set_mv_man', True)]


def test_set_mv_man():
    for op_mode, src_mode, set_command, changes_expected in test_scenario_mv:
        for command in [-500, -10, 500, 1000, 10000]:
            pid_ctrl = init_pid_ctrl(op_mode=op_mode, src_mode=src_mode)
            eval(f'pid_ctrl.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, changes expected: {changes_expected}')
            if changes_expected:
                if -10 <= command <= 1000:
                    assert pid_ctrl.get_mv() == command
                else:
                    assert pid_ctrl.get_mv() == -10
            else:
                assert pid_ctrl.get_mv() == -10
            pid_ctrl.op_src_mode._opmode_to_off()


def test_pid_aut_man():
    for command in [-10, 1000]:
        pid_ctrl = init_pid_ctrl(op_mode='aut', src_mode='man')
        pid_ctrl.set_sp_man(command)
        print(f'Scenario: sp {command}')
        sleep(2)
        if -10 <= command <= 1000:
            assert pid_ctrl.get_mv() == command
        else:
            assert pid_ctrl.get_mv() == -10
        pid_ctrl.op_src_mode._opmode_to_off()


def test_pid_aut_int():
    for command in [-10, 1000]:
        pid_ctrl = init_pid_ctrl(op_mode='aut', src_mode='int')
        pid_ctrl.set_sp_int(command)
        print(f'Scenario: sp {command}')
        sleep(1)
        if -10 <= command <= 1000:
            assert pid_ctrl.get_mv() == command
        else:
            assert pid_ctrl.get_mv() == -10
        pid_ctrl.op_src_mode._opmode_to_off()
