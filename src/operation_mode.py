from src.variable import Variable
from opcua import ua


class OperationMode:

    def __init__(self, opcua_server, opcua_ns, opcua_prefix):
        self.state_channel = False
        self.mode = 'off'
        self.source_mode = None

        self.variables = {}

        self.opcua_server = opcua_server
        self.opcua_ns = opcua_ns
        self.opcua_prefix = f'{opcua_prefix}.operation_mode'

        self.cb_exit_offline_mode = None

        self._attach_opcua_nodes()

    def attach_source_mode(self, source_mode):
        self.source_mode = source_mode

    def _attach_opcua_nodes(self):

        variables = {
            'StateChannel': {'type': ua.VariantType.Boolean, 'init_value': False, 'callback': self.set_StateChannel, 'writable': True},
            'StateOffAut': {'type': ua.VariantType.Boolean, 'init_value': False, 'callback': self.set_StateOffAut, 'writable': True},
            'StateOpAut': {'type': ua.VariantType.Boolean, 'init_value': False, 'callback': self.set_StateOpAut, 'writable': True},
            'StateAutAut': {'type': ua.VariantType.Boolean, 'init_value': False, 'callback': self.set_StateAutAut, 'writable': True},
            'StateOffOp': {'type': ua.VariantType.Boolean, 'init_value': False, 'callback': self.set_StateOffOp, 'writable': True},
            'StateOpOp': {'type': ua.VariantType.Boolean, 'init_value': False, 'callback': self.set_StateOpOp, 'writable': True},
            'StateAutOp': {'type': ua.VariantType.Boolean, 'init_value': False, 'callback': self.set_StateAutOp, 'writable': True},
            'StateOpAct': {'type': ua.VariantType.Boolean, 'init_value': False, 'callback': None, 'writable': False},
            'StateAutAct': {'type': ua.VariantType.Boolean, 'init_value': False, 'callback': None, 'writable': False},
            'StateOffAct': {'type': ua.VariantType.Boolean, 'init_value': True, 'callback': None, 'writable': False}
        }

        for var_name, var_dict in variables.items():
            var_opcua_node_obj = self.opcua_server.get_node(f'ns={self.opcua_ns};s={self.opcua_prefix}.{var_name}')
            self.variables[var_name] = Variable(var_name,
                                                opcua_type=var_dict['type'],
                                                init_value=var_dict['init_value'],
                                                opcua_node_obj=var_opcua_node_obj,
                                                writable=var_dict['writable'],
                                                callback=var_dict['callback'])

    def _switch_to_offline(self):
        self.mode = 'off'
        self.variables['StateOpAct'].write_value(False)
        self.variables['StateAutAct'].write_value(False)
        self.variables['StateOffAct'].write_value(True)
        print('Operation mode is now off')

    def _switch_to_automatic(self):
        self.mode = 'aut'
        self.variables['StateOpAct'].write_value(False)
        self.variables['StateAutAct'].write_value(True)
        self.variables['StateOffAct'].write_value(False)
        if self.cb_exit_offline_mode is not None:
            print('Applying exit offline mode callback')
            self.cb_exit_offline_mode()
        print('Operation mode is now aut')
        self.source_mode.switch_to_internal()

    def _switch_to_operator(self):
        self.mode = 'op'
        self.variables['StateOpAct'].write_value(True)
        self.variables['StateAutAct'].write_value(False)
        self.variables['StateOffAct'].write_value(False)
        if self.cb_exit_offline_mode is not None:
            print('Applying exit offline mode callback')
            self.cb_exit_offline_mode()
        print('Operation mode is now op')

    def set_StateChannel(self, value):
        self.state_channel = value
        print('Operation mode channel is now %s' % value)

    def set_StateAutAut(self, value):
        if self.state_channel and value:
            if self.mode == 'off' or self.mode == 'op':
                self._switch_to_automatic()
                self.variables['StateAutAut'].write_value(False)

    def set_StateAutOp(self, value):
        if not self.state_channel and value:
            if self.mode == 'off' or self.mode == 'op':
                self._switch_to_automatic()
                self.variables['StateAutOp'].write_value(False)

    def set_StateOffAut(self, value):
        if self.state_channel and value:
            if self.mode == 'aut' or self.mode == 'op':
                self._switch_to_offline()
                self.variables['StateOffAut'].write_value(False)

    def set_StateOffOp(self, value):
        if not self.state_channel and value:
            if self.mode == 'aut' or self.mode == 'op':
                self._switch_to_offline()
                self.variables['StateOffOp'].write_value(False)

    def set_StateOpAut(self, value):
        if self.state_channel and value:
            if self.mode == 'off' or self.mode == 'aut':
                self._switch_to_operator()
                self.variables['StateOpAut'].write_value(False)

    def set_StateOpOp(self, value):
        if not self.state_channel and value:
            if self.mode == 'off' or self.mode == 'aut':
                self._switch_to_operator()
                self.variables['StateOpOp'].write_value(False)

    def add_cb_exit_offline_mode(self, callback):
        self.cb_exit_offline_mode = callback

