import pytest
from mtppy.active_elements import MonAnaVlv
import time


def init_mon_ana_vlv(op_mode='off', src_mode='int', open_fbk_calc=True, close_fbk_calc=True, pos_fbk_calc=True,
                     safe_pos=1, safe_pos_en=True, perm_en=False, intl_en=False, prot_en=False, mon_en=True,
                     mon_safe_pos=True, mon_stat_ti=1, mon_dyn_ti=1, pos_tolerance=1, mon_pos_ti=1):
    mon_ana_vlv = MonAnaVlv('tag', tag_description='',
                            pos_min=2, pos_max=10, pos_scl_min=0, pos_scl_max=10, pos_unit=0,
                            open_fbk_calc=open_fbk_calc, close_fbk_calc=close_fbk_calc, pos_fbk_calc=pos_fbk_calc,
                            safe_pos=safe_pos, safe_pos_en=safe_pos_en, perm_en=perm_en, intl_en=intl_en,
                            prot_en=prot_en, mon_en=mon_en, mon_safe_pos=mon_safe_pos, mon_stat_ti=mon_stat_ti,
                            mon_dyn_ti=mon_dyn_ti, pos_tolerance=pos_tolerance, mon_pos_ti=mon_pos_ti)
    if op_mode == 'op':
        mon_ana_vlv.op_src_mode.attributes['StateOpOp'].set_value(True)
    elif op_mode == 'aut':
        mon_ana_vlv.op_src_mode.attributes['StateAutOp'].set_value(True)
    elif op_mode == 'off':
        pass
    else:
        raise ValueError(f'Operation mode {op_mode} is unknown')

    if src_mode == 'man':
        mon_ana_vlv.op_src_mode.attributes['SrcManOp'].set_value(True)
    elif src_mode == 'int':
        mon_ana_vlv.op_src_mode.attributes['SrcIntOp'].set_value(True)
    else:
        raise ValueError(f'Source mode {src_mode} is unknown')
    return mon_ana_vlv


test_scenario_no_control_signals = [('off', 'int', 'set_open_op'),
                                    ('off', 'man', 'set_open_op'),
                                    ('aut', 'int', 'set_open_op'),
                                    ('aut', 'man', 'set_open_op'),

                                    ('off', 'int', 'set_open_aut'),
                                    ('off', 'man', 'set_open_aut'),
                                    ('op', 'int', 'set_open_aut'),
                                    ('op', 'man', 'set_open_aut'),

                                    ('off', 'int', 'set_close_op'),
                                    ('off', 'man', 'set_close_op'),
                                    ('aut', 'int', 'set_close_op'),
                                    ('aut', 'man', 'set_close_op'),

                                    ('off', 'int', 'set_close_aut'),
                                    ('off', 'man', 'set_close_aut'),
                                    ('op', 'int', 'set_close_aut'),
                                    ('op', 'man', 'set_close_aut')]


def test_static_error():
    for op_mode, src_mode, set_command in test_scenario_no_control_signals:
        for command in [True, False]:
            mon_ana_vlv = init_mon_ana_vlv(op_mode=op_mode, src_mode=src_mode)

            mon_ana_vlv.start_monitor()
            eval(f'mon_ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}')

            # mimic an error situation: OpenFbk changes to True without any change in control signal
            mon_ana_vlv.attributes['OpenFbk'].set_value(True)
            time.sleep(1.1)  # monitor time has expired (> 1s)

            assert mon_ana_vlv.attributes['MonStatErr'].value == True
            assert mon_ana_vlv.attributes['MonDynErr'].value == False
            assert mon_ana_vlv.attributes['SafePosAct'].value == True
            assert mon_ana_vlv.attributes['OpenFbk'].value == True  # safe position of valve is open

            time.sleep(0.5)

            # after valve is set to safe position (open), the OpenFbk becomes to False --> another static error
            mon_ana_vlv.attributes['OpenFbk'].set_value(False)
            time.sleep(1.1)  # monitor time has expired (> 1s)

            assert mon_ana_vlv.attributes['MonStatErr'].value == True
            assert mon_ana_vlv.attributes['MonDynErr'].value == False
            assert mon_ana_vlv.attributes['SafePosAct'].value == True
            assert mon_ana_vlv.attributes['OpenFbk'].value == True  # safe position of valve is open

            mon_ana_vlv.set_stop_monitor()
            mon_ana_vlv.monitor_static_thread.join()
            mon_ana_vlv.monitor_dynamic_thread.join()


def test_static_error_within_monitor_time():
    """If the required state is set on the interface before the time has expired (wait tme < 1s in this test),
    there is no error"""

    for op_mode, src_mode, set_command in test_scenario_no_control_signals:
        for command in [True, False]:
            mon_ana_vlv = init_mon_ana_vlv(op_mode=op_mode, src_mode=src_mode)

            mon_ana_vlv.start_monitor()
            eval(f'mon_ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}')

            # mimic an error situation: OpenFbk changes to True without any change in control signal
            mon_ana_vlv.attributes['OpenFbk'].set_value(True)
            time.sleep(0.6)  # monitor time has not expired (1s)

            assert mon_ana_vlv.attributes['MonStatErr'].value == False
            assert mon_ana_vlv.attributes['MonDynErr'].value == False
            assert mon_ana_vlv.attributes['SafePosAct'].value == False

            mon_ana_vlv.set_stop_monitor()
            mon_ana_vlv.monitor_static_thread.join()
            mon_ana_vlv.monitor_dynamic_thread.join()


