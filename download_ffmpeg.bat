@echo off
echo ========================================
echo  Baixando FFmpeg Essentials
echo ========================================
echo.

REM Criar pasta ffmpeg se não existir
if not exist "ffmpeg" mkdir ffmpeg

echo Baixando FFmpeg essentials (versao compacta)...
echo Isso pode levar alguns minutos...
echo.

REM Baixar FFmpeg essentials (versão menor, ~30MB)
powershell -Command "& {Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'ffmpeg-essentials.zip'}"

if %errorlevel% neq 0 (
    echo ERRO: Falha ao baixar FFmpeg
    pause
    exit /b 1
)

echo.
echo Extraindo arquivos...
powershell -Command "& {Expand-Archive -Path 'ffmpeg-essentials.zip' -DestinationPath 'ffmpeg_temp' -Force}"

if %errorlevel% neq 0 (
    echo ERRO: Falha ao extrair FFmpeg
    del ffmpeg-essentials.zip
    pause
    exit /b 1
)

echo.
echo Organizando arquivos...

REM Encontrar a pasta bin dentro do extraído
for /d %%i in (ffmpeg_temp\ffmpeg-*) do (
    xcopy "%%i\bin\*" "ffmpeg\" /Y /I
)

echo.
echo Limpando arquivos temporarios...
del ffmpeg-essentials.zip
rmdir /s /q ffmpeg_temp

echo.
echo ========================================
echo  FFmpeg baixado com sucesso!
echo  Arquivos em: .\ffmpeg\
echo ========================================
echo.
pause
