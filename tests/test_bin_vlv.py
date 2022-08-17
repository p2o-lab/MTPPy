import pytest
from mtppy.active_elements import BinVlv


def init_bin_vlv(op_mode='off', src_mode='int', open_fbk_calc=True, close_fbk_calc=True, safe_pos=0, safe_pos_en=True,
                 perm_en=False, intl_en=False, prot_en=False):
    bin_vlv = BinVlv('tag', tag_description='', open_fbk_calc=open_fbk_calc, close_fbk_calc=close_fbk_calc,
                     safe_pos=safe_pos, safe_pos_en=safe_pos_en, perm_en=perm_en, intl_en=intl_en, prot_en=prot_en)

    if op_mode == 'op':
        bin_vlv.op_src_mode.attributes['StateOpOp'].set_value(True)
    elif op_mode == 'aut':
        bin_vlv.op_src_mode.attributes['StateAutOp'].set_value(True)
    elif op_mode == 'off':
        pass
    else:
        raise ValueError(f'Operation mode {op_mode} is unknown')

    if src_mode == 'man':
        bin_vlv.op_src_mode.attributes['SrcManOp'].set_value(True)
    elif src_mode == 'int':
        bin_vlv.op_src_mode.attributes['SrcIntOp'].set_value(True)
    else:
        raise ValueError(f'Source mode {src_mode} is unknown')
    return bin_vlv


test_scenario = [('off', 'int', 'set_open_op', False, False),
                 ('off', 'man', 'set_open_op', False, False),
                 ('op', 'int', 'set_open_op', True, True),
                 ('op', 'man', 'set_open_op', True, True),
                 ('aut', 'int', 'set_open_op', False, False),
                 ('aut', 'man', 'set_open_op', False, False),

                 ('off', 'int', 'set_open_aut', False, False),
                 ('off', 'man', 'set_open_aut', False, False),
                 ('op', 'int', 'set_open_aut', False, False),
                 ('op', 'man', 'set_open_aut', False, False),
                 ('aut', 'int', 'set_open_aut', True, True),
                 ('aut', 'man', 'set_open_aut', True, True),

                 ('off', 'int', 'set_close_op', False, False),
                 ('off', 'man', 'set_close_op', False, False),
                 ('op', 'int', 'set_close_op', False, True),
                 ('op', 'man', 'set_close_op', False, True),
                 ('aut', 'int', 'set_close_op', False, False),
                 ('aut', 'man', 'set_close_op', False, False),

                 ('off', 'int', 'set_close_aut', False, False),
                 ('off', 'man', 'set_close_aut', False, False),
                 ('op', 'int', 'set_close_aut', False, False),
                 ('op', 'man', 'set_close_aut', False, False),
                 ('aut', 'int', 'set_close_aut', False, True),
                 ('aut', 'man', 'set_close_aut', False, True)]


def test_open_close():
    for op_mode, src_mode, set_command, expected_ctrl, expected_fbk in test_scenario:
        for command in [True, False]:
            bin_vlv = init_bin_vlv(op_mode=op_mode, src_mode=src_mode)
            eval(f'bin_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {expected_ctrl}')
            if set_command in ['set_open_op', 'set_open_aut']:
                if command:
                    assert bin_vlv.attributes['Ctrl'].value == expected_ctrl
                    assert bin_vlv.get_open_fbk() == expected_fbk
                    assert bin_vlv.get_close_fbk() == False
                else:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == False
            elif set_command in ['set_close_op', 'set_close_aut']:
                if command:
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.attributes['Ctrl'].value == expected_ctrl
                    assert bin_vlv.get_close_fbk() == expected_fbk
                else:
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_close_fbk() == False


