@echo off

REM ===== BLOCO 1: PARAR PROCESSOS DO GERENCIADOR =====
taskkill /F /IM AcPowerNotification.exe >nul 2>&1
taskkill /F /IM Aac3572MbHal_x86.exe >nul 2>&1
taskkill /F /IM Aac3572DramHal_x86.exe >nul 2>&1
taskkill /F /IM ArmouryCrate.UserSessionHelper.exe >nul 2>&1
taskkill /F /IM ArmouryHtmlDebugServer.exe >nul 2>&1
taskkill /F /IM ArmourySocketServer.exe >nul 2>&1
taskkill /F /IM AsusCertService.exe >nul 2>&1
taskkill /F /IM extensionCardHal_x86.exe >nul 2>&1
taskkill /F /IM atkexComSvc.exe >nul 2>&1
taskkill /F /IM GameSDK.exe >nul 2>&1
taskkill /F /IM ROGLiveService.exe >nul 2>&1
taskkill /F /IM asus_framework.exe >nul 2>&1
taskkill /F /IM armouryCrate.exe >nul 2>&1
taskkill /F /IM ArmouryCrateControlInterface.exe >nul 2>&1
taskkill /F /IM AacAmbientLighting.exe >nul 2>&1
taskkill /F /IM AacKingstonDramHal_x86.exe >nul 2>&1
REM Espera 2 segundos antes de parar os serviços
timeout /t 2 >nul

REM ===== BLOCO 2: PARAR SERVIÇOS ASUS =====
net stop "ArmouryCrateService" >nul 2>&1
net stop "AsusCertService" >nul 2>&1
net stop "ASUSComSvc" >nul 2>&1
net stop "AsusFanControlService" >nul 2>&1
net stop "AsusROGLSLService" >nul 2>&1
net stop "AsusUpdateCheck" >nul 2>&1
net stop "GameSDK Service" >nul 2>&1
net stop "ROG Live Service" >nul 2>&1
net stop "LightingService" >nul 2>&1

exit
