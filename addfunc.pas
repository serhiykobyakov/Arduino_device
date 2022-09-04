unit addfunc;

{$mode delphi}

interface

uses
  Classes, SysUtils, Dialogs, Forms,
  synaser,
  DateUtils;

  function GetArduinoDeviceIDstring(ComPort: string): string;
  function Str2Float(val: string): Extended;
  procedure sleepFor(msec: longint);



implementation


function GetArduinoDeviceIDstring(ComPort: string): string;
// get the ID string of Arduino device if it is connected to port 'ComPort'
// return empty string otherwise
var
  ser: TBlockSerial;
  str: string;
begin
  str := '';
  ser := TBlockSerial.Create;

    try
      ser.Connect(ComPort);
      ser.config(115200, 8, 'N', SB1, False, False);
      SleepFor(300);
      ser.SendByte(ord('?'));
      if ser.canread(5000) then str := Trim(ser.Recvstring(100));
      if (CompareStr(str, 'Ready!') = 0) or (Length(str) = 0) then
// boards with non-native USB port (Uno etc)
// MUST say "Ready!" at the end of setup
// because of their initialization lag
        begin
          ser.Purge;
          SleepFor(300);
          ser.SendByte(ord('?'));
          if ser.canread(2000) then str := Trim(ser.Recvstring(500));
        end;
    finally
      ser.Free;
    end;

  Result := str;
end;


function Str2Float(val: string): Extended;
begin
  try
    Result := StrToFloat(StringReplace(StringReplace(val, '.', DefaultFormatSettings.DecimalSeparator, [rfReplaceAll]), ',', DefaultFormatSettings.DecimalSeparator, [rfReplaceAll]));
  except
    On E: Exception do
      Showmessage('Exception when converting ' + val + ' to float');
  end;
end;

procedure SleepFor(msec: longint);
// non-blocking sleep function
// allow the PC to do something while the application sleeps
var
  tstartwait, tstopwait: TDateTime;
begin
  tstartwait := Now;
  repeat
    Application.ProcessMessages;
    tstopwait := Now;
  until MillisecondsBetween(tstopwait, tstartwait) > msec;
end;

end.

