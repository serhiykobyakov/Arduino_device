unit ArduinoDevice;

{ Copyright: (c) Serhiy Kobyakov

Version: 06.09.2022 }


interface

uses
  Classes, Dialogs, SysUtils, DateUtils,
  FileUtil,
  Controls,
  addfunc,
  synaser;


type

  { _ArduinoDevice }  // general Arduino device class

  _ArduinoDevice = Object

    private
      ser: TBlockSerial;
      function GetComPort: string;
      function GetComPortSpeed: integer;
      function GetDeviceID: string;
      function GetInitTimeout: integer;
      function GetLongReadTimeout: integer;
      function GetReadTimeout: integer;

    protected
      theDeviceID: string;
      theComPort: string;
      theComPortSpeed: integer;
      theInitTimeout: integer;
      theLongReadTimeout: integer;
      theReadTimeout: integer;

      // send string and get string
      function SendAndGetAnswer(str: string): string;

      // send single character and get string
      // faster communication when you need to send only a single byte
      function SendCharAndGetAnswer(ch: char): string;

    public
      constructor Init(ComPort: string);
      destructor Done;

      property DeviceID: string Read GetDeviceID;
      property ComPort: string Read GetComPort;
      property ComPortSpeed: integer Read GetComPortSpeed;
      property InitTimeout: integer Read GetInitTimeout;
      property LongReadTimeout: integer Read GetLongReadTimeout;
      property ReadTimeout: integer Read GetReadTimeout;
  end;



implementation


{ _ArduinoDevice }

function _ArduinoDevice.GetComPort: string;
begin
  Result := theComPort;
end;

function _ArduinoDevice.GetComPortSpeed: integer;
begin
  Result := theComPortSpeed;
end;

function _ArduinoDevice.GetDeviceID: string;
begin
  Result := theDeviceID;
end;

function _ArduinoDevice.GetInitTimeout: integer;
begin
  Result := theInitTimeout;
end;

function _ArduinoDevice.GetLongReadTimeout: integer;
begin
  Result := theLongReadTimeout;
end;

function _ArduinoDevice.GetReadTimeout: integer;
begin
  Result := theReadTimeout;
end;

function _ArduinoDevice.SendAndGetAnswer(str: string): string;
begin
  ser.SendString(str);
//  ser.Flush;
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
//  ser.Flush;
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
begin
  theComPort := ComPort; // save the com port address to object variables

  ser := TBlockSerial.Create;
  try
    ser.Connect(ComPort);
    ser.config(theComPortSpeed, 8, 'N', SB1, False, False);
    sleepFor(theInitTimeout);
    ser.SendString('?');
    if ser.canread(500) then ser.Recvstring(100); // read first answer
  finally
    ser.Flush;
  end;

end;


destructor _ArduinoDevice.Done;
begin
  ser.Free;
end;



end.
