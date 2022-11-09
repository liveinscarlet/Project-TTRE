from visa import *
from pyvisa import vpp43

## Requires VISA installed on Control PC
## 'http://www.agilent.com/find/visa'
## Requires PyVISA to use VISA in Python
## 'http://pyvisa.sourceforge.net/pyvisa/'

## N1010A Remove S4P Example:
## 86108A Module in Slot 1/2

## Connecton to N1010A software is accomplished via LAN and the following connections are supported
## SOCKET LAN Visa Address: 'TCPIP0::156.140.158.223::5025::SOCKET'
## HiSLIP LAN Visa Address: '156.140.158.223::hislip0::INSTR'
## The N1010A software does not support the following connections
## GPIB Visa Address'GPIB0::7::INSTR'
## VXI-11 LAN Visa Address: 'TCPIP0::156.140.158.223::inst0::INSTR'
myinst = vpp43.open(resource_manager.session,"TCPIP0::156.140.158.223::5025::SOCKET", access_mode=0, open_timeout=5000)

##Set Timeout
vpp43.set_attribute(myinst, VI_ATTR_TMO_VALUE, 10000)

##set termination character to CHR(10) (i.e. "\n")
##enable terminate reads on termination character
vpp43.set_attribute(myinst, VI_ATTR_TERMCHAR, 10)
vpp43.set_attribute(myinst, VI_ATTR_TERMCHAR_EN, 1)

## Inst ID Query
vpp43.write(myinst, "*CLS"+chr(10))

## Skip setup if not using 86108A
## setup=0 skip
## setup=1 perform
setup=0
if setup:

    ## Reset Instrument
    vpp43.write(myinst, ":SYSTem:DEFault"+chr(10))
    vpp43.write(myinst, "*OPC?"+chr(10))
    print "Default Setup Complete: " + vpp43.read(myinst, 100)

    ## Activate Measurement Channels
    ## Set channel BW to 32 GHz
    vpp43.write(myinst, ":CHAN1A:BANDwidth BANDwidth3"+chr(10))

    ## Lock CDR
    ## Set CDR Rate to 10G
    vpp43.write(myinst, ":CRECovery1:CRATe 1.03125E+10"+chr(10))
    ## Set CDR PLL BW to 500 kHz
    vpp43.write(myinst, ":CRECovery1:CLBandwidth 5.00E+5"+chr(10))
    ## Lock CDR
    vpp43.write(myinst, ":CRECovery1:RELock"+chr(10))
    vpp43.write(myinst, "*OPC?"+chr(10))
    print "CDR Setup Complete: " + vpp43.read(myinst, 100)

    ## Turn on PTB
    vpp43.write(myinst, ":PTIMebase1:RSOurce INTernal"+chr(10))
    vpp43.write(myinst, ":PTIMebase1:STATe ON"+chr(10))
    vpp43.write(myinst, ":PTIMebase1:RTReference"+chr(10))
    vpp43.write(myinst, "*OPC?"+chr(10))
    print "PTB Setup Complete: " + vpp43.read(myinst, 100)


## Activate Pattern Lock
vpp43.write(myinst, ":TRIGger:PLOCk ON"+chr(10))
vpp43.write(myinst, "*OPC?"+chr(10))
print "Pattern Lock Setup Complete: " + vpp43.read(myinst, 100)


## Enter Eye Diagram Mode
vpp43.write(myinst, ":SYSTem:MODE EYE"+chr(10))

## Setup Apply S2P Math Function
## Define Math Function Apply S2P
vpp43.write(myinst, ":FUNCtion2:FOPerator CONVolve"+chr(10))
vpp43.write(myinst, ":SPRocess2:CONVolve:FNAMe \"C:\\Program Files\\Agilent\\FlexDCA\\Demo\\S-Parameter Data\\Demo\\TDRDemoBoard_ET55780\\ET55780_10.5inch_Equalization.s2p\""+chr(10))
##Define Input Channel for Math Function
vpp43.write(myinst, ":FUNCtion2:OPERand1 CHAN1A"+chr(10))
##Define Color for Math Function 2
vpp43.write(myinst, ":FUNCtion2:COLor TCOLor5"+chr(10))
##Turn on Math Function 2
vpp43.write(myinst, ":FUNCtion2:DISPlay ON"+chr(10))

## Autoscale
vpp43.write(myinst, ":SYST:AUT"+chr(10))
vpp43.write(myinst, "*OPC?"+chr(10))
print "Pattern Lock Setup Complete: " + vpp43.read(myinst, 100)

## Setup Acquisition Limit
vpp43.write(myinst, ":ACQuire:CDISplay"+chr(10))
vpp43.write(myinst, ":LTESt:ACQuire:CTYPe:PATTerns 1"+chr(10))
vpp43.write(myinst, ":LTESt:ACQuire:STATe ON"+chr(10))
vpp43.write(myinst, ":ACQuire:RUN"+chr(10))
vpp43.write(myinst, "*OPC?"+chr(10))
print "Acquisition Limit Complete: " + vpp43.read(myinst, 100)


## Save Pattern Waveform
## Define Source as math function
vpp43.write(myinst, ":DISK:WAVeform:SAVE:SOURce FUNCtion2"+chr(10))
## Define format as CSV
vpp43.write(myinst, ":DISK:WAVeform:FFORmat TEXT"+chr(10))
## Define file name 
vpp43.write(myinst, ":DISK:WAVeform:FNAMe \"D:\\User Files\\Waveforms\\patternwaveform2.csv\""+chr(10))
## Save File to directory 'D:\User Files\Waveforms'
vpp43.write(myinst, ":DISK:WAVeform:SAVE"+chr(10))
vpp43.write(myinst, "*OPC?"+chr(10))
print "Pattern Waveform Save Complete: " + vpp43.read(myinst, 100)

## Save Screen Image
## Define file name
vpp43.write(myinst, ":DISK:SIMage:FNAMe \"D:\\User Files\\Screen Images\\screenimage2.jpg\""+chr(10))
## Save Screen Image
vpp43.write(myinst, ":DISK:SIMage:SAVE"+chr(10))
vpp43.write(myinst, "*OPC?"+chr(10))
print "Screen Image Save Complete: " + vpp43.read(myinst, 100)

## Turn off Acquisition Limit
vpp43.write(myinst, ":LTESt:ACQuire:STATe OFF"+chr(10))

## Query for Instrument Messages
while True:
    vpp43.write(myinst, ":SYSTem:ERRor?"+chr(10))
    Result = vpp43.read(myinst, 100)
    ErrorList = Result.split(',')
    Error = ErrorList[0]
    print "Message #: " + ErrorList[0]
    print "Message Description: " + ErrorList[1]
    if int(Error) == 0:
        break

vpp43.close(myinst)
print "Complete"

        