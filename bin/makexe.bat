@echo off
rem File: makexe.bat
rem Date: 17 dic 15
rem Note: conversione di RAEE in un exe
rem       eseguendo dal prompt DOS il comando makexe viene creata
rem       la cartella dist che contiene tutto quello che serve per l'esecuzione
rem       per completare l'installazione basta copiarci dentro le due cartelle db e prog
rem       il file di esecuzione iniziale RAEE.ra ed il font cambria per l'installazione
rem       Serve aver installato il tools py2exe

c:\bin\python3.4.1\python setup.py py2exe 

pause