from visa import *
from pyvisa import vpp43

## Connecton to N1010A software is accomplished via LAN and the following connections are supported
## SOCKET LAN Visa Address: 'TCPIP0::156.140.158.223::5025::SOCKET'
## HiSLIP LAN Visa Address: '156.140.158.223::hislip0::INSTR'
## The N1010A software does not support the following connections
## GPIB Visa Address'GPIB0::7::INSTR'
## VXI-11 LAN Visa Address: 'TCPIP0::156.140.158.223::inst0::INSTR'

##"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
## Copyright � 2011 Agilent Technologies Inc. All rights reserved.
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
print (vpp43.read(myinst, 100))

## Skip setup if using different modules
## setup=0 skip
## setup=1 perform
setup=0
if setup:

    ## Reset Instrument
    ##:SYSTem:DEFault
    vpp43.write(myinst, ":SYSTem:DEFault"+chr(10))
    vpp43.write(myinst, "*OPC?"+chr(10))
    print ("Default Setup Complete: " + vpp43.read(myinst, 100))

    ## Send Commands to Setup Instrument

## Send Commmands to perform measurement    

## Query for Errors
while True:
    vpp43.write(myinst, ":SYSTem:ERRor?"+chr(10))
    Result = vpp43.read(myinst, 100)
    ErrorList = Result.split(',')
    Error = ErrorList[0]
    print ("Error #: " + ErrorList[0])
    print ("Error Description: " + ErrorList[1])
    if int(Error) == 0:
        break

## Close Visa Connection
vpp43.close(myinst)
print ("Complete")
