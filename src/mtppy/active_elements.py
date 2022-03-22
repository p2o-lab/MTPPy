from mtppy.attribute import Attribute

from mtppy.operation_source_mode import OperationSourceMode
from mtppy.suc_data_assembly import SUCActiveElement


class AnaDrv(SUCActiveElement):
    def __init__(self, tag_name, tag_description='',
                 rpm_min=0, rpm_max=1000, rpm_scl_min=0, rpm_scl_max=1000, rpm_unit=0,
                 rev_fbk_calc=True, fwd_fbk_calc=True, rpm_fbk_calc=True,
                 safe_pos=0, fwd_en=True, rev_en=False, perm_en=False, intl_en=False, prot_en=False):
        super().__init__(tag_name, tag_description)

        self.op_src_mode = OperationSourceMode()

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
        self._add_attribute(Attribute('SafePosAct', bool, init_value=1))
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
        self._add_attribute(Attribute('Rpm', float, init_value=0))
        self._add_attribute(Attribute('RpmRbk', float, init_value=0))
        self._add_attribute(Attribute('RevFbkCalc', bool, init_value=rev_fbk_calc))
        self._add_attribute(Attribute('RevFbk', bool, init_value=0))
        self._add_attribute(Attribute('FwdFbkCalc', bool, init_value=fwd_fbk_calc))
        self._add_attribute(Attribute('RpmFbkCalc', bool, init_value=rpm_fbk_calc))
        self._add_attribute(Attribute('RpmFbk', float, init_value=0))
        self._add_attribute(Attribute('Trip', bool, init_value=0))
        self._add_attribute(Attribute('PermEn', bool, init_value=perm_en))
        self._add_attribute(Attribute('Permit', bool, init_value=0))
        self._add_attribute(Attribute('IntlEn', bool, init_value=intl_en))
        self._add_attribute(Attribute('Interlock', bool, init_value=0))
        self._add_attribute(Attribute('ProtEn', bool, init_value=prot_en))
        self._add_attribute(Attribute('Protect', bool, init_value=0))
        self._add_attribute(Attribute('ResetOp', bool, init_value=0, sub_cb=self.set_reset_op))
        self._add_attribute(Attribute('ResetAut', bool, init_value=0, sub_cb=self.set_reset_aut))

    def active_save_pos(self):
        self.attributes['SafePosAct'].set_value(self.safe_pos)

    def set_fwd_op(self, value):
        print('FwdOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'] and self.fwd_en and value:
            self._run_fwd_drv()
            self.attributes['FwdOp'].set_value(False)

    def set_rev_op(self, value):
        print('RevOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'] and self.rev_en and value:
            self._run_rev_drv()
            self.attributes['RevOp'].set_value(False)

    def set_stop_op(self, value):
        print('StopOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'] and value:
            self._stop_drv()
            self.attributes['StopOp'].set_value(False)

    def set_reset_op(self, value):
        print('ResetOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'] and value:
            self._reset_drv()
            self.attributes['ResetOp'].set_value(False)

    def set_fwd_aut(self, value):
        print('FwdAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and self.fwd_en and value:
            self._run_fwd_drv()

    def set_rev_aut(self, value):
        print('RevAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and self.rev_en and value:
            self._run_rev_drv()

    def set_stop_aut(self, value):
        print('StopAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and value:
            self._stop_drv()

    def set_reset_aut(self, value):
        print('ResetAut set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and value:
            self._reset_drv()

    def _run_fwd_drv(self):
        if self._run_allowed():
            self.attributes['FwdCtrl'].set_value(True)
            self.attributes['RevCtrl'].set_value(False)

    def _run_rev_drv(self):
        if self._run_allowed():
            self.attributes['FwdCtrl'].set_value(False)
            self.attributes['RevCtrl'].set_value(True)

    def _stop_drv(self):
        self.attributes['FwdCtrl'].set_value(False)
        self.attributes['RevCtrl'].set_value(False)

    def _reset_drv(self):
        if self.attributes['ProtEn'].value and not self.attributes['Protect'].value:
            self.attributes['Protect'].set_value(True)
        self.attributes['FwdCtrl'].set_value(False)
        self.attributes['RevCtrl'].set_value(False)

    def set_rpm_int(self, value):
        print('RpmInt set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcIntAct']:
            self._set_rpm(value)

    def set_rpm_man(self, value):
        print('RpmIntMan set to %s' % value)
        if self.op_src_mode.attributes['SrcManAct']:
            self._set_rpm(value)

    def valid_value(self, value):
        if value < self.rpm_min or value > self.rpm_max:
            return False
        else:
            return True

    def _set_rpm(self, value):
        if self.valid_value(value):
            self.attributes['Rpm'].set_value(value)
            print('Rpm set to %s' % value)
        else:
            print('Rpm cannot be set to %s (out of range)' % value)

    def set_rpm_rbk(self, value):
        self.attributes['RpmRbk'].set_value(value)
        print('RpmRbk set to %s' % value)

    def set_rpm_fbk(self, value):
        if self.attributes['RpmFbkCalc'].value:
            value = self.attributes['Rpm']
        self.attributes['RpmFbk'].set_value(value)
        print('RpmFbk set to %s' % value)

    def set_rev_fbk(self, value):
        if self.attributes['RevFbkCalc'].value:
            value = self.attributes['RevCtrl']
        self.attributes['RevFbk'].set_value(value)
        print('RevFbk set to %s' % value)

    def set_fwd_fbk(self, value):
        if self.attributes['FwdFbkCalc'].value:
            value = self.attributes['FwdCtrl']
        self.attributes['FwdFbk'].set_value(value)
        print('FwdFbk set to %s' % value)

    def set_trip(self, value):
        self.attributes['Trip'].set_value(value)
        print('Trip set to %s' % value)

    def set_permit(self, value):
        if self.attributes['PermEn'].value:
            value = True
        self.attributes['Permit'].set_value(value)
        print('Permit set to %s' % value)

    def set_intl(self, value):
        if self.attributes['IntlEn'].value:
            value = True
        self.attributes['Interlock'].set_value(value)
        print('Interlock set to %s' % value)

    def set_protect(self, value):
        if self.attributes['ProtEn'].value:
            value = True
        if value:
            self._reset_drv()
        self.attributes['Protect'].set_value(value)
        print('Protect set to %s' % value)

    def _run_allowed(self):
        if self.attributes['PermEn'].value and not self.attributes['Permit'].value:
            return False
        if self.attributes['IntlEn'].value and not self.attributes['Interlock'].value:
            return False
        if self.attributes['ProtEn'].value and not self.attributes['Protect'].value:
            return False
        return True

    def get_rpm_fbk(self):
        return self.attributes['RpmFbk'].value

    def get_fwd_fbk(self):
        return self.attributes['FwdFbk'].value

    def get_rev_fbk(self):
        return self.attributes['RevFbk'].value


class PIDCtrl(SUCActiveElement):
    pass
