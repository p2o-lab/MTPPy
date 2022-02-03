from src.variable import Variable


class SourceMode:

    def __init__(self, opcua_server, opcua_ns, opcua_prefix):
        self.state_channel = False
        self.mode = 'off'

        self.variables = {}

        self.opcua_server = opcua_server
        self.opcua_ns = opcua_ns
        self.opcua_prefix = f'{opcua_prefix}.source_mode'

        self._attach_opcua_nodes()

    def _attach_opcua_nodes(self):

        variables = {
            'StateChannel': {'init_value': False, 'callback': self.set_StateChannel, 'writable': True},
            'StateOffAut': {'init_value': False, 'callback': self.set_StateOffAut, 'writable': True},
            'StateOpAut': {'init_value': False, 'callback': self.set_StateOpAut, 'writable': True},
            'StateAutAut': {'init_value': False, 'callback': self.set_StateAutAut, 'writable': True},
            'StateOffOp': {'init_value': False, 'callback': self.set_StateOffOp, 'writable': True},
            'StateOpOp': {'init_value': False, 'callback': self.set_StateOpOp, 'writable': True},
            'StateAutOp': {'init_value': False, 'callback': self.set_StateAutOp, 'writable': True},
            'StateOpAct': {'init_value': False, 'callback': None, 'writable': False},
            'StateAutAct': {'init_value': False, 'callback': None, 'writable': False},
            'StateOffAct': {'init_value': True, 'callback': None, 'writable': False}
        }

        for var_name, var_dict in variables.items():
            var_opcua_node_obj = self.opcua_server.get_node(f'ns={self.opcua_ns};s={self.opcua_prefix}.{var_name}')
            self.variables[var_name] = Variable(var_name, init_value=var_dict['init_value'],
                                                opcua_node_obj=var_opcua_node_obj,
                                                writable=var_dict['writable'],
                                                callback=var_dict['callback'])

    def _switch_to_offline(self):
        self.mode = 'off'
        self.variables['StateOpAct'].write_value(False)
        self.variables['StateAutAct'].write_value(False)
        self.variables['StateOffAct'].write_value(True)
        print('off')

    def _switch_to_automatic(self):
        self.mode = 'aut'
        self.variables['StateOpAct'].write_value(False)
        self.variables['StateAutAct'].write_value(True)
        self.variables['StateOffAct'].write_value(False)
        print('aut')

    def _switch_to_operator(self):
        self.mode = 'op'
        self.variables['StateOpAct'].write_value(True)
        self.variables['StateAutAct'].write_value(False)
        self.variables['StateOffAct'].write_value(False)
        print('op')

    def set_StateChannel(self, value):
        self.state_channel = value
        print('state channel to %s' % value)

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
