import logging

from mtppy.suc_data_assembly import *


class Procedure(SUCServiceProcedure):
    def __init__(self, procedure_id: int, tag_name: str, tag_description: str = '', is_self_completing: bool = False,
                 is_default: bool = False):
        """
        Represents a procedure of a service.
        :param procedure_id: Procedure id.
        :param tag_name: Tag name of the procedure.
        :param tag_description: Tag description of the procedure.
        :param is_self_completing: Self-completing or not.
        :param is_default: Default or not.
        """
        super().__init__(procedure_id, tag_name, tag_description, is_self_completing, is_default)
        self.procedure_parameters = {}
        self.process_value_ins = {}
        self.report_values = {}
        self.process_value_outs = {}

    def add_procedure_parameter(self, procedure_parameter: SUCOperationElement):
        """
        Adds a procedure parameter to the procedure.
        :param procedure_parameter: Procedure parameter.
        :return:
        """
        if isinstance(procedure_parameter, SUCOperationElement):
            self.procedure_parameters[procedure_parameter.tag_name] = procedure_parameter
        else:
            raise TypeError()

    def add_procedure_value_in(self, process_value_in):
        """
        Adds an value in to the procedure. NOT IMPLEMENTED.
        :param process_value_in: Value in.
        :return:
        """
        raise NotImplementedError()

    def add_report_value(self, report_value: SUCIndicatorElement):
        """
        Adds a report value to the procedure.
        :param report_value: Report value.
        :return:
        """
        if isinstance(report_value, SUCIndicatorElement):
            self.report_values[report_value.tag_name] = report_value
        else:
            raise TypeError()

    def add_procedure_value_out(self, process_value_out: SUCIndicatorElement):
        """
        Adds an value out to the procedure.
        :param process_value_out: Value in.
        :return:
        """
        if isinstance(process_value_out, SUCIndicatorElement):
            self.process_value_outs[process_value_out.tag_name] = process_value_out
        else:
            raise TypeError()

    def apply_procedure_parameters(self):
        """
        Applies procedure parameters.
        :return:
        """
        logging.debug('Applying procedure parameters')
        for procedure_parameter in self.procedure_parameters.values():
            procedure_parameter.set_v_out()
