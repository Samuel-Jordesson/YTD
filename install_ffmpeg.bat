@echo off
echo Instalando FFmpeg...
echo.

REM Verificar se winget está disponível
winget --version >nul 2>&1
if %errorlevel% == 0 (
    echo Instalando FFmpeg via winget...
    winget install --id Gyan.FFmpeg -e
) else (
    echo.
    echo AVISO: winget não encontrado!
    echo.
    echo Por favor, instale o FFmpeg manualmente:
    echo 1. Acesse: https://www.gyan.dev/ffmpeg/builds/
    echo 2. Baixe: ffmpeg-release-essentials.zip
    echo 3. Extraia para C:\ffmpeg
    echo 4. Adicione C:\ffmpeg\bin ao PATH do sistema
    echo.
    pause
)

echo.
echo Instalação concluída!
pause
