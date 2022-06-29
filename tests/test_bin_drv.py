import pytest
from mtppy.active_elements import BinDrv


def init_bin_drv(op_mode='off', src_mode='int', rev_fbk_calc=True, fwd_fbk_calc=True,
                 safe_pos=0, fwd_en=True, rev_en=False, perm_en=False, intl_en=False, prot_en=False):
    bin_drv = BinDrv('tag', tag_description='', rev_fbk_calc=rev_fbk_calc, fwd_fbk_calc=fwd_fbk_calc, safe_pos=safe_pos,
                     fwd_en=fwd_en, rev_en=rev_en, perm_en=perm_en, intl_en=intl_en, prot_en=prot_en)

    if op_mode == 'op':
        bin_drv.op_src_mode.attributes['StateOpOp'].set_value(True)
    elif op_mode == 'aut':
        bin_drv.op_src_mode.attributes['StateAutOp'].set_value(True)
    elif op_mode == 'off':
        pass
    else:
        raise ValueError(f'Operation mode {op_mode} is unknown')

    if src_mode == 'man':
        bin_drv.op_src_mode.attributes['SrcManOp'].set_value(True)
    elif src_mode == 'int':
        bin_drv.op_src_mode.attributes['SrcIntOp'].set_value(True)
    else:
        raise ValueError(f'Source mode {src_mode} is unknown')
    return bin_drv


test_scenario = [('off', 'int', 'set_fwd_op', False),
                 ('off', 'man', 'set_fwd_op', False),
                 ('op', 'int', 'set_fwd_op', True),
                 ('op', 'man', 'set_fwd_op', True),
                 ('aut', 'int', 'set_fwd_op', False),
                 ('aut', 'man', 'set_fwd_op', False),

                 ('off', 'int', 'set_fwd_aut', False),
                 ('off', 'man', 'set_fwd_aut', False),
                 ('op', 'int', 'set_fwd_aut', False),
                 ('op', 'man', 'set_fwd_aut', False),
                 ('aut', 'int', 'set_fwd_aut', True),
                 ('aut', 'man', 'set_fwd_aut', True),

                 ('off', 'int', 'set_rev_op', False),
                 ('off', 'man', 'set_rev_op', False),
                 ('op', 'int', 'set_rev_op', True),
                 ('op', 'man', 'set_rev_op', True),
                 ('aut', 'int', 'set_rev_op', False),
                 ('aut', 'man', 'set_rev_op', False),

                 ('off', 'int', 'set_rev_aut', False),
                 ('off', 'man', 'set_rev_aut', False),
                 ('op', 'int', 'set_rev_aut', False),
                 ('op', 'man', 'set_rev_aut', False),
                 ('aut', 'int', 'set_rev_aut', True),
                 ('aut', 'man', 'set_rev_aut', True)]


def test_fwd_rev():
    for op_mode, src_mode, set_command, expected_result in test_scenario:
        for command in [True, False]:
            bin_drv = init_bin_drv(op_mode=op_mode, src_mode=src_mode, fwd_en=True, rev_en=True)
            eval(f'bin_drv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {expected_result}')
            if set_command in ['set_fwd_op', 'set_fwd_aut']:
                if command:
                    assert bin_drv.attributes['FwdCtrl'].value == expected_result
                    assert bin_drv.get_fwd_fbk() == expected_result
                    assert bin_drv.attributes['RevCtrl'].value == False
                    assert bin_drv.get_rev_fbk() == False
                else:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.get_fwd_fbk() == False
                    assert bin_drv.attributes['RevCtrl'].value == False
                    assert bin_drv.get_rev_fbk() == False
            elif set_command in ['set_rev_op', 'set_rev_aut']:
                if command:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.get_fwd_fbk() == False
                    assert bin_drv.attributes['RevCtrl'].value == expected_result
                    assert bin_drv.get_rev_fbk() == expected_result
                else:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.get_fwd_fbk() == False
                    assert bin_drv.attributes['RevCtrl'].value == False
                    assert bin_drv.get_rev_fbk() == False


