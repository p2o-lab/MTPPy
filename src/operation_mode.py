from src.variable import Variable


class OperationMode:

    def __init__(self, opcua_server, opcua_ns, opcua_prefix, source_mode):
        self.source_channel = False
        self.operation_mode = 'off'

        self.source_mode = source_mode

        self.variables = {}

        self.opcua_server = opcua_server
        self.opcua_ns = opcua_ns
        self.opcua_prefix = f'{opcua_prefix}.operation_mode'

        self._attach_opcua_nodes()

    def _attach_opcua_nodes(self):

        variables = {
            'SrcChannel': {'init_value': False, 'callback': self.set_SrcChannel, 'writable': True},
            'SrcExtAut': {'init_value': False, 'callback': self.set_SrcExtAut, 'writable': True},
            'SrcIntOp': {'init_value': False, 'callback': self.set_SrcIntOp, 'writable': True},
            'SrcIntAut': {'init_value': False, 'callback': self.set_SrcIntAut, 'writable': True},
            'SrcExtOp': {'init_value': False, 'callback': self.set_SrcExtOp, 'writable': True},
            'SrcIntAct': {'init_value': False, 'callback': None, 'writable': False},
            'SrcExtAct': {'init_value': False, 'callback': None, 'writable': False},
         }

        for var_name, var_dict in variables.items():
            var_opcua_node_obj = self.opcua_server.get_node(f'ns={self.opcua_ns};s={self.opcua_prefix}.{var_name}')
            self.variables[var_name] = Variable(var_name, init_value=var_dict['init_value'],
                                                opcua_node_obj=var_opcua_node_obj,
                                                writable=var_dict['writable'],
                                                callback=var_dict['callback'])

    def _switch_to_offline(self):
        self.mode = 'off'
        self.variables['SrcIntAct'].write_value(False)
        self.variables['SrcExtAct'].write_value(False)
        print('off')

    def _switch_to_internal(self):
        self.mode = 'int'
        self.variables['SrcIntAct'].write_value(True)
        self.variables['SrcExtAct'].write_value(False)
        print('int')

    def _switch_to_external(self):
        self.mode = 'ext'
        self.variables['SrcIntAct'].write_value(True)
        self.variables['SrcExtAct'].write_value(False)
        print('ext')

    def set_SrcChannel(self, value):
        self.source_channel = value
        print('source channel to %s' % value)

    def set_SrcExtAut(self, value):
        if self.source_mode.mode != 'off':
            if self.source_channel and value and self.source_mode == 'int':
                self._switch_to_external()
                self.variables['SrcExtAut'].write_value(False)

    def set_SrcExtOp(self, value):
        if self.source_mode.mode != 'off':
            if not self.source_channel and value and self.source_mode == 'int':
                self._switch_to_external()
                self.variables['SrcExtOp'].write_value(False)

    def set_SrcIntAut(self, value):
        if self.source_mode.mode != 'off':
            if self.source_channel and value and self.source_mode == 'ext':
                self._switch_to_internal()
                self.variables['SrcIntAut'].write_value(False)

    def set_SrcIntOp(self, value):
        if self.source_mode.mode != 'off':
            if not self.source_channel and value and self.source_mode == 'ext':
                self._switch_to_internal()
                self.variables['SrcIntOp'].write_value(False)
