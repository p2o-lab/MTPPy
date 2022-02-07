from src.operation_source_mode import OperationStateMode
from src.control_element_bin_serv_param import ControlElementsBinServParam
from src.control_element_d_int_serv_param import ControlElementsDIntServParam
from src.control_element_ana_serv_param import ControlElementsAnaServParam
from src.control_element_string_serv_param import ControlElementsStringServParam


class OperationElement:
    def __init__(self, tag_name, tag_description=''):
        self.tag_name = tag_name
        self.tag_description = tag_description
        self.op_src_mode = OperationStateMode()
        self.control_elements = None


class BinServParam:
    def __init__(self, tag_name, tag_description='', v_state_0='false', v_state_1='true'):
        self.tag_name = tag_name
        self.tag_description = tag_description
        self.v_state_0 = v_state_0
        self.v_state_1 = v_state_1

        self.op_src_mode = OperationStateMode()
        self.control_elements = ControlElementsBinServParam(v_state_0=self.v_state_0,
                                                            v_state_1=self.v_state_1,
                                                            op_src_mode=self.op_src_mode)


class DIntServParam(OperationElement):
    def __init__(self, tag_name, v_min=0, v_max=100, v_scl_min=0, v_scl_max=100, v_unit=0):
        super().__init__(tag_name)
        self.v_min = v_min
        self.v_max = v_max
        self.v_scl_min = v_scl_min
        self.v_scl_max = v_scl_max
        self.v_unit = v_unit

    def attach(self, opcua_prefix, opcua_server, opcua_ns):
        super().attach(opcua_prefix, opcua_server, opcua_ns)
        self.control_elements = ControlElementsDIntServParam(opcua_server=opcua_server,
                                                             opcua_ns=opcua_ns,
                                                             opcua_prefix=self.opcua_prefix,
                                                             source_mode=self.source_mode,
                                                             operation_mode=self.operation_mode,
                                                             v_min=self.v_min,
                                                             v_max=self.v_max,
                                                             v_scl_min=self.v_scl_min,
                                                             v_scl_max=self.v_scl_max,
                                                             v_unit=self.v_unit
                                                             )


class AnaServParam(OperationElement):
    def __init__(self, tag_name, v_min=0, v_max=100, v_scl_min=0, v_scl_max=100, v_unit=0):
        super().__init__(tag_name)
        self.v_min = v_min
        self.v_max = v_max
        self.v_scl_min = v_scl_min
        self.v_scl_max = v_scl_max
        self.v_unit = v_unit

    def attach(self, opcua_prefix, opcua_server, opcua_ns):
        super().attach(opcua_prefix, opcua_server, opcua_ns)
        self.control_elements = ControlElementsAnaServParam(opcua_server=opcua_server,
                                                            opcua_ns=opcua_ns,
                                                            opcua_prefix=self.opcua_prefix,
                                                            source_mode=self.source_mode,
                                                            operation_mode=self.operation_mode,
                                                            v_min=self.v_min,
                                                            v_max=self.v_max,
                                                            v_scl_min=self.v_scl_min,
                                                            v_scl_max=self.v_scl_max,
                                                            v_unit=self.v_unit
                                                            )


class StringServParam(OperationElement):
    def __init__(self, tag_name):
        super().__init__(tag_name)

    def attach(self, opcua_prefix, opcua_server, opcua_ns):
        super().attach(opcua_prefix, opcua_server, opcua_ns)
        self.control_elements = ControlElementsStringServParam(opcua_server=opcua_server,
                                                              opcua_ns=opcua_ns,
                                                              opcua_prefix=self.opcua_prefix,
                                                              source_mode=self.source_mode,
                                                              operation_mode=self.operation_mode
                                                              )
