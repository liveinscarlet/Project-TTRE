%% Requires Matlab Instrument Control Toolbox
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
%% Set Termination character to CHR(10) (i.e. "/n")
s=tcpip('156.140.158.223', 5025, 'Terminator', 10);
fopen(s);

%% Set Timout
s.Timeout=10;

%% query inst ID
fprintf(s, '*CLS');
fprintf(s, '*IDN?');
id=fscanf(s)

%% Skip setup if not using 86108A
%% setup = 0 then skip
%% setup = 1 then perform
setup = 0;
if setup == 1
    %% Reset Instrument
    fprintf(s, ':SYSTem:DEFault');
    fprintf(s, '*OPC?');
    RSTcomplete=fscanf(s)

     %% Activate Measurement Channels
    %% Set BW to 32 GHz
    fprintf(s, ':CHAN1A:BANDwidth BANDwidth3');

    %% Lock CDDR
    %% SEt CDR Rate to 10G
    fprintf(s, ':CRECovery1:CRATe 1.03125E+10');
    
    %% Set CDR PLL BW to 500 kHz
    fprintf(s, ':CRECovery1:CLBandwidth 5.00E+5');
    
    %%Lock CDR
    fprintf(s, ':CRECovery1:RELock');
    fprintf(s, '*OPC?');
    CDRcomplete=fscanf(s)
    
    %% Turn on PTB
    fprintf(s, ':PTIMebase1:RSOurce INTernal');
    fprintf(s, ':PTIMebase1:STATe ON');
    fprintf(s, ':PTIMebase1:RTReference');
    fprintf(s, '*OPC?');
    PTBcomplete=fscanf(s)
    
end

%% Activate Pattern Lock
fprintf(s, ':TRIGger:PLOCk ON');
fprintf(s, '*OPC?');
PLOCKcomplete=fscanf(s)

%% Enter Eye Diagram Mode
fprintf(s, ':SYSTem:MODE EYE');

%% Setup Apply S2P Math Function
%% Define Math Function Apply S2P
fprintf(s, ':FUNCtion2:FOPerator CONVolve');
fprintf(s, ':SPRocess2:CONVolve:FNAMe "C:\Program Files\Agilent\FlexDCA\Demo\S-Parameter Data\Demo\TDRDemoBoard_ET55780\ET55780_10.5inch_Equalization.s2p"');
%% Define Input Channel for Math Function
fprintf(s, ':FUNCtion2:OPERand1 CHAN1A');
%% Define Color for Math Function 2
fprintf(s, ':FUNCtion2:COLor TCOLor5');
%%Turn on Math Function 2
fprintf(s, ':FUNCtion2:DISPlay ON');

%% Autoscale
fprintf(s, ':SYST:AUT');
fprintf(s, '*OPC?');
AUTcomplete=fscanf(s)

%% Setup Acquisition Limit
fprintf(s, ':ACQuire:CDISplay');
fprintf(s, ':LTESt:ACQuire:CTYPe:PATTerns 1');
fprintf(s, ':LTESt:ACQuire:STATe ON');
fprintf(s, ':ACQuire:RUN');
fprintf(s, '*OPC?');
ACQcomplete=fscanf(s)

%% Save Pattern Waveform
%% Define Source as math function
fprintf(s, ':DISK:WAVeform:SAVE:SOURce FUNCtion2');
%% Define format as CSV
fprintf(s, ':DISK:WAVeform:FFORmat TEXT');
%% Define file name 
fprintf(s, ':DISK:WAVeform:FNAMe "D:\User Files\Waveforms\patternwaveform2.csv"');
%% Save File to directory 'D:\User Files\Waveforms'
fprintf(s, ':DISK:WAVeform:SAVE');
fprintf(s, '*OPC?');
PATcomplete=fscanf(s)

%% Save Screen Image
%% Define file name
fprintf(s, ':DISK:SIMage:FNAMe "D:\User Files\Screen Images\screenimage2.jpg"');
%% Save Screen Image
fprintf(s, ':DISK:SIMage:SAVE');
fprintf(s, '*OPC?');
IMAGEcomplete=fscanf(s)

%% Turn off Acquisition Limit
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






        