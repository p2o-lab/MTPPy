import logging
from opcua import Server, ua
from mtppy.communication_object import OPCUACommunicationObject
from mtppy.service import Service
from mtppy.suc_data_assembly import SUCDataAssembly, SUCActiveElement
from mtppy.mtp_generator import MTPGenerator


class OPCUAServerPEA:
    def __init__(self, mtp_generator: MTPGenerator = None, endpoint: str ='opc.tcp://127.0.0.1:4840/'):
        """
        Defines an OPC UA server for PEA.
        :param mtp_generator: Instance of an MTP generator. If specified, an MTP file is generated each time
        the class is instantiated. If not specified, no MTP file is going to be generated.
        :param endpoint: Endpoint of the OPC UA server. If not specified, opc.tcp://0.0.0.0:4840/ is used.
        """
        self.service_set = {}
        self.active_elements = {}
        self.endpoint = endpoint
        self.opcua_server = None
        self.opcua_ns = 3
        self.subscription_list = SubscriptionList()
        self._init_opcua_server()
        self.mtp = mtp_generator

    def add_service(self, service: Service):
        """
        Add a service to the PEA.
        :param service: Service instance.
        :return:
        """
        self.service_set[service.tag_name] = service

    def add_active_element(self, active_element: SUCActiveElement):
        """
        Add an active element to the PEA.
        :param active_element: Active element (e.g. AnaVlv, BinVlv, etc.)
        :return:
        """
        self.active_elements[active_element.tag_name] = active_element

    def _init_opcua_server(self):
        """
        Initialises an OPC UA server and sets the endpoint.
        :return:
        """
        logging.info(f'Initialisation of OPC UA server: {self.endpoint}')
        self.opcua_server = Server()
        self.opcua_server.set_endpoint(self.endpoint)
        # self.opcua_ns = self.opcua_server.register_namespace('namespace_idx')

    def get_opcua_server(self):
        """
        Get an OPC UA server instance object.
        :return:
        """
        return self.opcua_server

    def get_opcua_ns(self):
        """
        Get an OPC UA server namespace index.
        :return:
        """
        return self.opcua_ns

    def run_opcua_server(self):
        """
        Starts the OPC UA server instance.
        :return:
        """
        self.opcua_server.start()
        self._build_opcua_server()
        self._start_subscription()

    def set_services_in_idle(self):
        for service in self.service_set.values():
            service.init_idle_state()

    def _build_opcua_server(self):
        """
        Creates an OPC UA server instance including required nodes according to defined data assemblies.
        :return:
        """
        logging.info(f'Adding OPC UA nodes to the server structure according to the PEA structure:')
        ns = self.opcua_ns
        server = self.opcua_server.get_objects_node()

        services_node_id = f'ns={ns};s=services'
        services_node = server.add_folder(services_node_id, "services")

        # initiate a new MTP that will be added to InstanceHierarchy: ModuleTypePackage
        if self.mtp:
            self.mtp.add_module_type_package('1.0.0', name='mtp_test', description='')

        # add InternalElement opcua server to ModuleTypePackage/CommunicationSet/SourceList
        if self.mtp:
            self.mtp.add_opcua_server(self.endpoint)

        for service in self.service_set.values():
            logging.info(f'- service {service.tag_name}')
            self._create_opcua_objects_for_folders(service, services_node_id, services_node)

        act_elem_node_id = f'ns={ns};s=active_elements'
        act_elem_node = server.add_folder(act_elem_node_id, "active_elements")
        for active_element in self.active_elements.values():
            logging.info(f'- active element {active_element.tag_name}')
            self._create_opcua_objects_for_folders(active_element, act_elem_node_id, act_elem_node)

        # add SupportedRoleClass to all InternalElements
        if self.mtp:
            self.mtp.apply_add_supported_role_class()

        # export manifest.aml
        if self.mtp:
            logging.info(f'MTP manifest export to {self.mtp.export_path}')
            self.mtp.export_manifest()

    def _create_opcua_objects_for_folders(self, data_assembly: SUCDataAssembly, parent_opcua_prefix: str, parent_opcua_object):
        """
        Iterates over data assemblies to create OPC UA folders.
        :param data_assembly: Data assembly.
        :param parent_opcua_prefix: Prefix as a string to add in front of the data assembly tag.
        :param parent_opcua_object: Parent OPC UA node where the data assembly is to add to.
        :return:
        """
        da_node_id = f'{parent_opcua_prefix}.{data_assembly.tag_name}'
        da_node = parent_opcua_object.add_folder(da_node_id, data_assembly.tag_name)

        # type of data assembly (e.g. services, active_elements, procedures etc.)
        da_type = parent_opcua_prefix.split('=')[-1].split('.')[-1]

        folders = ['configuration_parameters', 'procedures','procedure_parameters',
                   'process_value_ins', 'report_values', 'process_value_outs']
        leaves = ['op_src_mode', 'state_machine', 'procedure_control']

        # create instance of  ServiceControl, HealthStateView, DIntServParam etc.
        if self.mtp:
            instance = self.mtp.create_instance(data_assembly, da_node_id)
        else:
            instance = None

        if self.mtp:
            link_id = self.mtp.random_id_generator()
            if da_type == 'services' or da_type in folders:
                link_id = self.mtp.create_components_for_services(data_assembly, da_type)
        else:
            link_id = None

        if hasattr(data_assembly, 'attributes'):
            self._create_opcua_objects_for_leaves(data_assembly, da_node_id, da_node, instance)

        for section_name in folders + leaves:
            if not hasattr(data_assembly, section_name):
                continue
            section = eval(f'data_assembly.{section_name}')
            section_node_id = f'{da_node_id}.{section_name}'
            section_node = da_node.add_folder(section_node_id, section_name)
            if section_name in folders:
                for parameter in eval(f'data_assembly.{section_name}.values()'):
                    self._create_opcua_objects_for_folders(parameter, section_node_id, section_node)
            if section_name in leaves:
                self._create_opcua_objects_for_leaves(section, section_node_id, section_node, instance)

        # create linked obj between instance and service component
        if self.mtp:
            self.mtp.add_linked_attr(instance, link_id)

    def _create_opcua_objects_for_leaves(self, opcua_object, parent_opcua_prefix: str, parent_opcua_object, par_instance):
        """
        Iterates over end objects (leaves) of data assemblies to create corresponding OPC UA nodes.
        :param opcua_object: Element of a data assembly that an OPC UA node is to create for.
        :param parent_opcua_prefix: Prefix as a string to add in front of the data assembly tag.
        :param parent_opcua_object: Parent OPC UA node where the data assembly is to add to.
        :param par_instance: Parameter instance.
        :return:
        """
        for attr in opcua_object.attributes.values():
            attribute_node_id = f'{parent_opcua_prefix}.{attr.name}'

            # We attach communication objects to be able to write values on opcua server on attributes change
            opcua_type = self._infer_data_type(attr.type)
            opcua_node_obj = parent_opcua_object.add_variable(attribute_node_id, attr.name, attr.init_value,
                                                              varianttype=opcua_type)
            logging.debug(f'OPCUA Node: {attribute_node_id}, Name: {attr.name}, Value: {attr.init_value}')
            opcua_node_obj.set_writable(False)
            opcua_comm_obj = OPCUACommunicationObject(opcua_node_obj, node_id=opcua_node_obj)
            attr.attach_communication_object(opcua_comm_obj)

            if self.mtp:
                linked_id = self.mtp.random_id_generator()  # create linked-id for opc ua node
                # add opc ua node and its attributes to ModuleTypePackage/CommunicationSet/SourceList/OPCUAServer
                self.mtp.add_external_interface(attribute_node_id, self.opcua_ns, linked_id)
            else:
                linked_id = None

            """
            add attributes of data assembly to corresponding instance under InstanceList 
            e.g.: attributes of services belong to InstanceList/ServiceControl

            exception: some attributes of procedure ('ProcedureId', 'IsSelfCompleting', 'IsDefault') should be 
            added to InstanceHierarchy_Service/service/procedure. The other attributes of procedure should belong to 
            InstanceList/HeathStateView
            """
            if type(opcua_object).__name__ == 'Procedure' and attr.name in ['ProcedureId', 'IsSelfCompleting', 'IsDefault']:
                pass
            else:
                if self.mtp:
                    self.mtp.add_attr_to_instance(par_instance, attr.name, attr.init_value, linked_id)

            # We subscribe to nodes that are writable attributes
            if attr.sub_cb is not None:
                opcua_node_obj.set_writable(True)
                self.subscription_list.append(opcua_node_obj, attr.sub_cb)

    @staticmethod
    def _infer_data_type(attribute_data_type):
        """
        Translate a python data type to a suitable OPC UA data type.
        :param attribute_data_type: Python variable.
        :return: OPC UA data type
        """
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

    def _start_subscription(self):
        """
        Subscribes to defined OPC UA nodes.
        :return:
        """
        handler = Marshalling()
        handler.import_subscription_list(self.subscription_list)
        sub = self.opcua_server.create_subscription(500, handler)
        handle = sub.subscribe_data_change(self.subscription_list.get_nodeid_list())


