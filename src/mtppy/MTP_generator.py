import xml.etree.ElementTree as ET
import random
import string


class MTP_generator:
    def __init__(self, writer_info: dict, export_path: string):
        self.template_path = '../manifest_files/manifest_template.xml'  # path of a manifest template containing generell infos
        self.writer_info = writer_info  # infos about manifest writer is configurable

        self.tree = ET.parse(self.template_path)
        self.root = self.tree.getroot()
        self.export_path = export_path  # path of generated manifest

        # first layer
        self.InstanceHierarchy_MTP = None
        self.InstanceHierarchy_Service = None

        # InstanceHierarchy MTP layer
        self.ModuleTypePackage = None

        # InternalElement MTP layer
        self.CommunicationSet = None
        self.ServicesSet = None

        # CommunicationSet layer
        self.InstanceList = None
        self.SourceList = None

        # SourceList layer
        self.OPCUA = None

        # InstanceHierarchy service layer
        self.Service = None
        self.ServiceProcedure = None

        self.__init_manifest()
        self.__init_InstanceHierarchy()
        self.edit_writer_information()

    def __init_manifest(self):
        self.InstanceHierarchy_MTP = ET.SubElement(self.root, "InstanceHierarchy")
        self.InstanceHierarchy_Service = ET.SubElement(self.root, "InstanceHierarchy")

    def __init_InstanceHierarchy(self):
        self.InstanceHierarchy_MTP.set('Name', 'ModuleTypePackage')
        self.InstanceHierarchy_MTP.set('ID', self.random_id_generator())
        id = self.random_id_generator()
        self.InstanceHierarchy_Service.set('Name', id)
        self.InstanceHierarchy_Service.set('ID', id)

    def edit_writer_information(self):
        writerHeader = self.root.find('AdditionalInformation/WriterHeader')
        for info in writerHeader.findall('./'):
            try:
                info.text = self.writer_info[info.tag]
            except Exception as e:
                print(e)

    def add_ModuleTypePackage(self, version: string, name: string, description=''):
        self.ModuleTypePackage = ET.Element("InternalElement", {'Name': name, 'ID': self.random_id_generator(),
                                                                'RefBaseSystemUnitPath': 'MTPSUCLib/ModuleTypePackage'})
        mtp_description = ET.SubElement(self.ModuleTypePackage, 'Description')
        mtp_description.text = description
        mtp_version = ET.SubElement(self.ModuleTypePackage, 'Version')
        mtp_version.text = version
        self.InstanceHierarchy_MTP.append(self.ModuleTypePackage)
        self.add_communicationSet()
        self.add_ServicesSet()

    def add_communicationSet(self):
        self.CommunicationSet = ET.SubElement(self.ModuleTypePackage, 'InternalElement')
        self.attribute_generator(self.CommunicationSet, 'Communication', self.random_id_generator(),
                                 'MTPSUCLib/CommunicationSet')
        self.InstanceList = ET.SubElement(self.CommunicationSet, 'InternalElement')
        self.attribute_generator(self.InstanceList, 'InstanceList', self.random_id_generator(),
                                 'MTPSUCLib/CommunicationSet/InstanceList')
        self.SourceList = ET.SubElement(self.CommunicationSet, 'InternalElement')
        self.attribute_generator(self.SourceList, 'SourceList', self.random_id_generator(),
                                 'MTPSUCLib/CommunicationSet/SourceList')

    def create_instance(self, data_assembly, node_id):
        """
        create data assembly instance
        :param data_assembly: data assembly object
        :param node_id: opcua node id used to construct instance name
        :return: instance of data assembly
        """
        instance_id = self.random_id_generator()
        instance_name = node_id.split('=')[-1]
        instance_basic_type = data_assembly.__class__.__bases__[-1].__name__
        instance_type_name = type(data_assembly).__name__
        instance = self.add_data_assembly_to_InstanceList(instance_name, instance_id, instance_basic_type,
                                                          instance_type_name)

        return instance

    def add_data_assembly_to_InstanceList(self, instance_name, instance_id, instance_basic_type, instance_type_name):
        """
        add data object (subclasses of assembly) to instance list
        :param instance_name: name of data object
        :param instance_id: id of data object
        :param instance_basic_type: type of data assembly (service, Procedure, operation element etc.)
        :param instance_type_name: used to distinguish data objects that have the same parent type (e.g. AnaSerParam,
        StringSerParam, DIntSerParam, etc.)
        :return: instance of data assembly
        """
        instance = ET.SubElement(self.InstanceList, 'InternalElement')
        name = None
        refPath = None

        if instance_basic_type == 'Service':
            name = instance_name + '.ServiceControl'
            refPath = 'MTPDataObjectSUCLib/DataAssembly/ServiceControl'
        elif instance_basic_type == 'SUCServiceProcedure':
            name = instance_name + '.HealthStateView'
            refPath = 'MTPDataObjectSUCLib/DataAssembly/DiagnosticElement/HealthStateView'
        elif instance_basic_type == 'SUCOperationElement':
            name = instance_name
            refPath = 'MTPDataObjectSUCLib/DataAssembly/OperationElement/' + instance_type_name
        elif instance_basic_type == 'SUCIndicatorElement':
            name = instance_name
            refPath = 'MTPDataObjectSUCLib/DataAssembly/IndicatorElement/' + instance_type_name
        elif instance_basic_type == 'SUCActiveElement':
            name = instance_name
            refPath = 'MTPDataObjectSUCLib/DataAssembly/ActiveElement/' + instance_type_name

        if name and refPath:
            # add instance attributes
            self.attribute_generator(instance, name, instance_id, refPath)
        else:
            self.InstanceList.remove(instance)
            raise TypeError('data assembly type error')

        return instance

    def create_components_for_services(self, data_assembly, section):
        """
        create components for InstanceHierarchy Services
        :param parent_elem: parent element of current component (e.g. parent of a procedure is a service)
        :param data_assembly: data assembly object
        :return: component of services: eg. service, procedure, config parameter, procedure parameter etc.
        """
        services_component_id = self.random_id_generator()
        service_component, link_id = self.add_components_to_services(data_assembly,
                                                                     services_component_id, section)

        # link_id: each component of services is through link_id linked to an InternalElement in InstanceList
        return link_id

    def add_components_to_services(self, data_assembly, sc_id, section):
        """
        add services and its components (config param, procedure, procedure param etc.) to InstanceHierarchy: Services
        s_component: service component
        """
        sc_name = data_assembly.tag_name
        s_component = None
        if section == 'services':
            s_component = ET.SubElement(self.InstanceHierarchy_Service, 'InternalElement')
            self.Service = s_component
            s_component.set('RefBaseSystemUnitPath', 'MTPServiceSUCLib/Service')

        elif section == 'configuration_parameters':
            s_component = ET.SubElement(self.Service, 'InternalElement')
            s_component.set('RefBaseSystemUnitPath', 'MTPServiceSUCLib/ServiceParameter/ConfigurationParameter')

        elif section == 'procedures':
            s_component = ET.SubElement(self.Service, 'InternalElement')
            self.ServiceProcedure = s_component
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
            s_component = ET.SubElement(self.ServiceProcedure, 'InternalElement')
            s_component.set('RefBaseSystemUnitPath', 'MTPServiceSUCLib/ServiceParameter/ProcedureParameter')

        elif section == 'process_value_ins':
            s_component = ET.SubElement(self.ServiceProcedure, 'InternalElement')
            s_component.set('RefBaseSystemUnitPath', 'MTPServiceSUCLib/ServiceParameter/ProcessValueIn')

        elif section == 'report_values':
            s_component = ET.SubElement(self.ServiceProcedure, 'InternalElement')
            s_component.set('RefBaseSystemUnitPath', 'MTPServiceSUCLib/ServiceParameter/ReportValue')

        elif section == 'process_value_outs':
            s_component = ET.SubElement(self.ServiceProcedure, 'InternalElement')
            s_component.set('RefBaseSystemUnitPath', 'MTPServiceSUCLib/ServiceParameter/ProcessValueOut')

        link_id = self.random_id_generator()

        if s_component is None:
            raise TypeError('service components type error')

        else:
            s_component.set('Name', sc_name)
            s_component.set('ID', sc_id)

            self.add_linked_attr(s_component, link_id)

        return s_component, link_id

    def add_linked_attr(self, parent, id):
        """
        add attribute whose value refers to an InternalElement under InstanceList
        :param parent: parent of attribute
        :param id: id linking to another element
        """
        attr = ET.SubElement(parent, 'Attribute')
        attr.set('Name', 'RefID')
        attr.set('AttributeDataType', 'xs:ID')
        attr_value = ET.SubElement(attr, 'Value')
        attr_value.text = id

    def add_ServicesSet(self):
        """
        ServiceSet is an InternalElement belonging to ModuleTypePackage and is connected
        through the linked-obj to InstanceHierarchy: Services
        """
        self.ServicesSet = ET.SubElement(self.ModuleTypePackage, 'InternalElement')
        self.attribute_generator(self.ServicesSet, 'Services', self.random_id_generator(),
                                 'MTPSUCLib/ServicesSet')
        ref_id = self.InstanceHierarchy_Service.get('ID')
        self.add_service_to_ServiceSet('ServiceReference',
                                       'AutomationMLInterfaceClassLib/AutomationMLBaseInterface/ExternalDataConnector',
                                       ref_id)

    def add_service_to_ServiceSet(self, name, refPath, id):
        service = ET.SubElement(self.ServicesSet, 'ExternalInterface')
        self.attribute_generator(service, name, self.random_id_generator(), refPath)
        self.add_linked_attr(service, id)

    def add_attr_to_instance(self, parent_elem, name, default, id):
        """
        add attrbutes of each data assembly to the corresponding instance
        """
        attr = ET.SubElement(parent_elem, 'Attribute')
        attr.set('Name', name)
        if name == 'tag_description' or name == 'tag_name':
            attr.set('AttributeDataType', 'xs:string')
            attr_value = ET.SubElement(attr, 'Value')
            attr_value.text = default
        else:

            attr.set('AttributeDataType', 'xs:IDREF')
            attr_default_value = ET.SubElement(attr, 'DefaultValue')
            attr_default_value.text = str(default)
            attr_value = ET.SubElement(attr, 'Value')
            attr_value.text = id

    def add_opcua_server(self, endpoint: string):
        """
        add InternalElement opcua server to ModuleTypePackage/CommunicationSet/SourceList
        :param endpoint:
        :return:
        """
        self.OPCUA = ET.SubElement(self.SourceList, 'InternalElement')
        self.attribute_generator(self.OPCUA, 'OPCServer', self.random_id_generator(),
                                 'MTPCommunicationSUCLib/ServerAssembly/OPCUAServer')
        opc_attributes = ET.SubElement(self.OPCUA, 'Attribute')
        opc_attributes.set('Name', 'Endpoint')
        opc_attributes.set('AttributeDataType', 'xs:string')
        opc_endpoint = ET.SubElement(opc_attributes, 'Value')
        opc_endpoint.text = str(endpoint)

    def add_external_interface(self, node_id, id, ns, access=1):
        """
        add opc ua node als ExternalInterface to ModuleTypePackage/CommunicationSet/SourceList/OPCUAServer
        """
        node_identifier = node_id
        node_name = node_id.split('=')[-1]

        elem = ET.SubElement(self.OPCUA, 'ExternalInterface')
        self.attribute_generator(elem, node_name, id, 'MTPCommunicationICLib/DataItem/OPCUAItem')

        # opc ua node attribute: identifier
        attr_id = ET.SubElement(elem, 'Attribute')
        attr_id.set('Name', 'Identifier')
        attr_id_value = ET.SubElement(attr_id, 'Value')
        attr_id_value.text = node_identifier

        # opc ua node attribute: namespace
        attr_ns = ET.SubElement(elem, 'Attribute')
        attr_ns.set('Name', 'Namespace')
        attr_ns_value = ET.SubElement(attr_ns, 'Value')
        attr_ns_value.text = str(ns)

        # opc ua node attribute: access
        attr_as = ET.SubElement(elem, 'Attribute')
        attr_as.set('Name', 'Access')
        attr_as_value = ET.SubElement(attr_as, 'Value')
        attr_as_value.text = str(access)

    def attribute_generator(self, elem, name, id, refPath):
        elem.set('Name', name)
        elem.set('ID', id)
        elem.set('RefBaseSystemUnitPath', refPath)

    def apply_add_SupportedRoleClass(self):
        #  apply function add_SupportedRoleClass() for InstanceHierarchies MTP and Services
        self.add_SupportedRoleClass(self.InstanceHierarchy_MTP)
        self.add_SupportedRoleClass(self.InstanceHierarchy_Service)

    def add_SupportedRoleClass(self, parent):
        # add SupportedRoleClass to all InternalElement
        for internal_element in parent.findall('InternalElement'):
            SupportedRoleClass = ET.SubElement(internal_element, 'SupportedRoleClass')
            SupportedRoleClass.set('RefRoleClassPath', 'AutomationMLBaseRoleClassLib/AutomationMLBaseRole')

            if internal_element.findall('InternalElement'):
                self.add_SupportedRoleClass(internal_element)

    def random_id_generator(self):
        # generate random id for different elements
        id1 = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        id2 = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        id3 = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        id4 = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        id5 = ''.join(random.sample(string.ascii_letters + string.digits, 4))

        id = id1 + '-' + id2 + '-' + id3 + '-' + id4 + '-' + id5
        return id

    def export_manifest(self):
        # export manifest
        self.root.set('FileName', self.export_path.split('/')[-1])
        self.tree = ET.ElementTree(self.root)
        self.pretty_print(self.root)
        self.tree.write(self.export_path)

    def pretty_print(self, elem, level=0):
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
