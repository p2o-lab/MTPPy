from src.DataAssembly import DataAssembly

class DiagnosticElement(DataAssembly):
    def __init__(self):
        super(DiagnosticElement,self).__init__()
        self.WQC=0

class HealthStateView(DiagnosticElement):
    def __init__(self):
        super(HealthStateView,self).__init__()
