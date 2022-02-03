from src.variable import Variable


class CommandControl:

    def __init__(self, opcua_server, opcua_ns, opcua_prefix, source_mode, operation_mode):
        self.source_mode = source_mode
        self.operation_mode = operation_mode

        self.variables = {}

        self.opcua_server = opcua_server
        self.opcua_ns = opcua_ns
        self.opcua_prefix = f'{opcua_prefix}.command_control'

        self._attach_opcua_nodes()

    def _attach_opcua_nodes(self):

        variables = {
            'CommandOp': {'init_value': 0, 'callback': self.set_CommandOp, 'writable': True},
            'CommandInt': {'init_value': 0, 'callback': self.set_CommandInt, 'writable': True},
            'CommandExt': {'init_value': 0, 'callback': self.set_CommandExt, 'writable': True},
        }

        for var_name, var_dict in variables.items():
            var_opcua_node_obj = self.opcua_server.get_node(f'ns={self.opcua_ns};s={self.opcua_prefix}.{var_name}')
            self.variables[var_name] = Variable(var_name, init_value=var_dict['init_value'],
                                                opcua_node_obj=var_opcua_node_obj,
                                                writable=var_dict['writable'],
                                                callback=var_dict['callback'])

    def set_CommandOp(self, value):
        pass

    def set_CommandInt(self, value):
        pass

    def set_CommandExt(self, value):
        pass

