from src.operation_source_mode import OperationSourceMode
from src.control_element_bin_serv_param import ControlElementsBinServParam
from src.control_element_d_int_serv_param import ControlElementsDIntServParam
from src.control_element_ana_serv_param import ControlElementsAnaServParam
from src.control_element_string_serv_param import ControlElementsStringServParam


class BinServParam:
    def __init__(self, tag_name, tag_description='', v_state_0='false', v_state_1='true'):
        self.tag_name = tag_name
        self.tag_description = tag_description

        self.op_src_mode = OperationSourceMode()
        self.control_elements = ControlElementsBinServParam(v_state_0=v_state_0,
                                                            v_state_1=v_state_1,
                                                            op_src_mode=self.op_src_mode)


class DIntServParam:
    def __init__(self, tag_name, tag_description='', v_min=0, v_max=100, v_scl_min=0, v_scl_max=100, v_unit=0):
        self.tag_name = tag_name
        self.tag_description = tag_description

        self.op_src_mode = OperationSourceMode()
        self.control_elements = ControlElementsDIntServParam(v_min=v_min,
                                                             v_max=v_max,
                                                             v_scl_min=v_scl_min,
                                                             v_scl_max=v_scl_max,
                                                             v_unit=v_unit,
                                                             op_src_mode=self.op_src_mode)


class AnaServParam:
    def __init__(self, tag_name, tag_description='', v_min=0, v_max=100, v_scl_min=0, v_scl_max=100, v_unit=0):
        self.tag_name = tag_name
        self.tag_description = tag_description

        self.op_src_mode = OperationSourceMode()
        self.control_elements = ControlElementsAnaServParam(v_min=v_min,
                                                            v_max=v_max,
                                                            v_scl_min=v_scl_min,
                                                            v_scl_max=v_scl_max,
                                                            v_unit=v_unit,
                                                            op_src_mode=self.op_src_mode)


class StringServParam:
    def __init__(self, tag_name, tag_description=''):
        self.tag_name = tag_name
        self.tag_description = tag_description

        self.op_src_mode = OperationSourceMode()
        self.control_elements = ControlElementsStringServParam(op_src_mode=self.op_src_mode)
