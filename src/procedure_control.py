from src.variable import Variable
from opcua import ua


class ProcedureControl:

    def __init__(self, opcua_server, opcua_ns, opcua_prefix, source_mode, operation_mode):
        self.procedure_op = 0
        self.procedure_int = 0
        self.procedure_ext = 0
        self.procedure_requested = 0
        self.procedure_current = 0

        self.source_mode = source_mode
        self.operation_mode = operation_mode

        self.variables = {}

        self.opcua_server = opcua_server
        self.opcua_ns = opcua_ns
        self.opcua_prefix = f'{opcua_prefix}.procedure_control'

        self._attach_opcua_nodes()

        self.procedures = []

    def _attach_opcua_nodes(self):

        variables = {
            'ProcedureOp': {'type': ua.VariantType.UInt32, 'init_value': 0, 'callback': self.set_ProcedureOp, 'writable': True},
            'ProcedureInt': {'type': ua.VariantType.UInt32, 'init_value': 0, 'callback': self.set_ProcedureInt, 'writable': True},
            'ProcedureExt': {'type': ua.VariantType.UInt32, 'init_value': 0, 'callback': self.set_ProcedureExt, 'writable': True},
            'ProcedureCur': {'type': ua.VariantType.UInt32, 'init_value': 0, 'callback': None, 'writable': False},
            'ProcedureReq': {'type': ua.VariantType.UInt32, 'init_value': 0, 'callback': None, 'writable': False},
        }

        for var_name, var_dict in variables.items():
            var_opcua_node_obj = self.opcua_server.get_node(f'ns={self.opcua_ns};s={self.opcua_prefix}.{var_name}')
            self.variables[var_name] = Variable(var_name, init_value=var_dict['init_value'],
                                                opcua_type=var_dict['type'],
                                                opcua_node_obj=var_opcua_node_obj,
                                                writable=var_dict['writable'],
                                                callback=var_dict['callback'])

    def set_ProcedureOp(self, value):
        self.procedure_op = value
        print('ProcedureOp set to %s' % value)
        self.select_procedure()

    def set_ProcedureInt(self, value):
        self.procedure_int = value
        print('ProcedureInt set to %s' % value)
        self.select_procedure()

    def set_ProcedureExt(self, value):
        self.procedure_ext = value
        print('ProcedureExt set to %s' % value)
        self.select_procedure()

    def select_procedure(self):
        if self.operation_mode.mode is not 'off':
            if self.operation_mode.variables['StateOpAct']:
                self.procedure_requested = self.procedure_op
                self.procedure_current = self.procedure_requested
            elif self.operation_mode.variables['StateAutAct'] and self.source_mode.variables['SrcIntAct']:
                self.procedure_requested = self.procedure_int
                self.procedure_current = self.procedure_requested
            elif self.operation_mode.variables['StateAutAct'] and self.source_mode.variables['SrcExtAct']:
                self.procedure_requested = self.procedure_ext
                self.procedure_current = self.procedure_requested

            self.variables['ProcedureReq'].write_value(self.procedure_requested)
            self.variables['ProcedureCur'].write_value(self.procedure_current)
            print('ProcedureReq set to %s' % self.procedure_requested)
            print('ProcedureCur set to %s' % self.procedure_current)

    def add_procedure(self, procedure):
        self.procedures.append(procedure)