def test_fwd_rev_en():
    for op_mode, src_mode, set_command, _ in test_scenario:
        for command in [True, False]:
            bin_drv = init_bin_drv(op_mode=op_mode, src_mode=src_mode, fwd_en=False, rev_en=False)
            eval(f'bin_drv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: False')
            assert bin_drv.attributes['FwdCtrl'].value == False
            assert bin_drv.attributes['RevCtrl'].value == False


def test_fwd_rev_trip():
    for op_mode, src_mode, set_command, _ in test_scenario:
        for command in [True, False]:
            bin_drv = init_bin_drv(op_mode=op_mode, src_mode=src_mode, fwd_en=True, rev_en=True)
            bin_drv.set_trip(False)
            eval(f'bin_drv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: False')
            assert bin_drv.attributes['SafePosAct'].value == True
            assert bin_drv.attributes['Trip'].value == False
            assert bin_drv.attributes['FwdCtrl'].value == False
            assert bin_drv.attributes['RevCtrl'].value == False


def test_fwd_rev_permit_en_true():
    for op_mode, src_mode, set_command, _ in test_scenario:
        for command in [True, False]:
            bin_drv = init_bin_drv(op_mode=op_mode, src_mode=src_mode, fwd_en=True, rev_en=True, perm_en=True)
            bin_drv.set_permit(False)
            eval(f'bin_drv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: False')
            assert bin_drv.attributes['SafePosAct'].value == False
            assert bin_drv.attributes['Permit'].value == False
            assert bin_drv.attributes['FwdCtrl'].value == False
            assert bin_drv.attributes['RevCtrl'].value == False
            assert bin_drv.get_fwd_fbk() == False
            assert bin_drv.get_rev_fbk() == False

    for op_mode, src_mode, set_command, expected_result in test_scenario:
        for command in [True, False]:
            bin_drv = init_bin_drv(op_mode=op_mode, src_mode=src_mode, fwd_en=True, rev_en=True, perm_en=True)
            bin_drv.set_permit(True)
            eval(f'bin_drv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {expected_result}')

            assert bin_drv.attributes['Permit'].value == True
            assert bin_drv.attributes['SafePosAct'].value == False
            if set_command in ['set_fwd_op', 'set_fwd_aut']:
                if command:
                    assert bin_drv.attributes['FwdCtrl'].value == expected_result
                    assert bin_drv.get_fwd_fbk() == expected_result
                    assert bin_drv.attributes['RevCtrl'].value == False
                    assert bin_drv.get_rev_fbk() == False
                else:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.get_fwd_fbk() == False
                    assert bin_drv.attributes['RevCtrl'].value == False
                    assert bin_drv.get_rev_fbk() == False
            elif set_command in ['set_rev_op', 'set_rev_aut']:
                if command:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.get_fwd_fbk() == False
                    assert bin_drv.attributes['RevCtrl'].value == expected_result
                    assert bin_drv.get_rev_fbk() == expected_result
                else:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.get_fwd_fbk() == False
                    assert bin_drv.attributes['RevCtrl'].value == False
                    assert bin_drv.get_rev_fbk() == False


def test_fwd_rev_permit_en_false():
    for op_mode, src_mode, set_command, expected_result in test_scenario:
        for command in [True, False]:
            ana_drv = init_bin_drv(op_mode=op_mode, src_mode=src_mode, fwd_en=True, rev_en=True, perm_en=False)
            ana_drv.set_permit(True)
            eval(f'ana_drv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {expected_result}')

            assert ana_drv.attributes['Permit'].value == True
            assert ana_drv.attributes['SafePosAct'].value == False
            if set_command in ['set_fwd_op', 'set_fwd_aut']:
                if command:
                    assert ana_drv.attributes['FwdCtrl'].value == expected_result
                    assert ana_drv.attributes['RevCtrl'].value == False
                else:
                    assert ana_drv.attributes['FwdCtrl'].value == False
                    assert ana_drv.attributes['RevCtrl'].value == False
            elif set_command in ['set_rev_op', 'set_rev_aut']:
                if command:
                    assert ana_drv.attributes['FwdCtrl'].value == False
                    assert ana_drv.attributes['RevCtrl'].value == expected_result
                else:
                    assert ana_drv.attributes['FwdCtrl'].value == False
                    assert ana_drv.attributes['RevCtrl'].value == False


