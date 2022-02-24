from src.mtppy.procedure import Procedure
from src.mtppy.operation_elements import *
from src.mtppy.indicator_elements import *

operation_elements = [AnaServParam('serv_param_ana', v_min=0, v_max=50, v_scl_min=0, v_scl_max=10, v_unit=23),
                    DIntServParam('serv_param_dint', v_min=-10, v_max=10, v_scl_min=0, v_scl_max=-10, v_unit=23),
                    BinServParam('serv_param_bin', v_state_0='state_0', v_state_1='state_1'),
                    StringServParam('serv_param_str')
                    ]

indicator_elements = [AnaView('proc_rv_ana', v_scl_min=0, v_scl_max=10, v_unit=23),
                      DIntView('proc_rv_dint', v_scl_min=0, v_scl_max=-10, v_unit=23),
                      BinView('proc_rv_bin', v_state_0='state_0', v_state_1='state_1'),
                      StringView('proc_rv_str'),
                      ]


def create_dummy_procedure():
    return Procedure(0, 'procedure')


def test_add_procedure_parameter():
    valid_parameters = operation_elements
    invalid_parameters = indicator_elements

    procedure = create_dummy_procedure()
    for valid_parameter in valid_parameters:
        procedure.add_procedure_parameter(valid_parameter)
        assert procedure.procedure_parameters[valid_parameter.tag_name] == valid_parameter

    procedure = create_dummy_procedure()
    for invalid_parameter in invalid_parameters:
        try:
            procedure.add_procedure_parameter(invalid_parameter)
            assert False
        except TypeError:
            assert True


def test_add_report_values():
    valid_parameters = indicator_elements
    invalid_parameters = operation_elements

    procedure = create_dummy_procedure()
    for valid_parameter in valid_parameters:
        procedure.add_report_value(valid_parameter)
        assert procedure.report_values[valid_parameter.tag_name] == valid_parameter

    procedure = create_dummy_procedure()
    for invalid_parameter in invalid_parameters:
        try:
            procedure.add_report_value(invalid_parameter)
            assert False
        except TypeError:
            assert True


def test_add_value_outs():
    valid_parameters = indicator_elements
    invalid_parameters = operation_elements

    procedure = create_dummy_procedure()
    for valid_parameter in valid_parameters:
        procedure.add_procedure_value_out(valid_parameter)
        assert procedure.process_value_outs[valid_parameter.tag_name] == valid_parameter

    procedure = create_dummy_procedure()
    for invalid_parameter in invalid_parameters:
        try:
            procedure.add_procedure_value_out(invalid_parameter)
            assert False
        except TypeError:
            assert True