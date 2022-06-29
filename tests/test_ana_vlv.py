import pytest
from mtppy.active_elements import AnaVlv


def init_ana_vlv(op_mode='off', src_mode='int', open_fbk_calc=True, close_fbk_calc=True, pos_fbk_calc=True,
                 safe_pos=0, safe_pos_en=True, perm_en=False, intl_en=False, prot_en=False):
    ana_vlv = AnaVlv('tag', tag_description='',
                     pos_min=2, pos_max=10, pos_scl_min=0, pos_scl_max=10, pos_unit=0,
                     open_fbk_calc=open_fbk_calc, close_fbk_calc=close_fbk_calc, pos_fbk_calc=pos_fbk_calc,
                     safe_pos=safe_pos, safe_pos_en=safe_pos_en, perm_en=perm_en, intl_en=intl_en, prot_en=prot_en)

    if op_mode == 'op':
        ana_vlv.op_src_mode.attributes['StateOpOp'].set_value(True)
    elif op_mode == 'aut':
        ana_vlv.op_src_mode.attributes['StateAutOp'].set_value(True)
    elif op_mode == 'off':
        pass
    else:
        raise ValueError(f'Operation mode {op_mode} is unknown')

    if src_mode == 'man':
        ana_vlv.op_src_mode.attributes['SrcManOp'].set_value(True)
    elif src_mode == 'int':
        ana_vlv.op_src_mode.attributes['SrcIntOp'].set_value(True)
    else:
        raise ValueError(f'Source mode {src_mode} is unknown')
    return ana_vlv


test_scenario = [('off', 'int', 'set_open_op', False),
                 ('off', 'man', 'set_open_op', False),
                 ('op', 'int', 'set_open_op', True),
                 ('op', 'man', 'set_open_op', True),
                 ('aut', 'int', 'set_open_op', False),
                 ('aut', 'man', 'set_open_op', False),

                 ('off', 'int', 'set_open_aut', False),
                 ('off', 'man', 'set_open_aut', False),
                 ('op', 'int', 'set_open_aut', False),
                 ('op', 'man', 'set_open_aut', False),
                 ('aut', 'int', 'set_open_aut', True),
                 ('aut', 'man', 'set_open_aut', True),

                 ('off', 'int', 'set_close_op', False),
                 ('off', 'man', 'set_close_op', False),
                 ('op', 'int', 'set_close_op', True),
                 ('op', 'man', 'set_close_op', True),
                 ('aut', 'int', 'set_close_op', False),
                 ('aut', 'man', 'set_close_op', False),

                 ('off', 'int', 'set_close_aut', False),
                 ('off', 'man', 'set_close_aut', False),
                 ('op', 'int', 'set_close_aut', False),
                 ('op', 'man', 'set_close_aut', False),
                 ('aut', 'int', 'set_close_aut', True),
                 ('aut', 'man', 'set_close_aut', True)]


def test_open_close():
    for op_mode, src_mode, set_command, expected_result in test_scenario:
        for command in [True, False]:
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode)
            eval(f'ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {expected_result}')
            if set_command in ['set_open_op', 'set_open_aut']:
                if command:
                    assert ana_vlv.attributes['OpenAct'].value == expected_result
                    assert ana_vlv.get_open_fbk() == expected_result
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False
                else:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False
            elif set_command in ['set_close_op', 'set_close_aut']:
                if command:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == expected_result
                    assert ana_vlv.get_close_fbk() == expected_result
                else:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False


def test_open_close_permit_en_true():
    for op_mode, src_mode, set_command, _ in test_scenario:
        for command in [True, False]:
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode, perm_en=True)
            ana_vlv.set_permit(False)
            eval(f'ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: False')
            assert ana_vlv.attributes['SafePosAct'].value == False
            assert ana_vlv.attributes['Permit'].value == False
            assert ana_vlv.attributes['OpenAct'].value == False
            assert ana_vlv.attributes['CloseAct'].value == False
            assert ana_vlv.get_open_fbk() == False
            assert ana_vlv.get_close_fbk() == False

    for op_mode, src_mode, set_command, expected_result in test_scenario:
        for command in [True, False]:
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode, perm_en=True)
            ana_vlv.set_permit(True)
            eval(f'ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {expected_result}')

            assert ana_vlv.attributes['Permit'].value == True
            assert ana_vlv.attributes['SafePosAct'].value == False
            if set_command in ['set_open_op', 'set_open_aut']:
                if command:
                    assert ana_vlv.attributes['OpenAct'].value == expected_result
                    assert ana_vlv.get_open_fbk() == expected_result
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False
                else:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False
            elif set_command in ['set_close_op', 'set_close_aut']:
                if command:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == expected_result
                    assert ana_vlv.get_close_fbk() == expected_result
                else:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False


