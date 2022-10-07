unit NewDevice;
{
NewDevice unit
Version -- date --

(c) -- author --
}



interface

uses
  Classes, SysUtils, dialogs, StdCtrls, Controls, Forms,
  IniFiles,
  addfunc,
  ArduinoDevice;


type

  { NewDevice_device }

  NewDevice_device = Object (_ArduinoDevice)
    private

    public
      constructor Init(_ComPort: string);
      destructor Done;

// example NewDevice functions:
      procedure Open;
      procedure Close;
  end;


implementation


constructor NewDevice_device.Init(_ComPort: string);
var
  MyForm: TForm;
  MyLabel: TLabel;
  AppIni: TIniFile;
  UpperInitStr, iniFile: string;
begin
// -----------------------------------------------------------------------------
// first things first
// the device ID string with which it responds to '?'
  theDeviceID := 'NewDevice';
// -----------------------------------------------------------------------------

  iniFile := Application.Location + theDeviceID + '.ini';
  If not FileExists(iniFile) then
    begin
      showmessage(theDeviceID + ':' + LineEnding +
          'procedure ''' + {$I %CURRENTROUTINE%} + ''' failed!' + LineEnding +
          'File ' + iniFile + 'has not been found!' + LineEnding +
          'Please fix it');
      halt(0);
    end;

// make a splash screen
// which shows initialization process
  MyForm := TForm.Create(nil);
  with MyForm do begin
     Caption := theDeviceID + ' initialization...';
     SetBounds(0, 0, 450, 90); Position:=poDesktopCenter; BorderStyle := bsNone;
     MyForm.Color := $00EEEEEE; end;

  MyLabel := TLabel.Create(MyForm);
  with MyLabel do begin
     Autosize := True; Align := alNone; Alignment := taCenter; Parent := MyForm;
     Visible := True; AnchorVerticalCenterTo(MyForm);
     AnchorHorizontalCenterTo(MyForm); end;

  MyForm.Show; MyForm.BringToFront;

  UpperInitStr := 'Initializing ' + theDeviceID + ':' + LineEnding;

  MyLabel.Caption:= UpperInitStr + 'Reading ' + theDeviceID + '.ini...';
  sleepFor(50); // refresh the Label to see the change

// -----------------------------------------------------------------------------
// Read the device variables from ini file:
  AppIni := TInifile.Create(iniFile);
    //fMaxPos := AppIni.ReadInteger(theDeviceID, 'MaxPos', 32800);
  AppIni.Free;
// -----------------------------------------------------------------------------

// Use basic device initialization
  MyLabel.Caption:= UpperInitStr + 'Connecting to ' + _ComPort + '...';
  sleepFor(200); // refresh the Label to see the change
  Inherited Init(_ComPort);

// Now, when communication with the device has been established
// we can send him commands
// Here we send those commands which are necessary before
// we start to work with the device

// Set the shutter into the start position as a last step of initialization
//  MyLabel.Caption:= UpperInitStr + 'Going to starting position...';
//  sleepFor(50); // small delay to refresh the Label
//  SendAndGetAnswer('i');

  MyLabel.Caption:= UpperInitStr + 'Done!';
  sleepFor(500); // refresh the Label just to see "Done"
  MyForm.Close;
  FreeAndNil(MyForm);
end;

destructor NewDevice_device.Done;
begin
// Put here the commands which have to be executed before disconnecting the device
//  SendCharAndGetAnswer('o');
  Inherited Done;
end;

procedure NewDevice_device.Open;
begin
// I don't use the device answer here to improve reliability
// but SendAndGetAnswer returns '0' after 'o' if everything is OK
//    SendCharAndGetAnswer('o');
end;

procedure NewDevice_device.Close;
begin
// I don't use the device answer here to improve reliability
// but SendAndGetAnswer returns '0' after 'c' if everything is OK
//    SendCharAndGetAnswer('c');
end;


end.


