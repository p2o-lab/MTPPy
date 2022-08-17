import pytest
from mtppy.active_elements import MonBinDrv
import time


def init_mon_bin_drv(op_mode='off', src_mode='int', rev_fbk_calc=True, fwd_fbk_calc=True, safe_pos=1, fwd_en=True,
                     rev_en=True, perm_en=False, intl_en=False, prot_en=False, mon_en=True, mon_safe_pos=1,
                     mon_stat_ti=0.5, mon_dyn_ti=0.5):
    mon_bin_drv = MonBinDrv('tag', tag_description='', rev_fbk_calc=rev_fbk_calc, fwd_fbk_calc=fwd_fbk_calc,
                            safe_pos=safe_pos, fwd_en=fwd_en, rev_en=rev_en, perm_en=perm_en, intl_en=intl_en,
                            prot_en=prot_en, mon_en=mon_en, mon_safe_pos=mon_safe_pos, mon_stat_ti=mon_stat_ti,
                            mon_dyn_ti=mon_dyn_ti)

    if op_mode == 'op':
        mon_bin_drv.op_src_mode.attributes['StateOpOp'].set_value(True)
    elif op_mode == 'aut':
        mon_bin_drv.op_src_mode.attributes['StateAutOp'].set_value(True)
    elif op_mode == 'off':
        pass
    else:
        raise ValueError(f'Operation mode {op_mode} is unknown')

    if src_mode == 'man':
        mon_bin_drv.op_src_mode.attributes['SrcManOp'].set_value(True)
    elif src_mode == 'int':
        mon_bin_drv.op_src_mode.attributes['SrcIntOp'].set_value(True)
    else:
        raise ValueError(f'Source mode {src_mode} is unknown')
    return mon_bin_drv


test_scenario_no_control_signals = [('off', 'int', 'set_fwd_op'),
                                    ('off', 'man', 'set_fwd_op'),
                                    ('aut', 'int', 'set_fwd_op'),
                                    ('aut', 'man', 'set_fwd_op'),

                                    ('off', 'int', 'set_fwd_aut'),
                                    ('off', 'man', 'set_fwd_aut'),
                                    ('op', 'int', 'set_fwd_aut'),
                                    ('op', 'man', 'set_fwd_aut'),

                                    ('off', 'int', 'set_rev_op'),
                                    ('off', 'man', 'set_rev_op'),
                                    ('aut', 'int', 'set_rev_op'),
                                    ('aut', 'man', 'set_rev_op'),

                                    ('off', 'int', 'set_rev_aut'),
                                    ('off', 'man', 'set_rev_aut'),
                                    ('op', 'int', 'set_rev_aut'),
                                    ('op', 'man', 'set_rev_aut')]


def test_static_error():
    for op_mode, src_mode, set_command in test_scenario_no_control_signals:
        for command in [True, False]:
            mon_bin_drv = init_mon_bin_drv(op_mode=op_mode, src_mode=src_mode)

            mon_bin_drv.start_monitor()
            eval(f'mon_bin_drv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}')

            mon_bin_drv.attributes['FwdFbk'].set_value(True)  # FwdFbk becomes to True without any control signals
            time.sleep(0.6)

            assert mon_bin_drv.attributes['MonStatErr'].value == True
            assert mon_bin_drv.attributes['SafePosAct'].value == True
            assert mon_bin_drv.attributes['FwdFbk'].value == True  # safe position is clockwise rotation

            mon_bin_drv.attributes['FwdFbk'].set_value(False)  # FwdFbk becomes to True without any control signals
            time.sleep(0.6)

            assert mon_bin_drv.attributes['MonStatErr'].value == True
            assert mon_bin_drv.attributes['SafePosAct'].value == True
            assert mon_bin_drv.attributes['FwdFbk'].value == True  # safe position is clockwise rotation

            mon_bin_drv.set_stop_monitor()
            mon_bin_drv.monitor_static_thread.join()
            mon_bin_drv.monitor_dynamic_thread.join()


def test_static_error_within_monitor_time():
    """If the required state is set on the interface before the time has expired (wait tme < 0.5s in this test),
    there is no error"""

    for op_mode, src_mode, set_command in test_scenario_no_control_signals:
        for command in [True, False]:
            mon_bin_drv = init_mon_bin_drv(op_mode=op_mode, src_mode=src_mode)

            mon_bin_drv.start_monitor()
            eval(f'mon_bin_drv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}')

            # mimic an error situation: FwdFbk changes to True without any change in control signal
            mon_bin_drv.attributes['FwdFbk'].set_value(True)
            time.sleep(0.3)  # monitor time has not expired (0.5s)

            assert mon_bin_drv.attributes['MonStatErr'].value == False
            assert mon_bin_drv.attributes['MonDynErr'].value == False
            assert mon_bin_drv.attributes['SafePosAct'].value == False

            mon_bin_drv.set_stop_monitor()
            mon_bin_drv.monitor_static_thread.join()
            mon_bin_drv.monitor_dynamic_thread.join()


test_scenario_control_signals_fwd = [('op', 'int', 'set_fwd_op', 'set_stop_op'),
                                     ('op', 'man', 'set_fwd_op', 'set_stop_op'),

                                     ('aut', 'int', 'set_fwd_aut', 'set_stop_aut'),
                                     ('aut', 'man', 'set_fwd_aut', 'set_stop_aut')]


