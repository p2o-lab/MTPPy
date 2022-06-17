import pytest
from mtppy.active_elements import MonBinVlv
import time


def init_mon_bin_vlv(op_mode='off', src_mode='int', open_fbk_calc=True, close_fbk_calc=True, safe_pos=1,
                     safe_pos_en=True, perm_en=False, intl_en=False, prot_en=False, mon_en=True, mon_safe_pos=1,
                     mon_stat_ti=1, mon_dyn_ti=1):
    mon_bin_vlv = MonBinVlv('tag', tag_description='', open_fbk_calc=open_fbk_calc, close_fbk_calc=close_fbk_calc,
                            safe_pos=safe_pos, safe_pos_en=safe_pos_en, perm_en=perm_en, intl_en=intl_en,
                            prot_en=prot_en, mon_en=mon_en, mon_safe_pos=mon_safe_pos, mon_stat_ti=mon_stat_ti,
                            mon_dyn_ti=mon_dyn_ti)
    if op_mode == 'op':
        mon_bin_vlv.op_src_mode.attributes['StateOpOp'].set_value(True)
    elif op_mode == 'aut':
        mon_bin_vlv.op_src_mode.attributes['StateAutOp'].set_value(True)
    elif op_mode == 'off':
        pass
    else:
        raise ValueError(f'Operation mode {op_mode} is unknown')

    if src_mode == 'man':
        mon_bin_vlv.op_src_mode.attributes['SrcManOp'].set_value(True)
    elif src_mode == 'int':
        mon_bin_vlv.op_src_mode.attributes['SrcIntOp'].set_value(True)
    else:
        raise ValueError(f'Source mode {src_mode} is unknown')
    return mon_bin_vlv


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
            mon_bin_vlv = init_mon_bin_vlv(op_mode=op_mode, src_mode=src_mode)

            mon_bin_vlv.start_monitor()
            time.sleep(0.5)
            eval(f'mon_bin_vlv.{set_command}({command})')
            print(f'Scenario: mode {op_mode} {src_mode}, {set_command}')

            mon_bin_vlv.attributes['Ctrl'].set_value(True)  # Ctrl becomes to True without any control signals
            time.sleep(1.1)

            assert mon_bin_vlv.attributes['MonStatErr'].value == True
            assert mon_bin_vlv.attributes['MonDynErr'].value == False
            assert mon_bin_vlv.attributes['SafePosAct'].value == True
            assert mon_bin_vlv.attributes['Ctrl'].value == True

            time.sleep(0.5)

            # after valve is set to safety position (open), the variable ctrl becomes to False --> another static error
            mon_bin_vlv.attributes['Ctrl'].set_value(False)
            time.sleep(1.1)

            assert mon_bin_vlv.attributes['MonStatErr'].value == True
            assert mon_bin_vlv.attributes['MonDynErr'].value == False
            assert mon_bin_vlv.attributes['SafePosAct'].value == True
            assert mon_bin_vlv.attributes['Ctrl'].value == True  # safety position of valve is open

            mon_bin_vlv.set_stop_monitor()
            mon_bin_vlv.monitor_static_thread.join()
            mon_bin_vlv.monitor_dynamic_thread.join()


test_scenario_control_signals = [('op', 'int', 'set_open_op', 'set_close_op'),
                                 ('op', 'man', 'set_open_op', 'set_close_op'),

                                 ('aut', 'int', 'set_open_aut', 'set_close_aut'),
                                 ('aut', 'man', 'set_open_aut', 'set_close_aut')]


def test_dynamic_error_open_close():
    for op_mode, src_mode, open_command, close_command in test_scenario_control_signals:
        mon_bin_vlv = init_mon_bin_vlv(op_mode=op_mode, src_mode=src_mode)

        mon_bin_vlv.start_monitor()
        time.sleep(0.5)
        eval(f'mon_bin_vlv.{open_command}(True)')
        print(f'Scenario: mode {op_mode} {src_mode}, {open_command}')

        # Ctrl dose not change to True after control signal has changed to open
        mon_bin_vlv.attributes['Ctrl'].set_value(False)
        time.sleep(1.1)

        assert mon_bin_vlv.attributes['MonDynErr'].value == True
        assert mon_bin_vlv.attributes['MonStatErr'].value == False
        assert mon_bin_vlv.attributes['SafePosAct'].value == True
        assert mon_bin_vlv.attributes['Ctrl'].value == True

        eval(f'mon_bin_vlv.{close_command}(True)')
        print(f'Scenario: mode {op_mode} {src_mode}, {close_command}')

        # Ctrl dose not change to False after control signal has changed to close
        mon_bin_vlv.attributes['Ctrl'].set_value(True)
        time.sleep(1.1)

        assert mon_bin_vlv.attributes['MonDynErr'].value == True
        assert mon_bin_vlv.attributes['MonStatErr'].value == False
        assert mon_bin_vlv.attributes['SafePosAct'].value == True
        assert mon_bin_vlv.attributes['Ctrl'].value == True

        mon_bin_vlv.set_stop_monitor()
        mon_bin_vlv.monitor_static_thread.join()
        mon_bin_vlv.monitor_dynamic_thread.join()


if __name__ == '__main__':
    pytest.main(['test_mon_bin_vlv.py', '-s'])
