@echo off
title Discord Admin Panel DX11 - rafamodzyt
cd /d "%~dp0panel_cpp"

if not exist DiscordAdminPanel.exe (
    echo [AVISO] Compilando DiscordAdminPanel.exe por primera vez...
    call build.bat
)

echo Iniciando Discord Admin Panel (C++ DirectX 11 Win32)...
start "" DiscordAdminPanel.exe
exit
