%% Requires Matlab Instrument Control Toolbox

%% N1010A Eye/Mask Example:
%% 83496A/B module left slot 1
%% 861xxA/B/C/D optical sampling module right slot 2

%% Connecton to N1010A software is accomplished via LAN using a SOCKET Connection

%%"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
%% Copyright © 2011 Agilent Technologies Inc. All rights reserved.
%%
%% You have a royalty-free right to use, modify, reproduce and distribute this
%% example files (and/or any modified version) in any way you find useful, provided
%% that you agree that Agilent has no warranty, obligations or liability for any
%% Sample Application Files.
%%
%%"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
%%

%% Connect to instrument using a SOCKET connection
s=tcpip('156.140.158.223', 5025, 'Terminator', 10);
fopen(s);
s.Timeout=20;

%% query inst ID
fprintf(s, '*CLS');
fprintf(s, '*IDN?');
id=fscanf(s)

%% Skip setup if not using CDR and Optical Module
%% setup = 0 then skip
%% setup = 1 then perform
setup = 0;
if setup == 1
    %% Reset Instrument
    fprintf(s, ':SYSTem:DEFault');
    fprintf(s, '*OPC?');
    complete=fscanf(s)

    %% Setup clock recovery
    %% Select Data Rate for CDR
    fprintf(s, ':CRECovery1:CRATe 2.4880000E+9');
    %% Select PLL BW for CDR
    fprintf(s, ':CRECovery1:CLBandwidth 5.00E+5');

    %% Lock CDR
    fprintf(s, ':CRECovery1:RELock');
    fprintf(s, '*OPC?');
    complete=fscanf(s)

    %% Set Trigger Source
    fprintf(s, ':TRIGger:SOurce SLOT1');

    %% Setup optical measurement channel
    %% Select Wavelength for Optical Channel
    fprintf(s, ':CHAN3A:WAVelength WAVelength2');
    %% Select Filter for Optical Channel
    fprintf(s, ':CHAN3A:FSELect FILTer2');
    %% Activate Filter
    fprintf(s, ':CHAN3A:FILTer ON');
end

%% Select Eye/Mask Mode and Autoscale
fprintf(s, ':ACQ:RUN');
fprintf(s, ':SYSTem:MODE EYE');
%% Autoscale Eye Diagram
fprintf(s, ':SYSTem:AUToscale');
fprintf(s, '*OPC?');
complete=fscanf(s)

%% Define and Load Mask 
fprintf(s, ':MTESt:LOAD:FNAMe "C:\Program Files\Agilent\FlexDCA\Demo\Masks\SONET_SDH\002.48832 - STM016_OC48.mskx"');
fprintf(s, ':MTESt:LOAD');

%% Setup Acquisition Limit and acquire data
fprintf(s, ':ACQuire:CDISplay');
fprintf(s, ':LTESt:ACQuire:CTYPe:WAVeforms 200');
fprintf(s, ':LTESt:ACQuire:STATe ON');
fprintf(s, ':ACQuire:RUN');
fprintf(s, '*OPC?');
complete=fscanf(s)

%% Setup Mask Margin
fprintf(s, ':MTESt:MARGin:STATe ON');
fprintf(s, ':MTESt:MARGin:METHod AUTO');
fprintf(s, ':MTESt:MARGin:AUTO:METHod HRATio');
fprintf(s, ':MTESt:MARGin:AUTO:HRATio 5e-5');

%% Query Mask Test Result
fprintf(s, ':MEASure:MTESt:HREGion1?');
Region1MaskHits=fscanf(s)
fprintf(s, ':MEASure:MTESt:HREGion2?');
Region2MaskHits=fscanf(s)
fprintf(s, ':MEASure:MTESt:HREGion3?');
Region3MaskHits=fscanf(s)
fprintf(s, ':MEASure:MTESt:MARgin?');
MaskTestMargin=fscanf(s)

%% Query Measurement Results
%%  For the most accurate Extinction Ratio Measurements refer to AN 1550-9 for correct procedure and calibration
%%  http://cp.literature.agilent.com/litweb/pdf/5989-2602EN.pdf

fprintf(s, ':MEASure:EYE:ERATio');
fprintf(s, ':MEASure:EYE:ERATio?');
ExtinctionRatio=fscanf(s)

fprintf(s, ':MEASure:EYE:AMPLitude');
fprintf(s, ':MEASure:EYE:AMPLitude?');
EyeAmplitude=fscanf(s)

fprintf(s, ':MEASure:EYE:RISetime');
fprintf(s, ':MEASure:EYE:RISetime?');
RiseTime=fscanf(s)

fprintf(s, ':MEASure:EYE:FALLtime');
fprintf(s, ':MEASure:EYE:FALLtime?');
FallTime=fscanf(s)

%% Turn off acquisition limit
fprintf(s, ':LTESt:ACQuire:STATe OFF');


%% Query for Errors
error = 1;
while (error)
    fprintf(s, ':SYSTem:ERRor?');
    myerrstring=fscanf(s)
    mysplit = strtrim(regexp(myerrstring, ',', 'split'));
    %% check if error = 0
    if  str2double(mysplit(1))==0
        error=0;
    end
end

fclose(s);
delete(s);
clear s;






        