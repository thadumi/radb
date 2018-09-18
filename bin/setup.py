# File: setup.py 
# Date: 20 gen 16
# Note: setup che serve per generare un programma .exe
#       da file compilati in Python

# come segue viene creato un exe che attiva una finestra DOS
'''
from distutils.core import setup
import py2exe
setup(console=['RAEE.py'])
'''

# come segue viene creato un exe che NON attiva una finestra DOS
from distutils.core import setup
import py2exe, sys, os
#setup(windows = [{'script':'RAEE.py'}] )
#setup(windows = [{'script':'ServerRAEE.py'}] )

# come segue vengono creati exe che attivano una finestra DOS
#setup(console = ['RAEE.py'] )
#setup(console = ['ServerRAEE.py'] )

#setup(windows = [{'script':'ClientRAEE.py'}] )
#setup(console = ['ServerRAEE.py'] )

setup(console = ['ClientRAEE.py'] )  #ok (se da solo)
#setup(console = ['ServerRAEE.py'] )  #ok (se da solo)

# setup(console = ['ClientRAEE.py','ServerRAEE.py'] )  # client+server

#setup(windows = [{'script':'ClientRAEE.py'},{'script':'ClientRAEE.py'}] )

#setup(console = ['.\gui\ClientRAEE.py'] )  #ok (se da solo)
#setup(console = ['.\core\ServerRAEE.py'] )  #ok (se da solo)



