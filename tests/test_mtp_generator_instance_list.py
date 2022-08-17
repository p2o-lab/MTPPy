"""
test functions create_instance, add_data_assembly_to_InstanceLis, add_attr_to_instance and add_external_interface
With these functions, data assembly and it´s attributes can be added under InstanceList and SourceList/OPCServer
"""
import pytest
from mtppy.mtp_generator import MTPGenerator
from mtppy.service import Service
from mtppy.procedure import Procedure
from mtppy.operation_elements import *
from mtppy.indicator_elements import *
from mtppy.active_elements import *
import xml.etree.ElementTree as ET


# basic infos needed to initiate mtp_generator
writer_info_dict = {'WriterName': 'tud/plt', 'WriterID': 'tud/plt', 'WriterVendor': 'tud',
                    'WriterVendorURL': 'www.tud.de',
                    'WriterVersion': '1.0.0', 'WriterRelease': '', 'LastWritingDateTime': 123,
                    'WriterProjectTitle': 'tu/plt/mtp', 'WriterProjectID': ''}
export_manifest_path = '../src/mtppy/example2_manifest.xml'
manifest_template_path = './manifest_template.xml'

# test obj: active element pid controller
pid_ctrl = PIDCtrl('pid_ctrl')

# test obj: active element analogue drive
analogue_drive = AnaDrv('analogue_drive')

# test obj: procedure report value
procedure_report_value = AnaView('generated_value', v_scl_min=0, v_scl_max=100, v_unit=23)

# test obj: procedure process value out
procedure_process_value_out = BinView('process_value_out')

# test obj: procedure
procedure = Procedure(0, 'cont', is_self_completing=False, is_default=True)
procedure.add_report_value(procedure_report_value)
procedure.add_procedure_value_out(procedure_process_value_out)

# test obj: service config parameter
serv_parameters = StringServParam('serv_param_str')


# test obj: service
class Service1(Service):
    def __init__(self, tag_name, tag_description):
        super().__init__(tag_name, tag_description)
        self.add_procedure(procedure)
        self.add_configuration_parameter(serv_parameters)

    def idle(self):
        pass

    def starting(self):
        pass

    def execute(self):
        pass

    def completing(self):
        pass

    def completed(self):
        pass

    def pausing(self):
        pass

    def paused(self):
        pass

    def resuming(self):
        pass

    def holding(self):
        pass

    def held(self):
        pass

    def unholding(self):
        pass

    def stopping(self):
        pass

    def stopped(self):
        pass

    def aborting(self):
        pass

    def aborted(self):
        pass

    def resetting(self):
        pass


service = Service1('service_test', '')


