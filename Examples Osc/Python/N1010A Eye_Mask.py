from visa import *
from pyvisa import vpp43

## Requires VISA installed on Control PC
## 'http://www.agilent.com/find/visa'
## Requires PyVISA to use VISA in Python
## 'http://pyvisa.sourceforge.net/pyvisa/'

## N1010A Eye/Mask Example:
## 83496A/B module left slot 1
## 861xxA/B/C/D optical sampling module right slot 2

## Connecton to N1010A software is accomplished via LAN and the following connections are supported
## SOCKET LAN Visa Address: 'TCPIP0::156.140.158.223::5025::SOCKET'
## HiSLIP LAN Visa Address: '156.140.158.223::hislip0::INSTR'
## The N1010A software does not support the following connections
## GPIB Visa Address'GPIB0::7::INSTR'
## VXI-11 LAN Visa Address: 'TCPIP0::156.140.158.223::inst0::INSTR'

##"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
## Copyright © 2011 Agilent Technologies Inc. All rights reserved.
##
## You have a royalty-free right to use, modify, reproduce and distribute this
## example files (and/or any modified version) in any way you find useful, provided
## that you agree that Agilent has no warranty, obligations or liability for any
## Sample Application Files.
##
##"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
##


myinst = vpp43.open(resource_manager.session,"TCPIP0::156.140.158.223::5025::SOCKET", access_mode=0, open_timeout=5000)

##Set Timeout
vpp43.set_attribute(myinst, VI_ATTR_TMO_VALUE, 20000)

##set termination character to CHR(10) (i.e. "\n")
##enable terminate reads on termination character
vpp43.set_attribute(myinst, VI_ATTR_TERMCHAR, 10)
vpp43.set_attribute(myinst, VI_ATTR_TERMCHAR_EN, 1)

## Inst ID Query
vpp43.write(myinst, "*CLS"+chr(10))
vpp43.write(myinst, "*IDN?"+chr(10))
print vpp43.read(myinst, 100)

## Skip setup if not using CDR and Optical Module
## setup=0 skip
## setup=1 perform
setup=0
if setup:

    ## Reset Instrument 
    ##:SYSTem:DEFault
    vpp43.write(myinst, ":SYSTem:DEFault"+chr(10))
    vpp43.write(myinst, "*OPC?"+chr(10))
    print "Default Setup Complete: " + vpp43.read(myinst, 100)
    
    ## Setup clock recovery
    ## Select Data Rate for CDR
    vpp43.write(myinst, ":CRECovery1:CRATe 2.4880000E+9"+chr(10))
    ## Select PLL BW for CDR
    vpp43.write(myinst, ":CRECovery1:CLBandwidth 5.00E+5"+chr(10))
    
    ## Lock CDR
    vpp43.write(myinst, ":CRECovery1:RELock"+chr(10))
    vpp43.write(myinst, "*OPC?"+chr(10))
    print "Clock Recovery Setup Complete: " + vpp43.read(myinst, 100)
    
    ##:TRIGger:TSOurce SLOT1
    vpp43.write(myinst, ":TRIGger:SOurce SLOT1"+chr(10))
    
    ## Setup optical measurement channel
    ## Select Wavelength for Optical Channel
    vpp43.write(myinst, ":CHAN3A:WAVelength WAVelength2"+chr(10))
    ## Select Filter for Optical Channel
    vpp43.write(myinst, ":CHAN3A:FSELect FILTer2"+chr(10))
    ## Activate Filter
    vpp43.write(myinst, ":CHAN3A:FILTer ON"+chr(10))

## Select Eye/Mask Mode and Autoscale
vpp43.write(myinst, ":ACQ:RUN"+chr(10))
vpp43.write(myinst, ":SYSTem:MODE EYE"+chr(10))
## Autoscale Eye Diagram
vpp43.write(myinst, ":SYSTem:AUToscale"+chr(10))
vpp43.write(myinst, "*OPC?"+chr(10))
print "Channel Setup and Autoscale Complete: " + vpp43.read(myinst, 100)

