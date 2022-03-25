from mtppy.attribute import Attribute

from mtppy.operation_source_mode import OperationSourceModeActiveElements
from mtppy.suc_data_assembly import SUCActiveElement

from time import sleep
from threading import Thread
from simple_pid import PID


class AnaDrv(SUCActiveElement):
    def __init__(self, tag_name, tag_description='',
                 rpm_min=0, rpm_max=1000, rpm_scl_min=0, rpm_scl_max=1000, rpm_unit=0,
                 rev_fbk_calc=True, fwd_fbk_calc=True, rpm_fbk_calc=True,
                 safe_pos=0, fwd_en=True, rev_en=False, perm_en=False, intl_en=False, prot_en=False):
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
            print('Permission is not given')
            return False
        if self.attributes['IntlEn'].value and self.attributes['Interlock'].value == 0:
            print('Interlock is active')
            return False
        if self.attributes['ProtEn'].value and self.attributes['Protect'].value == 0:
            print('Protect is active')
            return False
        if not self.attributes['Trip'].value:
            print('Drive protection triggered')
            return False
        return True

    def set_fwd_op(self, value: bool):
        print('FwdOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and self.fwd_en:
            if value and self._run_allowed():
                self._run_fwd_drv()
                self.attributes['FwdOp'].value = False

    def set_rev_op(self, value: bool):
        print('RevOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and self.rev_en:
            if value and self._run_allowed():
                self._run_rev_drv()
                self.attributes['RevOp'].value = False

    def set_stop_op(self, value: bool):
        print('StopOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and value:
            self._stop_drv()
            self.attributes['StopOp'].set_value(False)

    def set_reset_op(self, value: bool):
        print('ResetOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value and value:
            self._reset_drv()
            self.attributes['ResetOp'].set_value(False)

    def set_fwd_aut(self, value: bool):
        print('FwdAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and self.fwd_en:
            if value and self._run_allowed():
                self._run_fwd_drv()

    def set_rev_aut(self, value: bool):
        print('RevAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and self.rev_en:
            if value and self._run_allowed():
                self._run_rev_drv()

    def set_stop_aut(self, value: bool):
        print('StopAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and value:
            self._stop_drv()

    def set_reset_aut(self, value: bool):
        print('ResetAut set to %s' % value)
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
        print('RpmInt set to %s' % value)
        if self.op_src_mode.attributes['SrcIntAct'].value:
            self._set_rpm(value)

    def set_rpm_man(self, value: float):
        print('RpmIntMan set to %s' % value)
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
            print('Rpm set to %s' % value)
            if self.attributes['RpmFbkCalc'].value:
                self.attributes['RpmFbk'].set_value(value)
        else:
            print('Rpm cannot be set to %s (out of range)' % value)

    def set_rpm_rbk(self, value: float):
        corr_value = self._correct_value(value)
        self.attributes['RpmRbk'].set_value(corr_value)
        print('RpmRbk set to %s' % corr_value)

    def set_rpm_fbk(self, value: float):
        if not self.attributes['RpmFbkCalc'].value:
            corr_value = self._correct_value(value)
            self.attributes['RpmFbk'].set_value(corr_value)
            print('RpmFbk set to %s' % corr_value)

    def set_rev_fbk(self, value: bool):
        if not self.attributes['RevFbkCalc'].value:
            self.attributes['RevFbk'].set_value(value)
            print('RevFbk set to %s' % value)

    def set_fwd_fbk(self, value: bool):
        if not self.attributes['FwdFbkCalc'].value:
            self.attributes['FwdFbk'].set_value(value)
            print('FwdFbk set to %s' % value)

    def set_trip(self, value: bool):
        self.attributes['Trip'].set_value(value)
        print('Trip set to %s' % value)
        self._expect_save_pos()

    def set_permit(self, value: bool):
        if not self.attributes['PermEn'].value:
            value = True
        self.attributes['Permit'].set_value(value)
        print('Permit set to %s' % value)
        self._expect_save_pos()

    def set_interlock(self, value: bool):
        if not self.attributes['IntlEn'].value:
            value = True
        self.attributes['Interlock'].set_value(value)
        print('Interlock set to %s' % value)
        self._expect_save_pos()

    def set_protect(self, value: bool):
        if not self.attributes['ProtEn'].value:
            value = True
        if value:
            self._reset_drv()
        self.attributes['Protect'].set_value(value)
        print('Protect set to %s' % value)
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


class PIDController:
    def __init__(self, kp=100, ki=10, kd=1, mv_min=0, mv_max=100, sample_time=0.1):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.mv_min = mv_min
        self.mv_max = mv_max
        self.sp = 0
        self.pv = 0
        self.mv = 0
        self.sample_time = sample_time

        self.ctrl = PID(Kp=self.kp, Ki=self.ki, Kd=self.kd, output_limits=(mv_min, mv_max), sample_time=sample_time)

        self.thread = Thread(target=self.loop)
        self.stop_flag = True
        self.stopped = True

    def set_limits(self, mv_min, mv_max):
        self.ctrl.output_limits = (mv_min, mv_max)

    def start(self):
        self.ctrl.setpoint = self.sp
        self.stopped = False
        self.stop_flag = False
        self.thread.start()

    def stop(self):
        self.stopped = False
        self.stop_flag = True
        while not self.stopped:
            sleep(0.1)
        self.ctrl.reset()

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
                 sp_man=0, sp_int=0, sp_scl_min=0, sp_scl_max=100, sp_unit=0,
                 sp_int_min=0, sp_int_max=100, sp_man_min=0, sp_man_max=100,
                 mv_man=0, mv_min=0, mv_max=1000, mv_unit=0, mv_scl_min=0, mv_scl_max=100,
                 P=100, Ti=10, Td=1):
        super().__init__(tag_name, tag_description)

        self.op_src_mode = OperationSourceModeActiveElements()

        self.pv_scl_min = pv_scl_min
        self.pv_scl_max = pv_scl_max
        self.pv_unit = pv_unit
        self.sp_man = sp_man
        self.sp_int = sp_int
        self.sp_scl_min = sp_scl_min
        self.sp_scl_max = sp_scl_max
        self.sp_unit = sp_unit
        self.sp_int_min = sp_int_min
        self.sp_int_max = sp_int_max
        self.sp_man_min = sp_man_min
        self.sp_man_max = sp_man_max
        self.sp = sp_int
        self.mv_man = mv_man
        self.mv_min = mv_min
        self.mv_max = mv_max
        self.mv_unit = mv_unit
        self.mv_scl_min = mv_scl_min
        self.mv_scl_max = mv_scl_max
        self.P = P
        self.Ti = Ti
        self.Td = Td

        self.ctrl = PIDController(kp=P, ki=Ti, kd=Td, mv_min=mv_min, mv_max=mv_max, sample_time=0.1)

        self._add_attribute(Attribute('PV', float, init_value=0))
        self._add_attribute(Attribute('PVSclMin', float, init_value=pv_scl_min))
        self._add_attribute(Attribute('PVSclMax', float, init_value=pv_scl_max))
        self._add_attribute(Attribute('PVUnit', int, init_value=pv_unit))
        self._add_attribute(Attribute('SPMan', float, init_value=sp_man, sub_cb=self.set_sp_man))
        self._add_attribute(Attribute('SPInt', float, init_value=sp_int, sub_cb=self.set_sp_int))
        self._add_attribute(Attribute('SPSclMin', float, init_value=sp_scl_min))
        self._add_attribute(Attribute('SPSclMax', float, init_value=sp_scl_max))
        self._add_attribute(Attribute('SPUnit', int, init_value=sp_unit))
        self._add_attribute(Attribute('SPIntMin', float, init_value=sp_int_min))
        self._add_attribute(Attribute('SPIntMax', float, init_value=sp_int_max))
        self._add_attribute(Attribute('SPManMin', float, init_value=sp_man_min))
        self._add_attribute(Attribute('SPManMax', float, init_value=sp_man_max))
        self._add_attribute(Attribute('SP', float, init_value=sp_int))
        self._add_attribute(Attribute('MVMan', float, init_value=mv_man, sub_cb=self.set_mv_man))
        self._add_attribute(Attribute('MV', float, init_value=0))
        self._add_attribute(Attribute('MVMin', float, init_value=mv_min))
        self._add_attribute(Attribute('MVMax', float, init_value=mv_max))
        self._add_attribute(Attribute('MVUnit', float, init_value=mv_unit))
        self._add_attribute(Attribute('MVSclMin', float, init_value=mv_scl_min))
        self._add_attribute(Attribute('MVSclMax', float, init_value=mv_scl_max))
        self._add_attribute(Attribute('P', float, init_value=P, sub_cb=self.set_p))
        self._add_attribute(Attribute('Ti', float, init_value=Ti, sub_cb=self.set_ti))
        self._add_attribute(Attribute('Td', float, init_value=Td, sub_cb=self.set_td))

        self.op_src_mode.add_exit_offline_callback(self.ctrl.start)
        self.op_src_mode.add_enter_offline_callback(self.ctrl.stop)

        Thread(target=self._update_mv_int_loop).start()

    def set_p(self, value):
        self.P = value
        self.ctrl.set_kp(value)

    def set_ti(self, value):
        self.Ti = value
        self.ctrl.set_ki(value)

    def set_td(self, value):
        self.Td = value
        self.ctrl.set_kd(value)

    def _valid_value(self, value, v_min, v_max):
        if value < v_min or value > v_max:
            return False
        else:
            return True

    def _set_sp(self, value, v_min, v_max):
        if self._valid_value(value, v_min, v_max):
            self.attributes['SP'].set_value(value)
            self.ctrl.set_sp(value)
            print('SP set to %s' % value)
        else:
            print('SP cannot be set to %s (out of range)' % value)

    def set_sp_man(self, value):
        print('SPMan set to %s' % value)
        if self.op_src_mode.attributes['SrcManAct'].value and self.op_src_mode.attributes['StateAutAct'].value:
            self._set_sp(value, self.sp_man_min, self.sp_man_max)

    def set_sp_int(self, value):
        print('SPInt set to %s' % value)
        if self.op_src_mode.attributes['SrcIntAct'].value and self.op_src_mode.attributes['StateAutAct'].value:
            self._set_sp(value, self.sp_int_min, self.sp_int_max)

    def _set_mv(self, value, v_min, v_max):
        if self._valid_value(value, v_min, v_max):
            self.attributes['MV'].set_value(value)
            print('MV set to %s' % value)
        else:
            print('MV cannot be set to %s (out of range)' % value)

    def set_mv_man(self, value):
        print('MVMan set to %s' % value)
        if self.op_src_mode.attributes['StateOPAct'].value:
            self._set_mv(value, self.mv_min, self.mv_max)

    def _update_mv_int_loop(self):
        while True:
            if self.op_src_mode.attributes['SrcIntAct'].value:
                value = self.ctrl.get_mv()
                self._set_mv(value, self.mv_min, self.mv_max)
            sleep(0.1)

    def set_pv(self, value):
        self.attributes['PV'].set_value(value)
        self.ctrl.set_pv(value)

    def get_mv(self):
        return self.attributes['MV'].value