def test_open_close_permit_en_true():
    for op_mode, src_mode, set_command, _, _ in test_scenario:
        for command in [True, False]:
            bin_vlv = init_bin_vlv(op_mode=op_mode, src_mode=src_mode, perm_en=True)
            bin_vlv.set_permit(False)
            eval(f'bin_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: False')
            assert bin_vlv.attributes['SafePosAct'].value == False
            assert bin_vlv.attributes['Permit'].value == False
            assert bin_vlv.attributes['Ctrl'].value == False
            assert bin_vlv.get_open_fbk() == False
            assert bin_vlv.get_close_fbk() == False

    for op_mode, src_mode, set_command, expected_ctrl, expected_fbk in test_scenario:
        for command in [True, False]:
            bin_vlv = init_bin_vlv(op_mode=op_mode, src_mode=src_mode, perm_en=True)
            bin_vlv.set_permit(True)
            eval(f'bin_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected_ctrl: {expected_ctrl}, '
                  f'expected_fbk: {expected_fbk}')

            assert bin_vlv.attributes['Permit'].value == True
            assert bin_vlv.attributes['SafePosAct'].value == False
            if set_command in ['set_open_op', 'set_open_aut']:
                if command:
                    assert bin_vlv.attributes['Ctrl'].value == expected_ctrl
                    assert bin_vlv.get_open_fbk() == expected_fbk
                    assert bin_vlv.get_close_fbk() == False
                else:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == False
            elif set_command in ['set_close_op', 'set_close_aut']:
                if command:
                    assert bin_vlv.attributes['Ctrl'].value == expected_ctrl
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == expected_fbk
                else:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == False


def test_open_close_permit_en_false():
    for op_mode, src_mode, set_command, expected_ctrl, expected_fbk in test_scenario:
        for command in [True, False]:
            bin_vlv = init_bin_vlv(op_mode=op_mode, src_mode=src_mode, perm_en=False)
            bin_vlv.set_permit(True)
            eval(f'bin_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected_ctrl: {expected_ctrl}, '
                  f'expected_fbk: {expected_fbk}')

            assert bin_vlv.attributes['Permit'].value == True
            assert bin_vlv.attributes['SafePosAct'].value == False
            if set_command in ['set_open_op', 'set_open_aut']:
                if command:
                    assert bin_vlv.attributes['Ctrl'].value == expected_ctrl
                    assert bin_vlv.get_open_fbk() == expected_fbk
                    assert bin_vlv.get_close_fbk() == False
                else:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == False
            elif set_command in ['set_close_op', 'set_close_aut']:
                if command:
                    assert bin_vlv.attributes['Ctrl'].value == expected_ctrl
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == expected_fbk
                else:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == False


def test_open_close_interlock_en_true():
    for op_mode, src_mode, set_command, _, _ in test_scenario:
        for command in [True, False]:
            bin_vlv = init_bin_vlv(op_mode=op_mode, src_mode=src_mode, intl_en=True)
            bin_vlv.set_interlock(False)
            eval(f'bin_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: False')

            assert bin_vlv.attributes['Interlock'].value == False
            assert bin_vlv.attributes['SafePosAct'].value == True
            assert bin_vlv.attributes['Ctrl'].value == False
            assert bin_vlv.get_open_fbk() == False
            assert bin_vlv.get_close_fbk() == True

    for op_mode, src_mode, set_command, expected_ctrl, expected_fbk in test_scenario:
        for command in [True, False]:
            bin_vlv = init_bin_vlv(op_mode=op_mode, src_mode=src_mode, intl_en=True)
            bin_vlv.set_interlock(True)
            eval(f'bin_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected_ctrl: {expected_ctrl}, '
                  f'expected_fbk: {expected_fbk}')

            assert bin_vlv.attributes['Interlock'].value == True
            assert bin_vlv.attributes['SafePosAct'].value == False
            if set_command in ['set_open_op', 'set_open_aut']:
                if command:
                    assert bin_vlv.attributes['Ctrl'].value == expected_ctrl
                    assert bin_vlv.get_open_fbk() == expected_fbk
                    assert bin_vlv.get_close_fbk() == False
                else:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == False
            elif set_command in ['set_close_op', 'set_close_aut']:
                if command:
                    assert bin_vlv.attributes['Ctrl'].value == expected_ctrl
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == expected_fbk
                else:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == False


