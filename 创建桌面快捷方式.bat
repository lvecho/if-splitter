@echo off
echo 正在创建桌面快捷方式...

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = oWS.ExpandEnvironmentStrings("%USERPROFILE%\Desktop\TIF图像分割工具.lnk") >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%~dp0TIF图像分割工具.exe" >> %SCRIPT%
echo oLink.WorkingDirectory = "%~dp0" >> %SCRIPT%
echo oLink.Description = "TIF图像分割工具" >> %SCRIPT%
echo oLink.IconLocation = "%~dp0TIF图像分割工具.exe,0" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%

echo 桌面快捷方式创建完成！
pause 