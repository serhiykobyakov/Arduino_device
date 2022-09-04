unit Unit1;

{$mode objfpc}{$H+}

interface

uses
  ...
  Forms, ArduinoDevice, MyNewDevice,
  ...;

type

  { TForm1 }

  TForm1 = class(TForm)
    ...
    procedure FormClose(Sender: TObject; var CloseAction: TCloseAction);
    procedure FormCreate(Sender: TObject);
    procedure SearchComDevices;
    ...
  private

  public

  end;


var
  ...
  itemslist, devlist, comportlist: TStringList;
  ...;

implementation


{ TForm1 }

procedure TForm1.SearchComDevices;
var
  MyForm: TForm;
  MyLabel: TLabel;
  i: integer;
begin
// -- make the splash screen ---
  MyForm := TForm.Create(nil);
  with MyForm do begin
      SetBounds(0, 0, 300, 450); Position:=poDesktopCenter;
      BorderStyle := bsNone; Color := $00EEEEEE; end;

  MyLabel := TLabel.Create(MyForm);
  with MyLabel do begin
      Autosize := True; Align := alNone;
     Alignment := taCenter; Parent := MyForm; Visible := True;
      AnchorVerticalCenterTo(MyForm);  AnchorHorizontalCenterTo(MyForm); end;

  MyForm.Show; MyForm.BringToFront;

  MyLabel.Caption := LineEnding + 'Searching for COM devices:' + LineEnding + ' ' + LineEnding;
  sleepFor(500);

  comportlist := TStringList.Create;
  devlist := TStringList.Create;

{$IFDEF Linux}
// let's find the list of COM ports with devices connected
  FileUtil.FindAllFiles(comportlist, '/dev/serial/by-path', '*', False);
  for i := 0 to comportlist.Count - 1 do comportlist.Strings[i] := ReplaceStr(fpReadLink(comportlist.Strings[i]), '../..', '/dev');
{$ENDIF}
{$IFDEF Windows}
  comportlist.CommaText:=GetSerialPortNames;
{$ENDIF}

  for i := 0 to comportlist.Count - 1 do
  begin
    devlist.Add(GetArduinoDeviceIDstring(comportlist.Strings[i]));
    MyLabel.Caption := MyLabel.Caption + LineEnding + comportlist.Strings[i] + ': ' + devlist.Strings[i];
    Application.ProcessMessages;
  end;
  MyLabel.Caption := MyLabel.Caption + LineEnding + ' ' + LineEnding + 'Done!';
  sleepFor(500);

// don't forget to free comportlist and devlist in Form1.OnClose!
  MyForm.Close;
  FreeAndNil(MyForm);
  sleepFor(50);
end;


procedure TForm1.FormClose(Sender: TObject; var CloseAction: TCloseAction);
begin

// Stop devices
  MyNewDevice.Done;

// Free dev lists
  comportlist.Free;
  devlist.Free;
end;


procedure TForm1.FormCreate(Sender: TObject);
var
//  AppIni: TIniFile;
  idstr: string;
begin

  Form1.SearchComDevices;

// Init device
  idstr := 'MyNewDevice';
  if devlist.IndexOf(idstr) = -1 then
    begin
      showmessage('Please connect ' + idstr + '!');
      halt(0);
    end
  else
      MyNewDevice.Init(comportlist.Strings[devlist.IndexOf(idstr)]);

// Init second device


end;


end.