def test_open_close_interlock_en_false():
    for op_mode, src_mode, set_command, expected_ctrl, expected_fbk in test_scenario:
        for command in [True, False]:
            bin_vlv = init_bin_vlv(op_mode=op_mode, src_mode=src_mode, intl_en=False)
            bin_vlv.set_interlock(True)
            eval(f'bin_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected_ctrl: {expected_ctrl}, '
                  f'expected_fbk: {expected_fbk}')

            assert bin_vlv.attributes['Interlock'].value == True
            assert bin_vlv.attributes['SafePosAct'].value == False
            if set_command in ['set_open_op', 'set_open_aut']:
                if command:
                    assert bin_vlv.attributes['Ctrl'].value == expected_ctrl
                    assert bin_vlv.get_open_fbk() == expected_fbk
                    assert bin_vlv.get_close_fbk() == False
                else:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == False
            elif set_command in ['set_close_op', 'set_close_aut']:
                if command:
                    assert bin_vlv.attributes['Ctrl'].value == expected_ctrl
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == expected_fbk
                else:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == False


def test_open_close_protect_en_true():
    for op_mode, src_mode, set_command, _, _ in test_scenario:
        for command in [True, False]:
            bin_vlv = init_bin_vlv(op_mode=op_mode, src_mode=src_mode, prot_en=True)
            bin_vlv.set_protect(False)
            eval(f'bin_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: False')

            assert bin_vlv.attributes['Protect'].value == False
            assert bin_vlv.attributes['SafePosAct'].value == True
            assert bin_vlv.attributes['Ctrl'].value == False
            assert bin_vlv.get_open_fbk() == False
            assert bin_vlv.get_close_fbk() == True

    for op_mode, src_mode, set_command, expected_ctrl, expected_fbk in test_scenario:
        for command in [True, False]:
            bin_vlv = init_bin_vlv(op_mode=op_mode, src_mode=src_mode, prot_en=True)
            bin_vlv.set_protect(True)
            eval(f'bin_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected_ctrl: {expected_ctrl}, '
                  f'expected_fbk: {expected_fbk}')

            assert bin_vlv.attributes['Protect'].value == True
            assert bin_vlv.attributes['SafePosAct'].value == False
            if set_command in ['set_open_op', 'set_open_aut']:
                if command:
                    assert bin_vlv.attributes['Ctrl'].value == expected_ctrl
                    assert bin_vlv.get_open_fbk() == expected_fbk
                    assert bin_vlv.get_close_fbk() == False
                else:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == False
            elif set_command in ['set_close_op', 'set_close_aut']:
                if command:
                    assert bin_vlv.attributes['Ctrl'].value == expected_ctrl
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == expected_fbk
                else:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == False


def test_open_close_protect_en_false():
    for op_mode, src_mode, set_command, expected_ctrl, expected_fbk in test_scenario:
        for command in [True, False]:
            bin_vlv = init_bin_vlv(op_mode=op_mode, src_mode=src_mode, prot_en=False)
            bin_vlv.set_protect(True)
            eval(f'bin_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected_ctrl: {expected_ctrl}, '
                  f'expected_fbk: {expected_fbk}')

            assert bin_vlv.attributes['Protect'].value == True
            assert bin_vlv.attributes['SafePosAct'].value == False
            if set_command in ['set_open_op', 'set_open_aut']:
                if command:
                    assert bin_vlv.attributes['Ctrl'].value == expected_ctrl
                    assert bin_vlv.get_open_fbk() == expected_fbk
                    assert bin_vlv.get_close_fbk() == False
                else:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == False
            elif set_command in ['set_close_op', 'set_close_aut']:
                if command:
                    assert bin_vlv.attributes['Ctrl'].value == expected_ctrl
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == expected_fbk
                else:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == False


