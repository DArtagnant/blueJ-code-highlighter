@echo off
setlocal

echo execution de pyinstaller...
pyinstaller --name "BlueJ-code-highlighter" --specpath ".\build" --onefile --noconsole ".\gui.py" > output_build.txt 2>&1

findstr "error: (225," output.txt > nul
if %errorlevel% equ 0 (
    echo WARNING la compilation d'une application graphique avec pyinstaller necessite de rajouter le dossier du projet en liste blanche
    echo executer de nouveau ce script apres ajout du chemin '%~dp0'
    echo ouverture de Windows Defender
    powershell -command "Start-Process 'windowsdefender://threatsettings'"
) else (
    echo compilation terminee, execution
    explorer .\dist\
    .\dist\gui.exe
)
del output_build.txt

endlocal