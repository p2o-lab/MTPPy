from mtppy.attribute import Attribute


class OperationSourceMode:
    def __init__(self):
        self.attributes = {
            'StateChannel': Attribute('StateChannel', bool, init_value=False, sub_cb=self.set_state_channel),
            'StateOffAut': Attribute('StateOffAut', bool, init_value=False, sub_cb=self.set_state_off_aut),
            'StateOpAut': Attribute('StateOpAut', bool, init_value=False, sub_cb=self.set_state_op_aut),
            'StateAutAut': Attribute('StateAutAut', bool, init_value=False, sub_cb=self.set_state_aut_aut),
            'StateOffOp': Attribute('StateOffOp', bool, init_value=False, sub_cb=self.set_state_off_op),
            'StateOpOp': Attribute('StateOpOp', bool, init_value=False, sub_cb=self.set_state_op_op),
            'StateAutOp': Attribute('StateAutOp', bool, init_value=False, sub_cb=self.set_state_aut_op),
            'StateOpAct': Attribute('StateOpAct', bool, init_value=False),
            'StateAutAct': Attribute('StateAutAct', bool, init_value=False),
            'StateOffAct': Attribute('StateOffAct', bool, init_value=True),

            'SrcChannel': Attribute('SrcChannel', bool, init_value=False, sub_cb=self.set_src_channel),
            'SrcExtAut': Attribute('SrcExtAut', bool, init_value=False, sub_cb=self.set_src_ext_aut),
            'SrcIntOp': Attribute('SrcIntOp', bool, init_value=False, sub_cb=self.set_src_int_op),
            'SrcIntAut': Attribute('SrcIntAut', bool, init_value=False, sub_cb=self.set_src_int_aut),
            'SrcExtOp': Attribute('SrcExtOp', bool, init_value=False, sub_cb=self.set_src_ext_op),
            'SrcIntAct': Attribute('SrcIntAct', bool, init_value=False),
            'SrcExtAct': Attribute('SrcExtAct', bool, init_value=False)
        }
        self.switch_to_offline_mode_allowed = False

        self.enter_offline_callbacks = []
        self.exit_offline_callbacks = []

    def allow_switch_to_offline_mode(self, allow_flag: bool):
        self.switch_to_offline_mode_allowed = allow_flag

    def add_enter_offline_callback(self, callback: callable):
        self.enter_offline_callbacks.append(callback)

    def add_exit_offline_callback(self, callback: callable):
        self.exit_offline_callbacks.append(callback)

    def _opmode_to_off(self):
        self.attributes['StateOpAct'].set_value(False)
        self.attributes['StateAutAct'].set_value(False)
        self.attributes['StateOffAct'].set_value(True)
        print('Operation mode is now off')
        self._src_to_off()

    def _opmode_to_aut(self):
        prev_mode_is_off = self.attributes['StateOffAct'].value
        self.attributes['StateOpAct'].set_value(False)
        self.attributes['StateAutAct'].set_value(True)
        self.attributes['StateOffAct'].set_value(False)

        if prev_mode_is_off and len(self.exit_offline_callbacks):
            print('Applying exit offline mode callbacks')
            [cb() for cb in self.exit_offline_callbacks]
        print('Operation mode is now aut')
        self._src_to_int()

    def _opmode_to_op(self):
        prev_mode_is_off = self.attributes['StateOffAct'].value
        self.attributes['StateOpAct'].set_value(True)
        self.attributes['StateAutAct'].set_value(False)
        self.attributes['StateOffAct'].set_value(False)

        if prev_mode_is_off and len(self.exit_offline_callbacks):
            print('Applying exit offline mode callbacks')
            [cb() for cb in self.exit_offline_callbacks]
        print('Operation mode is now op')
        self._src_to_off()

    def set_state_channel(self, value: bool):
        print('Operation mode channel is now %s' % value)

    def set_state_aut_aut(self, value: bool):
        print(f'StateAutAut set to {value}')
        if self.attributes['StateChannel'].value and value:
            if self.attributes['StateOffAct'] or self.attributes['StateOpAct']:
                self._opmode_to_aut()

    def set_state_aut_op(self, value: bool):
        print(f'StateAutOp set to {value}')
        if not self.attributes['StateChannel'].value and value:
            if self.attributes['StateOffAct'] or self.attributes['StateOpAct']:
                self._opmode_to_aut()
                self.attributes['StateAutOp'].set_value(False)

    def set_state_off_aut(self, value: bool):
        print(f'StateOffAut set to {value}')
        if self.attributes['StateChannel'].value and value and self.switch_to_offline_mode_allowed:
            if self.attributes['StateAutAct'] or self.attributes['StateOpAct']:
                self._opmode_to_off()

    def set_state_off_op(self, value: bool):
        print(f'StateOffOp set to {value}')
        if not self.attributes['StateChannel'].value and value and self.switch_to_offline_mode_allowed:
            if self.attributes['StateAutAct'] or self.attributes['StateOpAct']:
                self._opmode_to_off()
                self.attributes['StateOffOp'].set_value(False)

    def set_state_op_aut(self, value: bool):
        print(f'StateOpAut set to {value}')
        if self.attributes['StateChannel'].value and value:
            if self.attributes['StateOffAct'] or self.attributes['StateOpAct']:
                self._opmode_to_op()

    def set_state_op_op(self, value: bool):
        print(f'StateOpOp set to {value}')
        if not self.attributes['StateChannel'].value and value:
            if self.attributes['StateOffAct'] or self.attributes['StateAutAct']:
                self._opmode_to_op()
                self.attributes['StateOpOp'].set_value(False)

    def _src_to_off(self):
        self.attributes['SrcIntAct'].set_value(False)
        self.attributes['SrcExtAct'].set_value(False)
        print('Source mode is now off')

    def _src_to_int(self):
        self.attributes['SrcIntAct'].set_value(True)
        self.attributes['SrcExtAct'].set_value(False)
        print('Source mode is now int')

    def _src_to_ext(self):
        self.attributes['SrcIntAct'].set_value(False)
        self.attributes['SrcExtAct'].set_value(True)
        print('Source mode is now ext')

    def set_src_channel(self, value: bool):
        print('Source mode channel is now %s' % value)

    def set_src_ext_aut(self, value: bool):
        if not self.attributes['StateOffAct'].value and value:
            if self.attributes['SrcChannel'].value:
                self._src_to_ext()

    def set_src_ext_op(self, value: bool):
        if not self.attributes['StateOffAct'].value and value:
            if not self.attributes['SrcChannel'].value:
                self._src_to_ext()
                self.attributes['SrcExtOp'].set_value(False)

    def set_src_int_aut(self, value: bool):
        if not self.attributes['StateOffAct'].value and value:
            if self.attributes['SrcChannel'].value:
                self._src_to_int()

    def set_src_int_op(self, value: bool):
        if not self.attributes['StateOffAct'].value and value:
            if not self.attributes['SrcChannel'].value:
                self._src_to_int()
                self.attributes['SrcIntOp'].set_value(False)
