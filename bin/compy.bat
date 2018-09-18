@echo off
rem File: COMPY.BAT
rem Date: 5 gen 16
rem Note: compilazione di tutti i moduli Python per RAEE

rem set pycpath=c:\cmd\
    set pycpath=.\

rem    call %pycpath%pyc RAEE
    call %pycpath%pyc ClientRAEE
    call %pycpath%pyc ServerRAEE
   
rem call %pycpath%pyc core\ServerRAEE
    call %pycpath%pyc core\Types
    call %pycpath%pyc core\Exp
    call %pycpath%pyc core\Relation
    call %pycpath%pyc core\Scanner
    call %pycpath%pyc core\Engine
    call %pycpath%pyc core\Server
    call %pycpath%pyc core\utils

rem call %pycpath%pyc gui\ClientRAEE
    call %pycpath%pyc gui\guihandler
    call %pycpath%pyc gui\maingui
    call %pycpath%pyc gui\utils
    call %pycpath%pyc gui\Table

pause


  