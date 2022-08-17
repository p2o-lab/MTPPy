import logging

from mtppy.attribute import Attribute
from mtppy.operation_source_mode import OperationSourceMode


class ProcedureControl:
    def __init__(self, procedures: dict, service_op_src_mode: OperationSourceMode):
        """
        Represents the procedure control.
        :param procedures: Procedures.
        :param service_op_src_mode: Operation and source mode of the service.
        """
        self.attributes = {
            'ProcedureOp': Attribute('ProcedureOp', int, init_value=0, sub_cb=self.set_procedure_op),
            'ProcedureInt': Attribute('ProcedureInt', int, init_value=0, sub_cb=self.set_procedure_int),
            'ProcedureExt': Attribute('ProcedureExt', int, init_value=0, sub_cb=self.set_procedure_ext),
            'ProcedureCur': Attribute('ProcedureCur', int, init_value=0),
            'ProcedureReq': Attribute('ProcedureReq', int, init_value=0),
        }

        self.procedures = procedures
        self.op_src_mode = service_op_src_mode
        self.default_procedure_id = None

    def set_procedure_op(self, value: int):
        logging.debug('ProcedureOP set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct'].value:
            self.set_procedure_req(value)

    def set_procedure_int(self, value: int):
        logging.debug('ProcedureInt set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and self.op_src_mode.attributes['SrcIntAct'].value:
            self.set_procedure_req(value)

    def set_procedure_ext(self, value: int):
        logging.debug('ProcedureExt set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'].value and self.op_src_mode.attributes['SrcExtAct'].value:
            self.set_procedure_req(value)

    def valid_value(self, value: int):
        if value not in self.procedures.keys():
            return False
        else:
            return True

    def set_procedure_req(self, value: int):
        if self.valid_value(value):
            self.attributes['ProcedureReq'].set_value(value)
            logging.debug('ProcedureReq set to %s' % value)
        else:
            logging.debug('ProcedureReq cannot be set to %s (out of range)' % value)

    def set_procedure_cur(self):
        procedure_req = self.attributes['ProcedureReq'].value
        self.attributes['ProcedureCur'].set_value(procedure_req)
        logging.debug('ProcedureCur set to %s' % procedure_req)

    def get_procedure_cur(self):
        return self.attributes['ProcedureCur'].value

    def apply_procedure_parameters(self):
        self.procedures[self.get_procedure_cur()].apply_procedure_parameters()