def test_open_close_permit_en_false():
    for op_mode, src_mode, set_command, expected_result in test_scenario:
        for command in [True, False]:
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode, perm_en=False)
            ana_vlv.set_permit(True)
            eval(f'ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {expected_result}')

            assert ana_vlv.attributes['Permit'].value == True
            assert ana_vlv.attributes['SafePosAct'].value == False
            if set_command in ['set_open_op', 'set_open_aut']:
                if command:
                    assert ana_vlv.attributes['OpenAct'].value == expected_result
                    assert ana_vlv.get_open_fbk() == expected_result
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False
                else:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False
            elif set_command in ['set_close_op', 'set_close_aut']:
                if command:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == expected_result
                    assert ana_vlv.get_close_fbk() == expected_result
                else:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False


def test_open_close_interlock_en_true():
    for op_mode, src_mode, set_command, _ in test_scenario:
        for command in [True, False]:
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode, intl_en=True)
            ana_vlv.set_interlock(False)
            eval(f'ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: False')

            assert ana_vlv.attributes['Interlock'].value == False
            assert ana_vlv.attributes['SafePosAct'].value == True
            assert ana_vlv.attributes['OpenAct'].value == False
            assert ana_vlv.attributes['CloseAct'].value == True
            assert ana_vlv.get_open_fbk() == False
            assert ana_vlv.get_close_fbk() == True

    for op_mode, src_mode, set_command, expected_result in test_scenario:
        for command in [True, False]:
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode, intl_en=True)
            ana_vlv.set_interlock(True)
            eval(f'ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {expected_result}')

            assert ana_vlv.attributes['Interlock'].value == True
            assert ana_vlv.attributes['SafePosAct'].value == False
            if set_command in ['set_open_op', 'set_open_aut']:
                if command:
                    assert ana_vlv.attributes['OpenAct'].value == expected_result
                    assert ana_vlv.get_open_fbk() == expected_result
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False
                else:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False
            elif set_command in ['set_close_op', 'set_close_aut']:
                if command:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == expected_result
                    assert ana_vlv.get_close_fbk() == expected_result
                else:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False


def test_open_close_interlock_en_false():
    for op_mode, src_mode, set_command, expected_result in test_scenario:
        for command in [True, False]:
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode, intl_en=False)
            ana_vlv.set_interlock(True)
            eval(f'ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {expected_result}')

            assert ana_vlv.attributes['Interlock'].value == True
            assert ana_vlv.attributes['SafePosAct'].value == False
            if set_command in ['set_open_op', 'set_open_aut']:
                if command:
                    assert ana_vlv.attributes['OpenAct'].value == expected_result
                    assert ana_vlv.get_open_fbk() == expected_result
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False
                else:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False
            elif set_command in ['set_close_op', 'set_close_aut']:
                if command:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == expected_result
                    assert ana_vlv.get_close_fbk() == expected_result
                else:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False


def test_open_close_protect_en_true():
    for op_mode, src_mode, set_command, _ in test_scenario:
        for command in [True, False]:
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode, prot_en=True)
            ana_vlv.set_protect(False)
            eval(f'ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: False')

            assert ana_vlv.attributes['Protect'].value == False
            assert ana_vlv.attributes['SafePosAct'].value == True
            assert ana_vlv.attributes['OpenAct'].value == False
            assert ana_vlv.attributes['CloseAct'].value == True

    for op_mode, src_mode, set_command, expected_result in test_scenario:
        for command in [True, False]:
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode, prot_en=True)
            ana_vlv.set_protect(True)
            assert ana_vlv.attributes['Protect'].value == True
            assert ana_vlv.attributes['SafePosAct'].value == False
            assert ana_vlv.attributes['OpenAct'].value == False  # state after calling reset
            assert ana_vlv.attributes['CloseAct'].value == False  # state after calling reset

            eval(f'ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {expected_result}')

            if set_command in ['set_open_op', 'set_open_aut']:
                if command:
                    assert ana_vlv.attributes['OpenAct'].value == expected_result
                    assert ana_vlv.get_open_fbk() == expected_result
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False
                else:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False
            elif set_command in ['set_rev_op', 'set_rev_aut']:
                if command:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == expected_result
                    assert ana_vlv.get_close_fbk() == expected_result
                else:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.get_open_fbk() == False
                    assert ana_vlv.attributes['CloseAct'].value == False
                    assert ana_vlv.get_close_fbk() == False


