SetTitleMatchMode, 2  ;

TaiKhoan := "LENHATANH"
SoTien := 20000


SetTitleMatchMode, 2  ;
WinActivate, GCafe+ server

Sleep, 100 ;
Click, 760, 70 ;
Loop, 3 ;
{
    Send, {Esc}
    Sleep, 100  ;
}
BlockInput, On  ;
CoordMode, Mouse, Screen  ;
Sleep, 100 ;
Click, 131, 100 ;
Sleep, 100 ;
Click, 368, 135 ;
Sleep, 50 ;
Send, ^a
Sleep, 50 ;
Send, %TaiKhoan% ;
Sleep, 50 ;
SendInput, {Enter} ;
Sleep, 100 ;
Click, 58, 188 ;
Sleep, 100 ;
Click, 58, 188 ;
Sleep, 100 ;
Click, 1310, 510 ;
Sleep, 100 ;
Send, %SoTien% ;
Sleep, 50 ;
SendInput, {Enter} ;
Sleep, 50 ;
SendInput, {Enter} ;
Sleep, 50 ;
BlockInput, Off  ;
ExitApp