def test_fwd_rev_interlock_en_true():
    for op_mode, src_mode, set_command, _ in test_scenario:
        for command in [True, False]:
            bin_drv = init_bin_drv(op_mode=op_mode, src_mode=src_mode, fwd_en=True, rev_en=True, intl_en=True)
            bin_drv.set_interlock(False)
            eval(f'bin_drv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: False')

            assert bin_drv.attributes['Interlock'].value == False
            assert bin_drv.attributes['SafePosAct'].value == True
            assert bin_drv.attributes['FwdCtrl'].value == False
            assert bin_drv.attributes['RevCtrl'].value == False

    for op_mode, src_mode, set_command, expected_result in test_scenario:
        for command in [True, False]:
            bin_drv = init_bin_drv(op_mode=op_mode, src_mode=src_mode, fwd_en=True, rev_en=True, intl_en=True)
            bin_drv.set_interlock(True)
            eval(f'bin_drv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {expected_result}')

            assert bin_drv.attributes['Interlock'].value == True
            assert bin_drv.attributes['SafePosAct'].value == False
            if set_command in ['set_fwd_op', 'set_fwd_aut']:
                if command:
                    assert bin_drv.attributes['FwdCtrl'].value == expected_result
                    assert bin_drv.attributes['RevCtrl'].value == False
                else:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.attributes['RevCtrl'].value == False
            elif set_command in ['set_rev_op', 'set_rev_aut']:
                if command:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.attributes['RevCtrl'].value == expected_result
                else:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.attributes['RevCtrl'].value == False


def test_fwd_rev_interlock_en_false():
    for op_mode, src_mode, set_command, expected_result in test_scenario:
        for command in [True, False]:
            bin_drv = init_bin_drv(op_mode=op_mode, src_mode=src_mode, fwd_en=True, rev_en=True, intl_en=False)
            bin_drv.set_interlock(True)
            eval(f'bin_drv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {expected_result}')

            assert bin_drv.attributes['Interlock'].value == True
            assert bin_drv.attributes['SafePosAct'].value == False
            if set_command in ['set_fwd_op', 'set_fwd_aut']:
                if command:
                    assert bin_drv.attributes['FwdCtrl'].value == expected_result
                    assert bin_drv.attributes['RevCtrl'].value == False
                else:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.attributes['RevCtrl'].value == False
            elif set_command in ['set_rev_op', 'set_rev_aut']:
                if command:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.attributes['RevCtrl'].value == expected_result
                else:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.attributes['RevCtrl'].value == False


def test_fwd_rev_protect_en_true():
    for op_mode, src_mode, set_command, _ in test_scenario:
        for command in [True, False]:
            bin_drv = init_bin_drv(op_mode=op_mode, src_mode=src_mode, fwd_en=True, rev_en=True, prot_en=True)
            bin_drv.set_protect(False)
            eval(f'bin_drv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: False')

            assert bin_drv.attributes['Protect'].value == False
            assert bin_drv.attributes['SafePosAct'].value == True
            assert bin_drv.attributes['FwdCtrl'].value == False
            assert bin_drv.attributes['RevCtrl'].value == False

    for op_mode, src_mode, set_command, expected_result in test_scenario:
        for command in [True, False]:
            bin_drv = init_bin_drv(op_mode=op_mode, src_mode=src_mode, fwd_en=True, rev_en=True, prot_en=True)
            bin_drv.set_protect(True)
            eval(f'bin_drv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {expected_result}')

            assert bin_drv.attributes['Protect'].value == True
            assert bin_drv.attributes['SafePosAct'].value == False
            if set_command in ['set_fwd_op', 'set_fwd_aut']:
                if command:
                    assert bin_drv.attributes['FwdCtrl'].value == expected_result
                    assert bin_drv.attributes['RevCtrl'].value == False
                else:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.attributes['RevCtrl'].value == False
            elif set_command in ['set_rev_op', 'set_rev_aut']:
                if command:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.attributes['RevCtrl'].value == expected_result
                else:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.attributes['RevCtrl'].value == False


