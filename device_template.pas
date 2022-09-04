unit MyNewDevice; // <-- change it!

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, dialogs, StdCtrls, Controls, Forms,
//  strutils,
  addfunc,
  ArduinoDevice;


type
// change it!
  MyNew_device = Object (_ArduinoDevice)
    private

    public
      constructor Init(ComPort: string);
      destructor Done;

// put here a device's procedure
      procedure DoSomething;
      function GetSomething(SomeInfo: string);

  end;


implementation

constructor MyNew_device.Init(ComPort: string);
var
  MyForm: TForm;
  MyLabel: TLabel;
  UpperInitStr: string;
begin
// -----------------------------------------------------------------------------
// Here we have to give all the necessary device parameters!!!

// the device ID string with which it responds to '?'
  MyNew_device.theDeviceID := 'MyShiningDevice'; // <-- this is the string the device
                                                     // have to answer when we ask '?'

// COM port speed, the default is 115200 in my lab
  MyNew_device.ComPortSpeed := 115200;

// max time in ms the device may take for its internal initialization
  MyNew_device.InitTimeout := 300;

// max time in ms the device may take before answer
// this is the longest time the device need to finish a separate command
// it is good idea to measure it before assign the value
  MyNew_device.LongReadTimeout := 25000;

// max time in ms the device may take before answer
// in the case of simple and fast queries
  MyNew_device.ReadTimeout := 1000;
// -----------------------------------------------------------------------------

// make a splash screen
// which shows initialization process
  MyForm := TForm.Create(nil);
  with MyForm do begin
     SetBounds(0, 0, 450, 90); Position:=poDesktopCenter; BorderStyle := bsNone;
     MyForm.Color := $00EEEEEE; end;

  MyLabel := TLabel.Create(MyForm);
  with MyLabel do begin
     Autosize := True; Align := alNone; Alignment := taCenter; Parent := MyForm;
     Visible := True; AnchorVerticalCenterTo(MyForm);
     AnchorHorizontalCenterTo(MyForm); end;
  UpperInitStr := 'Initializing ' + theDeviceID + ':' + LineEnding;

  MyForm.Show; MyForm.BringToFront;
  MyLabel.Caption:= UpperInitStr + 'Connecting to ' + ComPort + '...';
  sleepFor(300);

// Use basic device initialization
  Inherited Init(ComPort);

// Do first thing after serial communication with the device
// have been established
  MyLabel.Caption:= UpperInitStr + 'Do first thing...';
  sleepFor(50); // small delay to refresh the Label
//  SendCharAndGetAnswer('1');

// Do second thing
  MyLabel.Caption:= UpperInitStr + 'Do second thing...';
  sleepFor(50); // small delay to refresh the Label
//  SendCharAndGetAnswer('2');






// ----------------------------------------------------

  MyLabel.Caption:= UpperInitStr + 'Done!';
  sleepFor(500); // refresh the Label just to see "Done"
  MyForm.Close;
  FreeAndNil(MyForm);
end;

destructor MyNew_device.Done;
begin
// ----------------------------------------------------
// some device-specific actions which is necessary
// before device shutdown

//  SendCharAndGetAnswer('3');



// ----------------------------------------------------
  Inherited Done;
end;

procedure MyNew_device.DoSomething;
begin
// I don't use the device answer here to improve reliability
// but SendAndGetAnswer returns '0' after 'o' if everything is OK
//    SendCharAndGetAnswer('1');
end;


function MyNew_device.GetSomething(SomeInfo: string);
begin
// I don't use the device answer here to improve reliability
// but SendAndGetAnswer returns '0' after 'c' if everything is OK
  Result := SomeDeviceFunction();
end;


end.


