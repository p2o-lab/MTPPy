from src.attribute import Attribute


class ControlElementsDIntServParam:

    def __init__(self, op_src_mode, v_min, v_max, v_scl_min, v_scl_max, v_unit):
        self.v_min = v_min
        self.v_max = v_max
        self.v_scl_min = v_scl_min
        self.v_scl_max = v_scl_max
        self.v_unit = v_unit

        self.op_src_mode = op_src_mode

        self.attributes = {}
        self._init_attributes()

    def _init_attributes(self):
        self.attributes = {
            'VOp': Attribute('VOp', int, init_value=0, cb_value_change=self.set_v_op),
            'VInt': Attribute('VInt', int, init_value=0, cb_value_change=self.set_v_int),
            'VExt': Attribute('VExt', int, init_value=0, cb_value_change=self.set_v_ext),
            'VReq': Attribute('VReq', int, init_value=0),
            'VOut': Attribute('VOut', int, init_value=0),
            'VFbk': Attribute('VFbk', int, init_value=0),
            'VUnit': Attribute('VUnit', int, init_value=self.v_unit),
            'VSclMin': Attribute('VSclMin', int, init_value=self.v_scl_min),
            'VSclMax': Attribute('VSclMax', int, init_value=self.v_scl_max),
            'VMin': Attribute('VMin', int, init_value=self.v_min),
            'VMax': Attribute('VMax', int, init_value=self.v_max),
            'Sync': Attribute('Sync', bool, False),
        }

    def set_v_op(self, value):
        print('VOp set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct']:
            self.set_v_req(value)

    def set_v_int(self, value):
        print('VInt set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcIntAct']:
            self.set_v_req(value)

    def set_v_ext(self, value):
        print('VExt set to %s' % value)
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
            print('VReq set to %s' % value)
        else:
            print('VReq cannot be set to %s (out of range)' % value)

    def set_v_out(self):
        v_req = self.attributes['VReq'].value
        self.attributes['VOut'].set_value(v_req)
        self.set_v_fbk(v_req)
        print('VOut set to %s' % v_req)

    def set_v_fbk(self, value):
        self.attributes['VFbk'].set_value(value)
        print('VFbk set to %s' % value)
