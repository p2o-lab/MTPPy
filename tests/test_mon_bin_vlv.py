import pytest
from mtppy.active_elements import MonBinVlv
import time

mon_bin_vlv = MonBinVlv('tag', tag_description='', open_fbk_calc=True, close_fbk_calc=True, safe_pos=1, safe_pos_en=1,
                        perm_en=False, intl_en=False, prot_en=False, mon_en=True, mon_safe_pos=1, mon_stat_ti=1,
                        mon_dyn_ti=1)


def test_static_error():
    mon_bin_vlv.start_monitor()
    time.sleep(2)

    mon_bin_vlv.attributes['Ctrl'].set_value(True)  # Ctrl becomes to True without any control signals
    time.sleep(2)

    assert mon_bin_vlv.attributes['MonStatErr'].value == True  # static error should be set to True
    assert mon_bin_vlv.attributes['SafePosAct'].value == True  # valva should be set to safety position
    assert mon_bin_vlv.attributes['Ctrl'].value == True  # safety position of valve is open
    time.sleep(2)

    # after valve is set to safety position (open), the variable ctrl becomes to False --> another static error
    mon_bin_vlv.attributes['Ctrl'].set_value(False)
    time.sleep(2)

    assert mon_bin_vlv.attributes['MonStatErr'].value == True
    assert mon_bin_vlv.attributes['SafePosAct'].value == True
    assert mon_bin_vlv.attributes['Ctrl'].value == True  # safety position of valve is open

    mon_bin_vlv.set_stop_monitor()
    mon_bin_vlv.monitor_static_thread.join()
    mon_bin_vlv.monitor_dynamic_thread.join()


if __name__ == '__main__':
    pytest.main(['test_mon_bin_vlv.py', '-s'])
