@echo off
title SHADOW BLOCK • Panel Web Profesional - rafamodzyt
cd /d "%~dp0web_panel"
echo ========================================================
echo    INICIANDO PANEL WEB PROFESIONAL SHADOW BLOCK
echo         Desarrollado y Creado por rafamodzyt
echo ========================================================
start "" "http://localhost:5000"
python server.py
pause
