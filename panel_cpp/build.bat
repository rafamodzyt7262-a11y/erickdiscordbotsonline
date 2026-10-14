@echo off
echo ========================================================
echo  Compilando Panel Discord C++ DX11 Win32 (Dear ImGui)
echo ========================================================

call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" 10.0.26100.0

if %errorlevel% neq 0 (
    echo [ERROR] No se pudo cargar el entorno de compilacion de MSVC 2022 x64.
    exit /b %errorlevel%
)

cl.exe /nologo /O2 /EHsc /std:c++17 /MD ^
    /I. /Iimgui /Iimgui\backends ^
    main.cpp ^
    discord_client.cpp ^
    imgui\imgui.cpp ^
    imgui\imgui_draw.cpp ^
    imgui\imgui_tables.cpp ^
    imgui\imgui_widgets.cpp ^
    imgui\backends\imgui_impl_win32.cpp ^
    imgui\backends\imgui_impl_dx11.cpp ^
    /Fe:DiscordAdminPanel.exe ^
    /link d3d11.lib d3dcompiler.lib dxgi.lib winhttp.lib user32.lib gdi32.lib shell32.lib

if %errorlevel% equ 0 (
    echo.
    echo [EXITO] DiscordAdminPanel.exe compilado correctamente!
    echo ========================================================
) else (
    echo.
    echo [ERROR] Fallo la compilacion. Revisa los errores arriba.
    echo ========================================================
)
