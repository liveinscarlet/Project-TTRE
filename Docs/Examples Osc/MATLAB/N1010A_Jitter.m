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
s.Timeout=20;

%% query inst ID
fprintf(s, '*CLS');
fprintf(s, '*IDN?');
id=fscanf(s)

%% Skip setup if not using 86108A module
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
    fprintf(s, ':DIFF1:DMODe ON');
    fprintf(s, ':CHAN1A:BANDwidth BANDwidth3');
    fprintf(s, ':CHAN2A:BANDwidth BANDwidth3');

    
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

%% Enter Jitter Mode
fprintf(s, ':SYSTem:MODE JITTer');
fprintf(s, '*OPC?');
complete=fscanf(s)

%% Setup Acquisition Limit
fprintf(s, ':ACQuire:CDISplay');
fprintf(s, ':LTESt:ACQuire:CTYPe:PATTerns 1');
fprintf(s, ':LTESt:ACQuire:STATe ON');
fprintf(s, ':ACQuire:RUN');
fprintf(s, '*OPC?');
ACQcomplete=fscanf(s)

%% Query Measurement Results
fprintf(s, ':MEASure:JITTer:TJ?');
TotalJitter=fscanf(s)
fprintf(s, ':MEASure:JITTer:DJ?');
DeterministicJitter=fscanf(s)
fprintf(s, ':MEASure:JITTer:RJ?');
RancomJitter=fscanf(s)

%% Query DDPWS, J2, J9, and UJ Jitter Results
fprintf(s, ':MEASure:JITTer:DDPWs');
fprintf(s, ':MEASure:JITTer:DDPWs?');
DDPWS=fscanf(s)
fprintf(s, ':MEASure:JITTer:JN:SJN J9');
fprintf(s, ':MEASure:JITTer:JN');
fprintf(s, ':MEASure:JITTer:JN?');
J9=fscanf(s)
fprintf(s, ':MEASure:JITTer:JN:SJN J2');
fprintf(s, ':MEASure:JITTer:JN');
fprintf(s, ':MEASure:JITTer:JN?');
J2=fscanf(s)
fprintf(s, ':MEASure:JITTer:UJ');
fprintf(s, ':MEASure:JITTer:UJ?');
UJ=fscanf(s)

%% Turn Off Acquisition Limit
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






        