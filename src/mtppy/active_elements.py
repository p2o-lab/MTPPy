import logging
import threading

from mtppy.attribute import Attribute

from mtppy.operation_source_mode import OperationSourceModeActiveElements
from mtppy.suc_data_assembly import SUCActiveElement

from time import sleep
from simple_pid import PID


class AnaVlv(SUCActiveElement):
    def __init__(self, tag_name, tag_description='',
                 pos_min=0, pos_max=1000, pos_scl_min=0, pos_scl_max=1000, pos_unit=0,
                 open_fbk_calc=True, close_fbk_calc=True, pos_fbk_calc=True,
                 safe_pos=0, safe_pos_en=False, perm_en=False, intl_en=False, prot_en=False):
        """
        Analog Valve (AnaVlv). Parameter names correspond attribute names in VDI/VDE/NAMUR 2658.
        """
        super().__init__(tag_name, tag_description)

        self.op_src_mode = OperationSourceModeActiveElements()

        self.pos_min = pos_min
        self.pos_max = pos_max
        self.pos_scl_min = pos_scl_min
        self.pos_scl_max = pos_scl_max
        self.pos_unit = pos_unit
        self.open_fbk_calc = open_fbk_calc
        self.close_fbk_calc = close_fbk_calc
        self.pos_fbk_calc = pos_fbk_calc

        self.safe_pos = safe_pos
        self.safe_pos_en = safe_pos_en
        self.perm_en = perm_en
        self.intl_en = intl_en
        self.prot_en = prot_en

        self._add_attribute(Attribute('SafePos', bool, init_value=safe_pos))
        self._add_attribute(Attribute('SafePosEn', bool, init_value=self.safe_pos_en))
        self._add_attribute(Attribute('SafePosAct', bool, init_value=False))  # default value should be true?
        self._add_attribute(Attribute('OpenAut', bool, init_value=0, sub_cb=self.set_open_aut))
        self._add_attribute(Attribute('CloseAut', bool, init_value=0, sub_cb=self.set_close_aut))
        self._add_attribute(Attribute('OpenOp', bool, init_value=0, sub_cb=self.set_open_op))
        self._add_attribute(Attribute('CloseOp', bool, init_value=0, sub_cb=self.set_close_op))
        self._add_attribute(Attribute('OpenAct', bool, init_value=0))
        self._add_attribute(Attribute('CloseAct', bool, init_value=0))
        self._add_attribute(Attribute('PosSclMin', float, init_value=self.pos_scl_min))
        self._add_attribute(Attribute('PosSclMax', float, init_value=self.pos_scl_max))
        self._add_attribute(Attribute('PosUnit', int, init_value=self.pos_unit))
        self._add_attribute(Attribute('PosMin', float, init_value=self.pos_min))
        self._add_attribute(Attribute('PosMax', float, init_value=self.pos_max))
        self._add_attribute(Attribute('PosInt', float, init_value=0, sub_cb=self.set_pos_int))
        self._add_attribute(Attribute('PosMan', float, init_value=0, sub_cb=self.set_pos_man))
        self._add_attribute(Attribute('PosRbk', float, init_value=pos_min))
        self._add_attribute(Attribute('Pos', float, init_value=pos_min))
        self._add_attribute(Attribute('OpenFbkCalc', bool, init_value=open_fbk_calc))
        self._add_attribute(Attribute('OpenFbk', bool, init_value=False))
        self._add_attribute(Attribute('CloseFbkCalc', bool, init_value=close_fbk_calc))
        self._add_attribute(Attribute('CloseFbk', bool, init_value=False))
        self._add_attribute(Attribute('PosFbkCalc', bool, init_value=pos_fbk_calc))
        self._add_attribute(Attribute('PosFbk', float, init_value=pos_min))
        self._add_attribute(Attribute('PermEn', bool, init_value=perm_en))
        self._add_attribute(Attribute('Permit', bool, init_value=0))
        self._add_attribute(Attribute('IntlEn', bool, init_value=intl_en))
        self._add_attribute(Attribute('Interlock', bool, init_value=0))
        self._add_attribute(Attribute('ProtEn', bool, init_value=prot_en))
        self._add_attribute(Attribute('Protect', bool, init_value=0))
        self._add_attribute(Attribute('ResetOp', bool, init_value=0, sub_cb=self.set_reset_op))
        self._add_attribute(Attribute('ResetAut', bool, init_value=0, sub_cb=self.set_reset_aut))

    def _expect_save_pos(self):
        if self._run_allowed():
            self.attributes['SafePosAct'].set_value(False)
        else:
            if self.attributes['SafePosEn'].value:
                self._go_save_pos()
            else:  # hold position
                logging.debug('Device has no safe position')
            self.attributes['SafePosAct'].set_value(True)

    def _go_save_pos(self):
        if self.attributes['SafePos'].value == 1:
            self._run_open_vlv()
            safe_pos = self.attributes['PosMax'].value

        else:
            self._run_close_vlv()
            safe_pos = self.attributes['PosMin'].value

        self.attributes['Pos'].set_value(safe_pos)
        logging.debug('Pos set to safe position %s' % safe_pos)

        if self.attributes['PosFbkCalc'].value:
            self.attributes['PosFbk'].set_value(safe_pos)

    def set_open_aut(self, value: bool):
        logging.debug(f'OpenAut set to {value}')
        if self.op_src_mode.attributes['StateAutAct'].value:
            if value and self._run_allowed():
                self._run_open_vlv()

    def set_close_aut(self, value: bool):
        logging.debug(f'CloseAut set to {value}')
        if self.op_src_mode.attributes['StateAutAct'].value:
            if value and self._run_allowed():
                self._run_close_vlv()

    def set_reset_aut(self, value: bool):
        logging.debug(f'ResetAut set to {value}')
        if self.op_src_mode.attributes['StateAutAct'].value and value:
            self._reset_vlv()

    def set_open_op(self, value: bool):
        logging.debug(f'OpenOp set to {value}')
        if self.op_src_mode.attributes['StateOpAct'].value:
            if value and self._run_allowed():
                self._run_open_vlv()
                self.attributes['OpenOp'].value = False

    def set_close_op(self, value: bool):
        logging.debug(f'CloseOp set to {value}')
        if self.op_src_mode.attributes['StateOpAct'].value:
            if value and self._run_allowed():
                self._run_close_vlv()
                self.attributes['CloseOp'].value = False

    def set_reset_op(self, value: bool):
        logging.debug(f'ResetOp set to {value}')
        if self.op_src_mode.attributes['StateOpAct'].value and value:
            self._reset_vlv()
            self.attributes['ResetOp'].set_value(False)

    def _run_allowed(self):
        if self.attributes['PermEn'].value and self.attributes['Permit'].value == 0:
            logging.debug(f'Permission is not given')
            return False
        if self.attributes['IntlEn'].value and self.attributes['Interlock'].value == 0:
            logging.debug(f'Interlock is active')
            return False
        if self.attributes['ProtEn'].value and self.attributes['Protect'].value == 0:
            logging.debug(f'Protect is active')
            return False
        return True

    def _run_open_vlv(self):
        self.attributes['OpenAct'].set_value(True)
        if self.attributes['OpenFbkCalc']:
            self.attributes['OpenFbk'].set_value(True)
        self.attributes['CloseAct'].set_value(False)
        if self.attributes['CloseFbkCalc']:
            self.attributes['CloseFbk'].set_value(False)

    def _run_close_vlv(self):
        self.attributes['OpenAct'].set_value(False)
        if self.attributes['OpenFbkCalc']:
            self.attributes['OpenFbk'].set_value(False)
        self.attributes['CloseAct'].set_value(True)
        if self.attributes['CloseFbkCalc']:
            self.attributes['CloseFbk'].set_value(True)

    def _reset_vlv(self):
        if self.attributes['ProtEn'].value and self.attributes['Protect'].value == 0:
            self.attributes['Protect'].set_value(True)
            self.attributes['SafePosAct'].set_value(False)
        self.attributes['OpenAct'].set_value(False)
        if self.attributes['OpenFbkCalc']:
            self.attributes['OpenFbk'].set_value(False)
        self.attributes['CloseAct'].set_value(False)
        if self.attributes['CloseFbkCalc']:
            self.attributes['CloseFbk'].set_value(False)

    def set_pos_int(self, value: float):
        logging.debug(f'PosInt set to {value}')
        if self.op_src_mode.attributes['SrcIntAct'].value:
            self._set_pos(value)

    def set_pos_man(self, value: float):
        logging.debug(f'PosMan set to {value}')
        if self.op_src_mode.attributes['SrcManAct'].value:
            self._set_pos(value)

    def _correct_value(self, value: float):
        if value > self.pos_max:
            return self.pos_max
        elif value < self.pos_min:
            return self.pos_min
        else:
            return value

    def valid_value(self, value: float):
        if value < self.pos_min or value > self.pos_max:
            return False
        else:
            return True

    def _set_pos(self, value: float):
        if not self._run_allowed():
            logging.debug('No position change is allowed')
            return

        if self.valid_value(value):
            # if SafePosAct is inactive -> manual or internal position specification
            if self.attributes['OpenAct'].value and not self.attributes['SafePosAct'].value:
                value = value
            elif self.attributes['CloseAct'].value and not self.attributes['SafePosAct'].value:
                value = self.attributes['PosMin'].value

            # if SafePosAct is active, safety setting for the position is accepted
            elif self.attributes['SafePosAct'].value or \
                    (self.attributes['PermEn'].value and self.attributes['Permit'].value == 0):
                logging.debug('manual or internal position specification inactive')
                return

            self.attributes['Pos'].set_value(value)
            logging.debug('Pos set to %s' % value)
            if self.attributes['PosFbkCalc'].value:
                self.attributes['PosFbk'].set_value(value)
        else:
            logging.debug('Pos cannot be set to %s (out of range)' % value)

    def set_pos_rbk(self, value: float):
        corr_value = self._correct_value(value)
        self.attributes['PosRbk'].set_value(corr_value)
        logging.debug(f'PosRbk set to {value}')

    def set_pos_fbk(self, value: float):
        if not self.attributes['PosFbkCalc'].value:
            corr_value = self._correct_value(value)
            self.attributes['PosFbk'].set_value(corr_value)
            logging.debug(f'PosFbk set to {value}')

    def set_open_fbk(self, value: bool):
        if not self.attributes['OpenFbkCalc'].value:
            self.attributes['OpenFbk'].set_value(value)
            logging.debug(f'OpenFbk set to {value}')

    def set_close_fbk(self, value: bool):
        if not self.attributes['CloseFbkCalc'].value:
            self.attributes['CloseFbk'].set_value(value)
            logging.debug(f'CloseFbk set to {value}')

    def set_permit(self, value: bool):
        if not self.attributes['PermEn'].value:
            value = True
        self.attributes['Permit'].set_value(value)
        logging.debug('Permit set to %s' % value)
        self.attributes['SafePosAct'].set_value(False)  # safety position should not be activated for permit mode

    def set_interlock(self, value: bool):
        if not self.attributes['IntlEn'].value:
            value = True
        self.attributes['Interlock'].set_value(value)
        logging.debug('Interlock set to %s' % value)
        self._expect_save_pos()

    def set_protect(self, value: bool):
        if not self.attributes['ProtEn'].value:
            value = True
        if value:
            self._reset_vlv()
        self.attributes['Protect'].set_value(value)
        logging.debug('Protect set to %s' % value)
        self._expect_save_pos()

    def get_pos(self):
        return self.attributes['Pos'].value

    def get_pos_rbk(self):
        return self.attributes['PosRbk'].value

    def get_pos_fbk(self):
        return self.attributes['PosFbk'].value

    def get_open_fbk(self):
        return self.attributes['OpenFbk'].value

    def get_close_fbk(self):
        return self.attributes['CloseFbk'].value