def test_open_close_protect_en_false():
    for op_mode, src_mode, set_command, expected_result in test_scenario:
        for command in [True, False]:
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode, prot_en=False)
            ana_vlv.set_protect(True)

            assert ana_vlv.attributes['Protect'].value == True
            assert ana_vlv.attributes['SafePosAct'].value == False
            assert ana_vlv.attributes['OpenAct'].value == False  # state after calling reset
            assert ana_vlv.attributes['CloseAct'].value == False  # state after calling reset

            eval(f'ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {expected_result}')
            if set_command in ['set_open_op', 'set_open_aut']:
                if command:
                    assert ana_vlv.attributes['OpenAct'].value == expected_result
                    assert ana_vlv.attributes['CloseAct'].value == False
                else:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.attributes['CloseAct'].value == False
            elif set_command in ['set_close_op', 'set_close_aut']:
                if command:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.attributes['CloseAct'].value == expected_result
                else:
                    assert ana_vlv.attributes['OpenAct'].value == False
                    assert ana_vlv.attributes['CloseAct'].value == False


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
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode, prot_en=True)

            # active protect lock
            ana_vlv.set_protect(False)
            assert ana_vlv.attributes['Protect'].value == False
            assert ana_vlv.attributes['SafePosAct'].value == True
            assert ana_vlv.attributes['OpenAct'].value == False
            assert ana_vlv.attributes['CloseAct'].value == True

            # call reset
            eval(f'ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, expected: {result}')

            if command:
                assert ana_vlv.attributes['Protect'].value == result
                assert ana_vlv.attributes['SafePosAct'].value != result
                assert ana_vlv.attributes['OpenAct'].value == False
                assert ana_vlv.attributes['CloseAct'].value != result
            else:
                assert ana_vlv.attributes['Protect'].value == False
                assert ana_vlv.attributes['SafePosAct'].value == True
                assert ana_vlv.attributes['OpenAct'].value == False
                assert ana_vlv.attributes['CloseAct'].value == True


test_scenario_pos = [('off', 'int', 'set_pos_int', False),
                     ('off', 'man', 'set_pos_int', False),
                     ('op', 'int', 'set_pos_int', True),
                     ('op', 'man', 'set_pos_int', False),
                     ('aut', 'int', 'set_pos_int', True),
                     ('aut', 'man', 'set_pos_int', False),

                     ('off', 'int', 'set_pos_man', False),
                     ('off', 'man', 'set_pos_man', False),
                     ('op', 'int', 'set_pos_man', False),
                     ('op', 'man', 'set_pos_man', True),
                     ('aut', 'int', 'set_pos_man', False),
                     ('aut', 'man', 'set_pos_man', True)]


def test_pos_open():
    for op_mode, src_mode, set_command, changes_expected in test_scenario_pos:
        for command in [-2, 2, 5, 10, 100]:
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode, pos_fbk_calc=True)
            if op_mode == 'op':
                ana_vlv.set_open_op(True)
            elif op_mode == 'aut':
                ana_vlv.set_open_aut(True)
            eval(f'ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, {command} changes expected: {changes_expected}')
            if changes_expected:
                if 2 <= command <= 10:
                    assert ana_vlv.get_pos() == command
                    assert ana_vlv.get_pos_fbk() == command
                else:
                    assert ana_vlv.get_pos() == 2
                    assert ana_vlv.get_pos_fbk() == 2
            else:
                assert ana_vlv.get_pos() == 2
                assert ana_vlv.get_pos_fbk() == 2


