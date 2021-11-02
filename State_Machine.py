#   States: ['Idle','Starting','Execute','Completing',
#         'Completed','Resuming','Paused','Pausing',
#         'Holding','Held','Unholding','Stopping','Stopped',
#         'Aborting','Aborted','Resetting']'

class Statemachine():
    def __init__(self):

        self.Pause_disabled=False
        self.Hold_disabled=False
        self.Pause_Hold_disabled=False

        self.Idle=16
        self.Starting=8
        self.Execute=64
        self.Completing=65536
        self.Completed=131072
        self.Resuming=16384
        self.Paused=32
        self.Pausing=8192
        self.Holding=1024
        self.Held=2048
        self.Unholding=4096
        self.Stopping=128
        self.Stopped=4
        self.Aborting=256
        self.Aborted=512
        self.Resetting=32678

        # [Undef,ResetEn,StartEn,StopEn,HoldEn,UnholdEn,PauseEn,ResumeEn,AbortEn,RestartEn,CompleteEn]

        self.IdleEn=268
        self.StartingEn=280
        self.CompletingEn=2266
        self.CompletedEn=266
        self.ResumingEn=280
        self.PausedEn=408
        self.PausingEn=280
        self.HoldingEn=264
        self.HeldEn=296
        self.UnholdingEn=280
        self.StoppingEn=256
        self.StoppedEn=258
        self.AbortingEn=0
        self.AbortedEn=2
        self.ResettingEn=264
        self.ExecuteEn = 1880

        self.act_state=self.Idle

    #TODO implement error messages if not valid state changes are blocked
    def Start(self, SC=True):
        if self.act_state==self.Idle:
            self.act_state = self.Starting
        if self.act_state==self.Starting and SC==True:
            self.act_state=self.Execute

    def Restart(self, SC=True):
        if self.act_state==self.Execute:
            self.act_state=self.Starting
        if self.act_state==self.Starting and SC==True:
            self.act_state=self.Execute

    def Complete(self,SC=True):
        if self.act_state==self.Execute:
            self.act_state=self.Completing
        if self.act_state==self.Completing and SC==True:
            self.act_state=self.Completed

    def Pause(self,SC=True):
        if self.act_state==self.Execute and self.Pause_disabled==False and self.Pause_Hold_disabled==False:
            self.act_state=self.Pausing
        if self.act_state==self.Pausing and SC==True:
            self.act_state=self.Paused

    def Resume(self,SC=True):
        if self.act_state==self.Paused:
            self.act_state=self.Resuming
        if self.act_state==self.Resuming and SC==True:
            self.act_state=self.Execute

    def Reset(self,SC=True):
        if self.act_state in [self.Completed,self.Stopped,self.Aborted]:
            self.act_state=self.Resetting
        if self.act_state==self.Resetting and SC==True:
            self.act_state=self.Idle

    def Hold(self,SC=True):
        if self.act_state in [self.Starting,self.Execute,self.Completing,
                self.Resuming,self.Paused,self.Pausing,self.Unholding] \
                and self.Hold_disabled==False and self.Pause_Hold_disabled==False :

            self.act_state=self.Holding
        if self.act_state==self.Holding and SC==True:
            self.act_state=self.Held

    def Unhold(self,SC=True):
        if self.act_state==self.Held:
            self.act_state=self.Unholding
        if self.act_state==self.Unholding and SC==True:
            self.act_state=self.Execute

    def Stop(self,SC=True):
        if self.act_state in [self.Idle,self.Starting,self.Execute,self.Completing,
                self.Completed,self.Resuming,self.Paused,self.Pausing,
                self.Holding,self.Held,self.Unholding,self.Resetting]:
            self.act_state=self.Stopping
        if self.act_state==self.Stopping and SC==True:
            self.act_state=self.Stopped

    def Abort(self,SC=True):
        if self.act_state in [self.Idle,self.Starting,self.Execute,self.Completing,
                self.Completed,self.Resuming,self.Paused,self.Pausing,
                self.Holding,self.Held,self.Unholding,self.Stopping,self.Stopped,self.Resetting]:
            self.act_state=self.Aborting
        if self.act_state==self.Aborting and SC==True:
            self.act_state=self.Aborted

    def get_current_state(self):

        CurrentState=self.act_state

        return CurrentState

    def get_command_en(self):
        CommandEN=0
        if self.act_state==self.Idle: CommandEN=self.IdleEn
        if self.act_state==self.Starting: CommandEN=self.StartingEn
        if self.act_state==self.Execute: CommandEN=self.ExecuteEn
        if self.act_state==self.Completing: CommandEN=self.CompletingEn
        if self.act_state==self.Completed: CommandEN=self.CompletedEn
        if self.act_state==self.Resuming: CommandEN=self.ResumingEn
        if self.act_state==self.Paused: CommandEN=self.PausedEn
        if self.act_state==self.Pausing: CommandEN=self.PausingEn
        if self.act_state==self.Holding: CommandEN=self.HoldingEn
        if self.act_state==self.Held: CommandEN=self.HeldEn
        if self.act_state==self.Unholding: CommandEN=self.UnholdingEn
        if self.act_state==self.Stopping: CommandEN=self.StoppingEn
        if self.act_state==self.Stopped: CommandEN=self.StoppedEn
        if self.act_state==self.Aborting: CommandEN=self.AbortingEn
        if self.act_state==self.Aborted: CommandEN=self.AbortedEn
        if self.act_state==self.Resetting: CommandEN=self.ResettingEn

        return CommandEN

    def ex_command(self,com_var:int,SC:bool=True):
        if com_var==2:
            self.Reset(SC)
        elif com_var==4:
            self.Start(SC)
        elif com_var==8:
            self.Stop(SC)
        elif com_var==16:
            self.Hold(SC)
        elif com_var==32:
            self.Unhold(SC)
        elif com_var==64:
            self.Pause(SC)
        elif com_var==128:
            self.Resume(SC)
        elif com_var==256:
            self.Abort(SC)
        elif com_var==512:
            self.Restart(SC)
        elif com_var==1024:
            self.Complete(SC)

#TODo discuss if the stop and abort loop are possible to disable

def diasable_pause_loop(self):

    self.Pause_disabled=True
    self.ExecuteEn = 1816

def disable_hold_loop(self):

    self.Hold_disabled=True

    self.StartingEn = 280
    self.ExecuteEn = 1880
    self.CompletingEn = 266
    self.ResumingEn = 280
    self.PausedEn = 408
    self.PausingEn = 280
    self.UnholdingEn = 280

def disable_hold_paus_loop(self):

    self.Pause_Hold_disabled = True
    self.StartingEn = 280
    self.ExecuteEn = 1816
    self.CompletingEn = 266
    self.ResumingEn = 280
    self.PausedEn = 408
    self.PausingEn = 280
    self.UnholdingEn = 280

def enable_all_loops(self):

    self.Pause_disabled = False
    self.Hold_disabled=False
    self.Pause_Hold_disabled = False

    self.IdleEn = 268
    self.StartingEn = 280
    self.CompletingEn = 2266
    self.CompletedEn = 266
    self.ResumingEn = 280
    self.PausedEn = 408
    self.PausingEn = 280
    self.HoldingEn = 264
    self.HeldEn = 296
    self.UnholdingEn = 280
    self.StoppingEn = 256
    self.StoppedEn = 258
    self.AbortingEn = 0
    self.AbortedEn = 2
    self.ResettingEn = 264
    self.ExecuteEn = 1880
