from src.data_assembly import DataAssembly
from src.operation_mode import OperationMode
from src.source_mode import SourceMode


class ServiceControl(DataAssembly):

    def __init__(self, tag_name, tag_description):
        super().__init__(tag_name, tag_description)

        self.WQC = 255
        self.OSLevel = 0

        self.CommandOp = False
        self.CommandInt = False
        self.CommandExt = False

        self.ProcedureOp = False
        self.ProcedureInt = False
        self.ProcedureExt = False
        self.ProcedureCur = 0
        self.ProcedureReq = 0

        self.PosTextID = 0
        self.InteractQuestionID = 0
        self.InteractAnswerID = 0

        self.operation_mode = OperationMode()
        self.source_mode = SourceMode()
