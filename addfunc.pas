unit addfunc;

{$mode delphi}

interface

uses
  Forms, SysUtils, DateUtils;

  procedure sleepFor(msec: longint);

implementation


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