class TestMTPInstanceList(object):  # test some functions of mtp generator
    def setup_class(self):
        self.mtp_generator = MTPGenerator(writer_info_dict, export_manifest_path, manifest_template_path)
        self.mtp_generator.add_module_type_package('1.0', 'mtp_test', '')
        self.module_type_package = self.mtp_generator.module_type_package
        endpoint = '127.0.0.0'
        self.mtp_generator.add_opcua_server(endpoint)

    def test_add_instance_report_value(self):
        # test: add report value of procedure to InstanceList
        node_id = 'ns=3;s=services.rand_num_gen.procedures.cont.report_values'
        internal_element = self.mtp_generator.create_instance(procedure_report_value, node_id)
        assert type(internal_element) == ET.Element
        report_value = self.mtp_generator.instance_list.findall('InternalElement')[0]

        # whether type and name of the report value obj are correct
        assert report_value.get('RefBaseSystemUnitPath') == 'MTPDataObjectSUCLib/DataAssembly/IndicatorElement/AnaView'
        assert report_value.get('Name') == 'services.rand_num_gen.procedures.cont.report_values'

        # initiate InstanceList for other tests
        self.mtp_generator.instance_list.remove(report_value)

    def test_add_instance_process_value_out(self):
        # test: add process value out of procedure to InstanceList
        node_id = 'ns=3;s=services.rand_num_gen.procedures.cont.process_value_outs'
        internal_element = self.mtp_generator.create_instance(procedure_process_value_out, node_id)
        assert type(internal_element) == ET.Element
        value_out = self.mtp_generator.instance_list.findall('InternalElement')[0]

        # whether type and name of the value out obj are correct
        assert value_out.get('RefBaseSystemUnitPath') == 'MTPDataObjectSUCLib/DataAssembly/IndicatorElement/BinView'
        assert value_out.get('Name') == 'services.rand_num_gen.procedures.cont.process_value_outs'

        # initiate InstanceList for other tests
        self.mtp_generator.instance_list.remove(value_out)

    def test_add_instance_type_error(self):
        # if type of the added obj does not belong to data assembly, a TypeError should be raised
        with pytest.raises(TypeError):
            node_id = 'ns=3;s=services.rand_num_gen.procedures.cont.report_values'
            self.mtp_generator.create_instance(1, node_id)
        assert len(self.mtp_generator.instance_list.findall('InstanceElement')) == 0

    def test_add_instance_procedure(self):
        # test: add procedure and associated report value to InstanceList
        # add procedure
        node_id = 'ns=3;s=services.rand_num_gen.procedures'
        self.mtp_generator.create_instance(procedure, node_id)
        proc = self.mtp_generator.instance_list.findall('InternalElement')[0]
        assert proc.get('RefBaseSystemUnitPath') == 'MTPDataObjectSUCLib/DataAssembly/DiagnosticElement/HealthStateView'
        assert proc.get('Name') == 'services.rand_num_gen.procedures.HealthStateView'

        # add report value
        node_id_rv = 'ns=3;s=services.rand_num_gen.procedures.cont.report_values'
        for report_values in procedure.report_values.values():
            self.mtp_generator.create_instance(report_values, node_id_rv)
        rv = self.mtp_generator.instance_list.findall('InternalElement')[1]
        assert rv.get('RefBaseSystemUnitPath') == 'MTPDataObjectSUCLib/DataAssembly/IndicatorElement/AnaView'
        assert rv.get('Name') == 'services.rand_num_gen.procedures.cont.report_values'

        # initiate InstanceList for other tests
        self.mtp_generator.instance_list.remove(proc)
        self.mtp_generator.instance_list.remove(rv)

    def test_add_instance_service(self):
        # test: add service and associated config para to InstanceList
        # add service
        node_id = 'ns=3;s=services'
        self.mtp_generator.create_instance(service, node_id)
        serv = self.mtp_generator.instance_list.findall('InternalElement')[0]
        assert serv.get('RefBaseSystemUnitPath') == 'MTPDataObjectSUCLib/DataAssembly/ServiceControl'
        assert serv.get('Name') == 'services.ServiceControl'

        # add config para
        node_id_cp = 'ns=3;s=services.service_test.config'
        for configs in service.configuration_parameters.values():
            self.mtp_generator.create_instance(configs, node_id_cp)
        config = self.mtp_generator.instance_list.findall('InternalElement')[1]
        assert config.get(
            'RefBaseSystemUnitPath') == 'MTPDataObjectSUCLib/DataAssembly/OperationElement/StringServParam'
        assert config.get('Name') == 'services.service_test.config'

        # initiate InstanceList for other tests
        self.mtp_generator.instance_list.remove(serv)
        self.mtp_generator.instance_list.remove(config)

    def test_add_instance_active_element_plt(self):
        # test: add active element PID controller to InstanceList
        node_id = 'ns=3;s=active_elements.pid_ctrl'
        self.mtp_generator.create_instance(pid_ctrl, node_id)
        active_element = self.mtp_generator.instance_list.findall('InternalElement')[0]
        assert active_element.get('RefBaseSystemUnitPath') == 'MTPDataObjectSUCLib/DataAssembly/ActiveElement/PIDCtrl'
        assert active_element.get('Name') == 'active_elements.pid_ctrl'

        # initiate InstanceList for other tests
        self.mtp_generator.instance_list.remove(active_element)

    def test_add_instance_active_element_analogue_drive(self):
        # test: add active element analogue drive to InstanceList
        node_id = 'ns=3;s=active_elements.analogue_drive'
        self.mtp_generator.create_instance(analogue_drive, node_id)
        act = self.mtp_generator.instance_list.findall('InternalElement')[0]
        assert act.get('RefBaseSystemUnitPath') == 'MTPDataObjectSUCLib/DataAssembly/ActiveElement/AnaDrv'
        assert act.get('Name') == 'active_elements.analogue_drive'

        # initiate InstanceList for other tests
        self.mtp_generator.instance_list.remove(act)

    def test_add_attr_to_instance(self):
        node_id = 'ns=3;s=active_elements.pid_ctrl'
        self.mtp_generator.create_instance(pid_ctrl, node_id)
        act = self.mtp_generator.instance_list.findall('InternalElement')[0]

        section_node_id = 'ns=3;s=active_elements.pid_ctrl'
        for attr in pid_ctrl.attributes.values():
            attribute_node_id = f'{section_node_id}.{attr.name}'
            linked_id = self.mtp_generator.random_id_generator()

            # add attributes to InstanceList and SourceList
            self.mtp_generator.add_external_interface(attribute_node_id, 3, linked_id)
            self.mtp_generator.add_attr_to_instance(act, attr.name, attr.init_value, linked_id)

        # if the attributes of PID Controller have been added to InstanceList successfully
        tag_name = act.findall(".//Attribute[@Name='tag_name']")[0].findall('.//')[0]
        assert tag_name.text == 'pid_ctrl'

        # active element plt should have 28 attributes (besides attributes of op_src_mode)
        assert len(act.findall('.//Attribute')) == 28

        # number of ExternalInterfaces should equal to the number of PID Controller attributes
        assert len(self.mtp_generator.opcua_server.findall(".//ExternalInterface")) == 28

        # each ExternalInterface has three attributes
        assert len(self.mtp_generator.opcua_server.findall(".//ExternalInterface")[0].findall('Attribute')) == 3

        # check, if ExternalInterface is connected to attribute of Instance
        linked_id_ei = self.mtp_generator.opcua_server.findall(".//ExternalInterface")[2].get('ID')
        linked_id_attr = act.findall('.//Attribute/Value')[2].text
        assert linked_id_attr == linked_id_ei


if __name__ == '__main__':
    pytest.main(['test_mtp_generator_instance_list.py', '-s'])
