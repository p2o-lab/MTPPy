

class Procedure(object):
    def __init__(self):
        self.IsSelfCompleting=False
        self.ProcedureId=0
        self.IsDefault=False

    def get_procedureid(self):
        return self.ProcedureId

    def get_isdefault(self):
        return self.IsDefault

    def get_isselfcompleting(self):
        return self.IsSelfCompleting
