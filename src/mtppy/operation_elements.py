import logging

from mtppy.attribute import Attribute
from mtppy.operation_source_mode import OperationSourceMode
from mtppy.suc_data_assembly import SUCOperationElement


class AnaServParam(SUCOperationElement):
    def __init__(self, tag_name: str, tag_description: str = '', v_min: float = 0, v_max: float = 100,
                 v_scl_min: float = 0, v_scl_max: float = 100, v_unit: int = 0):
        """
        Analog Service Parameter (AnaServParam). Parameter names correspond attribute names in VDI/VDE/NAMUR 2658.
        """
        super().__init__(tag_name, tag_description)

        self.op_src_mode = OperationSourceMode()

        self.v_min = v_min
        self.v_max = v_max
        self.v_scl_min = v_scl_min
        self.v_scl_max = v_scl_max
        self.v_unit = v_unit

        self._add_attribute(Attribute('VOp', float, init_value=v_min, sub_cb=self.set_v_op))
        self._add_attribute(Attribute('VInt', float, init_value=v_min, sub_cb=self.set_v_int))
        self._add_attribute(Attribute('VExt', float, init_value=v_min, sub_cb=self.set_v_ext))
        self._add_attribute(Attribute('VReq', float, init_value=v_min))
        self._add_attribute(Attribute('VOut', float, init_value=0))
        self._add_attribute(Attribute('VFbk', float, init_value=0))
        self._add_attribute(Attribute('VUnit', int, init_value=self.v_unit))
        self._add_attribute(Attribute('VSclMin', float, init_value=self.v_scl_min))
        self._add_attribute(Attribute('VSclMax', float, init_value=self.v_scl_max))
        self._add_attribute(Attribute('VMin', float, init_value=self.v_min))
        self._add_attribute(Attribute('VMax', float, init_value=self.v_max))
        self._add_attribute(Attribute('Sync', bool, False))

    def set_v_op(self, value):
        logging.debug('VOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct']:
            self.set_v_req(value)

    def set_v_int(self, value):
        logging.debug('VInt set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcIntAct']:
            self.set_v_req(value)

    def set_v_ext(self, value):
        logging.debug('VExt set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcExtAct']:
            self.set_v_req(value)

    def valid_value(self, value):
        if value < self.v_min or value > self.v_max:
            return False
        else:
            return True

    def set_v_req(self, value):
        if self.valid_value(value):
            self.attributes['VReq'].set_value(value)
            logging.debug('VReq set to %s' % value)
        else:
            logging.debug('VReq cannot be set to %s (out of range)' % value)

    def set_v_out(self):
        v_req = self.attributes['VReq'].value
        self.attributes['VOut'].set_value(v_req)
        self.set_v_fbk(v_req)
        logging.debug('VOut set to %s' % v_req)

    def get_v_out(self):
        return self.attributes['VOut'].value

    def set_v_fbk(self, value):
        self.attributes['VFbk'].set_value(value)
        logging.debug('VFbk set to %s' % value)


class BinServParam(SUCOperationElement):
    def __init__(self, tag_name: str, tag_description: str = '', v_state_0: str = 'false', v_state_1: str = 'true'):
        """
        Binary Service Parameter (BinServParam). Parameter names correspond attribute names in VDI/VDE/NAMUR 2658.
        """
        super().__init__(tag_name, tag_description)

        self.op_src_mode = OperationSourceMode()

        self.v_state_0 = v_state_0
        self.v_state_1 = v_state_1

        self._add_attribute(Attribute('VOp', bool, init_value=False, sub_cb=self.set_v_op))
        self._add_attribute(Attribute('VInt', bool, init_value=False, sub_cb=self.set_v_int))
        self._add_attribute(Attribute('VExt', bool, init_value=False, sub_cb=self.set_v_ext))
        self._add_attribute(Attribute('VReq', bool, init_value=False))
        self._add_attribute(Attribute('VOut', bool, init_value=False))
        self._add_attribute(Attribute('VFbk', bool, init_value=False))
        self._add_attribute(Attribute('VState0', str, init_value=self.v_state_0))
        self._add_attribute(Attribute('VState1', str, init_value=self.v_state_1))
        self._add_attribute(Attribute('Sync', bool, False))

    def set_v_op(self, value):
        logging.debug('VOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct']:
            self.set_v_req(value)

    def set_v_int(self, value):
        logging.debug('VInt set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcIntAct']:
            self.set_v_req(value)

    def set_v_ext(self, value):
        logging.debug('VExt set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcExtAct']:
            self.set_v_req(value)

    def set_v_req(self, value):
        self.attributes['VReq'].set_value(value)
        logging.debug('VReq set to %s' % value)

    def set_v_out(self):
        v_req = self.attributes['VReq'].value
        self.attributes['VOut'].set_value(v_req)
        self.set_v_fbk(v_req)
        logging.debug('VOut set to %s' % v_req)

    def get_v_out(self):
        return self.attributes['VOut'].value

    def set_v_fbk(self, value):
        self.attributes['VFbk'].set_value(value)
        logging.debug('VFbk set to %s' % value)