def test_fwd_rev_protect_en_false():
    for op_mode, src_mode, set_command, expected_result in test_scenario:
        for command in [True, False]:
            bin_drv = init_bin_drv(op_mode=op_mode, src_mode=src_mode, fwd_en=True, rev_en=True, prot_en=False)
            bin_drv.set_protect(True)
            eval(f'bin_drv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {expected_result}')

            assert bin_drv.attributes['Protect'].value == True
            assert bin_drv.attributes['SafePosAct'].value == False
            if set_command in ['set_fwd_op', 'set_fwd_aut']:
                if command:
                    assert bin_drv.attributes['FwdCtrl'].value == expected_result
                    assert bin_drv.attributes['RevCtrl'].value == False
                else:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.attributes['RevCtrl'].value == False
            elif set_command in ['set_rev_op', 'set_rev_aut']:
                if command:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.attributes['RevCtrl'].value == expected_result
                else:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                    assert bin_drv.attributes['RevCtrl'].value == False


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
            bin_drv = init_bin_drv(op_mode=op_mode, src_mode=src_mode, fwd_en=True, rev_en=True, prot_en=True)

            bin_drv.set_protect(False)
            assert bin_drv.attributes['Protect'].value == False
            assert bin_drv.attributes['SafePosAct'].value == True

            eval(f'bin_drv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {result}')

            if command:
                assert bin_drv.attributes['Protect'].value == result
                assert bin_drv.attributes['SafePosAct'].value != result
            else:
                assert bin_drv.attributes['Protect'].value == False
                assert bin_drv.attributes['SafePosAct'].value == True


test_scenario_stop = [('op', 'int', 'set_stop_op', True),
                      ('op', 'man', 'set_stop_op', True),
                      ('aut', 'int', 'set_stop_op', False),
                      ('aut', 'man', 'set_stop_op', False),

                      ('op', 'int', 'set_stop_aut', False),
                      ('op', 'man', 'set_stop_aut', False),
                      ('aut', 'int', 'set_stop_aut', True),
                      ('aut', 'man', 'set_stop_aut', True)]


def test_stop():
    for op_mode, src_mode, set_command, changes_expected in test_scenario_stop:
        for command in [True, False]:
            bin_drv = init_bin_drv(op_mode=op_mode, src_mode=src_mode, fwd_en=True, rev_en=True)
            if op_mode == 'op':  # open valve
                bin_drv.set_fwd_op(True)
            elif op_mode == 'aut':
                bin_drv.set_fwd_aut(True)

            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {changes_expected}')
            if changes_expected:
                assert bin_drv.attributes['FwdCtrl'].value == True
                eval(f'bin_drv.{set_command}({command})')
                if command:
                    assert bin_drv.attributes['FwdCtrl'].value == False
                else:
                    assert bin_drv.attributes['FwdCtrl'].value == True
            else:
                assert bin_drv.attributes['FwdCtrl'].value == True


def test_fwd_fbk():
    bin_drv = init_bin_drv(fwd_fbk_calc=False, rev_fbk_calc=False)
    assert bin_drv.get_fwd_fbk() == False
    bin_drv.set_fwd_fbk(True)
    assert bin_drv.get_fwd_fbk() == True


def test_rev_fbk():
    bin_drv = init_bin_drv(fwd_fbk_calc=False, rev_fbk_calc=False)
    assert bin_drv.get_rev_fbk() == False
    bin_drv.set_rev_fbk(True)
    assert bin_drv.get_rev_fbk() == True


if __name__ == '__main__':
    pytest.main(['test_bin_drv.py', '-s'])
