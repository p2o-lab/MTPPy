from src.attribute import Attribute


class ControlElementsBinServParam:

    def __init__(self, op_src_mode, v_state_0='false', v_state_1='true'):
        self.v_state_0 = v_state_0
        self.v_state_1 = v_state_1

        self.op_src_mode = op_src_mode

        self.attributes = {}
        self._init_attributes()

    def _init_attributes(self):
        self.attributes = {
            'VOp': Attribute('VOp', bool, init_value=False, cb_value_change=self.set_v_op),
            'VInt': Attribute('VInt', bool, init_value=False, cb_value_change=self.set_v_int),
            'VExt': Attribute('VExt', bool, init_value=False, cb_value_change=self.set_v_ext),
            'VReq': Attribute('VReq', bool, init_value=False),
            'VOut': Attribute('VOut', bool, init_value=False),
            'VFbk': Attribute('VFbk', bool, init_value=False),
            'VState0': Attribute('VState0', str, init_value=self.v_state_0),
            'VState1': Attribute('VState1', str, init_value=self.v_state_1),
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

    def set_v_req(self, value):
        self.attributes['VReq'].set_value(value)
        print('VReq set to %s' % value)

    def set_v_out(self):
        v_req = self.attributes['VReq'].value
        self.attributes['VOut'].set_value(v_req)
        self.set_v_fbk(v_req)
        print('VOut set to %s' % v_req)

    def set_v_fbk(self, value):
        self.attributes['VFbk'].set_value(value)
        print('VFbk set to %s' % value)