def test_pos_close():
    for op_mode, src_mode, set_command, changes_expected in test_scenario_pos:
        for command in [-2, 2, 5, 10, 100]:
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode, pos_fbk_calc=True)
            if op_mode == 'op':
                ana_vlv.set_close_op(True)
            elif op_mode == 'aut':
                ana_vlv.set_close_aut(True)
            eval(f'ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, {command} changes expected: {changes_expected}')

            assert ana_vlv.get_pos() == 2
            assert ana_vlv.get_pos_fbk() == 2


test_scenario_safe_pos_en = [('op', 'int', 'set_pos_int', 1, True),
                             ('aut', 'int', 'set_pos_int', 1, True),
                             ('op', 'man', 'set_pos_man', 1, True),
                             ('aut', 'man', 'set_pos_man', 1, True),
                             ('op', 'int', 'set_pos_int', 1, False),
                             ('aut', 'int', 'set_pos_int', 1, False),
                             ('op', 'man', 'set_pos_man', 1, False),
                             ('aut', 'man', 'set_pos_man', 1, False),
                             ('op', 'int', 'set_pos_int', 0, True),
                             ('aut', 'int', 'set_pos_int', 0, True),
                             ('op', 'man', 'set_pos_man', 0, True),
                             ('aut', 'man', 'set_pos_man', 0, True),
                             ('op', 'int', 'set_pos_int', 0, False),
                             ('aut', 'int', 'set_pos_int', 0, False),
                             ('op', 'man', 'set_pos_man', 0, False),
                             ('aut', 'man', 'set_pos_man', 0, False)]


def test_safe_pos_en_true_interlock():
    for op_mode, src_mode, set_command, safe_pos, safe_pos_en in test_scenario_safe_pos_en:
        for command in [5, 7]:
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode, pos_fbk_calc=True, safe_pos=safe_pos,
                                   safe_pos_en=safe_pos_en, intl_en=True)
            ana_vlv.set_interlock(True)  # interlock is inactive
            if op_mode == 'op':  # open valve
                ana_vlv.set_open_op(True)
            elif op_mode == 'aut':
                ana_vlv.set_open_aut(True)
            eval(f'ana_vlv.{set_command}({command})')  # set legal position
            ana_vlv.set_interlock(False)  # active interlock after setting a position
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, {command}, safe_pos: {safe_pos}, '
                  f'safe_pos_en: {safe_pos_en}')

            # if safe_pos_en is true, valve should be to set to safety position (max or min) after interlock is
            # activated
            if safe_pos_en:
                if safe_pos == 1:
                    assert ana_vlv.get_pos() == 10
                    assert ana_vlv.get_pos_fbk() == 10
                elif safe_pos == 0:
                    assert ana_vlv.get_pos() == 2
                    assert ana_vlv.get_pos_fbk() == 2

            # if safe_pos_en is false, current valve position should be hold after interlock is activated
            else:
                assert ana_vlv.get_pos() == command
                assert ana_vlv.get_pos_fbk() == command

            # try to set new value (6) for position, after interlock is activated again, the position should not be
            # changed
            eval(f'ana_vlv.{set_command}(6)')  # set legal position
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, 6, safe_pos: {safe_pos}, '
                  f'safe_pos_en: {safe_pos_en}, safe_pos_act: True')
            if safe_pos_en:
                if safe_pos == 1:
                    assert ana_vlv.get_pos() == 10
                    assert ana_vlv.get_pos_fbk() == 10
                elif safe_pos == 0:
                    assert ana_vlv.get_pos() == 2
                    assert ana_vlv.get_pos_fbk() == 2

            else:
                assert ana_vlv.get_pos() == command
                assert ana_vlv.get_pos_fbk() == command


