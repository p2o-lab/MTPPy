from mtppy.suc_data_assembly import SUCServiceProcedure


class Procedure(SUCServiceProcedure):
    def __init__(self, procedure_id, tag_name, tag_description='', is_self_completing=False, is_default=False):
        super().__init__(procedure_id, tag_name, tag_description, is_self_completing, is_default)
        self.procedure_parameters = {}
        self.process_value_ins = {}
        self.report_values = {}
        self.process_value_outs = {}

    def add_procedure_parameter(self, procedure_parameter):
        self.procedure_parameters[procedure_parameter.tag_name] = procedure_parameter

    def add_procedure_value_in(self, process_value_in):
        self.process_value_ins[process_value_in.tag_name] = process_value_in

    def add_report_value(self, report_value):
        self.report_values[report_value.tag_name] = report_value

    def add_procedure_value_out(self, process_value_out):
        self.process_value_outs[process_value_out.tag_name] = process_value_out