class DIntServParam(SUCOperationElement):
    def __init__(self, tag_name: str, tag_description: str = '', v_min: int = 0, v_max: int = 100, v_scl_min: int = 0,
                 v_scl_max: int = 100, v_unit: int = 0):
        """
        Discrete Integer Service Parameter (DIntServParam). Parameter names correspond attribute names in VDI/VDE/NAMUR 2658.
        """
        super().__init__(tag_name, tag_description)

        self.op_src_mode = OperationSourceMode()

        self.v_min = v_min
        self.v_max = v_max
        self.v_scl_min = v_scl_min
        self.v_scl_max = v_scl_max
        self.v_unit = v_unit

        self._add_attribute(Attribute('VOp', int, init_value=v_min, sub_cb=self.set_v_op))
        self._add_attribute(Attribute('VInt', int, init_value=v_min, sub_cb=self.set_v_int))
        self._add_attribute(Attribute('VExt', int, init_value=v_min, sub_cb=self.set_v_ext))
        self._add_attribute(Attribute('VReq', int, init_value=v_min))
        self._add_attribute(Attribute('VOut', int, init_value=0))
        self._add_attribute(Attribute('VFbk', int, init_value=0))
        self._add_attribute(Attribute('VUnit', int, init_value=self.v_unit))
        self._add_attribute(Attribute('VSclMin', int, init_value=self.v_scl_min))
        self._add_attribute(Attribute('VSclMax', int, init_value=self.v_scl_max))
        self._add_attribute(Attribute('VMin', int, init_value=self.v_min))
        self._add_attribute(Attribute('VMax', int, init_value=self.v_max))
        self._add_attribute(Attribute('Sync', bool, False))

    def set_v_op(self, value):
        logging.debug('VOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct']:
            self.set_v_req(value)

    def set_v_int(self, value):
        logging.debug('VInt set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcIntAct']:
            self.set_v_req(value)

    def set_v_ext(self, value):
        logging.debug('VExt set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcExtAct']:
            self.set_v_req(value)

    def valid_value(self, value):
        if value < self.v_min or value > self.v_max:
            return False
        else:
            return True

    def set_v_req(self, value):
        if self.valid_value(value):
            self.attributes['VReq'].set_value(value)
            logging.debug('VReq set to %s' % value)
        else:
            logging.debug('VReq cannot be set to %s (out of range)' % value)

    def set_v_out(self):
        v_req = self.attributes['VReq'].value
        self.attributes['VOut'].set_value(v_req)
        self.set_v_fbk(v_req)
        logging.debug('VOut set to %s' % v_req)

    def get_v_out(self):
        return self.attributes['VOut'].value

    def set_v_fbk(self, value):
        self.attributes['VFbk'].set_value(value)
        logging.debug('VFbk set to %s' % value)


class StringServParam(SUCOperationElement):
    def __init__(self, tag_name: str, tag_description: str = ''):
        """
        String Service Parameter (StringServParam). Parameter names correspond attribute names in VDI/VDE/NAMUR 2658.
        """
        super().__init__(tag_name, tag_description)

        self.op_src_mode = OperationSourceMode()

        self._add_attribute(Attribute('VOp', str, init_value='', sub_cb=self.set_v_op))
        self._add_attribute(Attribute('VInt', str, init_value='', sub_cb=self.set_v_int))
        self._add_attribute(Attribute('VExt', str, init_value='', sub_cb=self.set_v_ext))
        self._add_attribute(Attribute('VReq', str, init_value=''))
        self._add_attribute(Attribute('VOut', str, init_value=''))
        self._add_attribute(Attribute('VFbk', str, init_value=''))
        self._add_attribute(Attribute('Sync', bool, False))

    def set_v_op(self, value):
        logging.debug('VOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct']:
            self.set_v_req(value)

    def set_v_int(self, value):
        logging.debug('VInt set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcIntAct']:
            self.set_v_req(value)

    def set_v_ext(self, value):
        logging.debug('VExt set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcExtAct']:
            self.set_v_req(value)

    def valid_value(self, value):
        return True

    def set_v_req(self, value):
        if self.valid_value(value):
            self.attributes['VReq'].set_value(value)
            logging.debug('VReq set to %s' % value)
        else:
            logging.debug('VReq cannot be set to %s (out of range)' % value)

    def set_v_out(self):
        v_req = self.attributes['VReq'].value
        self.attributes['VOut'].set_value(v_req)
        self.set_v_fbk(v_req)
        logging.debug('VOut set to %s' % v_req)

    def get_v_out(self):
        return self.attributes['VOut'].value

    def set_v_fbk(self, value):
        self.attributes['VFbk'].set_value(value)
        logging.debug('VFbk set to %s' % value)