test_scenario_reset = [('off', 'int', 'set_reset_op', False),
                       ('off', 'man', 'set_reset_op', False),
                       ('op', 'int', 'set_reset_op', True),
                       ('op', 'man', 'set_reset_op', True),
                       ('aut', 'int', 'set_reset_op', False),
                       ('aut', 'man', 'set_reset_op', False),

                       ('off', 'int', 'set_reset_aut', False),
                       ('off', 'man', 'set_reset_aut', False),
                       ('op', 'int', 'set_reset_aut', False),
                       ('op', 'man', 'set_reset_aut', False),
                       ('aut', 'int', 'set_reset_aut', True),
                       ('aut', 'man', 'set_reset_aut', True)]


def test_reset():
    for op_mode, src_mode, set_command, result in test_scenario_reset:
        for command in [True, False]:
            bin_vlv = init_bin_vlv(op_mode=op_mode, src_mode=src_mode, prot_en=True)

            bin_vlv.set_protect(False)
            assert bin_vlv.attributes['Protect'].value == False
            assert bin_vlv.attributes['SafePosAct'].value == True
            assert bin_vlv.get_open_fbk() == False
            assert bin_vlv.get_close_fbk() == True

            eval(f'bin_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {result}')

            if command:
                assert bin_vlv.attributes['Protect'].value == result
                assert bin_vlv.attributes['SafePosAct'].value != result
                assert bin_vlv.get_close_fbk() != result

            else:
                assert bin_vlv.attributes['Protect'].value == False
                assert bin_vlv.attributes['SafePosAct'].value == True
                assert bin_vlv.get_close_fbk() == True


test_scenario_safe_pos_en = [('op', 'int', 'set_open_op', 1, True),
                             ('op', 'man', 'set_open_op', 1, True),

                             ('aut', 'int', 'set_open_aut', 1, False),
                             ('aut', 'man', 'set_open_aut', 1, False),

                             ('op', 'int', 'set_close_op', 0, True),
                             ('op', 'man', 'set_close_op', 0, True),

                             ('aut', 'int', 'set_close_aut', 0, False),
                             ('aut', 'man', 'set_close_aut', 0, False)]


def test_safe_pos_en_interlock():
    for op_mode, src_mode, set_command, safe_pos, safe_pos_en in test_scenario_safe_pos_en:
        bin_vlv = init_bin_vlv(op_mode=op_mode, src_mode=src_mode, safe_pos=safe_pos,
                               safe_pos_en=safe_pos_en, intl_en=True)
        bin_vlv.set_interlock(True)  # interlock is inactive
        eval(f'bin_vlv.{set_command}(True)')
        bin_vlv.set_interlock(False)  # active interlock after setting a position
        print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, True, safe_pos: {safe_pos}, '
              f'safe_pos_en: {safe_pos_en}')

        # if safe_pos_en is true, state should be to set to safety position (open or close) after interlock is
        # activated
        if set_command in ['set_open_op', 'set_open_aut']:
            if safe_pos_en:
                if safe_pos == 1:
                    assert bin_vlv.attributes['Ctrl'].value == True
                    assert bin_vlv.get_open_fbk() == True
                    assert bin_vlv.get_close_fbk() == False
                elif safe_pos == 0:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == False

            # if safe_pos_en is false, current valve state is the last active state
            else:
                assert bin_vlv.attributes['Ctrl'].value == True
                assert bin_vlv.get_open_fbk() == True
                assert bin_vlv.get_close_fbk() == False

        if set_command in ['set_close_op', 'set_close_aut']:
            if safe_pos_en:
                if safe_pos == 1:
                    assert bin_vlv.attributes['Ctrl'].value == True
                    assert bin_vlv.get_open_fbk() == True
                    assert bin_vlv.get_close_fbk() == False
                elif safe_pos == 0:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == True

            # if safe_pos_en is false, current valve state is the last active state
            else:
                assert bin_vlv.attributes['Ctrl'].value == False
                assert bin_vlv.get_open_fbk() == False
                assert bin_vlv.get_close_fbk() == True