class SubscriptionList:
    def __init__(self):
        """
        Subscription list that contains all OPC UA nodes that PEA must subscribe to.
        """
        self.sub_list = {}

    def append(self, node_id, cb_value_change):
        """
        Add an subscription entity.
        :param node_id: OPC UA node.
        :param cb_value_change: Callback function for a value change.
        :return:
        """
        identifier = node_id.nodeid.Identifier
        self.sub_list[identifier] = {'node_id': node_id, 'callback': cb_value_change}

    def get_nodeid_list(self):
        """
        Extract a list of node ids in the subscription list.
        :return: List of node ids.
        """
        if len(self.sub_list) == 0:
            return None
        else:
            node_id_list = []
            for node_id in self.sub_list.values():
                node_id_list.append(node_id['node_id'])
            return node_id_list

    def get_callback(self, node_id):
        """
        Get a callback function for a specific OPC UA node.
        :param node_id: OPC UA node id
        :return:
        """
        identifier = node_id.nodeid.Identifier
        if identifier in self.sub_list.keys():
            return self.sub_list[identifier]['callback']
        else:
            return None


class Marshalling(object):
    def __init__(self):
        """
        Supplementary class for marshalling OPC UA subscriptions.
        """
        self.subscription_list = None

    def import_subscription_list(self, subscription_list: SubscriptionList):
        """
        Import a subscription list.
        :param subscription_list: Subscription list.
        :return:
        """
        self.subscription_list = subscription_list

    def datachange_notification(self, node, val, data):
        """
        Executes a callback function if data value changes.
        :param node: OPC UA node.
        :param val: Value after change.
        :param data: Not used.
        :return:
        """
        callback = self.find_set_callback(node)
        if callback is not None:
            try:
                callback(val)
            except Exception as exc:
                pass
                logging.warning(f'Something wrong with callback {callback}: {exc}')

    def find_set_callback(self, node_id):
        """
        Finds a callback function to a specific OPC UA node by nodeid.
        :param node_id: Node id.
        :return: Callback function.
        """
        return self.subscription_list.get_callback(node_id)
