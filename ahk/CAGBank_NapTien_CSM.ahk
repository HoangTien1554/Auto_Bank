SetTitleMatchMode, 2  ;

TaiKhoan := "VINHCAG"
SoTien := 20000

SetTitleMatchMode, 2  ;
WinActivate, Cyber Station Manager
WinWaitActive, Cyber Station Manager

Sleep, 100 ;
Click, 8400, 75 ;
Loop, 3 ;
{
    Send, {Esc}
    Sleep, 100  ; Đợi 100ms giữa mỗi lần bấm
}
BlockInput, On  ;
CoordMode, Mouse, Screen  ;
Sleep, 100 ;
Click, 140, 100 ;
Sleep, 100 ;
Click, 440, 176 ;
Sleep, 50 ;
Send, ^a
Sleep, 50 ;
Send, %TaiKhoan% ;
Sleep, 100 ;
SendInput, {Enter} ;
Sleep, 100 ;
Click, 100, 235 ;
Sleep, 100 ;
Click, 100, 235 ;
Sleep, 100 ;
Click, 1295, 540 ;
Sleep, 100 ;
Send, %SoTien% ;
Sleep, 100 ;
Click, 920, 630 ;
Sleep, 100 ;
Click, 960, 560 ;
Sleep, 100 ;
Click, 910, 730 ;
Sleep, 100 ;
DllCall("ShowCursor", "Int", 1)  ;
BlockInput, Off  ;
ExitApp
