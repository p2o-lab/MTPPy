from src.variable import Variable
from opcua import ua


class ControlElementsStringServParam:

    def __init__(self, opcua_server, opcua_ns, opcua_prefix, source_mode, operation_mode):

        self.source_mode = source_mode
        self.operation_mode = operation_mode

        self.variables = {}

        self.opcua_server = opcua_server
        self.opcua_ns = opcua_ns
        self.opcua_prefix = f'{opcua_prefix}.control_elements'

        self.source_mode = None
        self._attach_opcua_nodes()

    def _attach_opcua_nodes(self):

        variables = {
            'VExt': {'type': ua.VariantType.String, 'init_value': 0, 'callback': self.set_VExt, 'writable': True},
            'VOp': {'type': ua.VariantType.String, 'init_value': 0, 'callback': self.set_VOp, 'writable': True},
            'VInt': {'type': ua.VariantType.String, 'init_value': 0, 'callback': self.set_VInt, 'writable': True},
            'VReq': {'type': ua.VariantType.String, 'init_value': 0, 'callback': None, 'writable': False},
            'VOut': {'type': ua.VariantType.String, 'init_value': 0, 'callback': None, 'writable': False},
            'VFbk': {'type': ua.VariantType.String, 'init_value': 0, 'callback': None, 'writable': False},
            'Sync': {'type': ua.VariantType.Boolean, 'init_value': False, 'callback': None, 'writable': False}
        }

        for var_name, var_dict in variables.items():
            var_opcua_node_obj = self.opcua_server.get_node(f'ns={self.opcua_ns};s={self.opcua_prefix}.{var_name}')
            self.variables[var_name] = Variable(var_name,
                                                opcua_type=var_dict['type'],
                                                init_value=var_dict['init_value'],
                                                opcua_node_obj=var_opcua_node_obj,
                                                writable=var_dict['writable'],
                                                callback=var_dict['callback'])

    def set_VOp(self, value):
        print('VOp set to %s' % value)
        if self.operation_mode.mode is 'op':
            self.set_VReq(value)

    def set_VInt(self, value):
        print('VInt set to %s' % value)
        if self.operation_mode.mode is 'aut' and self.source_mode.mode is 'int':
            self.set_VReq(value)

    def set_VExt(self, value):
        print('VExt set to %s' % value)
        if self.operation_mode.mode is 'aut' and self.source_mode.mode is 'ext':
            self.set_VReq(value)

    def set_VReq(self, value):
        self.variables['VReq'].write_value(value)
        print('VReq set to %s' % value)

    def set_VOut(self):
        v_req = self.variables['VReq'].value
        self.variables['VOut'].write_value(v_req)
        print('VOut set to %s' % v_req)
