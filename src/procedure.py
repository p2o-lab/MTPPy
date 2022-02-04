class Procedure:
    def __init__(self, procedure_id, is_self_completing=False, is_default=False):
        self.procedure_id = procedure_id
        self.is_self_completing = is_self_completing
        self.is_default = is_default
        self.procedure_parameters = []
        self.process_value_ins = []
        self.report_values = []
        self.process_value_outs = []

    def add_procedure_parameter(self, procedure_parameter):
        self.procedure_parameters.append(procedure_parameter)

    def add_procedure_value_in(self, process_value_in):
        self.process_value_ins.append(process_value_in)

    def add_report_value(self, report_value):
        self.report_values.append(report_value)

    def add_procedure_value_out(self, process_value_out):
        self.process_value_outs.append(process_value_out)
