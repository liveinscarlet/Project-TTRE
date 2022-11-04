#import visa
import pyvisa

class oscil(object):
    if __name__ == '__main__':
        rm = pyvisa.ResourceManager()
        myinst = rm.open_resource("TCPIP0::192.168.1.10::inst0::INSTR") #Для корректной работы надо отключать защиту осцила
    print(myinst.query("*IDN?"))
    #def dataExtraction (self):

    pass

class PURigol (object):
    if __name__ == '__main__':
        rm = pyvisa.ResourceManager()
        #myinst = rm.open_resource("TCPIP0::192.168.1.10::inst0::INSTR") Узнать IP БП и поменять код соответственно
    pass



