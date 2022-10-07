unit addfunc;

{ Copyright: (c) Serhiy Kobyakov

Version: 06.09.2022 }


interface

uses
  Classes, SysUtils, Dialogs, Forms,
  FileUtil,
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
  FindFiles: TStringList;
begin
  str := '';

{$IFDEF Linux}
// remove lock-file
// I assume that the application we use have to be the one which use
// the serial comunication on this PC
// remove it if it is not the case but be ready to communication failiure
// when the lock-file exists
  FindFiles := TStringList.Create;
  try
    FindAllFiles(FindFiles, '/var/lock/', '*' + ExtractFileName(ComPort), true);
    if (FindFiles.Count = 1) then DeleteFile(FindFiles.Strings[0]);
  finally
    FindFiles.Clear;
    FindAllFiles(FindFiles, '/var/lock/', '*' + ExtractFileName(ComPort), true);
    If FindFiles.Count > 0 then
      showmessage('Can''t remove lock-file:' + LineEnding + FindFiles.Strings[0]);
    FindFiles.Free;
  end;
{$ENDIF}

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

