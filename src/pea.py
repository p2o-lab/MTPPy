from opcua import Server


class PEA:
    def __init__(self, endpoint='opc.tcp://0.0.0.0:4840/'):
        self.endpoint = endpoint
        self.opcua_server = None
        self.opcua_idx = None
        self.service_set = {}
        self.subscription_list = []
        self.init_opcua_server()

    def init_opcua_server(self):
        self.opcua_server = Server()
        self.opcua_server.set_endpoint(self.endpoint)
        self.opcua_idx = self.opcua_server.register_namespace('namespace_idx')

    def get_server_obj(self):
        return self.opcua_server

    def get_server_ns(self):
        return self.opcua_idx

    def create_nodes(self):
        idx = self.opcua_idx
        ns = 3
        objects = self.opcua_server.get_objects_node()

        services_folder_nodeid = f'ns={ns};s=services'
        services_folder = objects.add_folder(services_folder_nodeid, "services")

        subscription_list = []

        for service in self.service_set.values():
            service_folder_nodeid = services_folder_nodeid + '.' + service.tag_name
            service_folder = services_folder.add_folder(service_folder_nodeid, service.tag_name)

            for folder in ['source_mode', 'operation_mode', 'state_machine', 'procedure_control']:
                service_section_folder_nodeid = service_folder_nodeid + '.' + folder
                service_section_folder = service_folder.add_folder(service_section_folder_nodeid, folder)

                for variable in eval(f'service.{folder}.variables.values()'):
                    service_section_folder.add_variable(variable.opcua_node_obj.nodeid, variable.name,
                                                        variable.init_value). \
                        set_writable(variable.writable)
                    opcua_node = self.opcua_server.get_node(variable.opcua_node_obj)
                    subscription_list.append(opcua_node)

            config_parameters_folder_nodeid = service_folder_nodeid + '.configuration_parameters'
            config_parameters_folder = service_folder.add_folder(config_parameters_folder_nodeid, 'configuration_parameters')
            for config_parameter in service.configuration_parameters.values():
                config_parameter_folder_nodeid = config_parameters_folder_nodeid + '.' + config_parameter.tag_name
                config_parameter_folder = config_parameters_folder.add_folder(config_parameter_folder_nodeid, config_parameter.tag_name)
                for folder in ['source_mode', 'operation_mode', 'control_elements']:
                    config_parameter_section_folder_nodeid = config_parameter_folder_nodeid + '.' + folder
                    config_parameter_section_folder = config_parameter_folder.add_folder(
                        config_parameter_section_folder_nodeid, folder)

                    for variable in eval(f'config_parameter.{folder}.variables.values()'):
                        config_parameter_section_folder.add_variable(variable.opcua_node_obj.nodeid, variable.name,
                                                            variable.init_value). \
                            set_writable(variable.writable)
                        opcua_node = self.opcua_server.get_node(variable.opcua_node_obj)
                        subscription_list.append(opcua_node)


        self.subscription_list = subscription_list

    def start_subscription(self):
        handler = Marshalling()
        handler.import_service_set(self.service_set)
        sub = self.opcua_server.create_subscription(500, handler)
        handle = sub.subscribe_data_change(self.subscription_list)

    def run_opcua_server(self):
        self.opcua_server.start()
        self.create_nodes()
        self.start_subscription()

    def add_service(self, service):
        self.service_set[service.tag_name] = service


class Marshalling(object):
    def import_service_set(self, services):
        self.service_set = services

    def datachange_notification(self, node, val, data):
        #print("Data change event", node, val)
        callback = self.find_set_callback(node)
        if callback is not None:
            callback(val)

    def find_set_callback(self, node_id):
        layers = node_id.nodeid.Identifier.split('.')
        if layers[0] == 'services':
            service_name = layers[1]
            if layers[2] == 'source_mode':
                var_name = layers[3]
                return self.service_set[service_name].source_mode.variables[var_name].callback
            if layers[2] == 'operation_mode':
                var_name = layers[3]
                return self.service_set[service_name].operation_mode.variables[var_name].callback
            if layers[2] == 'state_machine':
                var_name = layers[3]
                return self.service_set[service_name].state_machine.variables[var_name].callback
            if layers[2] == 'procedure_control':
                var_name = layers[3]
                return self.service_set[service_name].procedure_control.variables[var_name].callback
            if layers[2] in 'configuration_parameters':
                parameter_name = layers[3]
                if layers[4] == 'source_mode':
                    var_name = layers[5]
                    return self.service_set[service_name].configuration_parameters[parameter_name].source_mode.variables[var_name].callback
                if layers[4] == 'operation_mode':
                    var_name = layers[5]
                    return self.service_set[service_name].configuration_parameters[parameter_name].operation_mode.variables[var_name].callback
                if layers[4] == 'control_elements':
                    var_name = layers[5]
                    return self.service_set[service_name].configuration_parameters[parameter_name].control_elements.variables[var_name].callback
