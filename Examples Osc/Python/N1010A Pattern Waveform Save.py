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
vpp43.set_attribute(myinst, VI_ATTR_TMO_VALUE, 60000)

##set termination character to CHR(10) (i.e. "\n")
##enable terminate reads on termination character
vpp43.set_attribute(myinst, VI_ATTR_TERMCHAR, 10)
vpp43.set_attribute(myinst, VI_ATTR_TERMCHAR_EN, 1)

## Inst ID Query
vpp43.write(myinst, "*CLS"+chr(10))
vpp43.write(myinst, "*IDN?"+chr(10))
print vpp43.read(myinst, 100)

## PTB On
vpp43.write(myinst, ":PTIM:STAT ON"+chr(10))
vpp43.write(myinst, "*OPC?"+chr(10))
print "PTB Complete: " + vpp43.read(myinst, 100)

## Pattern Lock ON
vpp43.write(myinst, ":TRIG:PLOC ON"+chr(10))
vpp43.write(myinst, "*OPC?"+chr(10))
print "Pattern Lock Complete: " + vpp43.read(myinst, 100)

## Acquire Entire Pattern On and define 16 points/bit
vpp43.write(myinst, ":ACQ:EPAT ON"+chr(10))
vpp43.write(myinst, ":ACQ:SPB:AUT MAN"+chr(10))
vpp43.write(myinst, ":ACQ:SPB 32"+chr(10))
vpp43.write(myinst, "*OPC?"+chr(10))
print "Acquire Entire Pattern Complete: " + vpp43.read(myinst, 100)

## Turn on Averaging to 32x
vpp43.write(myinst, ":ACQ:SMO AVER"+chr(10))
vpp43.write(myinst, ":ACQ:ECO 32"+chr(10))

##Define Acquisition Limit
##Need to set to 32 patterns to get 32 averages set above
vpp43.write(myinst, ":LTESt:ACQ:CTYP:PATT 32"+chr(10))
vpp43.write(myinst, ":LTESt:ACQ:STAT ON"+chr(10))
vpp43.write(myinst, ":RUN"+chr(10))
vpp43.write(myinst, "*OPC?"+chr(10))

## Define waveform to save
vpp43.write(myinst, ":DISK:WAV:SAVE:SOUR CHAN1A"+chr(10))

## Save *.wfmx
vpp43.write(myinst, ":DISK:WAV:FFOR INT"+chr(10))
vpp43.write(myinst, ":DISK:WAV:FNAM \"D:\\User Files\\Waveforms\\mypattern_wfmx.wfmx\""+chr(10))
vpp43.write(myinst, ":DISK:WAV:SAVE"+chr(10))
vpp43.write(myinst, "*OPC?"+chr(10))
print "Acquire Entire Pattern Complete: " + vpp43.read(myinst, 100)

## Save *.csv
vpp43.write(myinst, ":DISK:WAV:FFOR TEXT"+chr(10))
vpp43.write(myinst, ":DISK:WAV:FNAM \"D:\\User Files\\Waveforms\\mypattern_csv.csv\""+chr(10))
vpp43.write(myinst, ":DISK:WAV:SAVE"+chr(10))
vpp43.write(myinst, "*OPC?"+chr(10))
print "Acquire Entire Pattern Complete: " + vpp43.read(myinst, 100)

## Turn Off Acq Limit
vpp43.write(myinst, ":LTESt:ACQ:STAT OFF"+chr(10))
vpp43.write(myinst, ":RUN"+chr(10))

## Query for Errors
while True:
    vpp43.write(myinst, ":SYSTem:ERRor?"+chr(10))
    Result = vpp43.read(myinst, 1000)
    ErrorList = Result.split(',')
    Error = ErrorList[0]
    print "Error #: " + ErrorList[0]
    ## print "Error Description: " + ErrorList[1]
    if int(Error) == 0:
        break

## Close Visa Connection
vpp43.close(myinst)
print "Complete"


        