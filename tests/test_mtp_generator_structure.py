"""
test the basic manifest structure
"""
import pytest
from mtppy.mtp_generator import MTPGenerator

# basic infos needed to initiate mtp_generator
writer_info_dict = {'WriterName': 'tud/plt/shk', 'WriterID': 'tud/plt', 'WriterVendor': 'tud',
                    'WriterVendorURL': 'www.tud.de',
                    'WriterVersion': '1.0.0', 'WriterRelease': '', 'LastWritingDateTime': 123,
                    'WriterProjectTitle': 'tu/plt/mtp', 'WriterProjectID': ''}
export_manifest_path = '../src/mtppy/example2_manifest.xml'
manifest_template_path = './manifest_template.xml'


class TestMTPStructure(object):  # test structure of manifest
    def setup_class(self):
        """
        initiate mtp generator and ModuleTypePackage
        """
        self.mtp_generator = MTPGenerator(writer_info_dict, export_manifest_path, manifest_template_path)
        self.mtp_generator.add_module_type_package('1.0', 'mtp_test', '')
        self.module_type_package = self.mtp_generator.module_type_package

    def test_structure(self):
        # test basic structure
        root = self.mtp_generator.root
        instanceHierarchy = root.findall('InstanceHierarchy')
        assert len(instanceHierarchy) == 2
        assert instanceHierarchy[0].get('Name') == 'ModuleTypePackage'
        assert instanceHierarchy[1].get('Name') == instanceHierarchy[1].get('ID')

    def test_structure_ModuleTypePackage(self):
        internalElements = self.module_type_package.findall('InternalElement')
        # ModuleTypePackage should has two InternalElements CommunicationSet and ServiceSet
        assert len(internalElements) == 2
        assert internalElements[0].get('Name') == 'Communication'
        assert internalElements[1].get('Name') == 'Services'

    def test_structure_CommunicationSet(self):
        communicationSet = self.module_type_package.findall('InternalElement')[0]
        # InternalElement CommunicationSet must have two InternalElements InstanceList and SourceList
        instanceList = communicationSet.findall("InternalElement/[@Name='InstanceList']")
        sourceList = communicationSet.findall("InternalElement/[@Name='SourceList']")
        assert len(instanceList) == 1
        assert len(sourceList) == 1

    def test_structure_SourceList(self):
        # InternalElement should have a sub-element OPCServer. The sub-element Value of OPCServer is the endpoint
        endpoint = '127.0.0.0'
        self.mtp_generator.add_opcua_server(endpoint)
        opcua_server = self.mtp_generator.source_list.findall('InternalElement')[0]
        opc_attribute = opcua_server.findall('Attribute')[0]
        assert opcua_server.get('Name') == 'OPCServer'
        assert opc_attribute.find('Value').text == endpoint

    def test_edit_writer_infos(self):
        self.mtp_generator.edit_writer_information()
        writer_header = self.mtp_generator.root.find('AdditionalInformation/WriterHeader')
        assert writer_header.find('./WriterVendorURL').text == 'www.tud.de'
        assert writer_header.find('./WriterProjectTitle').text == 'tu/plt/mtp'
        assert writer_header.find('./WriterName').text == 'tud/plt/shk'
        assert writer_header.find('./WriterRelease').text == ''

    def test_edit_writer_infos_error(self):
        # writer info dict with wrong key 'WriterName1' and 'WriterID1'
        writer_info_dict1 = {'WriterName1': 'tud/plt/shk', 'WriterID1': 'tud/plt', 'WriterVendor': 'tud',
                             'WriterVendorURL': 'www.tud.de',
                             'WriterVersion': '1.0.0', 'WriterRelease': '', 'LastWritingDateTime': 123,
                             'WriterProjectTitle': 'tu/plt/mtp', 'WriterProjectID': ''}

        # a KeyError should be raised
        with pytest.raises(KeyError):
            mtp_generator = MTPGenerator(writer_info_dict1, export_manifest_path, manifest_template_path)
            mtp_generator.edit_writer_information()

    def test_add_supported_role_class(self):
        # test if SupportedRoleClass is added to all InternalElements
        self.mtp_generator.apply_add_supported_role_class()
        for internal_element in self.mtp_generator.root.iter('InternalElement'):
            supported_role_class = internal_element.find('SupportedRoleClass')
            assert supported_role_class.get('RefRoleClassPath') == 'AutomationMLBaseRoleClassLib/AutomationMLBaseRole'

    def test_random_id_generator(self):
        random_id = self.mtp_generator.random_id_generator()
        assert len(random_id.split('-')) == 5

        for i in random_id.split('-'):
            assert len(i) == 4


if __name__ == '__main__':
    pytest.main(['test_mtp_generator_structure.py', '-s'])
