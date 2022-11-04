#import visa
from numpy import arrange
import pyvisa

V_start, V_max, V_min = 0, 30, -30
step = 0.5
V_plus = arrange(V_start, V_max, step)  #Array of positive voltages
V_minus = arrange(V_min, V_start, step)  #Array of negative voltages

class oscil(object):
    if __name__ == '__main__':
        rm = pyvisa.ResourceManager()
        myOsc = rm.open_resource("TCPIP0::192.168.1.10::inst0::INSTR") #Для корректной работы надо отключать защиту осцила
    print(myOsc.query("*IDN?"))
    #def dataExtraction (self):

    pass

class PURigol (object):
    if __name__ == '__main__':
        rm = pyvisa.ResourceManager()
        myPU = rm.open_resource("TCPIP0::192.168.1.10::inst0::INSTR") #Узнать IP БП и поменять код соответственно
    print (myPU.querry("*IDN?"))

    def Deafult_Setup(self):
        PURigol.myPU.querry(":CH1 :CURR:PROT 0.1")
        PURigol.myPU.querry(":CH2 :CURR:PROT 0.1")
        PURigol.myPU.querry(":APPL CH1,0,0")
        PURigol.myPU.querry(":APPL CH2,0,0")

    def VoltagesChange (self):
        i, j = 0, 0
        for i in V_plus:
            for j in V_minus:
                PURigol.myPU.querry ("APPL CH2, j")
                j+=step
            j=0
            i+=step
            PURigol.myPU.querry("APPL CH1, i")

    def SetVolt (self, volt_plus, volt_minus):
        PURigol.myPU.querry(":APPL CH1, volt_plus")
        PURigol.myPU.querry(":APPL CH2, volt_minus")

    pass



