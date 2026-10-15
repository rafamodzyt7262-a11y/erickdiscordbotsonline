@echo off
title Erick x & Admin Bot 24/7 - Multi-Bot Discord
color 0B
cd /d "%~dp0"

echo ========================================================
echo    SISTEMA DISCORD 24/7 - ERICK X EN CANAL GENERAL
echo             Desarrollado por rafamodzyt
echo ========================================================
echo.
echo Presiona Ctrl + C en cualquier momento para detener.
echo.

:loop
python run_all.py
echo.
echo [ALERTA] El proceso principal finalizo. Reiniciando automaticamente en 3 segundos...
timeout /t 3 /nobreak >nul
goto loop
