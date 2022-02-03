from src.DataAssembly import DataAssembly

class ActiveElement(DataAssembly):
    def __init__(self):
        super(DataAssembly,self).__init__()
        self.WQC=0
        self.OSLevel

class PIDCtrl(ActiveElement):
    ##Todo implement functionality
    def __init__(self):
        super(ActiveElement,self).__init__()
        self.StateChannel=False
        self.StateOffAut=False
        self.StateOpAut=False
        self.StateAutAut=False
        self.StateOffOp=False
        self.StateOpOp=False
        self.StateAutOp=False
        self.StateOpAct=False
        self.StateAutAct=False
        self.StateOffAct=False
        self.SrcChannel=False
        self.SrcManAut=False
        self.SrcIntAut=False
        self.SrcIntOp=False
        self.SrcManOp=False
        self.SrcIntAct=False
        self.SrcManAct=False
        self.PV=0
        self.PVSclMin=0
        self.PVSclMax=100
        self.PVUnit=0
        self.SPMan=0
        self.SPInt=0
        self.SPSclMin=0
        self.SPSclMax=100
        self.SPUnit=0
        self.SPIntMin=0
        self.SPIntMax=100
        self.SPManMin=0
        self.SPManMax=100
        self.SP=0
        self.MVMan=0
        self.MV=0
        self.MVMin=0
        self.MVMax=100
        self.MVUnit=0
        self.MVSclMin=0
        self.MVSclMax=100
        self.P=0
        self.Ti=0
        self.Td=0

class BinVlv(ActiveElement):
    ##Todo implement functionality
    def __init__(self):
        super(ActiveElement,self).__init__()
        self.StateChannel=False
        self.StateOffAut=False
        self.StateOpAut=False
        self.StateAutAut=False
        self.StateOffOp=False
        self.StateOpOp=False
        self.StateAutOp=False
        self.StateOpAct=False
        self.StateAutAct=False
        self.StateOffAct=False
        self.SafePos=False
        self.SafePosEn=False
        self.SafePosAct=False
        self.OpenOp=False
        self.CloseOp=False
        self.OpenAut=False
        self.CloseAut=False
        self.Ctrl=False
        self.OpenFbkCalc=False
        self.OpenFbk=False
        self.CloseFbkCalc=False
        self.CloseFbk=False
        self.PermEn=False
        self.Permit=False
        self.IntlEn=False
        self.Interlock=False
        self.ProtEn=False
        self.Protect=False
        self.ResetOp=False
        self.ResetAut=False

class MonBinVlv(BinVlv):
    ##Todo implement functionality
    def __init__(self):
        super(BinVlv,self).__init__()
        self.MonEn=False
        self.MonSafePos=False
        self.MonStatErr=False
        self.MonDynErr=False
        self.MonStatTi=0
        self.MonDynTi=0

class AnaVlv(ActiveElement):
    ##Todo implement functionality
    def __init__(self):
        super(ActiveElement,self).__init__()
        self.StateChannel=False
        self.StateOffAut=False
        self.StateOpAut=False
        self.StateAutAut=False
        self.StateOffOp=False
        self.StateOpOp=False
        self.StateAutOp=False
        self.StateOpAct=False
        self.StateAutAct=False
        self.StateOffAct=False
        self.SrcChannel=False
        self.SrcManAut=False
        self.SrcIntAut=False
        self.SrcIntOp=False
        self.SrcManOp=False
        self.SrcIntAct=False
        self.SrcManAct=False
        self.SafePos=False
        self.SafePosEn=False
        self.SafePosAct=False
        self.OpenAut=False
        self.CloseAut=False
        self.OpenOp=False
        self.CloseOp=False
        self.OpenAct=False
        self.CloseAct=False
        self.PosSclMin=0
        self.PosSclMax=100
        self.PosUnit=0
        self.PosMin=0
        self.PosMax=100
        self.PosInt=0
        self.PosMan=0
        self.PosRbk=0
        self.Pos=0
        self.OpenFbkCalc=False
        self.OpenFbk=False
        self.CloseFbkCalc=False
        self.CloseFbk=False
        self.PosFbkCalc=False
        self.PosFbk=0
        self.PermEn=False
        self.Permit=False
        self.IntlEn=False
        self.Interlock=False
        self.ProtEn=False
        self.Protect=False
        self.ResetOp=False
        self.ResetAut=False

