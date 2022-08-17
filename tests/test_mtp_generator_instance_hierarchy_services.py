"""
test functions create_components_for_services and add_components_to_services.
With these two functions, service and its sub-components (e.g. config param, procedure, procedure param etc. ) can be
added to InstanceHierarchy services
"""
import pytest
from mtppy.mtp_generator import MTPGenerator
from mtppy.service import Service
from mtppy.procedure import Procedure
from mtppy.operation_elements import *
from mtppy.indicator_elements import *
from mtppy.active_elements import *

# basic infos needed to initiate mtp_generator
writer_info_dict = {'WriterName': 'tud/plt', 'WriterID': 'tud/plt', 'WriterVendor': 'tud',
                    'WriterVendorURL': 'www.tud.de',
                    'WriterVersion': '1.0.0', 'WriterRelease': '', 'LastWritingDateTime': 123,
                    'WriterProjectTitle': 'tu/plt/mtp', 'WriterProjectID': ''}
export_manifest_path = '../src/mtppy/example2_manifest.xml'
manifest_template_path = './manifest_template.xml'

# test obj: active element pid controller
pid_ctrl = PIDCtrl('pid_ctrl')

# test obj: procedure report value
procedure_report_value = BinView('proc_rv_bin', v_state_0='state_0', v_state_1='state_1')

# test obj: procedure process value out
procedure_process_value_out = BinView('process_value_out')

# test obj: procedure parameter
procedure_param = DIntServParam('proc_param_dint', v_min=-10, v_max=10, v_scl_min=0, v_scl_max=-10, v_unit=23)

# test obj: procedure
procedure = Procedure(0, 'cont', is_self_completing=False, is_default=True)
procedure.add_report_value(procedure_report_value)
procedure.add_procedure_value_out(procedure_process_value_out)
procedure.add_procedure_parameter(procedure_param)

# test obj: service config parameter
serv_parameters = AnaServParam('serv_param_ana', v_min=0, v_max=50, v_scl_min=0, v_scl_max=10, v_unit=23)


# test obj: service
class ServiceObject(Service):
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


service1 = ServiceObject('service_test1', '')


class TestInstanceHierarchyServices(object):  # test some functions of mtp generator
    def setup_class(self):
        self.mtp_generator = MTPGenerator(writer_info_dict, export_manifest_path, manifest_template_path)

    def test_add_service_to_InstanceHierarchy(self):
        """
        test case: opcua server has two services
        """
        self.mtp_generator.create_components_for_services(service1, 'services')
        # test, if two InternalElements are added to InstanceHierarchy Services
        # the name of these two InternalElements should correspond the service name
        service_name = self.mtp_generator.instance_hierarchy_service.find('InternalElement').get('Name')
        assert service_name == 'service_test1'

    def test_add_components_to_service(self):
        self.mtp_generator.create_components_for_services(serv_parameters, 'configuration_parameters')
        self.mtp_generator.create_components_for_services(procedure, 'procedures')

        # InternalElement service should only have two sub-InternalElements config param and procedure
        service_sub_elements = self.mtp_generator.instance_hierarchy_service.find('InternalElement')
        assert len(service_sub_elements.findall('InternalElement')) == 2

    def test_add_components_to_procedure(self):
        self.mtp_generator.create_components_for_services(procedure_param, 'procedure_parameters')
        self.mtp_generator.create_components_for_services(procedure_report_value, 'report_values')
        self.mtp_generator.create_components_for_services(procedure_process_value_out, 'process_value_outs')

        # in this test case, a procedure should have one report value, one value out and one procedure parameter
        procedure_ie = self.mtp_generator.instance_hierarchy_service.findall('InternalElement/InternalElement')[1]
        assert len(procedure_ie.findall('InternalElement')) == 3

        pro_parameters = procedure_ie.findall('InternalElement')[0]
        report_value = procedure_ie.findall('InternalElement')[1]
        value_out = procedure_ie.findall('InternalElement')[2]

        assert pro_parameters.get('Name') == 'proc_param_dint'
        assert report_value.get('Name') == 'proc_rv_bin'
        assert value_out.get('Name') == 'process_value_out'

    def test_add_wrong_type(self):
        # if the type of data assembly, it should not be added to InstanceHierarchy service and
        # a TypeError should be raised
        with pytest.raises(TypeError):
            self.mtp_generator.create_components_for_services(pid_ctrl, 'active_elements')


if __name__ == '__main__':
    pytest.main(['test_mtp_generator_instance_hierarchy_services.py', '-s'])
