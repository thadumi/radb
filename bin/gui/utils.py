# File: utils.py  
# Date: 10 gen 16
# Note: modulo di funzioni utilities 

# dizionario di conversione degli operatori: da formato editor/GUI
# a formato testuale per l'engine:
opconv = {
           '+' : '+',
           '=' : '=',
           '≠' : '!=',
           '<' : '<',
           '>' : '>',
           '≤' : '<=',
           '≥' : '=',
           '∧' : 'and',
           '∨' : 'or',
           '¬' : 'not',
           '∩' : 'inters',
           '∪' : 'union',
           '÷' : 'division',
           '∸' : 'difference',
           'π' : 'projection',
           'σ' : 'selection',
           'ρ' : 'rename',
           '⨝' : 'join',
           '⟕' : 'ljoin',
           '⟖' : 'rjoin',
           '⟗' : 'fjoin',
           #'←' :  ':=',
           '→' :  '->',
           '(' : '(',
           ')' : ')',
           '⦇' : '[',
           '⦈' : ']'
         }

debugmode = False

def setDebug(mode):
    #print('settato debugmode =',mode)
    global debugmode
    debugmode = mode
   
def debug(msg):
    global debugmode
    if debugmode:
        print('DEBUG:',msg)

# converte una stringa con caratteri speciali in stringa ASCII
# usando le definizioni del dizionario dello Scanner
# in modo da rendere s compatibile con il formato dell'engine RA
def conv(s):
    # trasformazione dell'assegnazione
    if s.find('←') >= 0:
        s = 'set ' + s.replace('←',' ')
    # trasformazione dei caratteri operatore          
    ris = ''
    for c in s:
        if c in opconv:
            #ris += opconv[c]
            if opconv[c][0].isalpha(): # carattere iniziale dell'operatore
                ris += ' '+opconv[c]+' '
            else:
                ris += opconv[c]
        else:
            ris += c
    return ris

#----------------------------------------------------------------
if __name__ == "__main__":
    s = 'T1←R⨝⦇Sigla=\'BL\'⦈S⟕REPARTO∸x'
    t = conv(s)
    print('T =',t)  
