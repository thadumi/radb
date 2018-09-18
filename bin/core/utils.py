# File: utils.py
# Date: 4 gen 16
# Note: modulo di funzoni utilities [nuovo lc]

#from . import Scanner

#$ import Exp

#from . import Exp

debugmode = False

def setDebug(mode):
    #print('settato debugmode =',mode)
    global debugmode
    debugmode = mode
   
def debug(msg):
    global debugmode
    if debugmode:
        #print('DEBUG:',Scanner.conv(msg))
        print('DEBUG:',msg)

"""  
def xxxparse(expr):  #PROVA DEL 31dic15
    # parsing di un'espressione dell'algebra relazione
    # e sua conversione in una stringa python eseguibile dalla funzione 'eval'
    
    print('------------ in parser: prima di t=: expr =',expr)
    t = Exp.Exp(expr)  # espressione in formato albero
    print('++++++++++++ in parser: dopo di t=:  t =',t)
    #print("EXP-ALBERO DA CONVERTIRE IN PYTHON =",t)
    debug("EXP-ALBERO DA CONVERTIRE IN PYTHON ="+str(t))
    return t.toPython()
"""    
