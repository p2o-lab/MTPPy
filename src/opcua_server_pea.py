from opcua import Server, ua
from src.communication_object import OPCUACommunicationObject


class OPCUAServerPEA:
    def __init__(self, endpoint='opc.tcp://0.0.0.0:4840/'):
        self.service_set = {}
        self.endpoint = endpoint
        self.opcua_server = None
        self.opcua_ns = 3
        self.subscription_list = SubscriptionList()
        self.init_opcua_server()

    def add_service(self, service):
        self.service_set[service.tag_name] = service

    def init_opcua_server(self):
        self.opcua_server = Server()
        self.opcua_server.set_endpoint(self.endpoint)
        #self.opcua_ns = self.opcua_server.register_namespace('namespace_idx')

    def get_opcua_server(self):
        return self.opcua_server

    def get_opcua_ns(self):
        return self.opcua_ns

    def run_opcua_server(self):
        self.opcua_server.start()
        self.build_opcua_server()
        self.start_subscription()
        #self.set_services_in_idle()

    def set_services_in_idle(self):
        for service in self.service_set.values():
            service.init_idle_state()

    def build_opcua_server(self):
        ns = self.opcua_ns
        server = self.opcua_server.get_objects_node()

        services_node_id = f'ns={ns};s=services'
        services_node = server.add_folder(services_node_id, "services")
        for service in self.service_set.values():
            self._create_opcua_objects_for_data_assemblies(service, services_node_id, services_node)

    def _create_opcua_objects_for_data_assemblies(self, data_assembly, parent_opcua_prefix, parent_opcua_object):
        da_node_id = f'{parent_opcua_prefix}.{data_assembly.tag_name}'
        da_node = parent_opcua_object.add_folder(da_node_id, data_assembly.tag_name)
        for section_name in ['op_src_mode', 'state_machine', 'control_elements', 'configuration_parameters',
                             'procedure_control']:
            if not hasattr(data_assembly, section_name):
                continue
            section = eval(f'data_assembly.{section_name}')
            section_node_id = f'{da_node_id}.{section_name}'
            print(section_node_id)
            section_node = da_node.add_folder(section_node_id, section_name)
            if section_name in ['op_src_mode', 'state_machine', 'control_elements', 'procedure_control']:
                self._create_opcua_objects_for_attributes(section, section_node_id, section_node)
            elif section_name in ['configuration_parameters']:
                for parameter in data_assembly.configuration_parameters.values():
                    self._create_opcua_objects_for_data_assemblies(parameter, section_node_id, section_node)

    def _create_opcua_objects_for_attributes(self, object, parent_opcua_prefix, parent_opcua_object):
        for attr in object.attributes.values():
            attribute_node_id = f'{parent_opcua_prefix}.{attr.name}'

            # We attach communication objects to be able to write values on opcua server on attributes change
            opcua_node_obj = parent_opcua_object.add_variable(attribute_node_id, attr.name, attr.init_value,
                                                              datatype=None)
            print(f'OPCUA Node: {attribute_node_id}, Name: {attr.name}, Value: {attr.init_value}')
            opcua_node_obj.set_writable(False)
            opcua_comm_obj = OPCUACommunicationObject(opcua_node_obj, node_id=opcua_node_obj)
            attr.attach_communication_object(opcua_comm_obj)

            # We subscribe to nodes that are writable attributes
            if attr.cb_value_change is not None:
                opcua_node_obj.set_writable(True)
                self.subscription_list.append(opcua_node_obj, attr.cb_value_change)

    def infere_data_type(self, attribute_data_type):
        if attribute_data_type == int:
            return ua.VariantType.Int64
        elif attribute_data_type == float:
            return ua.VariantType.Float
        elif attribute_data_type == bool:
            return ua.VariantType.Boolean
        elif attribute_data_type == str:
            return ua.VariantType.String
        else:
            return None

    def start_subscription(self):
        handler = Marshalling()
        handler.import_subscription_list(self.subscription_list)
        sub = self.opcua_server.create_subscription(500, handler)
        handle = sub.subscribe_data_change(self.subscription_list.get_nodeid_list())


class SubscriptionList:
    def __init__(self):
        self.sub_list = {}

    def append(self, node_id, cb_value_change):
        identifier = node_id.nodeid.Identifier
        self.sub_list[identifier] = {'node_id': node_id, 'callback': cb_value_change}

    def get_nodeid_list(self):
        if len(self.sub_list) == 0:
            return None
        else:
            node_id_list = []
            for node_id in self.sub_list.values():
                node_id_list.append(node_id['node_id'])
            return node_id_list

    def get_callback(self, node_id):
        identifier = node_id.nodeid.Identifier
        if identifier in self.sub_list.keys():
            return self.sub_list[identifier]['callback']
        else:
            return None


class Marshalling(object):
    def import_subscription_list(self, subscription_list: SubscriptionList):
        self.subscription_list = subscription_list

    def datachange_notification(self, node, val, data):
        # print("Data change event", node, val)
        callback = self.find_set_callback(node)
        if callback is not None:
            callback(val)

    def find_set_callback(self, node_id):
        return self.subscription_list.get_callback(node_id)
