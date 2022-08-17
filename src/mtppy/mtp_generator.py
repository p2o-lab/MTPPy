from mtppy.suc_data_assembly import *
import xml.etree.ElementTree as ET
import random
import string


class MTPGenerator:
    def __init__(self, writer_infos: dict, export_path: str, manifest_template_path: str):
        """
        Represents an MTP generator.
        :param writer_infos: Writer info section that will be put in the header of the generate manifest.
        :param export_path: Path where to save the generated MTP manifest.
        :param manifest_template_path: Path where the manifest template is placed.
        """

        # path of a manifest template containing general infos
        self.template_path = manifest_template_path
        self.writer_infos = writer_infos  # infos about manifest writer is configurable

        self.tree = ET.parse(self.template_path)
        self.root = self.tree.getroot()
        self.export_path = export_path  # path of generated manifest

        # first layer: instance hierarchy MTP and instance hierarchy service
        self.instance_hierarchy_mtp = None
        self.instance_hierarchy_service = None

        # instance hierarchy MTP layer: internal element module type package
        self.module_type_package = None

        # internal element module type package layer: communication set and services set
        self.communication_set = None
        self.services_set = None

        # communication set layer: instance list and source list
        self.instance_list = None
        self.source_list = None

        # source list layer: internal element opcua server
        self.opcua_server = None

        # instance hierarchy service layer: internal element service
        self.service = None

        # layer: instance hierarchy service/internal element service/internal element procedure
        self.service_procedure = None

        self.__init_manifest()  # add first layers (instance hierarchies mtp and service) to manifest
        self.__init_instance_hierarchies()  # add attributes for instance hierarchies mtp and service
        self.edit_writer_information()

    def __init_manifest(self):
        self.instance_hierarchy_mtp = ET.SubElement(self.root, "InstanceHierarchy")
        self.instance_hierarchy_service = ET.SubElement(self.root, "InstanceHierarchy")

    def __init_instance_hierarchies(self):
        # instance hierarchy:  ModuleTypePackage
        self.instance_hierarchy_mtp.set('Name', 'ModuleTypePackage')
        self.instance_hierarchy_mtp.set('ID', self.random_id_generator())

        # instance hierarchy: Service
        service_instance_hierarchy_id = self.random_id_generator()
        self.instance_hierarchy_service.set('Name', service_instance_hierarchy_id)
        self.instance_hierarchy_service.set('ID', service_instance_hierarchy_id)

    def edit_writer_information(self):
        writer_header = self.root.find('AdditionalInformation/WriterHeader')
        for writer_info in writer_header.findall('./'):
            if writer_info.tag in list(self.writer_infos.keys()):
                writer_info.text = self.writer_infos[writer_info.tag]
            else:
                raise KeyError('key of writer info dict is not correct')

    def add_module_type_package(self, version: str, name: str, description: str):
        """
        add internal element module type package to instance hierarchy mtp
        :param version: version of mtp
        :param name: name of mtp
        :param description: description of mtp
        """

        # create internal element
        self.module_type_package = ET.Element("InternalElement",
                                              {'Name': name, 'ID': self.random_id_generator(),
                                               'RefBaseSystemUnitPath': 'MTPSUCLib/ModuleTypePackage'})
        # add sub-elements to internal element mtp
        mtp_description = ET.SubElement(self.module_type_package, 'Description')
        mtp_description.text = description
        mtp_version = ET.SubElement(self.module_type_package, 'Version')
        mtp_version.text = version
        self.instance_hierarchy_mtp.append(self.module_type_package)
        self.__add_communication_set()
        self.__add_services_set(self.instance_hierarchy_service.get('ID'))

    def __add_communication_set(self):
        # add communication set to internal element module type package
        self.communication_set = ET.SubElement(self.module_type_package, 'InternalElement')
        self.generate_attributes(self.communication_set, 'Communication', self.random_id_generator(),
                                 'MTPSUCLib/CommunicationSet')
        self.instance_list = ET.SubElement(self.communication_set, 'InternalElement')
        self.generate_attributes(self.instance_list, 'InstanceList', self.random_id_generator(),
                                 'MTPSUCLib/CommunicationSet/InstanceList')
        self.source_list = ET.SubElement(self.communication_set, 'InternalElement')
        self.generate_attributes(self.source_list, 'SourceList', self.random_id_generator(),
                                 'MTPSUCLib/CommunicationSet/SourceList')

    def create_instance(self, data_assembly: SUCDataAssembly, opc_node_id: str) -> ET.Element:
        """
        create instance for each data assembly
        :param data_assembly: data assembly object
        :param opc_node_id: opcua node id used to construct instance name
        :return: manifest instance of data assembly
        """
        instance_id = self.random_id_generator()
        instance_name = opc_node_id.split('=')[-1]
        instance_basic_type = data_assembly.__class__.__bases__[-1].__name__
        instance_type_name = type(data_assembly).__name__
        instance = self.add_data_assembly_to_instance_list(instance_name, instance_id, instance_basic_type,
                                                           instance_type_name)

        return instance

    def add_data_assembly_to_instance_list(self, instance_name: str, instance_id: str,
                                           instance_basic_type: str, instance_type_name: str) -> ET.Element:
        """
        add data object (subclasses of data assembly) to instance list
        :param instance_name: name of data object
        :param instance_id: id of data object
        :param instance_basic_type: type of data assembly (service, Procedure, operation element etc.)
        :param instance_type_name: used to distinguish data objects that have the same parent type (e.g. AnaSerParam,
        StringSerParam, DIntSerParam, etc.)
        :return: instance of data assembly
        """
        if instance_basic_type == 'Service':
            name = instance_name + '.ServiceControl'
            reference_path = 'MTPDataObjectSUCLib/DataAssembly/ServiceControl'
        elif instance_basic_type == 'SUCServiceProcedure':
            name = instance_name + '.HealthStateView'
            reference_path = 'MTPDataObjectSUCLib/DataAssembly/DiagnosticElement/HealthStateView'
        elif instance_basic_type == 'SUCOperationElement':
            name = instance_name
            reference_path = 'MTPDataObjectSUCLib/DataAssembly/OperationElement/' + instance_type_name
        elif instance_basic_type == 'SUCIndicatorElement':
            name = instance_name
            reference_path = 'MTPDataObjectSUCLib/DataAssembly/IndicatorElement/' + instance_type_name
        elif instance_basic_type == 'SUCActiveElement':
            name = instance_name
            reference_path = 'MTPDataObjectSUCLib/DataAssembly/ActiveElement/' + instance_type_name
        else:
            raise TypeError('data assembly type error')

        instance = ET.SubElement(self.instance_list, 'InternalElement')

        # add instance attributes
        self.generate_attributes(instance, name, instance_id, reference_path)

        return instance

    def create_components_for_services(self, data_assembly: SUCDataAssembly, section: str) -> str:
        """
        create components for InstanceHierarchy Services
        :param parent_elem: parent element of current component (e.g. parent of a procedure is a service)
        :param data_assembly: data assembly object
        :return: component of services: eg. service, procedure, config parameter, procedure parameter etc.
        """
        services_component_id = self.random_id_generator()
        link_id = self.add_components_to_services(data_assembly, services_component_id, section)

        # link_id: each component of services is through link_id linked to an InternalElement in InstanceList
        return link_id

    def add_components_to_services(self, data_assembly: SUCDataAssembly, sc_id: str, section: str) -> str:
        """
        add services and its components (config param, procedure, procedure param etc.) to InstanceHierarchy: Services
        s_component: service component
        """
        service_component_name = data_assembly.tag_name
        if section == 'services':
            s_component = ET.SubElement(self.instance_hierarchy_service, 'InternalElement')
            self.service = s_component
            s_component.set('RefBaseSystemUnitPath', 'MTPServiceSUCLib/Service')

        elif section == 'configuration_parameters':
            s_component = ET.SubElement(self.service, 'InternalElement')
            s_component.set('RefBaseSystemUnitPath', 'MTPServiceSUCLib/ServiceParameter/ConfigurationParameter')

        elif section == 'procedures':
            s_component = ET.SubElement(self.service, 'InternalElement')
            self.service_procedure = s_component
            s_component.set('RefBaseSystemUnitPath', 'MTPServiceSUCLib/ServiceProcedure')
            attr = ET.SubElement(s_component, 'Attribute')
            attr.set('Name', 'ProcedureID')
            attr.set('AttributeDataType', 'xs:IDREF')
            attr_value = ET.SubElement(attr, 'Value')
            attr_value.text = str(data_assembly.attributes['ProcedureId'].value)

            attr = ET.SubElement(s_component, 'Attribute')
            attr.set('Name', 'IsDefault')
            attr.set('AttributeDataType', 'xs:IDREF')
            attr_value = ET.SubElement(attr, 'Value')
            attr_value.text = str(data_assembly.attributes['IsDefault'].value)

            attr = ET.SubElement(s_component, 'Attribute')
            attr.set('Name', 'IsSelfCompleting')
            attr.set('AttributeDataType', 'xs:IDREF')
            attr_value = ET.SubElement(attr, 'Value')
            attr_value.text = str(data_assembly.attributes['IsSelfCompleting'].value)

        elif section == 'procedure_parameters':
            s_component = ET.SubElement(self.service_procedure, 'InternalElement')
            s_component.set('RefBaseSystemUnitPath', 'MTPServiceSUCLib/ServiceParameter/ProcedureParameter')

        elif section == 'process_value_ins':
            s_component = ET.SubElement(self.service_procedure, 'InternalElement')
            s_component.set('RefBaseSystemUnitPath', 'MTPServiceSUCLib/ServiceParameter/ProcessValueIn')

        elif section == 'report_values':
            s_component = ET.SubElement(self.service_procedure, 'InternalElement')
            s_component.set('RefBaseSystemUnitPath', 'MTPServiceSUCLib/ServiceParameter/ReportValue')

        elif section == 'process_value_outs':
            s_component = ET.SubElement(self.service_procedure, 'InternalElement')
            s_component.set('RefBaseSystemUnitPath', 'MTPServiceSUCLib/ServiceParameter/ProcessValueOut')

        else:
            raise TypeError('service components type error')

        link_id = self.random_id_generator()

        s_component.set('Name', service_component_name)
        s_component.set('ID', sc_id)

        self.add_linked_attr(s_component, link_id)

        return link_id

    @staticmethod
    def add_linked_attr(parent: ET.Element, link_id: str):
        """
        add attribute whose value refers to an InternalElement under InstanceList
        :param parent: parent of attribute
        :param link_id: id linking to another element
        """
        attr = ET.SubElement(parent, 'Attribute')
        attr.set('Name', 'RefID')
        attr.set('AttributeDataType', 'xs:ID')
        attr_value = ET.SubElement(attr, 'Value')
        attr_value.text = link_id

    def __add_services_set(self, linked_id: str):
        """
        ServiceSet is an InternalElement which belongs to ModuleTypePackage
        :param linked_id: Url or ID referring to instance hierarchy services
        """
        self.services_set = ET.SubElement(self.module_type_package, 'InternalElement')
        self.generate_attributes(self.services_set, 'Services', self.random_id_generator(),
                                 'MTPSUCLib/ServicesSet')
        self.__add_service_to_service_set('ServiceReference',
                                          'AutomationMLInterfaceClassLib/AutomationMLBaseInterface'
                                          '/ExternalDataConnector', linked_id)

    def __add_service_to_service_set(self, name: str, refPath: str, linked_id: str):
        """
        service object in this function is an ExternalDataConnector referring to InstanceHierarchy: Services which
        could be created in the same manifest or in a separate .aml file.
        """
        service = ET.SubElement(self.services_set, 'ExternalInterface')
        self.generate_attributes(service, name, self.random_id_generator(), refPath)
        self.add_linked_attr(service, linked_id)

    @staticmethod
    def add_attr_to_instance(parent_elem: ET.Element, name: str, default_value: str, attr_id: str):
        """
        add attrbutes of each data assembly to the corresponding instance
        :param parent_elem: data assembly to which the attributes should be added
        :param name: attribute name
        :param default_value: default value of attribute
        :param attr_id: each attribute has the same ID as the external interface of source list
        """
        attr = ET.SubElement(parent_elem, 'Attribute')
        attr.set('Name', name)

        # tag name and tag description are not linked to external interface in source list
        if name == 'tag_description' or name == 'tag_name':
            attr.set('AttributeDataType', 'xs:string')
            attr_value = ET.SubElement(attr, 'Value')
            attr_value.text = default_value
        else:
            attr.set('AttributeDataType', 'xs:IDREF')
            attr_default_value = ET.SubElement(attr, 'DefaultValue')
            attr_default_value.text = str(default_value)
            attr_value = ET.SubElement(attr, 'Value')
            attr_value.text = attr_id

    def add_opcua_server(self, endpoint: str):
        """
        add InternalElement opcua server to ModuleTypePackage/CommunicationSet/SourceList
        :param endpoint: endpoint of opc ua server
        """
        self.opcua_server = ET.SubElement(self.source_list, 'InternalElement')
        self.generate_attributes(self.opcua_server, 'OPCServer', self.random_id_generator(),
                                 'MTPCommunicationSUCLib/ServerAssembly/OPCUAServer')
        opc_attributes = ET.SubElement(self.opcua_server, 'Attribute')
        opc_attributes.set('Name', 'Endpoint')
        opc_attributes.set('AttributeDataType', 'xs:string')
        opc_endpoint = ET.SubElement(opc_attributes, 'Value')
        opc_endpoint.text = endpoint

    def add_external_interface(self, opc_node_id: str, opc_ns: int, linked_attr_id: str, access=1):
        """
        add opc ua node als ExternalInterface to ModuleTypePackage/CommunicationSet/SourceList/OPCUAServer
        :param opc_node_id: opc ua node id
        :param opc_ns: opc ua namespace
        :param linked_attr_id: id connecting external interface and the corresponding attribute of data assembly
        :param access: access level of each external element
        """
        node_identifier = opc_node_id
        node_name = opc_node_id.split('=')[-1]

        elem = ET.SubElement(self.opcua_server, 'ExternalInterface')
        self.generate_attributes(elem, node_name, linked_attr_id, 'MTPCommunicationICLib/DataItem/OPCUAItem')

        # opc ua node attribute: identifier
        attr_identifier = ET.SubElement(elem, 'Attribute')
        attr_identifier.set('Name', 'Identifier')
        attr_identifier_value = ET.SubElement(attr_identifier, 'Value')
        attr_identifier_value.text = node_identifier

        # opc ua node attribute: namespace
        attr_ns = ET.SubElement(elem, 'Attribute')
        attr_ns.set('Name', 'Namespace')
        attr_ns_value = ET.SubElement(attr_ns, 'Value')
        attr_ns_value.text = str(opc_ns)

        # opc ua node attribute: access
        attr_access = ET.SubElement(elem, 'Attribute')
        attr_access.set('Name', 'Access')
        attr_as_value = ET.SubElement(attr_access, 'Value')
        attr_as_value.text = str(access)

    @staticmethod
    def generate_attributes(elem: ET.Element, name: str, attr_id: str, reference_path: str):
        """
        crate attribute for each object that has the following attributes: name, id and reference_path
        """
        elem.set('Name', name)
        elem.set('ID', attr_id)
        elem.set('RefBaseSystemUnitPath', reference_path)

    def apply_add_supported_role_class(self):
        """
        apply function add_SupportedRoleClass() for InstanceHierarchies MTP and Services
        """
        self.add_supported_role_class(self.instance_hierarchy_mtp)
        self.add_supported_role_class(self.instance_hierarchy_service)

    def add_supported_role_class(self, parent: ET.Element):
        """
        add SupportedRoleClass to all InternalElement
        :param parent: internal element
        """
        for internal_element in parent.findall('InternalElement'):
            SupportedRoleClass = ET.SubElement(internal_element, 'SupportedRoleClass')
            SupportedRoleClass.set('RefRoleClassPath', 'AutomationMLBaseRoleClassLib/AutomationMLBaseRole')

            if internal_element.findall('InternalElement'):
                self.add_supported_role_class(internal_element)

    @staticmethod
    def random_id_generator() -> str:
        """
        # generate random id for different elements
        :return: id which contains five parts
        """
        # generate random id for different elements
        id1 = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        id2 = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        id3 = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        id4 = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        id5 = ''.join(random.sample(string.ascii_letters + string.digits, 4))

        random_id = id1 + '-' + id2 + '-' + id3 + '-' + id4 + '-' + id5
        return random_id

    def export_manifest(self):
        """
        export manifest
        """
        self.root.set('FileName', self.export_path.split('/')[-1])
        self.tree = ET.ElementTree(self.root)
        self.pretty_print(self.root)
        self.tree.write(self.export_path)

    def pretty_print(self, elem: ET.Element, level=0):
        """
        add indents to exported .aml file
        :param elem: root of the element tree
        :param level: layer of the element tree, 0 represents the first layer (root)
        """
        i = "\n" + level * "\t"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "\t"
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.pretty_print(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
