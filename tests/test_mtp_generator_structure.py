"""
test the basic manifest structure
"""
import pytest
from mtppy.MTP_generator import MTP_generator

# basic infos needed to initiate mtp_generator
writer_info_dict = {'WriterName': 'tud/plt', 'WriterID': 'tud/plt', 'WriterVendor': 'tud',
                    'WriterVendorURL': 'www.tud.de',
                    'WriterVersion': '1.0.0', 'WriterRelease': '', 'LastWritingDateTime': 123,
                    'WriterProjectTitle': 'tu/plt/mtp', 'WriterProjectID': ''}
export_manifest_path = '../src/mtppy/example2_manifest.xml'


class Test_MTP_Structure(object):  # test structure of manifest
    def setup_class(self):
        """
        initiate mtp generator and ModuleTypePackage
        """
        self.mtp_generator = MTP_generator(writer_info_dict, export_manifest_path)
        self.mtp_generator.add_ModuleTypePackage(1.0, 'mtp_test', '')
        self.ModuleTypePackage = self.mtp_generator.ModuleTypePackage

    def test_structure(self):
        # test basic structure
        root = self.mtp_generator.root
        InstanceHierarchy = root.findall('InstanceHierarchy')
        assert len(InstanceHierarchy) == 2
        assert InstanceHierarchy[0].get('Name') == 'ModuleTypePackage'
        assert InstanceHierarchy[1].get('Name') == InstanceHierarchy[1].get('ID')

    def test_structure_ModuleTypePackage(self):
        InternalElements = self.ModuleTypePackage.findall('InternalElement')
        # ModuleTypePackage should has two InternalElements CommunicationSet and ServiceSet
        assert len(InternalElements) == 2
        assert InternalElements[0].get('Name') == 'Communication'
        assert InternalElements[1].get('Name') == 'Services'

    def test_structure_CommunicationSet(self):
        CommunicationSet = self.ModuleTypePackage.findall('InternalElement')[0]
        # InternalElement CommunicationSet must have two InternalElements InstanceList and SourceList
        InstanceList = CommunicationSet.findall("InternalElement/[@Name='InstanceList']")
        SourceList = CommunicationSet.findall("InternalElement/[@Name='SourceList']")
        assert len(InstanceList) == 1
        assert len(SourceList) == 1

    def test_structure_SourceList(self):
        # InternalElement should have a sub-element OPCServer. The sub-element Value of OPCServer is the endpoint
        endpoint = '127.0.0.0'
        self.mtp_generator.add_opcua_server(endpoint)
        opcua_server = self.mtp_generator.SourceList.findall('InternalElement')[0]
        Attribute = opcua_server.findall('Attribute')[0]
        assert opcua_server.get('Name') == 'OPCServer'
        assert Attribute.find('Value').text == endpoint

    def test_random_id_generator(self):
        id = self.mtp_generator.random_id_generator()
        assert len(id.split('-')) == 5

        for i in id.split('-'):
            assert len(i) == 4


if __name__ == '__main__':
    pytest.main(['test_mtp_generator_structure.py', '-s'])