class MonAnaVlv(AnaVlv):
    ##Todo implement functionality
    def __init__(self):
        super(AnaVlv,self).__init__()
        self.MonEn=False
        self.MonSafePos=False
        self.MonStatErr=False
        self.MonDynErr=False
        self.MonStatTi=False
        self.MonDynTi=False
        self.PosReachedFbk=0
        self.PosTolerance=0
        self.MonPosTi=False
        self.MonPosErr=False

class BinDrv(ActiveElement):
    ##Todo implement functionality
    def __init__(self):
        super(ActiveElement,self).__init__()
        self.StateChannel=False
        self.StateOffAut=False
        self.StateOpAut=False
        self.StateAutAut=False
        self.StateOffOp=False
        self.StateOpOp=False
        self.StateAutOp=False
        self.StateOpAct=False
        self.StateAutAct=False
        self.StateOffAct=False
        self.SafePos=False
        self.SafePosAct=False
        self.FwdEn=False
        self.RevEn=False
        self.StopOp=False
        self.FwdOp=False
        self.RevOp=False
        self.StopAut=False
        self.FwdAut=False
        self.RevAut=False
        self.FwdCtrl=False
        self.RevCtrl=False
        self.RevFbkCalc=False
        self.RevFbk=False
        self.FwdFbkCalc=False
        self.FwdFbk=False
        self.Trip=False
        self.PermEn=False
        self.Permit=False
        self.IntlEn=False
        self.Interlock=False
        self.ProtEn=False
        self.Protect=False
        self.ResetOp=False
        self.ResetAut=False

class MonBinDrv(BinDrv):

    def __init__(self):
        super(BinDrv,self).__init__()
        self.MonEn=False
        self.MonSafePos=False
        self.MonStatErr=False
        self.MonDynErr=False
        self.MonStatTi=0
        self.MonDynTi=0

class AnaDrv(ActiveElement):
    def __init__(self):
        super(ActiveElement,self).__init__()
        self.StateChannel=False
        self.StateOffAut=False
        self.StateOpAut=False
        self.StateAutAut=False
        self.StateOffOp=False
        self.StateOpOp=False
        self.StateAutOp=False
        self.StateOpAct=False
        self.StateAutAct=False
        self.StateOffAct=False
        self.SrcChannel=False
        self.SrcManAut=False
        self.SrcIntAut=False
        self.SrcIntOp=False
        self.SrcManOp=False
        self.SrcIntAct=False
        self.SrcManAct=False
        self.SafePos=False
        self.SafePosAct=False
        self.FwdEn=False
        self.RevEn=False
        self.StopOp=False
        self.FwdOp=False
        self.RevOp=False
        self.StopAut=False
        self.FwdAut=False
        self.RevAut=False
        self.FwdCtrl=False
        self.RevCtrl=False
        self.RpmSclMin=0
        self.RpmSclMax=100
        self.RpmUnit=0
        self.RpmMin=0
        self.RpmMax=100
        self.RpmInt=0
        self.RpmMan=0
        self.Rpm=0
        self.RpmRbk=0
        self.RevFbkCalc=False
        self.RevFbk=False
        self.FwdFbkCalc=False
        self.FwdFbk=False
        self.RpmFbkCalc=False
        self.RpmFbk=False
        self.Trip=False
        self.PermEn=False
        self.Permit=False
        self.IntlEn=False
        self.Interlock=False
        self.ProtEn=False
        self.Protect=False
        self.ResetOp=False
        self.ResetAut=False

class MonAnaDrv(AnaDrv):
    def __init__(self):
        super(AnaDrv).__init__()
        self.MonEn=False
        self.MonSafePos=False
        self.MonStatErr=False
        self.MonDynErr=False
        self.MonStatTi=0
        self.MonDynTi=0
        self.RpmErr=False
        self.RpmAHEn=False
        self.RpmALEn=False
        self.RpmAHAct=False
        self.RpmALAct=False
        self.RpmAHLim=100
        self.RpmALLim=0








