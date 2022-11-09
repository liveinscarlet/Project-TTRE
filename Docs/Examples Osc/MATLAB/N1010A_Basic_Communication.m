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

%% Skip setup if different module
%% setup = 0 then skip
%% setup = 1 then perform
setup = 0;
if setup == 1
    %% Reset Instrument
    fprintf(s, ':SYSTem:DEFault');
    fprintf(s, '*OPC?');
    RSTcomplete=fscanf(s)

    %% Send commands to setup instrument
  
end

%% Send commands to perform measurements


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






        