from mtppy.attribute import Attribute


class ProcedureControl:

    def __init__(self, procedures, service_op_src_mode):
        self.procedures = procedures
        self.op_src_mode = service_op_src_mode
        self.default_procedure_id = None

        self.attributes = {}
        self._init_attributes()

    def _init_attributes(self):
        self.attributes = {
            'ProcedureOp': Attribute('ProcedureOp', int, init_value=0, sub_cb=self.set_procedure_op),
            'ProcedureInt': Attribute('ProcedureInt', int, init_value=0, sub_cb=self.set_procedure_int),
            'ProcedureExt': Attribute('ProcedureExt', int, init_value=0, sub_cb=self.set_procedure_ext),
            'ProcedureCur': Attribute('ProcedureCur', int, init_value=0),
            'ProcedureReq': Attribute('ProcedureReq', int, init_value=0),
        }

    def set_procedure_op(self, value):
        print('ProcedureOP set to %s' % value)
        if self.op_src_mode.attributes['StateOpAct']:
            self.set_procedure_req(value)

    def set_procedure_int(self, value):
        print('ProcedureInt set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcIntAct']:
            self.set_procedure_req(value)

    def set_procedure_ext(self, value):
        print('ProcedureExt set to %s' % value)
        if self.op_src_mode.attributes['StateAutAct'] and self.op_src_mode.attributes['SrcExtAct']:
            self.set_procedure_req(value)

    def valid_value(self, value):
        if value not in self.procedures.keys():
            return False
        else:
            return True

    def set_procedure_req(self, value):
        if self.valid_value(value):
            self.attributes['ProcedureReq'].set_value(value)
            print('ProcedureReq set to %s' % value)
        else:
            print('ProcedureReq cannot be set to %s (out of range)' % value)

    def set_procedure_cur(self):
        procedure_req = self.attributes['ProcedureReq'].value
        self.attributes['ProcedureCur'].set_value(procedure_req)
        print('ProcedureCur set to %s' % procedure_req)

    def get_procedure_cur(self):
        return self.attributes['ProcedureCur'].value
