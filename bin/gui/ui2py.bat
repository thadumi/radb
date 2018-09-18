@echo off
rem file: ui2py.bat
rem date: 27 dic 15
rem note: generazione del file .py per Python 
rem       a partire dal file .ui generato con QtDesigner

rem set DIR=C:\bin\python3.4.1\Lib\site-packages\PyQt5

    set DIR=C:\bin\python3.4.1\Lib\site-packages\PyQt4

   %DIR%\pyuic4 -o maingui.py maingui.ui

rem %DIR%\pyuic5 -o maingui.py maingui.ui

pause