##Define and Load Mask 
vpp43.write(myinst, ":MTESt:LOAD:FNAMe \"C:\\Program Files\\Agilent\\FlexDCA\\Demo\\Masks\\SONET_SDH\\002.48832 - STM016_OC48.mskx\""+chr(10))
vpp43.write(myinst, ":MTESt:LOAD"+chr(10))

## Setup Acquisition Limit and acquire data
vpp43.write(myinst, ":ACQuire:CDISplay"+chr(10))
vpp43.write(myinst, ":LTESt:ACQuire:CTYPe:WAVeforms 200"+chr(10))
vpp43.write(myinst, ":LTESt:ACQuire:STATe ON"+chr(10))
vpp43.write(myinst, ":ACQuire:RUN"+chr(10))
vpp43.write(myinst, "*OPC?"+chr(10))
print "Acquisition Complete: " + vpp43.read(myinst, 100)

##Setup Mask Margin
vpp43.write(myinst, ":MTESt:MARGin:STATe ON"+chr(10))
vpp43.write(myinst, ":MTESt:MARGin:METHod AUTO"+chr(10))
vpp43.write(myinst, ":MTESt:MARGin:AUTO:METHod HRATio"+chr(10))
vpp43.write(myinst, ":MTESt:MARGin:AUTO:HRATio 5e-5"+chr(10))

## Query Mask Test Result
vpp43.write(myinst, ":MEASure:MTESt:HREGion1?"+chr(10))
print "Region 1 Mask Hits: " + vpp43.read(myinst, 100)
vpp43.write(myinst, ":MEASure:MTESt:HREGion2?"+chr(10))
print "Region 2 Mask Hits: " + vpp43.read(myinst, 100)
vpp43.write(myinst, ":MEASure:MTESt:HREGion3?"+chr(10))
print "Region 3 Mask Hits: " + vpp43.read(myinst, 100)
vpp43.write(myinst, ":MEASure:MTESt:MARgin?"+chr(10))
print "Mask Test Margin: " + vpp43.read(myinst, 100)

## Query Measurement Results
##  For the most accurate Extinction Ratio Measurements refer to AN 1550-9 for correct procedure and calibration
##  http://cp.literature.agilent.com/litweb/pdf/5989-2602EN.pdf
vpp43.write(myinst, ":MEASure:EYE:ERATio"+chr(10))
vpp43.write(myinst, ":MEASure:EYE:ERATio?"+chr(10))
print "Extinctionn Ratio: " + vpp43.read(myinst, 100)
vpp43.write(myinst, ":MEASure:EYE:AMPLitude"+chr(10))
vpp43.write(myinst, ":MEASure:EYE:AMPLitude?"+chr(10))
print "Eye Amplitude: " + vpp43.read(myinst, 100)
vpp43.write(myinst, ":MEASure:EYE:RISetime"+chr(10))
vpp43.write(myinst, ":MEASure:EYE:RISetime?"+chr(10))
print "Rise Time: " + vpp43.read(myinst, 100)
vpp43.write(myinst, ":MEASure:EYE:FALLtime"+chr(10))
vpp43.write(myinst, ":MEASure:EYE:FALLtime?"+chr(10))
print "Fall Time: " + vpp43.read(myinst, 100)

## Turn off Acquisition Limit
vpp43.write(myinst, ":LTESt:ACQuire:STATe OFF"+chr(10))

## Query for Errors
while True:
    vpp43.write(myinst, ":SYSTem:ERRor?"+chr(10))
    Result = vpp43.read(myinst, 100)
    ErrorList = Result.split(',')
    Error = ErrorList[0]
    print "Error #: " + ErrorList[0]
    print "Error Description: " + ErrorList[1]
    if int(Error) == 0:
        break

## Close Visa Connection
vpp43.close(myinst)
print "Complete"


        