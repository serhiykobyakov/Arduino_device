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


type

  { _ArduinoDevice }  // general Arduino device class

  _ArduinoDevice = Object

    private
      ser: TBlockSerial;

    protected
      function SendAndGetAnswer(str: string): string;

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


constructor _ArduinoDevice.Init(ComPort: string);
var
  FindFiles: TStringList;
begin
  theComPort := ComPort; // save the com port address to object variables

{$IFDEF Linux}
// remove lock-file
// I assume that the main application (or some other) can cometimes leave lock file
// so it would be better to remove it before w econnect to the device
  FindFiles := TStringList.Create;
  try
    FindAllFiles(FindFiles, '/var/lock/', '*' + ExtractFileName(ComPort), true);
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
    ser.SendString('?');
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
