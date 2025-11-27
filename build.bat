@echo off
echo Criando executavel do YTD Downloader...
python -m PyInstaller --noconsole --onefile --icon="fiveicon.png" --add-data="Group 3.png;." --add-data="YTD.png;." --add-data="fiveicon.png;." --add-data="fiveicon.ico;." --add-data="ffmpeg;ffmpeg" --add-data="C:\Users\Murucupi\AppData\Roaming\Python\Python313\site-packages\customtkinter;customtkinter" --name="YTD Downloader" youtube_downloader_gui.py
echo.
echo Processo concluido! O executavel esta na pasta 'dist'.
pause
