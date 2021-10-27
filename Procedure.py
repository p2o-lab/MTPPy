

class Procedure(object):
    def __init__(self,ProcedureId:int,SelfCompleting:bool=False,IsDefault:bool=False):
        self.IsSelfCompleting=SelfCompleting
        self.ProcedureId=ProcedureId
        self.IsDefault=IsDefault

    def get_procedureid(self):
        return self.ProcedureId

    def get_isdefault(self):
        return self.IsDefault

    def get_isselfcompleting(self):
        return self.IsSelfCompleting
