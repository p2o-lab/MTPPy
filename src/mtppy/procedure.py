from mtppy.suc_data_assembly import *


class Procedure(SUCServiceProcedure):
    def __init__(self, procedure_id: int, tag_name: str, tag_description='', is_self_completing=False, is_default=False):
        super().__init__(procedure_id, tag_name, tag_description, is_self_completing, is_default)
        self.procedure_parameters = {}
        self.process_value_ins = {}
        self.report_values = {}
        self.process_value_outs = {}

    def add_procedure_parameter(self, procedure_parameter: SUCOperationElement):
        if isinstance(procedure_parameter, SUCOperationElement):
            self.procedure_parameters[procedure_parameter.tag_name] = procedure_parameter
        else:
            raise TypeError()

    def add_procedure_value_in(self, process_value_in):
        raise NotImplementedError()

    def add_report_value(self, report_value: SUCIndicatorElement):
        if isinstance(report_value, SUCIndicatorElement):
            self.report_values[report_value.tag_name] = report_value
        else:
            raise TypeError()

    def add_procedure_value_out(self, process_value_out: SUCIndicatorElement):
        if isinstance(process_value_out, SUCIndicatorElement):
            self.process_value_outs[process_value_out.tag_name] = process_value_out
        else:
            raise TypeError()

    def apply_procedure_parameters(self):
        print('Applying procedure parameters')
        for procedure_parameter in self.procedure_parameters.values():
            procedure_parameter.set_v_out()
