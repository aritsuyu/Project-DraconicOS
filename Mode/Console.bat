@echo off
color 0a
title aOS Gaming 2.5 - Otimizado
timeout /t 2
echo "Transformando em um Console..."

REM ===== SISTEMA CORE =====
echo "Parando Explorer temporariamente..."
taskkill /f /im explorer.exe >nul 2>&1
timeout /t 2

REM ===== APLICAÇÕES DE TERCEIROS =====
echo "Fechando aplicacoes de terceiros..."
taskkill /IM wallpaper32.exe /F >nul 2>&1
taskkill /IM chatgpt.exe /F >nul 2>&1
taskkill /IM losslessscaling.exe /F >nul 2>&1
taskkill /IM quicklook.exe /F >nul 2>&1
taskkill /IM rainmeter.exe /F >nul 2>&1
taskkill /IM kpm.exe /F >nul 2>&1
taskkill /IM FluentFlyout.exe /F >nul 2>&1
taskkill /IM PowerToys.exe /F >nul 2>&1
taskkill /IM Flow.Launcher.exe /F >nul 2>&1
taskkill /IM Dropshelf.exe /F >nul 2>&1
taskkill /IM iCUE.exe /F >nul 2>&1
taskkill /IM MusicPresence.exe /F >nul 2>&1

REM ===== NAVEGADORES =====
echo "Fechando navegadores..."
taskkill /IM brave.exe /F >nul 2>&1
taskkill /IM chrome.exe /F >nul 2>&1
taskkill /IM firefox.exe /F >nul 2>&1
taskkill /IM edge.exe /F >nul 2>&1
taskkill /IM msedge.exe /F >nul 2>&1
taskkill /IM opera.exe /F >nul 2>&1
taskkill /IM claude.exe /F >nul 2>&1

REM ===== COMUNICACAO =====
echo "Fechando apps de comunicacao..."
taskkill /IM discord.exe /F >nul 2>&1
taskkill /IM slack.exe /F >nul 2>&1
taskkill /IM teams.exe /F >nul 2>&1
taskkill /IM zoom.exe /F >nul 2>&1
taskkill /IM skype.exe /F >nul 2>&1
taskkill /IM whatsapp.exe /F >nul 2>&1
taskkill /IM telegram.exe /F >nul 2>&1

REM ===== STREAMING/MIDIA =====
echo "Fechando apps de streaming..."
taskkill /IM spotify.exe /F >nul 2>&1
taskkill /IM vlc.exe /F >nul 2>&1
taskkill /IM netflix.exe /F >nul 2>&1
taskkill /IM obs64.exe /F >nul 2>&1
taskkill /IM obs32.exe /F >nul 2>&1
taskkill /IM streamlabs.exe /F >nul 2>&1

REM ===== PRODUTIVIDADE =====
echo "Fechando apps de produtividade..."
taskkill /IM notepad++.exe /F >nul 2>&1
taskkill /IM code.exe /F >nul 2>&1
taskkill /IM winword.exe /F >nul 2>&1
taskkill /IM excel.exe /F >nul 2>&1
taskkill /IM powerpoint.exe /F >nul 2>&1
taskkill /IM notion.exe /F >nul 2>&1

REM ===== SERVICOS APPLE iCLOUD =====
echo "Fechando servicos iCloud..."
taskkill /IM iClouddDrive.exe /F >nul 2>&1
taskkill /IM iCloudPhotos.exe /F >nul 2>&1
taskkill /IM ApplePhotoStreams.exe /F >nul 2>&1
taskkill /IM iCloudHome.exe /F >nul 2>&1
taskkill /IM iCloudCKKS.exe /F >nul 2>&1
taskkill /IM CrossDeviceService.exe /F >nul 2>&1
taskkill /IM CrossDeviceResume.exe /F >nul 2>&1

REM ===== COMPONENTES WINDOWS =====
echo "Otimizando componentes Windows..."
taskkill /IM Widgets.exe /F >nul 2>&1
taskkill /IM PhoneExperienceHost.exe /F >nul 2>&1
taskkill /IM vgtray.exe /F >nul 2>&1
taskkill /im dwm.exe /f >nul 2>&1
taskkill /im ApplicationFrameHost.exe /f >nul 2>&1
taskkill /im ShellExperienceHost.exe /f >nul 2>&1
taskkill /im TextInputHost.exe /f >nul 2>&1
taskkill /im SearchApp.exe /f >nul 2>&1
taskkill /IM StartMenuExperienceHost.exe /F >nul 2>&1
taskkill /IM GameBarPresenceWriter.exe /F >nul 2>&1
taskkill /IM GameBar.exe /F >nul 2>&1

REM ===== SERVICOS ADICIONAIS =====
echo "Parando servicos desnecessarios..."
taskkill /IM OneDrive.exe /F >nul 2>&1
taskkill /IM GoogleDriveFS.exe /F >nul 2>&1
taskkill /IM DropboxUpdate.exe /F >nul 2>&1
taskkill /IM AdobeUpdateService.exe /F >nul 2>&1
taskkill /IM NVDisplay.Container.exe /F >nul 2>&1
taskkill /IM RadeonSoftware.exe /F >nul 2>&1

REM ===== LIMPEZA MEMORIA =====
echo "Limpando memoria..."
timeout /t 2

REM ===== REINICIAR EXPLORER =====
echo "Reiniciando Explorer..."
start explorer.exe
timeout /t 1

REM ===== PLUGIN LOADER =====
echo "Iniciando Plugin Loader..."
start "C:\Users\aarit\Apps\PluginLoader_noconsole.exe"

REM ===== OTIMIZACOES EXTRAS =====
echo "Aplicando otimizacoes de prioridade..."
wmic process where name="explorer.exe" CALL setpriority "below normal"

echo "Sistema otimizado para gaming!"
echo "Pressione qualquer tecla para sair..."
pause >nul
exit