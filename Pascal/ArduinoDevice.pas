unit ArduinoDevice;
{
Base Arduino device unit
Version: 2023.10.03

(c) Serhiy Kobyakov
}


interface

uses
  Classes, Dialogs, SysUtils, DateUtils,
  FileUtil,
  Controls,
  IniFiles,
  Forms,
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

      procedure WriteToLog(str: string);

    protected
      theDeviceID: string;
      theComPort: string;
      theComPortSpeed: integer;
      theInitTimeout: integer;
      theLongReadTimeout: integer;
      theReadTimeout: integer;

// send string and get string
      function SendStr(cmd: string): boolean;
      function ReceiveStr(): string;
      function SendAndGetAnswer(cmd: string): string;

// send single character and get string
// faster communication when you need to send a single byte only
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

procedure _ArduinoDevice.WriteToLog(str: string);
// write a log message to file
var
  fileName: string;
  f: Text;
begin
  fileName := theDeviceID + '.log';
  Assign(f, fileName);

  if not FileExists(fileName) then Rewrite(f);

  Append(f);
  WriteLn(f, DateTimeToStr(Now) + ' ' + theDeviceID + ' at ' + theComPort);
  WriteLn(f, str);
  WriteLn(f, LineEnding);
  Close(f);
end;

function _ArduinoDevice.SendStr(cmd: string): boolean;
var
  sendOK: boolean;
  attempt_counter, bytesSent: Word;
begin
  sendOK := False;
  attempt_counter := 0;

  Repeat
    attempt_counter := attempt_counter + 1;

    try
      bytesSent := 0;
      bytesSent := ser.SendBuffer(Pointer(cmd), Length(cmd));
    finally
    end;

    if (bytesSent = Length(cmd)) then sendOK := True;

    if (not sendOK) then
      begin
        WriteToLog('  problem sending ' + cmd + ' command' + LineEnding +
                   '  ' + IntToStr(bytesSent) + ' bytes sent instead of ' +
                   IntToStr(Length(cmd)) + LineEnding +
                   '  this is ' + IntToStr(attempt_counter) + ' attempt');
        sleepFor(Round(theLongReadTimeout/20));
      end;

    if attempt_counter > 5 then Break;

  Until sendOK;

  Result := sendOK;
end;

function _ArduinoDevice.ReceiveStr: string;
// base function to receive string from device
// use it in your device unit!
var
  readOK: boolean;
  attempt_counter: Word;
  theResult: string;
  startReading: TDateTime;
begin
  readOK := False;
  attempt_counter := 0;

  Repeat
    attempt_counter := attempt_counter + 1;
    startReading := Now;
    Repeat
      try
        theResult := '';
        theResult := ser.Recvstring(theLongReadTimeout)
      finally
        if length(theResult) = 0 then sleepFor(20);
      end;

      // escape the loop if we spent too much time inside the loop
      if MillisecondsBetween(Now, startReading) > theLongReadTimeout then Break;

    Until length(theResult) > 0;

    if (length(theResult) > 0) then readOK := True
    else WriteToLog('  problem reading from serial port' + LineEnding +
                    '  this is ' + IntToStr(attempt_counter) + ' attempt' + LineEnding +
                    '  the result: ' + theResult + ' len: ' + IntToStr(length(theResult)));

    // escape the function if we fail 6 times
    if attempt_counter > 5 then Break;

  Until readOK;

  Result := theResult;
end;


function _ArduinoDevice.SendAndGetAnswer(cmd: string): string;
begin
  SendStr(cmd);
  sleepFor(20); // there must be some time between sending and receiving!
  Result := ReceiveStr();
end;

function _ArduinoDevice.SendCharAndGetAnswer(ch: char): string;
begin
// send command
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
var
  iniFile: string;
  AppIni: TIniFile;
begin
  iniFile := Application.Location + theDeviceID + '.ini';
  If not FileExists(iniFile) then
    begin
      showmessage(theDeviceID + ':' + LineEnding +
          'procedure ''' + {$I %CURRENTROUTINE%} + ''' failed!' + LineEnding +
          'File ' + iniFile + 'has not been found!' + LineEnding +
          'Please fix it');
      halt(0);
    end;

// Read the device variables from ini file:
  AppIni := TInifile.Create(iniFile);
    theComPortSpeed := AppIni.ReadInteger(theDeviceID, 'ComPortSpeed', 115200);

// max time in ms the device may take for its internal initialization
    theInitTimeout := AppIni.ReadInteger(theDeviceID, 'InitTimeout', 3000);

// max time in ms the device may take before answer
// it is good idea to measure the longest run
// before assign the value
    theLongReadTimeout := AppIni.ReadInteger(theDeviceID, 'LongReadTimeout', 3000);

// max time in ms the device may take before answer
// in the case of simple and fast queries
    theReadTimeout := AppIni.ReadInteger(theDeviceID, 'ReadTimeout', 1000);
  AppIni.Free;

  theComPort := ComPort; // save the com port address to object variables

// start serial communication
  ser := TBlockSerial.Create;
  try
    ser.Connect(ComPort);
    ser.config(theComPortSpeed, 8, 'N', SB1, False, False);
    sleepFor(theInitTimeout);
    if ser.canread(500) then  // read if there something in serial port
      ser.Recvstring(100);    // for example "Ready!"
  finally
    ser.Purge;
  end;

end;


destructor _ArduinoDevice.Done;
begin
  ser.Free;
end;



end.
