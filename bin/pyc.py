# File: pyc.py
# Date: 15 gen 15
# Note: compilazione in bytecode;
#       esempio d'uso:
#            python pyc.py nomefile

import py_compile
import sys

# py_compile.compile('esempio.py','esempio.pyc')   # prova

sorgente = sys.argv[1]
print('sorgente =', sorgente)
py_compile.compile(sorgente+'.py',sorgente+'.pyc')
print('compilato!')


