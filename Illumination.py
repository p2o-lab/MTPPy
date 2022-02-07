from Service_control import Service_control
from src.Procedure import Procedure

#import RPi.GPIO as GPIO

class Continous(Procedure):
    def __init__(self):
        super(Continous,self).__init__()
        self.IsSelfCompleting=False
        self.ProcedureId=0
        self.IsDefault=True

class Strobe_mode(Procedure):
    def __init__(self):
        super(Strobe_mode,self).__init__()
        self.IsSelfCompleting=False
        self.ProcedureId=1
        self.IsDefault=False

class Trigger_based(Procedure):
    def __init__(self):
        super(Trigger_based,self).__init__()
        self.IsSelfCompleting=False
        self.ProcedureId=2
        self.IsDefault=False

class Illuminaton(Service_control):
    def __init__(self,node,client,opc_address,Wavelength,Intensity_setpoint,
                 Frequency_setpoint,Duration_setpoint,Intensity_feedback):
        super(Illuminaton,self).__init__(node,client,opc_address)
        self.Wavelength=Wavelength
        self.Wavelength.VMax=800
        self.Intensity_setpoint=Intensity_setpoint
        self.Frequency_setpoint=Frequency_setpoint
        self.Duration_setpoint=Duration_setpoint
        self.Intensity_feedback=Intensity_feedback
        #self.Light_trigger=Light_trigger

        self.P_Continous=Continous()
        self.P_Strobe_mode=Strobe_mode()
        self.P_Trigger_based=Trigger_based()
        
        # GPIO.setwarnings(False)
        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(31, GPIO.OUT)
        # GPIO.setup(33, GPIO.OUT)
        # GPIO.setup(35, GPIO.OUT)
        #
        # self.R = GPIO.PWM(35,200)
        # self.G = GPIO.PWM(31,200)
        # self.B = GPIO.PWM(33,200)


    def Idle(self):
       pass

    def Starting(self):
        self.Wavelength.set_VOut()
        self.Intensity_setpoint.set_VOut()
        self.Frequency_setpoint.set_VOut()
        self.Duration_setpoint.set_VOut()
        self.R.start(0)
        self.G.start(0)
        self.B.start(0)

        self.Service_SM.Start(sc=True)

    def Execute(self):
        R1, G1, B1 = self.wavelength_to_rgb(self.Wavelength.VOut)
        Intensity=self.Intensity_setpoint.VOut/100     
        print(Intensity,R1,G1,B1,)
        if self.ProcedureCur==self.P_Continous.ProcedureId:
            self.R.ChangeDutyCycle(Intensity*R1)
            self.G.ChangeDutyCycle(Intensity*G1)
            self.B.ChangeDutyCycle(Intensity*B1)
            

        if self.ProcedureCur == self.P_Strobe_mode.ProcedureId:
            while self.stop_execute==False:
                pass
                # self.R_GPIO.ChangeDutyCycle(Intensity*R1)
                # self.G_GPIO.ChangeDutyCycle(Intensity*G1)
                # self.B_GPIO.ChangeDutyCycle(Intensity*B1)
                # sleep(self.Duration_setpoint.VOut)
                # self.R_GPIO.ChangeDutyCycle(0)
                # self.G_GPIO.ChangeDutyCycle(0)
                # self.B_GPIO.ChangeDutyCycle(0)
        # if self.ProcedureCur == self.P_Strobe_mode.ProcedureId:
        #     while self.stop_execute==False:
        #         if self.Light_trigger==True:
        #             # self.R_GPIO.ChangeDutyCycle(10,Intensity*(self.R/255))
        #             # self.G_GPIO.ChangeDutyCycle(11,Intensity*(self.G/255))
        #             # self.B_GPIO.ChangeDutyCycle(12,Intensity*(self.B/255))
        #             pass
        #         else:
        #             # self.R_GPIO.ChangeDutyCycle(10,0)
        #             # self.G_GPIO.ChangeDutyCycle(11,0)
        #             # self.B_GPIO.ChangeDutyCycle(12,0)
        #             pass


    def Completing(self):
        # self.R.stop()
        # self.G.stop()
        # self.B.stop()
        #GPIO.cleanup()
        self.Service_SM.Complete(SC=True)


    def Completed(self):
        pass

    def Resuming(self):
        self.Service_SM.Resume(SC=True)

    def Paused(self):
        pass

    def Pausing(self):
        self.Service_SM.Pause(SC=True)

    def Holding(self):
        self.Service_SM.Hold(SC=True)

    def Held(self):
        pass

    def Unholding(self):
        self.Service_SM.Unhold(SC=True)

    def Stopping(self):
        self.Service_SM.Stop(SC=True)

    def Stopped(self):
        pass

    def Aborting(self):
        self.Service_SM.Abort(SC=True)

    def Aborted(self):
        pass

    def Resetting(self):
        self.Service_SM.Reset(SC=True)

    def Sync_operation_mode(self):
        pass

    def Service_activated(self):
        pass

    def wavelength_to_rgb(self,Wavelength, gamma=1):

        '''This converts a given wavelength of light to an
        approximate RGB color value. The wavelength must be given
        in nanometers in the range from 380 nm through 750 nm
        (789 THz through 400 THz).
        Based on code by Dan Bruton
        http://www.physics.sfasu.edu/astro/color/spectra.html
        '''

        wavelength = Wavelength
        
        if wavelength >= 380 and wavelength <= 440:
            attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
            R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
            G = 0.0
            B = (1.0 * attenuation) ** gamma
        elif wavelength >= 440 and wavelength <= 490:
            R = 0.0
            G = ((wavelength - 440) / (490 - 440)) ** gamma
            B = 1.0
        elif wavelength >= 490 and wavelength <= 510:
            R = 0.0
            G = 1.0
            B = (-(wavelength - 510) / (510 - 490)) ** gamma
        elif wavelength >= 510 and wavelength <= 580:
            R = ((wavelength - 510) / (580 - 510)) ** gamma
            G = 1.0
            B = 0.0
        elif wavelength >= 580 and wavelength <= 645:
            R = 1.0
            G = (-(wavelength - 645) / (645 - 580)) ** gamma
            B = 0.0
        elif wavelength >= 645 and wavelength <= 750:
            attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
            R = (1.0 * attenuation) ** gamma
            G = 0.0
            B = 0.0
        else:
            R = 0.0
            G = 0.0
            B = 0.0

        return (int(100*R), int(100*G), int(100*B))