@echo off

@REM Generate start.bat
set current_dir=%~dp0
set drive_letter=%current_dir:~0,2%

(
    echo %drive_letter%
    echo cd %current_dir%
    echo python main.py ^> last_run.txt
) > %current_dir%\start.bat

@REM Register scheduled event to launch start.bat (run every 5 minutes, whether the user is logged on or not)
(
    echo $PswSecret = Read-Host 'Enter password' -AsSecureString;
    echo $PswValue = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto^([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR^($PswSecret^)^);
    echo $Trigger = New-ScheduledTaskTrigger -Once -At ^(Get-Date^) -RepetitionInterval ^(New-TimeSpan -Minutes 5^);
    echo $Action = New-ScheduledTaskAction -Execute '%current_dir%start.bat'
    echo Register-ScheduledTask aws-ddns -Action $Action -Trigger $Trigger -User ^"$env:USERDOMAIN\$env:USERNAME^" -Password $PswValue
) > register-event.ps1
powershell.exe -ExecutionPolicy ByPass -File register-event.ps1

del register-event.ps1

@REM Wait for user confirm
echo Don't forget to create config.json
pause