def test_safe_pos_en_protect():
    for op_mode, src_mode, set_command, safe_pos, safe_pos_en in test_scenario_safe_pos_en:
        bin_vlv = init_bin_vlv(op_mode=op_mode, src_mode=src_mode, safe_pos=safe_pos,
                               safe_pos_en=safe_pos_en, prot_en=True)
        bin_vlv.set_protect(True)  # protect is inactive
        eval(f'bin_vlv.{set_command}(True)')
        bin_vlv.set_protect(False)  # active protect after setting a position
        print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, True, safe_pos: {safe_pos}, '
              f'safe_pos_en: {safe_pos_en}')

        # if safe_pos_en is true, state should be to set to safety position (open or close) after protection is
        # activated
        if set_command in ['set_open_op', 'set_open_aut']:
            if safe_pos_en:
                if safe_pos == 1:
                    assert bin_vlv.attributes['Ctrl'].value == True
                    assert bin_vlv.get_open_fbk() == True
                    assert bin_vlv.get_close_fbk() == False
                elif safe_pos == 0:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == False

            # if safe_pos_en is false, current valve state is the last active state
            else:
                assert bin_vlv.attributes['Ctrl'].value == True
                assert bin_vlv.get_open_fbk() == True
                assert bin_vlv.get_close_fbk() == False

        if set_command in ['set_close_op', 'set_close_aut']:
            if safe_pos_en:
                if safe_pos == 1:
                    assert bin_vlv.attributes['Ctrl'].value == True
                    assert bin_vlv.get_open_fbk() == True
                    assert bin_vlv.get_close_fbk() == False
                elif safe_pos == 0:
                    assert bin_vlv.attributes['Ctrl'].value == False
                    assert bin_vlv.get_open_fbk() == False
                    assert bin_vlv.get_close_fbk() == True

            # if safe_pos_en is false, current valve state is the last active state
            else:
                assert bin_vlv.attributes['Ctrl'].value == False
                assert bin_vlv.get_open_fbk() == False
                assert bin_vlv.get_close_fbk() == True


def test_safe_pos_en_permit():
    for op_mode, src_mode, set_command, safe_pos, safe_pos_en in test_scenario_safe_pos_en:
        bin_vlv = init_bin_vlv(op_mode=op_mode, src_mode=src_mode, safe_pos=safe_pos,
                               safe_pos_en=safe_pos_en, perm_en=True)
        bin_vlv.set_permit(True)  # permit is inactive
        eval(f'bin_vlv.{set_command}(True)')
        bin_vlv.set_permit(False)  # active permit after setting a position
        print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, True, safe_pos: {safe_pos}, '
              f'safe_pos_en: {safe_pos_en}')

        if set_command in ['set_open_op', 'set_open_aut']:
            assert bin_vlv.attributes['Ctrl'].value == True
            assert bin_vlv.get_open_fbk() == True
            assert bin_vlv.get_close_fbk() == False

        if set_command in ['set_close_op', 'set_close_aut']:
            assert bin_vlv.attributes['Ctrl'].value == False
            assert bin_vlv.get_open_fbk() == False
            assert bin_vlv.get_close_fbk() == True


def test_open_fbk():
    bin_vlv = init_bin_vlv(open_fbk_calc=False, close_fbk_calc=False)
    assert bin_vlv.get_open_fbk() == False
    bin_vlv.set_open_fbk(True)
    assert bin_vlv.get_open_fbk() == True


def test_close_fbk():
    bin_vlv = init_bin_vlv(open_fbk_calc=False, close_fbk_calc=False)
    assert bin_vlv.get_close_fbk() == False
    bin_vlv.set_close_fbk(True)
    assert bin_vlv.get_close_fbk() == True


if __name__ == '__main__':
    pytest.main(['test_bin_vlv.py', '-s'])
