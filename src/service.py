from src.source_mode import SourceMode
from src.operation_mode import OperationMode
from src.variable import Variable


class Service:
    def __init__(self, tag_name, opcua_server, opcua_ns):
        self.tag_name = tag_name
        self.opcua_prefix = f'services.{tag_name}'
        self.opcua_server = opcua_server
        self.opcua_ns = opcua_ns

        self.source_mode = SourceMode(opcua_server, opcua_ns, self.opcua_prefix)
        self.operation_mode = OperationMode(opcua_server, opcua_ns, self.opcua_prefix, self.source_mode)

        self.configuration_parameters = []

        self.WQC = 255
        self.OSLevel = 0

        self.variables = {}
        serv_variables = {
            'CommandOp': False,
            'CommandInt': False,
            'CommandExt': False,
            'ProcedureOp': False,
            'ProcedureInt': False,
            'ProcedureExt': False,
            'ProcedureCur': 0,
            'ProcedureReq': 0,
            'PosTextID': 0,
            'InteractQuestionID': 0,
            'InteractAnswerID': 0
        }

        for var_name, var_init_value in serv_variables.items():
            var_opcua_node_obj = self.opcua_server.get_node(f'ns={self.opcua_ns};s={self.opcua_prefix}.{var_name}')
            self.variables[var_name] = Variable(var_name, var_init_value, var_opcua_node_obj)

