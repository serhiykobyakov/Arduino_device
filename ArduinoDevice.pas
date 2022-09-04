unit ArduinoDevice;


interface

uses
  Classes, Dialogs, SysUtils, DateUtils,
  FileUtil,
  {$IFDEF Linux}
//  baseunix,
  unix,
  {$ENDIF}
  Controls,
  addfunc,
  synaser;


function GetArduinoDeviceIDstring(ComPort: string): string;

type

  { _ArduinoDevice }  // general Arduino device class

  _ArduinoDevice = Object

    private
      ser: TBlockSerial;

    protected
      function SendAndGetAnswer(str: string): string;
      function SendCharAndGetAnswer(ch: char): string;

    public
      constructor Init(ComPort: string);
      destructor Done;

    public
      theDeviceID: string; static;
      theComPort: string; static;
      ComPortSpeed: integer; static;
      InitTimeout: integer; static;
      LongReadTimeout: integer; static;
      ReadTimeout: integer; static;
  end;



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
      if (CompareStr(str, 'Ready!') = 0) then
// boards with non-native USB port (Uno etc)
// MUST say "Ready!" at the end of setup
// because of their initialization lag
        begin
          ser.Purge;
          SleepFor(300);
          ser.SendByte(ord('?'));
          if ser.canread(4000) then str := Trim(ser.Recvstring(3500));
        end;
    finally
      ser.Free;
    end;

  Result := str;
end;



{ _ArduinoDevice }

function _ArduinoDevice.SendAndGetAnswer(str: string): string;
begin
  ser.SendString(str);
  ser.Flush;
  if ser.canread(LongReadTimeout) then
    Result := ser.Recvstring(ReadTimeout)
  else
    begin
      showmessage(theDeviceID + LineEnding +
                  'no responce to "' + str + '" command!' + LineEnding +
                  'Check connection or device power');
      Result := '';
    end;
end;

function _ArduinoDevice.SendCharAndGetAnswer(ch: char): string;
begin
  ser.SendByte(ord(ch));
  ser.Flush;
  if ser.canread(LongReadTimeout) then
    Result := ser.Recvstring(ReadTimeout)
  else
    begin
      showmessage(theDeviceID + LineEnding +
                  'no responce to "' + ch + '" command!' + LineEnding +
                  'Check connection or device power');
      Result := '';
    end;
end;


constructor _ArduinoDevice.Init(ComPort: string);
var
  FindFiles: TStringList;
begin
  theComPort := ComPort; // save the com port address to object variables

{$IFDEF Linux}
// remove lock-file
  FindFiles := TStringList.Create;
  try
    FindAllFiles(FindFiles, '/var/lock', '*' + ExtractFileName(ComPort) + '*', true);
    if (FindFiles.Count = 1) then DeleteFile(FindFiles.Strings[0]);
  finally
    FindFiles.Free;
  end;
{$ENDIF}

  ser := TBlockSerial.Create;
  try
    ser.Connect(ComPort);
    ser.config(ComPortSpeed, 8, 'N', SB1, False, False);
    sleepFor(InitTimeout);
//    ser.SendString('?');
    ser.SendByte(ord('?'));
    if ser.canread(5000) then ser.Recvstring(100); // read first answer
  finally
    ser.Flush;
  end;

end;


destructor _ArduinoDevice.Done;
begin
  ser.Free;
end;



end.
