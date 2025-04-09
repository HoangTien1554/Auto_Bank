SetTitleMatchMode, 2  ;

TaiKhoan := "vinh"
SoTien := 10000


SetTitleMatchMode, 2  ;
WinActivate, FNet
WinWaitActive, FNet

Sleep, 100 ;
Click, 760, 70 ;
Loop, 3 ;
{
    Send, {Esc}
    Sleep, 100  ; Đợi 100ms giữa mỗi lần bấm
}
BlockInput, On  ;
CoordMode, Mouse, Screen  ;
Sleep, 100 ;
Click, 180, 110 ;
Sleep, 100 ;
Click, 440, 190 ;
Sleep, 50 ;
Send, ^a
Sleep, 50 ;
Send, %TaiKhoan% ;
Sleep, 100 ;
SendInput, {Enter} ;
Sleep, 100 ;
Click, 100, 250 ;
Sleep, 100 ;
Click, 100, 250 ;
Sleep, 100 ;
Click, 1295, 430 ;
Sleep, 100 ;
Send, %SoTien% ;
Sleep, 100 ;
Click, 760, 620 ;
Sleep, 100 ;
Click, 925, 731 ;
Sleep, 100 ;
BlockInput, Off ;
ExitApp