test_scenario_control_signals = [('op', 'int', 'set_open_op', 'set_close_op'),
                                 ('op', 'man', 'set_open_op', 'set_close_op'),

                                 ('aut', 'int', 'set_open_aut', 'set_close_aut'),
                                 ('aut', 'man', 'set_open_aut', 'set_close_aut')]


def test_dynamic_error_open_close():
    for op_mode, src_mode, open_command, close_command in test_scenario_control_signals:
        mon_ana_vlv = init_mon_ana_vlv(op_mode=op_mode, src_mode=src_mode)

        mon_ana_vlv.start_monitor()
        eval(f'mon_ana_vlv.{open_command}(True)')
        print(f'Scenario: mode {op_mode} {src_mode}, {open_command}')

        # mimic an error situation: OpenFbk dose not change to True after control signal has changed to open
        mon_ana_vlv.attributes['OpenFbk'].set_value(False)
        time.sleep(1.1)  # monitor time has expired (> 1s)

        assert mon_ana_vlv.attributes['MonDynErr'].value == True
        assert mon_ana_vlv.attributes['MonStatErr'].value == False
        assert mon_ana_vlv.attributes['SafePosAct'].value == True
        assert mon_ana_vlv.attributes['OpenFbk'].value == True  # safe position of valve is open

        eval(f'mon_ana_vlv.{close_command}(True)')
        print(f'Scenario: mode {op_mode} {src_mode}, {close_command}')

        # mimic an error situation: OpenFbk dose not change to False after control signal has changed to close
        mon_ana_vlv.attributes['OpenFbk'].set_value(True)
        time.sleep(1.1)  # monitor time has expired (> 1s)

        assert mon_ana_vlv.attributes['MonDynErr'].value == True
        assert mon_ana_vlv.attributes['MonStatErr'].value == False
        assert mon_ana_vlv.attributes['SafePosAct'].value == True
        assert mon_ana_vlv.attributes['OpenFbk'].value == True  # safe position of valve is open

        mon_ana_vlv.set_stop_monitor()
        mon_ana_vlv.monitor_static_thread.join()
        mon_ana_vlv.monitor_dynamic_thread.join()


test_scenario_pos = [('op', 'int', 'set_pos_int'),
                     ('aut', 'int', 'set_pos_int'),
                     ('op', 'man', 'set_pos_man'),
                     ('aut', 'man', 'set_pos_man')]


def test_pos_open():
    for op_mode, src_mode, set_command in test_scenario_pos:
        for command in [-2, 4, 7, 10, 100]:  # pos min is 2, pos max is 10
            mon_ana_vlv = init_mon_ana_vlv(op_mode=op_mode, src_mode=src_mode, pos_fbk_calc=True)
            if op_mode == 'op':
                mon_ana_vlv.set_open_op(True)
            elif op_mode == 'aut':
                mon_ana_vlv.set_open_aut(True)
            eval(f'mon_ana_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}, {command}')
            mon_ana_vlv.attributes['PosFbk'].set_value(7.5)  # position tolerance is 1, pos_fbk is 2.5 --> pos error
            time.sleep(1.5)  # time for monitoring pos error is 1s
            if 2 <= command < 6 or 8 < command <= 10:  # out of the pos tolerance range
                assert mon_ana_vlv.attributes['PosReachedFbk'].value == False
                assert mon_ana_vlv.attributes['MonPosErr'].value == True
                assert mon_ana_vlv.attributes['SafePosAct'].value == True
                assert mon_ana_vlv.attributes['OpenAct'].value == True

            elif 6 <= command <= 8:  # within the pos tolerance range
                assert mon_ana_vlv.attributes['PosReachedFbk'].value == True
                assert mon_ana_vlv.attributes['MonPosErr'].value == False
                assert mon_ana_vlv.attributes['SafePosAct'].value == False

            else:
                assert mon_ana_vlv.attributes['PosReachedFbk'].value == False
                assert mon_ana_vlv.attributes['MonPosErr'].value == False
                assert mon_ana_vlv.attributes['SafePosAct'].value == False


test_scenario_control_signals_reset = [('op', 'int', 'set_reset_op'),
                                       ('op', 'man', 'set_reset_op'),

                                       ('aut', 'int', 'set_reset_aut'),
                                       ('aut', 'man', 'set_reset_aut')]


def test_dynamic_error_reset():
    for op_mode, src_mode, set_command in test_scenario_control_signals_reset:
        mon_ana_vlv = init_mon_ana_vlv(op_mode=op_mode, src_mode=src_mode)

        mon_ana_vlv.start_monitor()
        # set valve to open
        if op_mode == 'op':
            mon_ana_vlv.set_open_op(True)
        elif op_mode == 'aut':
            mon_ana_vlv.set_open_aut(True)
        time.sleep(1.1)

        # reset valve
        eval(f'mon_ana_vlv.{set_command}(True)')
        print(f'Scenario: mode {op_mode} {src_mode}, {set_command}')

        # mimic an error situation: OpenFbk dose not change to False after reset changes to True
        mon_ana_vlv.attributes['OpenFbk'].set_value(True)
        time.sleep(1.1)

        assert mon_ana_vlv.attributes['MonDynErr'].value == True
        assert mon_ana_vlv.attributes['MonStatErr'].value == False
        assert mon_ana_vlv.attributes['SafePosAct'].value == True
        assert mon_ana_vlv.attributes['OpenFbk'].value == True  # safe position of valve is open

        mon_ana_vlv.set_stop_monitor()
        mon_ana_vlv.monitor_static_thread.join()
        mon_ana_vlv.monitor_dynamic_thread.join()


if __name__ == '__main__':
    pytest.main(['test_mon_ana_vlv.py', '-s'])