def test_safe_pos_en_true_protect():
    for op_mode, src_mode, set_command, safe_pos, safe_pos_en in test_scenario_safe_pos_en:
        for command in [5, 7]:
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode, pos_fbk_calc=True, safe_pos=safe_pos,
                                   safe_pos_en=safe_pos_en, prot_en=True)
            ana_vlv.set_protect(True)  # protect lock is inactive
            if op_mode == 'op':  # open valve
                ana_vlv.set_open_op(True)
            elif op_mode == 'aut':
                ana_vlv.set_open_aut(True)
            eval(f'ana_vlv.{set_command}({command})')  # set legal position
            ana_vlv.set_protect(False)  # active protect lock after setting a position
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, {command}, safe_pos: {safe_pos}, '
                  f'safe_pos_en: {safe_pos_en}')

            # if safe_pos_en is true, valve should be to set to safety position (max or min) after protect lock is
            # activated
            if safe_pos_en:
                if safe_pos == 1:
                    assert ana_vlv.get_pos() == 10
                    assert ana_vlv.get_pos_fbk() == 10
                elif safe_pos == 0:
                    assert ana_vlv.get_pos() == 2
                    assert ana_vlv.get_pos_fbk() == 2

            # if safe_pos_en is false, current valve position should be hold after protect lock is activated
            else:
                assert ana_vlv.get_pos() == command
                assert ana_vlv.get_pos_fbk() == command

            # try to set new value (6) for position, after protect lock is activated again, the position should not be
            # changed
            eval(f'ana_vlv.{set_command}(6)')  # set legal position
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, 6, safe_pos: {safe_pos}, '
                  f'safe_pos_en: {safe_pos_en}, safe_pos_act: True')
            if safe_pos_en:
                if safe_pos == 1:
                    assert ana_vlv.get_pos() == 10
                    assert ana_vlv.get_pos_fbk() == 10
                elif safe_pos == 0:
                    assert ana_vlv.get_pos() == 2
                    assert ana_vlv.get_pos_fbk() == 2

            else:
                assert ana_vlv.get_pos() == command
                assert ana_vlv.get_pos_fbk() == command


def test_safe_pos_en_true_permit():
    for op_mode, src_mode, set_command, safe_pos, safe_pos_en in test_scenario_safe_pos_en:
        for command in [5, 7]:
            ana_vlv = init_ana_vlv(op_mode=op_mode, src_mode=src_mode, pos_fbk_calc=True, safe_pos=safe_pos,
                                   safe_pos_en=safe_pos_en, perm_en=True)
            ana_vlv.set_permit(True)  # permit lock is inactive
            if op_mode == 'op':  # open valve
                ana_vlv.set_open_op(True)
            elif op_mode == 'aut':
                ana_vlv.set_open_aut(True)
            eval(f'ana_vlv.{set_command}({command})')  # set legal position
            ana_vlv.set_permit(False)  # active permit lock after setting a position
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, {command}, safe_pos: {safe_pos}, '
                  f'safe_pos_en: {safe_pos_en}')

            # activated DataAssembly in the locked state (permit mode) is not set to the safe position
            assert ana_vlv.get_pos() == command
            assert ana_vlv.get_pos_fbk() == command

            # try to set new position after permit is activated, position should not be changed
            eval(f'ana_vlv.{set_command}(6)')
            assert ana_vlv.get_pos() == command
            assert ana_vlv.get_pos_fbk() == command


def test_pos_rbk():
    for pos in [-2, 2, 5, 10, 100]:
        ana_vlv = init_ana_vlv()
        ana_vlv.set_pos_rbk(pos)

        if 2 <= pos <= 10:
            assert ana_vlv.get_pos_rbk() == pos
        elif pos < 2:
            assert ana_vlv.get_pos_rbk() == 2
        elif pos > 10:
            assert ana_vlv.get_pos_rbk() == 10


def test_pos_fbk():
    for pos in [-2, 2, 5, 10, 100]:
        for fbk_calc in [False, True]:
            ana_vlv = init_ana_vlv(pos_fbk_calc=fbk_calc)
            ana_vlv.set_pos_fbk(pos)
            if not fbk_calc:
                if 2 <= pos <= 10:
                    assert ana_vlv.get_pos_fbk() == pos
                elif pos < 2:
                    assert ana_vlv.get_pos_fbk() == 2
                elif pos > 10:
                    assert ana_vlv.get_pos_fbk() == 10


def test_open_fbk():
    ana_vlv = init_ana_vlv(open_fbk_calc=False, close_fbk_calc=False)
    assert ana_vlv.get_open_fbk() == False
    ana_vlv.set_open_fbk(True)
    assert ana_vlv.get_open_fbk() == True


def test_close_fbk():
    ana_vlv = init_ana_vlv(open_fbk_calc=False, close_fbk_calc=False)
    assert ana_vlv.get_close_fbk() == False
    ana_vlv.set_close_fbk(True)
    assert ana_vlv.get_close_fbk() == True


if __name__ == '__main__':
    pytest.main(['test_ana_vlv.py', '-s'])
