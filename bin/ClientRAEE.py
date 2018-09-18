# File: ClientRAEE.py - Relational Algebra Expressions Evaluator
# Date: 13 giu 16
# Note: main del programma RAEE:
#       attiva l'interfaccia grafica
#       ed attiva l'esecuzione delle funzioni del core
#       modificato il 27dic15 per riusare PyQt4
#       (PyQt5 dava errore in fase di esecuzione)

import sys, os
import sip  # needed to convert into exe (in Windows) #RIM[13giu16]!!!!!

#from PyQt4 import QtGui #, QtCore
import PyQt4 #import QtGui #, QtCore

#from PyQt5 import QtGui , QtWidgets #, QtCore
from gui import maingui, guihandler 

version = "RAEE - v. 0.50 - 8 gen 16" 
guihandler.version = version

app = PyQt4.QtGui.QApplication(sys.argv)  # per PyQt4
#app = QtWidgets.QApplication(sys.argv)  # per PyQt5
app.setOrganizationName('None')
app.setApplicationName('RAEE')
        
ui = maingui.Ui_MainWindow()
Form = guihandler.relForm(ui)
Form.setFont(PyQt4.QtGui.QFont("Arial")) # serve?
ui.setupUi(Form)
Form.restore_settings()
#print("guihandler2: PATH =",os.getcwd())
fname = os.getcwd()+'\\'+'initRAEE.ra' # nome programma di init
#print("ClientRAEE: FNAME =",fname)
Form.execute(fname) # programma di configurazione
#print('eseguito file RAEE.ra')
Form.show()
sys.exit(app.exec_())   