def test_dynamic_error_fwd_stop():
    for op_mode, src_mode, fwd_command, stop_command in test_scenario_control_signals_fwd:
        mon_bin_drv = init_mon_bin_drv(op_mode=op_mode, src_mode=src_mode)

        mon_bin_drv.start_monitor()
        eval(f'mon_bin_drv.{fwd_command}(True)')
        print(f'Scenario: mode {op_mode} {src_mode}, {fwd_command}')

        # FwdFbk dose not change to True after control signal has changed to clockwise rotation
        mon_bin_drv.attributes['FwdFbk'].set_value(False)
        time.sleep(0.6)

        assert mon_bin_drv.attributes['MonDynErr'].value == True
        assert mon_bin_drv.attributes['MonStatErr'].value == False
        assert mon_bin_drv.attributes['SafePosAct'].value == True
        assert mon_bin_drv.attributes['FwdFbk'].value == True  # safe position is clockwise rotation

        eval(f'mon_bin_drv.{stop_command}(True)')
        print(f'Scenario: mode {op_mode} {src_mode}, {stop_command}')

        # FwdFbk dose not change to False after control signal has changed to stop
        mon_bin_drv.attributes['FwdFbk'].set_value(True)
        time.sleep(0.6)

        assert mon_bin_drv.attributes['MonDynErr'].value == True
        assert mon_bin_drv.attributes['MonStatErr'].value == False
        assert mon_bin_drv.attributes['SafePosAct'].value == True
        assert mon_bin_drv.attributes['FwdFbk'].value == True  # safe position is clockwise rotation

        mon_bin_drv.set_stop_monitor()
        mon_bin_drv.monitor_static_thread.join()
        mon_bin_drv.monitor_dynamic_thread.join()


test_scenario_control_signals_rev = [('op', 'int', 'set_rev_op', 'set_stop_op'),
                                     ('op', 'man', 'set_rev_op', 'set_stop_op'),

                                     ('aut', 'int', 'set_rev_aut', 'set_stop_aut'),
                                     ('aut', 'man', 'set_rev_aut', 'set_stop_aut')]


def test_dynamic_error_rev_stop():
    for op_mode, src_mode, rev_command, stop_command in test_scenario_control_signals_rev:
        mon_bin_drv = init_mon_bin_drv(op_mode=op_mode, src_mode=src_mode)

        mon_bin_drv.start_monitor()
        eval(f'mon_bin_drv.{rev_command}(True)')
        print(f'Scenario: mode {op_mode} {src_mode}, {rev_command}')

        # RevFbk dose not change to True after control signal has changed to anti-clockwise rotation
        mon_bin_drv.attributes['RevFbk'].set_value(False)
        time.sleep(0.6)
        assert mon_bin_drv.attributes['MonDynErr'].value == True
        assert mon_bin_drv.attributes['MonStatErr'].value == False
        assert mon_bin_drv.attributes['SafePosAct'].value == True
        assert mon_bin_drv.attributes['FwdFbk'].value == True  # safe position is clockwise rotation

        eval(f'mon_bin_drv.{stop_command}(True)')
        print(f'Scenario: mode {op_mode} {src_mode}, {stop_command}')

        # FwdFbk dose not change to False after control signal has changed to stop
        mon_bin_drv.attributes['FwdFbk'].set_value(True)
        time.sleep(0.6)

        assert mon_bin_drv.attributes['MonDynErr'].value == True
        assert mon_bin_drv.attributes['MonStatErr'].value == False
        assert mon_bin_drv.attributes['SafePosAct'].value == True
        assert mon_bin_drv.attributes['FwdFbk'].value == True  # safe position is clockwise rotation

        mon_bin_drv.set_stop_monitor()
        mon_bin_drv.monitor_static_thread.join()
        mon_bin_drv.monitor_dynamic_thread.join()


test_scenario_control_signals_reset = [('op', 'int', 'set_reset_op'),
                                       ('op', 'man', 'set_reset_op'),

                                       ('aut', 'int', 'set_reset_aut'),
                                       ('aut', 'man', 'set_reset_aut')]


def test_dynamic_error_reset():
    for op_mode, src_mode, set_command in test_scenario_control_signals_reset:
        mon_bin_drv = init_mon_bin_drv(op_mode=op_mode, src_mode=src_mode)

        mon_bin_drv.start_monitor()
        # set valve to open
        if op_mode == 'op':
            mon_bin_drv.set_fwd_op(True)
        elif op_mode == 'aut':
            mon_bin_drv.set_fwd_aut(True)
        time.sleep(0.6)

        # reset valve
        eval(f'mon_bin_drv.{set_command}(True)')
        print(f'Scenario: mode {op_mode} {src_mode}, {set_command}')

        # mimic an error situation: FwdFbk dose not change to False after reset changes to True
        mon_bin_drv.attributes['FwdFbk'].set_value(True)
        time.sleep(0.6)

        assert mon_bin_drv.attributes['MonDynErr'].value == True
        assert mon_bin_drv.attributes['MonStatErr'].value == False
        assert mon_bin_drv.attributes['SafePosAct'].value == True
        assert mon_bin_drv.attributes['FwdFbk'].value == True  # safe position of valve is open

        mon_bin_drv.set_stop_monitor()
        mon_bin_drv.monitor_static_thread.join()
        mon_bin_drv.monitor_dynamic_thread.join()


if __name__ == '__main__':
    pytest.main(['test_mon_bin_drv.py', '-s'])
