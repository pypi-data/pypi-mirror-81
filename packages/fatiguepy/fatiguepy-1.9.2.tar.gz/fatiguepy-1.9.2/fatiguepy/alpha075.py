import numpy as np
from . import prob_moment, Narrow_Band, Rainflow

class AL:
    def __new__(cls, *args, **kwargs):
        instance = super(AL, cls).__new__(cls)
        return instance

    def __init__(self, k, C, Y, f, xf, s):
        self.k = k
        self.C = C
        self.Y = Y
        self.f = f
        self.xf = xf
        self.s = s
        moment = prob_moment.Probability_Moment(self.Y, self.f)
        self.alpha075 = moment.alpha075()
        self.DNB = Narrow_Band.NB(self.k, self.C, self.Y, self.f, self.xf, self.s).Damage()

    def Damage(self):

        DAL = (self.alpha075**2) * self.DNB

        return DAL

    def Lifes(self):  # ciclos
        TALs = 1 / self.Damage()
        return TALs

    def Lifeh(self):  # horas
        TALh = self.xf * self.Life() / (60 * 60)
        return TALh
    
    def Life(self):
        TAL = self.Lifes()/self.xf
        return TAL
    
    def relative_error(self, y, x, method="Rainflow", experimental_value=None, type='cycles'):
        if type=="cycles":
            AL_value = self.Life()
            RF_value = Rainflow.rainflowD(self.C, self.k, y, x).Life()
        elif type=="damage":
            AL_value = self.Damage()
            RF_value = Rainflow.rainflowD(self.C, self.k, y, x).Damage()
        elif type!="cycles" and type!="damage":
            raise UnboundLocalError("Invalid type. Try 'cycles' or 'damage'")
        
        if(method == "Rainflow"):
            err = (AL_value - RF_value)/RF_value
        elif(method == "Experimental" and experimental_value != None):
            EX_value = experimental_value
            err = (AL_value - EX_value)/EX_value
        elif(method == "Experimental" and experimental_value == None):
            raise UnboundLocalError("Dexperimental must be different from None for method 'Experimental'")
        elif(method != "Experimental" and method != "Rainflow"):
            raise UnboundLocalError("Invalid Method. Try method='Rainflow' or method='Experimental'")

        return err
