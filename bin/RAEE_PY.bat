@echo off
rem File: RAEE_PY.bat - attiva il server e poi il client come compilati Python
rem Date: 15 gen 16
rem Note: esecuzione del programma RAEE 
rem       con start /B non apre la finestra DOS (???)
rem       il primo argomento dopo start e' il titolo della finestra
rem       start con l'opzione /MIN arriva il prog con finestra DOS iconizzata

rem start "server RAEE - ver. 4gen16" c:\bin\python3.4.1\python bin\core\Engine.pyc

rem start "server RAEE - ver. 5gen16"  c:\bin\python3.4.1\python core\ServerRAEE.pyc

   start "server RAEE - ver. 6gen16" c:\bin\python3.4.1\python ServerRAEE.pyc

rem --- per test ----
rem  c:\bin\python3.4.1\python ServerRAEE.pyc

rem echo 'sto per eseguire la GUI'
rem pause

rem start "client RAEE - ver. 4gen16" c:\bin\python3.4.1\python bin\RAEE.pyc
rem start "client RAEE - ver. 5gen16" c:\bin\python3.4.1\python gui\ClientRAEE.pyc
    start "client RAEE - ver. 5gen16" c:\bin\python3.4.1\python ClientRAEE.pyc

rem pause