class MonAnaVlvValues:
    def __init__(self, open_aut, open_op, close_aut, close_op, reset_aut, reset_op, pos):
        self.open_aut = open_aut
        self.open_op = open_op
        self.close_aut = close_aut
        self.close_op = close_op
        self.reset_aut = reset_aut
        self.reset_op = reset_op
        self.pos = pos
        self.lock = threading.Lock()
        self.stop_event_lock = threading.Event()


class MonAnaVlv(AnaVlv):
    def __init__(self, tag_name, tag_description='', pos_min=0, pos_max=1000, pos_scl_min=0, pos_scl_max=1000,
                 pos_unit=0, open_fbk_calc=True, close_fbk_calc=True, pos_fbk_calc=True, safe_pos=0,
                 safe_pos_en=False, perm_en=False, intl_en=False, prot_en=False, mon_en=True, mon_safe_pos=True,
                 mon_stat_ti=1, mon_dyn_ti=1, pos_tolerance=1, mon_pos_ti=1):
        super().__init__(tag_name, tag_description, pos_min, pos_max, pos_scl_min, pos_scl_max, pos_unit, open_fbk_calc,
                         close_fbk_calc, pos_fbk_calc, safe_pos, safe_pos_en, perm_en, intl_en, prot_en)

        self.mon_en = mon_en
        self.mon_safe_pos = mon_safe_pos
        self.mon_stat_ti = mon_stat_ti
        self.mon_dyn_ti = mon_dyn_ti
        self.pos_tolerance = pos_tolerance
        self.mon_pos_ti = mon_pos_ti

        self._add_attribute(Attribute('MonEn', bool, init_value=mon_en))
        self._add_attribute(Attribute('MonSafePos', bool, init_value=mon_safe_pos))
        self._add_attribute(Attribute('MonStatErr', bool, init_value=False))
        self._add_attribute(Attribute('MonDynErr', bool, init_value=False))
        self._add_attribute(Attribute('MonStatTi', float, init_value=mon_stat_ti))
        self._add_attribute(Attribute('MonDynTi', float, init_value=mon_dyn_ti))
        self._add_attribute(Attribute('PosReachedFbk', bool, init_value=False))
        self._add_attribute(Attribute('PosTolerance', float, init_value=pos_tolerance))
        self._add_attribute(Attribute('MonPosTi', float, init_value=mon_pos_ti))
        self._add_attribute(Attribute('MonPosErr', bool, init_value=False))
        self.monitored_values = MonAnaVlvValues(self.attributes['OpenAut'].value, self.attributes['OpenOp'].value,
                                                self.attributes['CloseAut'].value, self.attributes['CloseOp'].value,
                                                self.attributes['ResetAut'].value, self.attributes['ResetOp'].value,
                                                self.attributes['Pos'].value)
        self.monitor_static_thread = None
        self.monitor_dynamic_thread = None
        self.monitor_pos_thread = None

    def _go_save_pos(self):
        if self.attributes['SafePos'].value == 1:
            self._run_open_vlv()
            safe_pos = self.attributes['PosMax'].value

        else:
            self._run_close_vlv()
            safe_pos = self.attributes['PosMin'].value

        self.attributes['Pos'].set_value(safe_pos)
        logging.debug('Pos set to safe position %s' % safe_pos)
        if self.attributes['MonEn'].value:
            self.monitored_values.pos = safe_pos
            self.monitor_pos_thread = threading.Thread(target=self.monitor_position_reached)
            self.monitor_pos_thread.start()

        if self.attributes['PosFbkCalc'].value:
            if self.attributes['MonEn'].value:
                self.monitored_values.lock.acquire()
                self.attributes['PosFbk'].set_value(safe_pos)
                self.monitored_values.lock.release()
            else:
                self.attributes['PosFbk'].set_value(safe_pos)

    def compare_states_control_signals(self, monitor_time):
        """
        compare states of valve and control signals
        :param monitor_time: MonStatTi or MonDynTi times
        :return: results of states and control signals comparisons (a list including True or False)
        """
        self.monitored_values.lock.acquire()
        open_fbk1 = self.attributes['OpenFbk'].value
        close_fbk1 = self.attributes['CloseFbk'].value
        open_op1 = self.monitored_values.open_op
        open_aut1 = self.monitored_values.open_aut
        close_op1 = self.monitored_values.close_op
        close_aut1 = self.monitored_values.close_aut
        reset_op1 = self.monitored_values.reset_op
        reset_aut1 = self.monitored_values.reset_aut
        self.monitored_values.lock.release()

        sleep(monitor_time)

        self.monitored_values.lock.acquire()
        open_fbk2 = self.attributes['OpenFbk'].value
        close_fbk2 = self.attributes['CloseFbk'].value
        open_op2 = self.monitored_values.open_op
        open_aut2 = self.monitored_values.open_aut
        close_op2 = self.monitored_values.close_op
        close_aut2 = self.monitored_values.close_aut
        reset_op2 = self.monitored_values.reset_op
        reset_aut2 = self.monitored_values.reset_aut
        self.monitored_values.lock.release()

        control_signals_comparison = [open_op1 == open_op2, open_aut1 == open_aut2, close_op1 == close_op2,
                                      close_aut1 == close_aut2, reset_op1 == reset_op2, reset_aut1 == reset_aut2]
        state_comparison = [open_fbk1 == open_fbk2, close_fbk1 == close_fbk2]

        return state_comparison, control_signals_comparison

    def monitor_static_error(self):
        """
        monitor static error
        """
        while True:
            if self.monitored_values.stop_event_lock.is_set():
                logging.debug('static monitoring stopped')
                break
            states, control_signals = self.compare_states_control_signals(self.attributes['MonStatTi'].value)

            if not all(states):  # if the states of valve changed
                if all(control_signals):  # but the control signals did not change
                    self.attributes['MonStatErr'].set_value(True)
                    logging.debug('Static error set to True')
                    self._handle_monitored_error()

    def monitor_dynamic_error(self):
        """
        monitor dynamic error
        """
        while True:
            if self.monitored_values.stop_event_lock.is_set():
                logging.debug('dynamic monitoring stopped')
                break
            states, control_signals = self.compare_states_control_signals(self.attributes['MonDynTi'].value)

            if all(states):  # if the states of valve did not changed
                if not all(control_signals):  # but a control command is executed
                    self.attributes['MonDynErr'].set_value(True)
                    logging.debug('Dynamic error set to True')
                    self._handle_monitored_error()

    def monitor_position_reached(self):
        """
        monitor postion error
        """
        pos = self.monitored_values.pos
        sleep(self.attributes['MonPosTi'].value)
        PosReachedFbk = abs(self.attributes['PosFbk'].value - pos) <= self.pos_tolerance
        self.attributes['PosReachedFbk'].set_value(PosReachedFbk)
        if not PosReachedFbk:
            self.attributes['MonPosErr'].set_value(True)
            logging.debug('position error set to True')
            self._handle_monitored_error()

    def _handle_monitored_error(self):
        if self.attributes['MonSafePos']:
            logging.debug('set valve to safety position')
            if self.attributes['SafePosEn'].value:
                self._go_save_pos()
            else:
                logging.debug('Device has no safe position')
            self.attributes['SafePosAct'].set_value(True)

    def start_monitor(self):
        if self.attributes['MonEn'].value:
            self.monitor_static_thread = threading.Thread(target=self.monitor_static_error)
            self.monitor_static_thread.start()
            logging.debug('static monitoring start')
            self.monitor_dynamic_thread = threading.Thread(target=self.monitor_dynamic_error)
            self.monitor_dynamic_thread.start()
            logging.debug('dynamic monitoring start')

    def set_open_aut(self, value: bool):
        logging.debug('OpenAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value:
            if value and self._run_allowed():
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.open_aut = value
                    self.monitored_values.lock.release()
                self._run_open_vlv()

    def set_close_aut(self, value: bool):
        if self.op_src_mode.attributes['StateAutAct'].value:
            if value and self._run_allowed():
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.close_aut = value
                    self.monitored_values.lock.release()
                logging.debug('CloseAut set to %s' % value)
                self._run_close_vlv()

    def set_reset_aut(self, value: bool):
        logging.debug('ResetAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and value:
            if self.attributes['MonEn'].value:
                self.monitored_values.lock.acquire()
                self.monitored_values.reset_aut = value
                self.monitored_values.lock.release()
            self._reset_vlv()

    def set_open_op(self, value: bool):
        logging.debug('OpenOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value:
            if value and self._run_allowed():
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.open_op = value
                    self.monitored_values.lock.release()
                self._run_open_vlv()
                self.attributes['OpenOp'].value = False

    def set_close_op(self, value: bool):
        logging.debug('CloseOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value:
            if value and self._run_allowed():
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.close_op = value
                    self.monitored_values.lock.release()
                self._run_close_vlv()
                self.attributes['CloseOp'].value = False

    def set_reset_op(self, value: bool):
        logging.debug('ResetOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and value:
            if self.attributes['MonEn'].value:
                self.monitored_values.lock.acquire()
                self.monitored_values.reset_op = value
                self.monitored_values.lock.release()
            self._reset_vlv()
            self.attributes['ResetOp'].set_value(False)

    def _set_pos(self, value: float):
        if self.valid_value(value):
            # if SafePosAct is inactive -> manual or internal position specification
            if self.attributes['OpenAct'].value and not self.attributes['SafePosAct'].value:
                value = value
            elif self.attributes['CloseAct'].value and not self.attributes['SafePosAct'].value:
                value = self.attributes['PosMin'].value

            # if SafePosAct is active, safety setting for the position is accepted
            elif self.attributes['SafePosAct'].value or \
                    (self.attributes['PermEn'].value and self.attributes['Permit'].value == 0):
                logging.debug('manual or internal position specification inactive')
                return

            self.attributes['Pos'].set_value(value)
            logging.debug('Pos set to %s' % value)

            # start monitor_pos_thread to after pos has been changed
            # if the position dose not change, there is no need to check the desired position
            if self.attributes['MonEn'].value:
                self.monitored_values.pos = value
                self.monitor_pos_thread = threading.Thread(target=self.monitor_position_reached)
                self.monitor_pos_thread.start()

            if self.attributes['PosFbkCalc'].value:
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.attributes['PosFbk'].set_value(value)
                    self.monitored_values.lock.release()
                else:
                    self.attributes['PosFbk'].set_value(value)
        else:
            logging.debug('Pos cannot be set to %s (out of range)' % value)

    def set_stop_monitor(self):
        self.monitored_values.stop_event_lock.set()


class BinVlv(SUCActiveElement):
    def __init__(self, tag_name: str, tag_description: str = '', open_fbk_calc: bool = True,
                 close_fbk_calc: bool = True,
                 safe_pos: int = 0, safe_pos_en: bool = False, perm_en: bool = False, intl_en: bool = False,
                 prot_en: bool = False):
        """
        Binary Valve (BinVlv). Parameter names correspond attribute names in VDI/VDE/NAMUR 2658.
        """

        super().__init__(tag_name, tag_description)

        self.op_src_mode = OperationSourceModeActiveElements()

        self.open_fbk_calc = open_fbk_calc
        self.close_fbk_calc = close_fbk_calc

        self.safe_pos = safe_pos
        self.safe_pos_en = safe_pos_en
        self.perm_en = perm_en
        self.intl_en = intl_en
        self.prot_en = prot_en

        self._add_attribute(Attribute('SafePos', bool, init_value=safe_pos))
        self._add_attribute(Attribute('SafePosEn', bool, init_value=self.safe_pos_en))
        self._add_attribute(Attribute('SafePosAct', bool, init_value=False))  # default value should be true?
        self._add_attribute(Attribute('OpenOp', bool, init_value=0, sub_cb=self.set_open_op))
        self._add_attribute(Attribute('CloseOp', bool, init_value=0, sub_cb=self.set_close_op))
        self._add_attribute(Attribute('OpenAut', bool, init_value=0, sub_cb=self.set_open_aut))
        self._add_attribute(Attribute('CloseAut', bool, init_value=0, sub_cb=self.set_close_aut))
        self._add_attribute(Attribute('Ctrl', bool, init_value=0))
        self._add_attribute(Attribute('OpenFbkCalc', bool, init_value=open_fbk_calc))
        self._add_attribute(Attribute('OpenFbk', bool, init_value=False))
        self._add_attribute(Attribute('CloseFbkCalc', bool, init_value=close_fbk_calc))
        self._add_attribute(Attribute('CloseFbk', bool, init_value=False))
        self._add_attribute(Attribute('PermEn', bool, init_value=perm_en))
        self._add_attribute(Attribute('Permit', bool, init_value=0))
        self._add_attribute(Attribute('IntlEn', bool, init_value=intl_en))
        self._add_attribute(Attribute('Interlock', bool, init_value=0))
        self._add_attribute(Attribute('ProtEn', bool, init_value=prot_en))
        self._add_attribute(Attribute('Protect', bool, init_value=0))
        self._add_attribute(Attribute('ResetOp', bool, init_value=0, sub_cb=self.set_reset_op))
        self._add_attribute(Attribute('ResetAut', bool, init_value=0, sub_cb=self.set_reset_aut))

    def _expect_save_pos(self):
        if self._run_allowed():
            self.attributes['SafePosAct'].set_value(False)
        else:
            if self.attributes['SafePosEn'].value:
                self._go_safe_pos()
            else:
                logging.debug('Device has no safe position')
            self.attributes['SafePosAct'].set_value(True)

    def _go_safe_pos(self):
        if self.attributes['SafePos'].value:
            self._run_open_vlv()
        else:
            self._run_close_vlv()

    def set_open_aut(self, value: bool):
        logging.debug('OpenAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value:
            if value and self._run_allowed():
                self._run_open_vlv()

    def set_close_aut(self, value: bool):
        logging.debug('CloseAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value:
            if value and self._run_allowed():
                self._run_close_vlv()

    def set_reset_aut(self, value: bool):
        logging.debug('ResetAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and value:
            self._reset_vlv()

    def set_open_op(self, value: bool):
        logging.debug('OpenOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value:
            if value and self._run_allowed():
                self._run_open_vlv()
                self.attributes['OpenOp'].value = False

    def set_close_op(self, value: bool):
        logging.debug('CloseOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value:
            if value and self._run_allowed():
                self._run_close_vlv()
                self.attributes['CloseOp'].value = False

    def set_reset_op(self, value: bool):
        logging.debug('ResetOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and value:
            self._reset_vlv()
            self.attributes['ResetOp'].set_value(False)

    def _run_allowed(self):
        if self.attributes['PermEn'].value and self.attributes['Permit'].value == 0:
            logging.debug('Permission is not given')
            return False
        if self.attributes['IntlEn'].value and self.attributes['Interlock'].value == 0:
            logging.debug('Interlock is active')
            return False
        if self.attributes['ProtEn'].value and self.attributes['Protect'].value == 0:
            logging.debug('Protect is active')
            return False
        return True

    def _run_open_vlv(self):
        self.attributes['Ctrl'].set_value(True)
        if self.attributes['OpenFbkCalc']:
            self.attributes['OpenFbk'].set_value(True)

        if self.attributes['CloseFbkCalc']:
            self.attributes['CloseFbk'].set_value(False)

    def _run_close_vlv(self):
        self.attributes['Ctrl'].set_value(False)
        if self.attributes['OpenFbkCalc']:
            self.attributes['OpenFbk'].set_value(False)

        if self.attributes['CloseFbkCalc']:
            self.attributes['CloseFbk'].set_value(True)

    def _reset_vlv(self):
        if self.attributes['ProtEn'].value and self.attributes['Protect'].value == 0:
            self.attributes['Protect'].set_value(True)

        if self.attributes['SafePosEn'].value:
            self.attributes['SafePosAct'].set_value(False)

        self.attributes['Ctrl'].set_value(False)
        if self.attributes['OpenFbkCalc']:
            self.attributes['OpenFbk'].set_value(False)

        if self.attributes['CloseFbkCalc']:
            self.attributes['CloseFbk'].set_value(False)

    def set_open_fbk(self, value: bool):
        if not self.attributes['OpenFbkCalc'].value:
            self.attributes['OpenFbk'].set_value(value)
            logging.debug('OpenFbk set to %s' % value)

    def set_close_fbk(self, value: bool):
        if not self.attributes['CloseFbkCalc'].value:
            self.attributes['CloseFbk'].set_value(value)
            logging.debug('CloseFbk set to %s' % value)

    def set_permit(self, value: bool):
        if not self.attributes['PermEn'].value:
            value = True
        self.attributes['Permit'].set_value(value)
        logging.debug('Permit set to %s' % value)
        self.attributes['SafePosAct'].set_value(False)

    def set_interlock(self, value: bool):
        if not self.attributes['IntlEn'].value:
            value = True
        self.attributes['Interlock'].set_value(value)
        logging.debug('Interlock set to %s' % value)
        self._expect_save_pos()

    def set_protect(self, value: bool):
        if not self.attributes['ProtEn'].value:
            value = True
        if value:
            self._reset_vlv()
        self.attributes['Protect'].set_value(value)
        logging.debug('Protect set to %s' % value)
        self._expect_save_pos()

    def get_open_fbk(self):
        return self.attributes['OpenFbk'].value

    def get_close_fbk(self):
        return self.attributes['CloseFbk'].value


class MonBinVlvValues:
    def __init__(self, open_aut, open_op, close_aut, close_op, reset_aut, reset_op):
        self.open_aut = open_aut
        self.open_op = open_op
        self.close_aut = close_aut
        self.close_op = close_op
        self.reset_aut = reset_aut
        self.reset_op = reset_op
        self.lock = threading.Lock()
        self.stop_event_lock = threading.Event()


class MonBinVlv(BinVlv):
    def __init__(self, tag_name, tag_description='', open_fbk_calc=True, close_fbk_calc=True,
                 safe_pos=0, safe_pos_en=False, perm_en=False, intl_en=False, prot_en=False,
                 mon_en=True, mon_safe_pos=True, mon_stat_ti=1, mon_dyn_ti=1):
        super().__init__(tag_name, tag_description, open_fbk_calc, close_fbk_calc, safe_pos, safe_pos_en, perm_en,
                         intl_en, prot_en)

        self.mon_en = mon_en
        self.mon_safe_pos = mon_safe_pos
        self.mon_stat_ti = mon_stat_ti
        self.mon_dyn_ti = mon_dyn_ti

        self._add_attribute(Attribute('MonEn', bool, init_value=mon_en))
        self._add_attribute(Attribute('MonSafePos', bool, init_value=mon_safe_pos))
        self._add_attribute(Attribute('MonStatErr', bool, init_value=False))
        self._add_attribute(Attribute('MonDynErr', bool, init_value=False))
        self._add_attribute(Attribute('MonStatTi', float, init_value=mon_stat_ti))
        self._add_attribute(Attribute('MonDynTi', float, init_value=mon_dyn_ti))
        self.monitored_values = MonBinVlvValues(self.attributes['OpenAut'].value, self.attributes['OpenOp'].value,
                                                self.attributes['CloseAut'].value, self.attributes['CloseOp'].value,
                                                self.attributes['ResetAut'].value, self.attributes['ResetOp'].value)
        self.monitor_static_thread = None
        self.monitor_dynamic_thread = None

    def compare_states_control_signals(self, monitor_time):
        """
        compare states of valve and control signals
        :param monitor_time: MonStatTi or MonDynTi times
        :return: results of states and control signals comparisons (a list including True or False)
        """
        self.monitored_values.lock.acquire()
        open_fbk1 = self.attributes['OpenFbk'].value
        close_fbk1 = self.attributes['CloseFbk'].value
        open_op1 = self.monitored_values.open_op
        open_aut1 = self.monitored_values.open_aut
        close_op1 = self.monitored_values.close_op
        close_aut1 = self.monitored_values.close_aut
        reset_op1 = self.monitored_values.reset_op
        reset_aut1 = self.monitored_values.reset_aut
        self.monitored_values.lock.release()

        sleep(monitor_time)

        self.monitored_values.lock.acquire()
        open_fbk2 = self.attributes['OpenFbk'].value
        close_fbk2 = self.attributes['CloseFbk'].value
        open_op2 = self.monitored_values.open_op
        open_aut2 = self.monitored_values.open_aut
        close_op2 = self.monitored_values.close_op
        close_aut2 = self.monitored_values.close_aut
        reset_op2 = self.monitored_values.reset_op
        reset_aut2 = self.monitored_values.reset_aut
        self.monitored_values.lock.release()

        control_signals_comparison = [open_op1 == open_op2, open_aut1 == open_aut2, close_op1 == close_op2,
                                      close_aut1 == close_aut2, reset_op1 == reset_op2, reset_aut1 == reset_aut2]
        state_comparison = [open_fbk1 == open_fbk2, close_fbk1 == close_fbk2]
        return state_comparison, control_signals_comparison

    def monitor_static_error(self):
        """
        monitor static error
        """
        while True:
            if self.monitored_values.stop_event_lock.is_set():
                logging.debug('static monitoring stopped')
                break
            states, control_signals = self.compare_states_control_signals(self.attributes['MonStatTi'].value)

            if not all(states):  # if the states of valve changed
                if all(control_signals):  # but the control signals did not change
                    self.attributes['MonStatErr'].set_value(True)
                    logging.debug('Static error set to True')
                    self._handle_monitored_error()

    def monitor_dynamic_error(self):
        """
        monitor dynamic error
        """
        while True:
            if self.monitored_values.stop_event_lock.is_set():
                logging.debug('dynamic monitoring stopped')
                break
            states, control_signals = self.compare_states_control_signals(self.attributes['MonDynTi'].value)

            if all(states):  # if the states of valve did not changed
                if not all(control_signals):  # but a control command is executed
                    self.attributes['MonDynErr'].set_value(True)
                    logging.debug('Dynamic error set to True')
                    self._handle_monitored_error()

    def _handle_monitored_error(self):
        if self.attributes['MonSafePos']:
            logging.debug('set valve to safety position')
            if self.attributes['SafePosEn'].value:
                self._go_safe_pos()
            else:
                logging.debug('Device has no safe position')
            self.attributes['SafePosAct'].set_value(True)

    def start_monitor(self):
        """
        start static and dynamic error monitoring thread
        """
        if self.attributes['MonEn'].value:
            self.monitor_static_thread = threading.Thread(target=self.monitor_static_error)
            self.monitor_static_thread.start()
            logging.debug('static monitoring start')
            self.monitor_dynamic_thread = threading.Thread(target=self.monitor_dynamic_error)
            self.monitor_dynamic_thread.start()
            logging.debug('dynamic monitoring start')

    def set_open_aut(self, value: bool):
        logging.debug('OpenAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value:
            if value and self._run_allowed():
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.open_aut = value
                    self.monitored_values.lock.release()
                self._run_open_vlv()

    def set_close_aut(self, value: bool):
        if self.op_src_mode.attributes['StateAutAct'].value:
            if value and self._run_allowed():
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.close_aut = value
                    self.monitored_values.lock.release()
                logging.debug('CloseAut set to %s' % value)
                self._run_close_vlv()

    def set_reset_aut(self, value: bool):
        logging.debug('ResetAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and value:
            if self.attributes['MonEn'].value:
                self.monitored_values.lock.acquire()
                self.monitored_values.reset_aut = value
                self.monitored_values.lock.release()
            self._reset_vlv()

    def set_open_op(self, value: bool):
        logging.debug('OpenOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value:
            if value and self._run_allowed():
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.open_op = value
                    self.monitored_values.lock.release()
                self._run_open_vlv()
                self.attributes['OpenOp'].value = False

    def set_close_op(self, value: bool):
        logging.debug('CloseOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value:
            if value and self._run_allowed():
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.close_op = value
                    self.monitored_values.lock.release()
                self._run_close_vlv()
                self.attributes['CloseOp'].value = False

    def set_reset_op(self, value: bool):
        logging.debug('ResetOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and value:
            if self.attributes['MonEn'].value:
                self.monitored_values.lock.acquire()
                self.monitored_values.reset_op = value
                self.monitored_values.lock.release()
            self._reset_vlv()
            self.attributes['ResetOp'].set_value(False)

    def set_stop_monitor(self):
        self.monitored_values.stop_event_lock.set()


class BinDrv(SUCActiveElement):
    def __init__(self, tag_name, tag_description='', rev_fbk_calc=True, fwd_fbk_calc=True, safe_pos=0, fwd_en=True,
                 rev_en=False, perm_en=False, intl_en=False, prot_en=False):
        super().__init__(tag_name, tag_description)

        self.op_src_mode = OperationSourceModeActiveElements()

        self.rev_fbk_calc = rev_fbk_calc
        self.fwd_fbk_calc = fwd_fbk_calc

        self.safe_pos = safe_pos
        self.fwd_en = fwd_en
        self.rev_en = rev_en
        self.perm_en = perm_en
        self.intl_en = intl_en
        self.prot_en = prot_en

        self._add_attribute(Attribute('SafePos', bool, init_value=safe_pos))
        self._add_attribute(Attribute('SafePosAct', bool, init_value=False))  # default value should be true?
        self._add_attribute(Attribute('FwdEn', bool, init_value=fwd_en))
        self._add_attribute(Attribute('RevEn', bool, init_value=rev_en))
        self._add_attribute(Attribute('StopOp', bool, init_value=0, sub_cb=self.set_stop_op))
        self._add_attribute(Attribute('FwdOp', bool, init_value=0, sub_cb=self.set_fwd_op))
        self._add_attribute(Attribute('RevOp', bool, init_value=0, sub_cb=self.set_rev_op))
        self._add_attribute(Attribute('StopAut', bool, init_value=0, sub_cb=self.set_stop_aut))
        self._add_attribute(Attribute('FwdAut', bool, init_value=0, sub_cb=self.set_fwd_aut))
        self._add_attribute(Attribute('RevAut', bool, init_value=0, sub_cb=self.set_rev_aut))
        self._add_attribute(Attribute('FwdCtrl', bool, init_value=0))
        self._add_attribute(Attribute('RevCtrl', bool, init_value=0))
        self._add_attribute(Attribute('RevFbkCalc', bool, init_value=rev_fbk_calc))
        self._add_attribute(Attribute('RevFbk', bool, init_value=False))
        self._add_attribute(Attribute('FwdFbkCalc', bool, init_value=fwd_fbk_calc))
        self._add_attribute(Attribute('FwdFbk', bool, init_value=False))
        self._add_attribute(Attribute('Trip', bool, init_value=True))
        self._add_attribute(Attribute('PermEn', bool, init_value=perm_en))
        self._add_attribute(Attribute('Permit', bool, init_value=0))
        self._add_attribute(Attribute('IntlEn', bool, init_value=intl_en))
        self._add_attribute(Attribute('Interlock', bool, init_value=0))
        self._add_attribute(Attribute('ProtEn', bool, init_value=prot_en))
        self._add_attribute(Attribute('Protect', bool, init_value=0))
        self._add_attribute(Attribute('ResetOp', bool, init_value=0, sub_cb=self.set_reset_op))
        self._add_attribute(Attribute('ResetAut', bool, init_value=0, sub_cb=self.set_reset_aut))

    def _expect_save_pos(self):
        if self._run_allowed():
            self.attributes['SafePosAct'].set_value(False)
        else:
            self._go_safe_pos()
            self.attributes['SafePosAct'].set_value(True)

    def _go_safe_pos(self):
        if self.attributes['SafePos'].value:
            self._run_fwd_drv()
        else:
            self._stop_drv()

    def _run_allowed(self):
        if self.attributes['PermEn'].value and self.attributes['Permit'].value == 0:
            logging.debug('Permission is not given')
            return False
        if self.attributes['IntlEn'].value and self.attributes['Interlock'].value == 0:
            logging.debug('Interlock is active')
            return False
        if self.attributes['ProtEn'].value and self.attributes['Protect'].value == 0:
            logging.debug('Protect is active')
            return False
        if not self.attributes['Trip'].value:
            logging.debug('tripped')
            return False
        return True

    def set_fwd_op(self, value: bool):
        logging.debug('FwdOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and self.fwd_en:
            if value and self._run_allowed():
                self._run_fwd_drv()
                self.attributes['FwdOp'].value = False

    def set_rev_op(self, value: bool):
        logging.debug('RevOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and self.rev_en:
            if value and self._run_allowed():
                self._run_rev_drv()
                self.attributes['RevOp'].value = False

    def set_stop_op(self, value: bool):
        logging.debug('StopOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and value:
            self._stop_drv()
            self.attributes['StopOp'].set_value(False)

    def set_reset_op(self, value: bool):
        logging.debug('ResetOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and value:
            self._reset_drv()
            self.attributes['ResetOp'].set_value(False)

    def set_fwd_aut(self, value: bool):
        logging.debug('FwdAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and self.fwd_en:
            if value and self._run_allowed():
                self._run_fwd_drv()

    def set_rev_aut(self, value: bool):
        logging.debug('RevAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and self.rev_en:
            if value and self._run_allowed():
                self._run_rev_drv()

    def set_stop_aut(self, value: bool):
        logging.debug('StopAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and value:
            self._stop_drv()

    def set_reset_aut(self, value: bool):
        logging.debug('ResetAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and value:
            self._reset_drv()

    def _run_fwd_drv(self):
        self.attributes['FwdCtrl'].set_value(True)
        if self.attributes['FwdFbkCalc']:
            self.attributes['FwdFbk'].set_value(True)
        self.attributes['RevCtrl'].set_value(False)
        if self.attributes['RevFbkCalc']:
            self.attributes['RevFbk'].set_value(False)

    def _run_rev_drv(self):
        self.attributes['FwdCtrl'].set_value(False)
        if self.attributes['FwdFbkCalc']:
            self.attributes['FwdFbk'].set_value(False)
        self.attributes['RevCtrl'].set_value(True)
        if self.attributes['RevFbkCalc']:
            self.attributes['RevFbk'].set_value(True)

    def _stop_drv(self):
        self.attributes['FwdCtrl'].set_value(False)
        if self.attributes['FwdFbkCalc']:
            self.attributes['FwdFbk'].set_value(False)
        self.attributes['RevCtrl'].set_value(False)
        if self.attributes['RevFbkCalc']:
            self.attributes['RevFbk'].set_value(False)

    def _reset_drv(self):
        if self.attributes['ProtEn'].value and self.attributes['Protect'].value == 0:
            self.attributes['Protect'].set_value(True)
            self.attributes['SafePosAct'].set_value(False)
        self._stop_drv()

    def set_rev_fbk(self, value: bool):
        if not self.attributes['RevFbkCalc'].value:
            self.attributes['RevFbk'].set_value(value)
            logging.debug('RevFbk set to %s' % value)

    def set_fwd_fbk(self, value: bool):
        if not self.attributes['FwdFbkCalc'].value:
            self.attributes['FwdFbk'].set_value(value)
            logging.debug('FwdFbk set to %s' % value)

    def set_trip(self, value: bool):
        self.attributes['Trip'].set_value(value)
        logging.debug('Trip set to %s' % value)
        self._expect_save_pos()

    def set_permit(self, value: bool):
        if not self.attributes['PermEn'].value:
            value = True
        self.attributes['Permit'].set_value(value)
        logging.debug('Permit set to %s' % value)
        self.attributes['SafePosAct'].set_value(False)

    def set_interlock(self, value: bool):
        if not self.attributes['IntlEn'].value:
            value = True
        self.attributes['Interlock'].set_value(value)
        logging.debug('Interlock set to %s' % value)
        self._expect_save_pos()

    def set_protect(self, value: bool):
        if not self.attributes['ProtEn'].value:
            value = True
        if value:
            self._reset_drv()
        self.attributes['Protect'].set_value(value)
        logging.debug('Protect set to %s' % value)
        self._expect_save_pos()

    def get_fwd_fbk(self):
        return self.attributes['FwdFbk'].value

    def get_rev_fbk(self):
        return self.attributes['RevFbk'].value


class MonBinDrvValues:
    def __init__(self, fwd_aut, fwd_op, rev_aut, rev_op, stop_aut, stop_op, reset_aut, reset_op):
        self.fwd_aut = fwd_aut
        self.fwd_op = fwd_op
        self.rev_aut = rev_aut
        self.rev_op = rev_op
        self.stop_aut = stop_aut
        self.stop_op = stop_op
        self.reset_aut = reset_aut
        self.reset_op = reset_op
        self.lock = threading.Lock()
        self.stop_event_lock = threading.Event()


class MonBinDrv(BinDrv):
    def __init__(self, tag_name, tag_description, rev_fbk_calc=True, fwd_fbk_calc=True, safe_pos=0, fwd_en=True,
                 rev_en=False, perm_en=False, intl_en=False, prot_en=False, mon_en=True, mon_safe_pos=True,
                 mon_stat_ti=1, mon_dyn_ti=1):
        super().__init__(tag_name, tag_description, rev_fbk_calc, fwd_fbk_calc, safe_pos, fwd_en, rev_en, perm_en,
                         intl_en, prot_en)

        self.mon_en = mon_en
        self.mon_safe_pos = mon_safe_pos
        self.mon_stat_ti = mon_stat_ti
        self.mon_dyn_ti = mon_dyn_ti

        self._add_attribute(Attribute('MonEn', bool, init_value=mon_en))
        self._add_attribute(Attribute('MonSafePos', bool, init_value=mon_safe_pos))
        self._add_attribute(Attribute('MonStatErr', bool, init_value=False))
        self._add_attribute(Attribute('MonDynErr', bool, init_value=False))
        self._add_attribute(Attribute('MonStatTi', float, init_value=mon_stat_ti))
        self._add_attribute(Attribute('MonDynTi', float, init_value=mon_dyn_ti))
        self.monitored_values = MonBinDrvValues(self.attributes['FwdAut'].value, self.attributes['FwdOp'].value,
                                                self.attributes['RevAut'].value, self.attributes['RevOp'].value,
                                                self.attributes['StopAut'].value, self.attributes['StopOp'].value,
                                                self.attributes['ResetAut'].value, self.attributes['ResetOp'].value)
        self.monitor_static_thread = None
        self.monitor_dynamic_thread = None

    def compare_states_control_signals(self, monitor_time):

        self.monitored_values.lock.acquire()
        fwd_fbk1 = self.attributes['FwdFbk'].value
        rev_fbk1 = self.attributes['RevFbk'].value
        fwd_op1 = self.monitored_values.fwd_op
        fwd_aut1 = self.monitored_values.fwd_aut
        rev_op1 = self.monitored_values.rev_op
        rev_aut1 = self.monitored_values.rev_aut
        stop_op1 = self.monitored_values.stop_op
        stop_aut1 = self.monitored_values.stop_aut
        reset_op1 = self.monitored_values.reset_op
        reset_aut1 = self.monitored_values.reset_aut
        self.monitored_values.lock.release()

        sleep(monitor_time)

        self.monitored_values.lock.acquire()
        fwd_fbk2 = self.attributes['FwdFbk'].value
        rev_fbk2 = self.attributes['RevFbk'].value
        fwd_op2 = self.monitored_values.fwd_op
        fwd_aut2 = self.monitored_values.fwd_aut
        rev_op2 = self.monitored_values.rev_op
        rev_aut2 = self.monitored_values.rev_aut
        stop_op2 = self.monitored_values.stop_op
        stop_aut2 = self.monitored_values.stop_aut
        reset_op2 = self.monitored_values.reset_op
        reset_aut2 = self.monitored_values.reset_aut
        self.monitored_values.lock.release()

        control_signals_comparison = [fwd_op1 == fwd_op2, fwd_aut1 == fwd_aut2, rev_op1 == rev_op2,
                                      rev_aut1 == rev_aut2, stop_op1 == stop_op2, stop_aut1 == stop_aut2,
                                      reset_op1 == reset_op2, reset_aut1 == reset_aut2]
        state_comparison = [fwd_fbk1 == fwd_fbk2, rev_fbk1 == rev_fbk2]
        return state_comparison, control_signals_comparison

    def monitor_static_error(self):
        while True:
            if self.monitored_values.stop_event_lock.is_set():
                logging.debug('static monitoring stopped')
                break
            states, control_signals = self.compare_states_control_signals(self.attributes['MonStatTi'].value)

            if not all(states):
                if all(control_signals):
                    self.attributes['MonStatErr'].set_value(True)
                    logging.debug('Static error set to True')
                    self._handle_monitored_error()

    def monitor_dynamic_error(self):
        while True:
            if self.monitored_values.stop_event_lock.is_set():
                logging.debug('dynamic monitoring stopped')
                break
            states, control_signals = self.compare_states_control_signals(self.attributes['MonDynTi'].value)

            if all(states):
                if not all(control_signals):
                    self.attributes['MonDynErr'].set_value(True)
                    logging.debug('Dynamic error set to True')
                    self._handle_monitored_error()

    def _handle_monitored_error(self):
        logging.debug('set valve to safety position')
        self._go_safe_pos()
        self.attributes['SafePosAct'].set_value(True)

    def start_monitor(self):
        if self.attributes['MonEn'].value:
            self.monitor_static_thread = threading.Thread(target=self.monitor_static_error)
            self.monitor_static_thread.start()
            logging.debug('static monitoring start')
            self.monitor_dynamic_thread = threading.Thread(target=self.monitor_dynamic_error)
            self.monitor_dynamic_thread.start()
            logging.debug('dynamic monitoring start')

    def set_fwd_op(self, value: bool):
        logging.debug('FwdOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and self.fwd_en:
            if value and self._run_allowed():
                self._run_fwd_drv()
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.fwd_op = value
                    self.monitored_values.lock.release()
                self.attributes['FwdOp'].value = False

    def set_rev_op(self, value: bool):
        logging.debug('RevOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and self.rev_en:
            if value and self._run_allowed():

                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.rev_op = value
                    self.monitored_values.lock.release()
                self._run_rev_drv()
                self.attributes['RevOp'].value = False

    def set_stop_op(self, value: bool):
        logging.debug('StopOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and value:
            if self.attributes['MonEn'].value:
                self.monitored_values.lock.acquire()
                self.monitored_values.stop_op = value
                self.monitored_values.lock.release()
            self._stop_drv()
            self.attributes['StopOp'].set_value(False)

    def set_reset_op(self, value: bool):
        logging.debug('ResetOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and value:
            if self.attributes['MonEn'].value:
                self.monitored_values.lock.acquire()
                self.monitored_values.reset_op = value
                self.monitored_values.lock.release()
            self._reset_drv()
            self.attributes['ResetOp'].set_value(False)

    def set_fwd_aut(self, value: bool):
        logging.debug('FwdAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and self.fwd_en:
            if value and self._run_allowed():
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.fwd_aut = value
                    self.monitored_values.lock.release()
                self._run_fwd_drv()

    def set_rev_aut(self, value: bool):
        logging.debug('RevAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and self.rev_en:
            if value and self._run_allowed():
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.rev_aut = value
                    self.monitored_values.lock.release()
                self._run_rev_drv()

    def set_stop_aut(self, value: bool):
        logging.debug('StopAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and value:
            if self.attributes['MonEn'].value:
                self.monitored_values.lock.acquire()
                self.monitored_values.stop_aut = value
                self.monitored_values.lock.release()
            self._stop_drv()

    def set_reset_aut(self, value: bool):
        logging.debug('ResetAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and value:
            if self.attributes['MonEn'].value:
                self.monitored_values.lock.acquire()
                self.monitored_values.reset_aut = value
                self.monitored_values.lock.release()
            self._reset_drv()

    def set_stop_monitor(self):
        self.monitored_values.stop_event_lock.set()


class AnaDrv(SUCActiveElement):
    def __init__(self, tag_name: str, tag_description: str = '',
                 rpm_min: float = 0, rpm_max: float = 1000, rpm_scl_min: float = 0, rpm_scl_max: float = 1000,
                 rpm_unit: int = 0,
                 rev_fbk_calc: bool = True, fwd_fbk_calc: bool = True, rpm_fbk_calc: bool = True,
                 safe_pos: int = 0, fwd_en: bool = True, rev_en: bool = False, perm_en: bool = False,
                 intl_en: bool = False, prot_en: bool = False):
        """
        Analog Drive (AnaDrv). Parameter names correspond attribute names in VDI/VDE/NAMUR 2658.
        """
        super().__init__(tag_name, tag_description)

        self.op_src_mode = OperationSourceModeActiveElements()

        self.rpm_min = rpm_min
        self.rpm_max = rpm_max
        self.rpm_scl_min = rpm_scl_min
        self.rpm_scl_max = rpm_scl_max
        self.rpm_unit = rpm_unit
        self.rev_fbk_calc = rev_fbk_calc
        self.fwd_fbk_calc = fwd_fbk_calc
        self.rpm_fbk_calc = rpm_fbk_calc

        self.safe_pos = safe_pos
        self.fwd_en = fwd_en
        self.rev_en = rev_en
        self.perm_en = perm_en
        self.intl_en = intl_en
        self.prot_en = prot_en

        self._add_attribute(Attribute('SafePos', bool, init_value=safe_pos))
        self._add_attribute(Attribute('SafePosAct', bool, init_value=True))
        self._add_attribute(Attribute('FwdEn', bool, init_value=fwd_en))
        self._add_attribute(Attribute('RevEn', bool, init_value=rev_en))
        self._add_attribute(Attribute('StopOp', bool, init_value=0, sub_cb=self.set_stop_op))
        self._add_attribute(Attribute('FwdOp', bool, init_value=0, sub_cb=self.set_fwd_op))
        self._add_attribute(Attribute('RevOp', bool, init_value=0, sub_cb=self.set_rev_op))
        self._add_attribute(Attribute('StopAut', bool, init_value=0, sub_cb=self.set_stop_aut))
        self._add_attribute(Attribute('FwdAut', bool, init_value=0, sub_cb=self.set_fwd_aut))
        self._add_attribute(Attribute('RevAut', bool, init_value=0, sub_cb=self.set_rev_aut))
        self._add_attribute(Attribute('FwdCtrl', bool, init_value=0))
        self._add_attribute(Attribute('RevCtrl', bool, init_value=0))
        self._add_attribute(Attribute('RpmSclMin', float, init_value=self.rpm_scl_min))
        self._add_attribute(Attribute('RpmSclMax', float, init_value=self.rpm_scl_max))
        self._add_attribute(Attribute('RpmUnit', int, init_value=self.rpm_unit))
        self._add_attribute(Attribute('RpmMin', float, init_value=self.rpm_min))
        self._add_attribute(Attribute('RpmMax', float, init_value=self.rpm_max))
        self._add_attribute(Attribute('RpmInt', float, init_value=0, sub_cb=self.set_rpm_int))
        self._add_attribute(Attribute('RpmMan', float, init_value=0, sub_cb=self.set_rpm_man))
        self._add_attribute(Attribute('Rpm', float, init_value=rpm_min))
        self._add_attribute(Attribute('RpmRbk', float, init_value=rpm_min))
        self._add_attribute(Attribute('RevFbkCalc', bool, init_value=rev_fbk_calc))
        self._add_attribute(Attribute('RevFbk', bool, init_value=False))
        self._add_attribute(Attribute('FwdFbkCalc', bool, init_value=fwd_fbk_calc))
        self._add_attribute(Attribute('FwdFbk', bool, init_value=False))
        self._add_attribute(Attribute('RpmFbkCalc', bool, init_value=rpm_fbk_calc))
        self._add_attribute(Attribute('RpmFbk', float, init_value=rpm_min))
        self._add_attribute(Attribute('Trip', bool, init_value=True))
        self._add_attribute(Attribute('PermEn', bool, init_value=perm_en))
        self._add_attribute(Attribute('Permit', bool, init_value=0))
        self._add_attribute(Attribute('IntlEn', bool, init_value=intl_en))
        self._add_attribute(Attribute('Interlock', bool, init_value=0))
        self._add_attribute(Attribute('ProtEn', bool, init_value=prot_en))
        self._add_attribute(Attribute('Protect', bool, init_value=0))
        self._add_attribute(Attribute('ResetOp', bool, init_value=0, sub_cb=self.set_reset_op))
        self._add_attribute(Attribute('ResetAut', bool, init_value=0, sub_cb=self.set_reset_aut))

    def _expect_save_pos(self):
        if self._run_allowed():
            self.attributes['SafePosAct'].set_value(False)
        else:
            self._go_save_pos()
            self.attributes['SafePosAct'].set_value(True)

    def _go_save_pos(self):
        if self.attributes['SafePos'].value:
            self._run_fwd_drv()
        else:
            self._stop_drv()

    def _run_allowed(self):
        if self.attributes['PermEn'].value and self.attributes['Permit'].value == 0:
            logging.debug('Permission is not given')
            return False
        if self.attributes['IntlEn'].value and self.attributes['Interlock'].value == 0:
            logging.debug('Interlock is active')
            return False
        if self.attributes['ProtEn'].value and self.attributes['Protect'].value == 0:
            logging.debug('Protect is active')
            return False
        if not self.attributes['Trip'].value:
            logging.debug('Drive protection triggered')
            return False
        return True

    def set_fwd_op(self, value: bool):
        logging.debug('FwdOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and self.fwd_en:
            if value and self._run_allowed():
                self._run_fwd_drv()
                self.attributes['FwdOp'].value = False

    def set_rev_op(self, value: bool):
        logging.debug('RevOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and self.rev_en:
            if value and self._run_allowed():
                self._run_rev_drv()
                self.attributes['RevOp'].value = False

    def set_stop_op(self, value: bool):
        logging.debug('StopOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and value:
            self._stop_drv()
            self.attributes['StopOp'].set_value(False)

    def set_reset_op(self, value: bool):
        logging.debug('ResetOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and value:
            self._reset_drv()
            self.attributes['ResetOp'].set_value(False)

    def set_fwd_aut(self, value: bool):
        logging.debug('FwdAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and self.fwd_en:
            if value and self._run_allowed():
                self._run_fwd_drv()

    def set_rev_aut(self, value: bool):
        logging.debug('RevAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and self.rev_en:
            if value and self._run_allowed():
                self._run_rev_drv()

    def set_stop_aut(self, value: bool):
        logging.debug('StopAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and value:
            self._stop_drv()

    def set_reset_aut(self, value: bool):
        logging.debug('ResetAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and value:
            self._reset_drv()

    def _run_fwd_drv(self):
        self.attributes['FwdCtrl'].set_value(True)
        if self.attributes['FwdFbkCalc']:
            self.attributes['FwdFbk'].set_value(True)
        self.attributes['RevCtrl'].set_value(False)
        if self.attributes['RevFbkCalc']:
            self.attributes['RevFbk'].set_value(False)

    def _run_rev_drv(self):
        self.attributes['FwdCtrl'].set_value(False)
        if self.attributes['FwdFbkCalc']:
            self.attributes['FwdFbk'].set_value(False)
        self.attributes['RevCtrl'].set_value(True)
        if self.attributes['RevFbkCalc']:
            self.attributes['RevFbk'].set_value(True)

    def _stop_drv(self):
        self.attributes['FwdCtrl'].set_value(False)
        if self.attributes['FwdFbkCalc']:
            self.attributes['FwdFbk'].set_value(False)
        self.attributes['RevCtrl'].set_value(False)
        if self.attributes['RevFbkCalc']:
            self.attributes['RevFbk'].set_value(False)

    def _reset_drv(self):
        if self.attributes['ProtEn'].value and self.attributes['Protect'].value == 0:
            self.attributes['Protect'].set_value(True)
            self.attributes['SafePosAct'].set_value(False)
        self._stop_drv()

    def set_rpm_int(self, value: float):
        logging.debug('RpmInt set to %s' % value)
        if self.op_src_mode.attributes['SrcIntAct'].value:
            self._set_rpm(value)

    def set_rpm_man(self, value: float):
        logging.debug('RpmIntMan set to %s' % value)
        if self.op_src_mode.attributes['SrcManAct'].value:
            self._set_rpm(value)

    def valid_value(self, value: float):
        if value < self.rpm_min or value > self.rpm_max:
            return False
        else:
            return True

    def _correct_value(self, value: float):
        if value > self.rpm_max:
            return self.rpm_max
        elif value < self.rpm_min:
            return self.rpm_min
        else:
            return value

    def _set_rpm(self, value: float):
        if self.valid_value(value):
            self.attributes['Rpm'].set_value(value)
            logging.debug('Rpm set to %s' % value)
            if self.attributes['RpmFbkCalc'].value:
                self.attributes['RpmFbk'].set_value(value)
        else:
            logging.debug('Rpm cannot be set to %s (out of range)' % value)

    def set_rpm_rbk(self, value: float):
        corr_value = self._correct_value(value)
        self.attributes['RpmRbk'].set_value(corr_value)
        logging.debug('RpmRbk set to %s' % corr_value)

    def set_rpm_fbk(self, value: float):
        if not self.attributes['RpmFbkCalc'].value:
            corr_value = self._correct_value(value)
            self.attributes['RpmFbk'].set_value(corr_value)
            logging.debug('RpmFbk set to %s' % corr_value)

    def set_rev_fbk(self, value: bool):
        if not self.attributes['RevFbkCalc'].value:
            self.attributes['RevFbk'].set_value(value)
            logging.debug('RevFbk set to %s' % value)

    def set_fwd_fbk(self, value: bool):
        if not self.attributes['FwdFbkCalc'].value:
            self.attributes['FwdFbk'].set_value(value)
            logging.debug('FwdFbk set to %s' % value)

    def set_trip(self, value: bool):
        self.attributes['Trip'].set_value(value)
        logging.debug('Trip set to %s' % value)
        self._expect_save_pos()

    def set_permit(self, value: bool):
        if not self.attributes['PermEn'].value:
            value = True
        self.attributes['Permit'].set_value(value)
        logging.debug('Permit set to %s' % value)
        self._expect_save_pos()

    def set_interlock(self, value: bool):
        if not self.attributes['IntlEn'].value:
            value = True
        self.attributes['Interlock'].set_value(value)
        logging.debug('Interlock set to %s' % value)
        self._expect_save_pos()

    def set_protect(self, value: bool):
        if not self.attributes['ProtEn'].value:
            value = True
        if value:
            self._reset_drv()
        self.attributes['Protect'].set_value(value)
        logging.debug('Protect set to %s' % value)
        self._expect_save_pos()

    def get_rpm(self):
        return self.attributes['Rpm'].value

    def get_rpm_rbk(self):
        return self.attributes['RpmRbk'].value

    def get_rpm_fbk(self):
        return self.attributes['RpmFbk'].value

    def get_fwd_fbk(self):
        return self.attributes['FwdFbk'].value

    def get_rev_fbk(self):
        return self.attributes['RevFbk'].value


class MonAnaDrvValues:
    def __init__(self, fwd_aut, fwd_op, rev_aut, rev_op, stop_aut, stop_op, reset_aut, reset_op, rpm):
        self.fwd_aut = fwd_aut
        self.fwd_op = fwd_op
        self.rev_aut = rev_aut
        self.rev_op = rev_op
        self.stop_aut = stop_aut
        self.stop_op = stop_op
        self.reset_aut = reset_aut
        self.reset_op = reset_op
        self.rpm = rpm
        self.lock = threading.Lock()
        self.stop_event_lock = threading.Event()


class MonAnaDrv(AnaDrv):
    def __init__(self, tag_name, tag_description, rpm_min=0, rpm_max=1000, rpm_scl_min=0, rpm_scl_max=1000, rpm_unit=0,
                 rev_fbk_calc=True, fwd_fbk_calc=True, rpm_fbk_calc=True, safe_pos=0, fwd_en=True, rev_en=False,
                 perm_en=False, intl_en=False, prot_en=False, mon_en=True, mon_safe_pos=True, mon_stat_ti=1,
                 mon_dyn_ti=1, rpm_ah_en=True, rpm_al_en=True, rpm_ah_lim=900, rpm_al_lim=50):
        super().__init__(tag_name, tag_description, rpm_min, rpm_max, rpm_scl_min, rpm_scl_max, rpm_unit, rev_fbk_calc,
                         fwd_fbk_calc, rpm_fbk_calc, safe_pos, fwd_en, rev_en, perm_en, intl_en, prot_en)

        self.mon_en = mon_en
        self.mon_safe_pos = mon_safe_pos
        self.mon_stat_ti = mon_stat_ti
        self.mon_dyn_ti = mon_dyn_ti
        self.rpm_ah_en = rpm_ah_en
        self.rpm_al_en = rpm_al_en
        self.rpm_ah_lim = rpm_ah_lim
        self.rpm_al_lim = rpm_ah_lim

        self._add_attribute(Attribute('MonEn', bool, init_value=mon_en))
        self._add_attribute(Attribute('MonSafePos', bool, init_value=mon_safe_pos))
        self._add_attribute(Attribute('MonStatErr', bool, init_value=False))
        self._add_attribute(Attribute('MonDynErr', bool, init_value=False))
        self._add_attribute(Attribute('MonStatTi', float, init_value=mon_stat_ti))
        self._add_attribute(Attribute('MonDynTi', float, init_value=mon_dyn_ti))
        self._add_attribute(Attribute('RpmErr', float, init_value=0))
        self._add_attribute(Attribute('RpmAHEn', bool, init_value=rpm_ah_en))
        self._add_attribute(Attribute('RpmALEn', bool, init_value=rpm_al_en))
        self._add_attribute(Attribute('RpmAHAct', bool, init_value=False))
        self._add_attribute(Attribute('RpmALAct', bool, init_value=False))
        self._add_attribute(Attribute('RpmAHLim', float, init_value=rpm_ah_lim))
        self._add_attribute(Attribute('RpmALLim', float, init_value=rpm_al_lim))
        self.monitored_values = MonAnaDrvValues(self.attributes['FwdAut'].value, self.attributes['FwdOp'].value,
                                                self.attributes['RevAut'].value, self.attributes['RevOp'].value,
                                                self.attributes['StopAut'].value, self.attributes['StopOp'].value,
                                                self.attributes['ResetAut'].value, self.attributes['ResetOp'].value,
                                                self.attributes['Rpm'].value)
        self.monitor_static_thread = None
        self.monitor_dynamic_thread = None
        self.monitor_rpm_error_thread = None
        self.monitor_rpm_limit_high_thread = None
        self.monitor_rpm_limit_low_thread = None

    def compare_states_control_signals(self, monitor_time):

        self.monitored_values.lock.acquire()
        fwd_ctrl1 = self.attributes['FwdFbk'].value
        rev_ctrl1 = self.attributes['RevFbk'].value
        fwd_op1 = self.monitored_values.fwd_op
        fwd_aut1 = self.monitored_values.fwd_aut
        rev_op1 = self.monitored_values.rev_op
        rev_aut1 = self.monitored_values.rev_aut
        stop_op1 = self.monitored_values.stop_op
        stop_aut1 = self.monitored_values.stop_aut
        reset_op1 = self.monitored_values.reset_op
        reset_aut1 = self.monitored_values.reset_aut
        self.monitored_values.lock.release()

        sleep(monitor_time)

        self.monitored_values.lock.acquire()
        fwd_ctrl2 = self.attributes['FwdFbk'].value
        rev_ctrl2 = self.attributes['RevFbk'].value
        fwd_op2 = self.monitored_values.fwd_op
        fwd_aut2 = self.monitored_values.fwd_aut
        rev_op2 = self.monitored_values.rev_op
        rev_aut2 = self.monitored_values.rev_aut
        stop_op2 = self.monitored_values.stop_op
        stop_aut2 = self.monitored_values.stop_aut
        reset_op2 = self.monitored_values.reset_op
        reset_aut2 = self.monitored_values.reset_aut
        self.monitored_values.lock.release()

        control_signals_comparison = [fwd_op1 == fwd_op2, fwd_aut1 == fwd_aut2, rev_op1 == rev_op2,
                                      rev_aut1 == rev_aut2, stop_op1 == stop_op2, stop_aut1 == stop_aut2,
                                      reset_op1 == reset_op2, reset_aut1 == reset_aut2]
        state_comparison = [fwd_ctrl1 == fwd_ctrl2, rev_ctrl1 == rev_ctrl2]
        return state_comparison, control_signals_comparison

    def monitor_static_error(self):
        while True:
            if self.monitored_values.stop_event_lock.is_set():
                logging.debug('static monitoring stopped')
                break
            states, control_signals = self.compare_states_control_signals(self.attributes['MonStatTi'].value)

            if not all(states):
                if all(control_signals):
                    self.attributes['MonStatErr'].set_value(True)
                    logging.debug('Static error set to True')
                    self._handle_monitored_error()

    def monitor_dynamic_error(self):
        while True:
            if self.monitored_values.stop_event_lock.is_set():
                logging.debug('dynamic monitoring stopped')
                break
            states, control_signals = self.compare_states_control_signals(self.attributes['MonDynTi'].value)

            if all(states):
                if not all(control_signals):
                    self.attributes['MonDynErr'].set_value(True)
                    logging.debug('Dynamic error set to True')
                    self._handle_monitored_error()

    def monitor_rpm_error(self):
        while True:
            if self.monitored_values.stop_event_lock.is_set():
                logging.debug('rpm monitoring stopped')
                break
            rpm_error = self.monitored_values.rpm - self.attributes['RpmFbk'].value
            if rpm_error:
                self.attributes['RpmErr'].set_value(rpm_error)
                logging.debug(f'Rpm error set to {rpm_error}')
                self._handle_monitored_error()

            sleep(0.01)

    def monitor_rpm_high_limit(self):
        while True:
            if self.monitored_values.stop_event_lock.is_set():
                logging.debug('rpm high limit monitoring stopped')
                break
            self.monitored_values.lock.acquire()
            high_limit_alarm = self.attributes['RpmFbk'].value > self.attributes['RpmAHLim'].value
            self.monitored_values.lock.release()
            if high_limit_alarm:
                self.attributes['RpmAHAct'].set_value(True)
                logging.debug('Rpm limit high set to True')
            sleep(0.01)

    def monitor_rpm_low_limit(self):
        while True:
            if self.monitored_values.stop_event_lock.is_set():
                logging.debug('rpm low limit monitoring stopped')
                break
            self.monitored_values.lock.acquire()
            low_limit_alarm = self.attributes['RpmFbk'].value < self.attributes['RpmALLim'].value
            self.monitored_values.lock.release()
            if low_limit_alarm:
                self.attributes['RpmALAct'].set_value(True)
                logging.debug('Rpm limit low set to True')
            sleep(0.01)

    def _handle_monitored_error(self):
        logging.debug('set valve to safety position')
        self._go_save_pos()
        self.attributes['SafePosAct'].set_value(True)

    def start_monitor(self):
        if self.attributes['MonEn'].value:
            self.monitor_static_thread = threading.Thread(target=self.monitor_static_error)
            self.monitor_static_thread.start()
            logging.debug('static monitoring start')

            self.monitor_dynamic_thread = threading.Thread(target=self.monitor_dynamic_error)
            self.monitor_dynamic_thread.start()
            logging.debug('dynamic monitoring start')

            self.monitor_rpm_error_thread = threading.Thread(target=self.monitor_rpm_error)
            self.monitor_rpm_error_thread.start()
            logging.debug('rpm error monitoring start')

        if self.attributes['RpmAHEn'].value:
            self.monitor_rpm_limit_high_thread = threading.Thread(target=self.monitor_rpm_high_limit)
            self.monitor_rpm_limit_high_thread.start()
            logging.debug('rpm high limit monitoring start')

        if self.attributes['RpmALEn'].value:
            self.monitor_rpm_limit_low_thread = threading.Thread(target=self.monitor_rpm_low_limit)
            self.monitor_rpm_limit_low_thread.start()
            logging.debug('rpm low limit monitoring start')

    def set_fwd_op(self, value: bool):
        logging.debug('FwdOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and self.fwd_en:
            if value and self._run_allowed():
                self._run_fwd_drv()
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.fwd_op = value
                    self.monitored_values.lock.release()
                self.attributes['FwdOp'].value = False

    def set_rev_op(self, value: bool):
        logging.debug('RevOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and self.rev_en:
            if value and self._run_allowed():

                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.rev_op = value
                    self.monitored_values.lock.release()
                self._run_rev_drv()
                self.attributes['RevOp'].value = False

    def set_stop_op(self, value: bool):
        logging.debug('StopOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and value:
            if self.attributes['MonEn'].value:
                self.monitored_values.lock.acquire()
                self.monitored_values.stop_op = value
                self.monitored_values.lock.release()
            self._stop_drv()
            self.attributes['StopOp'].set_value(False)

    def set_reset_op(self, value: bool):
        logging.debug('ResetOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and value:
            if self.attributes['MonEn'].value:
                self.monitored_values.lock.acquire()
                self.monitored_values.reset_op = value
                self.monitored_values.lock.release()
            self._reset_drv()
            self.attributes['ResetOp'].set_value(False)

    def set_fwd_aut(self, value: bool):
        logging.debug('FwdAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and self.fwd_en:
            if value and self._run_allowed():
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.fwd_aut = value
                    self.monitored_values.lock.release()
                self._run_fwd_drv()

    def set_rev_aut(self, value: bool):
        logging.debug('RevAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and self.rev_en:
            if value and self._run_allowed():
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.monitored_values.rev_aut = value
                    self.monitored_values.lock.release()
                self._run_rev_drv()

    def set_stop_aut(self, value: bool):
        logging.debug('StopAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and value:
            if self.attributes['MonEn'].value:
                self.monitored_values.lock.acquire()
                self.monitored_values.stop_aut = value
                self.monitored_values.lock.release()
            self._stop_drv()

    def set_reset_aut(self, value: bool):
        logging.debug('ResetAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and value:
            if self.attributes['MonEn'].value:
                self.monitored_values.lock.acquire()
                self.monitored_values.reset_aut = value
                self.monitored_values.lock.release()
            self._reset_drv()

    def _set_rpm(self, value: float):
        if self.valid_value(value):
            self.attributes['Rpm'].set_value(value)
            if self.attributes['MonEn'].value:
                self.monitored_values.lock.acquire()
                self.monitored_values.rpm = value
                self.monitored_values.lock.release()
            logging.debug('Rpm set to %s' % value)

            if self.attributes['RpmFbkCalc'].value:
                if self.attributes['MonEn'].value:
                    self.monitored_values.lock.acquire()
                    self.attributes['RpmFbk'].set_value(value)
                    self.monitored_values.lock.release()
                else:
                    self.attributes['RpmFbk'].set_value(value)

        else:
            logging.debug('Rpm cannot be set to %s (out of range)' % value)

    def set_stop_monitor(self):
        self.monitored_values.stop_event_lock.set()


class PIDController:
    def __init__(self, mv_init_value=0, kp=100, ki=10, kd=1, mv_min=0, mv_max=100, sample_time=0.1):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.mv_min = mv_min
        self.mv_max = mv_max
        self.sp = 0
        self.pv = 0
        self.mv = mv_init_value
        self.sample_time = sample_time

        self.ctrl = PID(Kp=self.kp, Ki=self.ki, Kd=self.kd, output_limits=(mv_min, mv_max), sample_time=sample_time)

        self.thread = threading.Thread(target=self.loop)
        self.stop_flag = True
        self.stopped = True

    def set_limits(self, mv_min, mv_max):
        self.ctrl.output_limits = (mv_min, mv_max)

    def start(self):
        logging.debug('Starting PID controller...')
        self.ctrl.setpoint = self.sp
        self.stopped = False
        self.stop_flag = False
        self.thread.start()
        logging.debug('Started')

    def stop(self):
        logging.debug('Stopping PID controller...')
        self.stopped = False
        self.stop_flag = True
        while not self.stopped:
            sleep(0.1)
        self.ctrl.reset()
        logging.debug('Stopped')

    def set_sp(self, sp):
        self.sp = sp
        self.ctrl.setpoint = sp

    def set_pv(self, pv):
        self.pv = pv

    def loop(self):
        while not self.stop_flag:
            self.mv = self.ctrl(self.pv)
            sleep(self.sample_time)
        self.stopped = True

    def get_mv(self):
        return self.mv

    def set_kp(self, kp):
        self.ctrl.Kp = kp

    def set_ki(self, ki):
        self.ctrl.Ki = ki

    def set_kd(self, kd):
        self.ctrl.Kd = kd


class PIDCtrl(SUCActiveElement):
    def __init__(self, tag_name, tag_description='',
                 pv_scl_min=0, pv_scl_max=100, pv_unit=0,
                 sp_scl_min=0, sp_scl_max=100, sp_unit=0,
                 sp_int_min=0, sp_int_max=100, sp_man_min=0, sp_man_max=100,
                 mv_min=0, mv_max=1000, mv_unit=0, mv_scl_min=0, mv_scl_max=100,
                 P=100, Ti=10, Td=1):
        super().__init__(tag_name, tag_description)

        self.op_src_mode = OperationSourceModeActiveElements()

        self.pv_scl_min = pv_scl_min
        self.pv_scl_max = pv_scl_max
        self.pv_unit = pv_unit
        self.sp_scl_min = sp_scl_min
        self.sp_scl_max = sp_scl_max
        self.sp_unit = sp_unit
        self.sp_int_min = sp_int_min
        self.sp_int_max = sp_int_max
        self.sp_man_min = sp_man_min
        self.sp_man_max = sp_man_max
        self.mv_min = mv_min
        self.mv_max = mv_max
        self.mv_unit = mv_unit
        self.mv_scl_min = mv_scl_min
        self.mv_scl_max = mv_scl_max
        self.P = P
        self.Ti = Ti
        self.Td = Td

        self.ctrl = PIDController(mv_init_value=mv_min, mv_min=mv_min, mv_max=mv_max,
                                  kp=P, ki=Ti, kd=Td, sample_time=0.1)

        self._add_attribute(Attribute('PV', float, init_value=0))
        self._add_attribute(Attribute('PVSclMin', float, init_value=pv_scl_min))
        self._add_attribute(Attribute('PVSclMax', float, init_value=pv_scl_max))
        self._add_attribute(Attribute('PVUnit', int, init_value=pv_unit))
        self._add_attribute(Attribute('SPMan', float, init_value=sp_man_min, sub_cb=self.set_sp_man))
        self._add_attribute(Attribute('SPInt', float, init_value=sp_int_min, sub_cb=self.set_sp_int))
        self._add_attribute(Attribute('SPSclMin', float, init_value=sp_scl_min))
        self._add_attribute(Attribute('SPSclMax', float, init_value=sp_scl_max))
        self._add_attribute(Attribute('SPUnit', int, init_value=sp_unit))
        self._add_attribute(Attribute('SPIntMin', float, init_value=sp_int_min))
        self._add_attribute(Attribute('SPIntMax', float, init_value=sp_int_max))
        self._add_attribute(Attribute('SPManMin', float, init_value=sp_man_min))
        self._add_attribute(Attribute('SPManMax', float, init_value=sp_man_max))
        self._add_attribute(Attribute('SP', float, init_value=sp_int_min))
        self._add_attribute(Attribute('MVMan', float, init_value=mv_min, sub_cb=self.set_mv_man))
        self._add_attribute(Attribute('MV', float, init_value=mv_min))
        self._add_attribute(Attribute('MVMin', float, init_value=mv_min))
        self._add_attribute(Attribute('MVMax', float, init_value=mv_max))
        self._add_attribute(Attribute('MVUnit', float, init_value=mv_unit))
        self._add_attribute(Attribute('MVSclMin', float, init_value=mv_scl_min))
        self._add_attribute(Attribute('MVSclMax', float, init_value=mv_scl_max))
        self._add_attribute(Attribute('P', float, init_value=P, sub_cb=self.set_p))
        self._add_attribute(Attribute('Ti', float, init_value=Ti, sub_cb=self.set_ti))
        self._add_attribute(Attribute('Td', float, init_value=Td, sub_cb=self.set_td))

        self.op_src_mode.add_enter_automatic_callback(self._start_aut_mv_update_loop)
        self.op_src_mode.add_exit_automatic_callback(self._stop_aut_mv_update_loop)

        self._stop_update_mv_flag = False
        self._stopped_update_mv_flag = False

    def set_p(self, value):
        self.P = value
        self.ctrl.set_kp(value)

    def set_ti(self, value):
        self.Ti = value
        self.ctrl.set_ki(value)

    def set_td(self, value):
        self.Td = value
        self.ctrl.set_kd(value)

    @staticmethod
    def _valid_value(value, v_min, v_max):
        if value < v_min or value > v_max:
            return False
        else:
            return True

    def _set_sp(self, value, v_min, v_max):
        if self._valid_value(value, v_min, v_max):
            self.attributes['SP'].set_value(value)
            self.ctrl.set_sp(value)
            logging.debug('SP set to %s' % value)
        else:
            logging.debug('SP cannot be set to %s (out of range)' % value)

    def set_sp_man(self, value):
        logging.debug('SPMan set to %s' % value)
        if self.op_src_mode.attributes['SrcManAct'].value and self.op_src_mode.attributes['StateAutAct'].value:
            self._set_sp(value, self.sp_man_min, self.sp_man_max)

    def set_sp_int(self, value):
        logging.debug('SPInt set to %s' % value)
        if self.op_src_mode.attributes['SrcIntAct'].value and self.op_src_mode.attributes['StateAutAct'].value:
            self._set_sp(value, self.sp_int_min, self.sp_int_max)

    def set_mv_man(self, value):
        logging.debug('MVMan set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value:
            self._set_mv(value, self.mv_min, self.mv_max)

    def _set_mv(self, value, v_min, v_max):
        if self._valid_value(value, v_min, v_max):
            self.attributes['MV'].set_value(value)
            logging.debug('MV set to %s' % value)
        else:
            logging.debug('MV cannot be set to %s (out of range)' % value)

    def _update_mv_int_loop(self):
        while not self._stop_update_mv_flag:
            if self.op_src_mode.attributes['StateAutAct'].value:
                value = self.ctrl.get_mv()
                self._set_mv(value, self.mv_min, self.mv_max)
            sleep(0.1)
        self._stopped_update_mv_flag = True

    def _start_aut_mv_update_loop(self):
        self._stop_update_mv_flag = False
        self.ctrl.start()
        threading.Thread(target=self._update_mv_int_loop).start()

    def _stop_aut_mv_update_loop(self):
        self._stop_update_mv_flag = True
        while not self._stopped_update_mv_flag:
            sleep(0.1)
        self.ctrl.stop()

    def set_pv(self, value):
        self.attributes['PV'].set_value(value)
        self.ctrl.set_pv(value)

    def get_mv(self):
        return self.attributes['MV'].value

    def get_sp(self):
        return self.attributes['SP'].value
