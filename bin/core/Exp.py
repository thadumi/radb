# File: Exp.py
# Date: 16 gen 16
# Note: the Exp class implements a parser for relational algebra;
#       an Exp object is based on a parse-tree form;
#       it is used to convert expressions into python expressions

import re

#import utils #, Scanner
import utils, Scanner

#========== COSTANTI ===============
NULLTOKEN = -1   # token 'nullo'
NULL = '-' #'NULL' # null value (to build tuples in outer joins)

# classi di token costituiti da piu' caratteri
SPACES = 0  # spazi (non e' un token effettivo)
NUMBER = 1  # numero
IDENT  = 2  # identificatore
STRING = 3  # stringa fra apici
ATTRIB = 4  # attributo fra parentesi (condizione, lista attributi, ...)

# token identificati da un simbolo univoco:
ADD = 20
SUB = 21
MUL = 22
DIV = 23
MOD = 24

AND = 30
OR = 31
NOT = 32

EQUAL = 40
NOTEQUAL = 41
LESS    = 42
GREATER = 43
LESSEQUAL = 44
GREATEREQUAL = 45

LEFTPAR = 50
RIGHTPAR = 51
LEFTSQUARE = 52
RIGHTSQUARE = 53
LEFTATTR = 54
RIGHTATTR = 55

ASSIGN = 60
ARROW = 61

# operazioni relazionali
UNION = 70
INTERSECTION = 71
DIFFERENCE = 72
DIVISION = 73
PRODUCT = 74

SELECTION = 100
PROJECTION = 101
RENAME = 102

JOIN = 200
LJOIN = 201
RJOIN = 202
FJOIN = 203
UNION = 204

RELATION = 1000
UNARY    = 1001
BINARY   = 1002

#===================================

# binary operators
b_operators = (PRODUCT, DIFFERENCE, UNION, INTERSECTION, DIVISION, JOIN, LJOIN, RJOIN, FJOIN)

# unary operators
u_operators = (PROJECTION, SELECTION, RENAME)

# Associates operator with python method
fun_dict = {
    PRODUCT:      'product',
    DIFFERENCE:   'difference',
    UNION:        'union',
    INTERSECTION: 'intersection',
    DIVISION:     'division',
    PROJECTION:   'projection',
    SELECTION:    'selection',
    RENAME:       'rename',
    JOIN:         'join',
    LJOIN:        'outer_left',       
    RJOIN:        'outer_right',      
    FJOIN:        'outer'
    }

regole = ([
               ('SPACES', r'\s+'),
               (ADD, r'\+'),
               (AND, r'and'),
               (OR, r'or'),
               (NOT, r'not'),
               (NOTEQUAL, r'!='), #!!!
               (EQUAL, r'='),
               (LESS, r'<'),
               (GREATER, r'>'),
               (LESSEQUAL, r'<='),
               (GREATEREQUAL, r'>='),
               (ASSIGN, r':='),
               (PROJECTION, r'projection'),
               (SELECTION, r'selection'),
               (RENAME, r'rename'),
               (PRODUCT, r'product'),
               (DIVISION, r'division'),
               (DIFFERENCE, r'difference'),
               (UNION, r'union'),
               (INTERSECTION, r'intersection'),
               (JOIN, r'join'),
               (LJOIN, r'outer_left'),
               (RJOIN, r'outer_right'),
               (FJOIN, r'outer'),
               #(LEFTSQUARE, r'\['),
               #(RIGHTSQUARE, r'\]'),
               (NUMBER, '[-+]?[0-9]*\.?[0-9]+'),  # non riconsce 67. SISTEMARE
               (IDENT, r'[a-zA-Z][a-zA-Z0-9]*'),
               (STRING, r'\'[a-zA-Z0-9]+\''),
               #('oprel', r'[=<>]+'),
               (LEFTPAR, r'\('),
               (RIGHTPAR, r'\)'),
               (ATTRIB, r'\[[a-zA-Z0-9()<>=!+\-\*/\', ]*\]'), #   [espressione]
               (NULLTOKEN, r'null_token')
             ])

#k = Scanner()  # global scanner (2015)

#$ k = Scanner(regole) # global scanner
k = Scanner.Scanner(regole) # global scanner

class TokenizerException (Exception):
    pass

class ParserException (Exception):
    pass


# simbolo unicarattere che costituisce un operatore o altro simbolo
def isOperator(op):
    #return '+-*÷∸∪∩/=πσρ⨝⟕⟖⟗←()→'.find(c) > -1
    return isUnary(op) or isBinary(op)

# simbolo unicarattere che costituisce un operatore UNARIO
def isUnary(op):
    #return 'πσρ'.find(c) > -1
    return op in u_operators

# simbolo unicarattere che costituisce un operatore BINARIO
def isBinary(op):
    #return '+-*÷∸∪∩/⨝⟕⟖⟗'.find(c) > -1
    return op in b_operators

# cambia gli operatori per la valutazione Python
def changeOperators(s):
        ''' modifica gli operatori scritti in edit (ad esempio nelle condizioni)
        in modo risultino compatibili con la valutazione (metodo eval()) di Python;
        la trasformazione di != in ! serve per 'compensare' la precedente sostituzione di != in !==
        '''
        #return self.replace('=','==').replace('≤','<=').replace('≠','!=').replace('≥','>=').replace(
        #    '∧','and').replace('∨','or').replace('¬','not').replace('NULL','\''+NULL+'\'') #ok: '\'-\'')
        return s.replace('=','==').replace('!=','!').replace('NULL','\''+NULL+'\'') #ok: '\'-\'')

# converts string into the original format of edit
# (used to manage error messages)
def decodeOperators(s):
    #return self.replace('==','=').replace('<=','≤').replace('!=','≠').replace('>=','≥').replace(
    #        'and','ᐱ').replace('or','ᐯ').replace('not','¬').replace(NULL,'NULL')
    return self.replace('==','=').replace(NULL,'NULL')     #2016     

def is_valid_relation_name(name):
    '''
    Checks if a name is valid for a relation.
    Returns boolean
    '''
    if re.match(r'^[_a-zA-Z]+[_a-zA-Z0-9]*$', name) == None:
        return False
    else:
        return True

class Exp(object):
    '''
    Class whose objects are relational expressions.
    Root node identify the expression.
    Leaves are relations and internal nodes are operations.
    The kind attribute says if node is: binary operator, unary op., or a relation.
    Se il nodo e' un operatore binario, esistono gli attributi left e right.
    Se il nodo e' un operatore unario esiste l'attributo child che referenzia
    il nodo figlio e l'attributo prop contenente la stringa con le proprieta' dell'operazione.
    Questa classe e' usata per convertire un'espressione in codice Python
    '''
       
    __hash__ = None

    # crea un'espressione ad albero a partire dalla stringa settata nello scanner
    # sexp : stringa dalla quale costruire l'espressione ad albero
    #        se sexp=None l'espressione viene costruita dallo scanner precedente
    #        se tipo!=None viene costruita un'espressione vuota di tipo 'type'
    #
    def __init__(self,sexp=None,kind=None):  
     
        '''Generates the tree from the tokenized expression
        If no expression is specified then it will create an empty node'''

        if sexp != None:
            utils.debug('========== EXP in init(NODE): SEXP = ['+sexp+']')
        if kind != None:
            utils.debug('========== EXP in init(NODE): TYPE = ['+str(kind)+']')

        if kind != None:
            self.kind = kind
            self.name = 'undef'
            self.attr = None
            self.child = None
            self.left = None
            self.right = None
            utils.debug('-------> CREATA EXP SENZA SCANNER')
            return

        # parte nuova 01nov15
        if sexp != None:
            k.setString(sexp)  # carica lo scanner globale
        #---- fine parte nuova --- 
                
        #utils.debug('--------------> in init: CURTOKEN ='+str(k.curToken()))
        #print('--------------> in init: CURTOKEN ='+str(k.curToken()))
        while k.curToken().type in (IDENT,SELECTION,PROJECTION,RENAME,LEFTPAR): # simboli FIRST
            #print('    Exp:----------> in while: CURTOKEN =',k.curToken())
            tt = k.curToken().type
            if tt == IDENT:
                # caso di stringa che costituisce il nome di una relazione:
                # viene costruito un nodo RELATION e viene eliminato il token
                #utils.debug("TROVATO TOKEN IDENT:"+k.curToken().name)
                self.kind = RELATION
                self.name = k.curToken().name
                self.attr = None
                self.left = None
                self.right = None
                self.child = None 
                if not is_valid_relation_name(self.name):
                    raise ParserException("'%s' is not a valid relation name" % self.name)
                k.getToken()  # salta il token 'nome tabella':
                #print("TOKEN ALLA FINE =",k.curToken().type)

            elif tt == LEFTPAR:
                # espressione fra parentesi tonde
                #print("TROVATO APERTA TONDA APERTA")
                k.getToken()  # salta parentesi aperta
                temp = Exp() # espressione AR fra tonde
                self.kind = temp.kind
                self.attr = temp.attr
                self.name = temp.name
                self.left = temp.left
                self.right = temp.right
                self.child = temp.child
                if k.curToken().type != RIGHTPAR:
                    raise ParserException("')' symbol expected")
                k.getToken() # salta parentesi chiusa
                #print('------ nodo FRA PARENTESI TONDE =',self)    
                                           
            #elif k.isUnary(k.curToken().name):
            elif isUnary(k.curToken().type):    
                #print("-------->TROVATO OPERATORE UNARIO",k.curToken().name)
                self.kind = UNARY
                self.name = k.curToken().name
                self.code = k.curToken().type  # codice intero operazione (2016)
                k.getToken() # salta l'operatore
                #print("TOKEN CORRENTE =",k.curToken())
                # controllo se c'e' l'attributo
                if k.curToken().type == ATTRIB:
                    attr = k.curToken().name
                    attr = attr[1:len(attr)-1] # eliminazione parentesi [..]
                    self.attr = attr
                    #print("Exp(isUnary): trovato attributo =",self.attr)
                    k.getToken() # salta l'attributo
                else:    
                    #print("NON TROVATO ATTRIBUTO")
                    raise ParserException("ERROR: attribute expected",tt)
                self.child = Exp()
                self.left = None
                self.right = None
                                
            else:    
                raise ParserException("ERROR: Unable to parse tokens",tt)

            if k.curToken().type == NULLTOKEN:
                break

            # controllo se a seguire la prima espressione c'e'
            # un operatore binario infisso che regge un'altra espressione
            #print("  ----TROVATO OPERATORE BINARIO: ",k.curToken().name)
            if isBinary(k.curToken().type):
                #print("  TROVATO OPERATORE BINARIO: ",k.curToken().name)

                # ridefinizione del nodo self
                #?self.kind = UNARY 
                #?self.name = k.curToken().name
                self.code = k.curToken().type  # codice intero operazione (2016)
                
                tn = k.curToken().name
                #print('----- TN=',tn)
                k.getToken() # salta l'op binario
                
                # il nodo corrente che contiene la prima parte dell'espressione
                # viene ricopiato in un nuovo nodo
                #lnode = node(self.kind)  #pld
                lnode = Exp(None,self.kind)
                lnode.name = self.name
                lnode.attr = self.attr 
                lnode.child = self.child
                lnode.left = self.left
                lnode.right = self.right
                #lnode.kind = UNARY #2016
                #lnode.code = self.code #2016
                
                # ridefinizione del nodo self
                #SOPRA! self.kind = BINARY 
                self.name = tn  #era 2015
                #self.code = k.curToken().type  # codice intero operazione (2016)
                self.kind = BINARY 
                
                if k.curToken().type == ATTRIB:
                    #self.attr = k.curToken().name
                    attr = k.curToken().name
                    attr = attr[1:len(attr)-1] # eliminazione parentesi [..]
                    self.attr = attr
                    #print("TROVATO ATTRIBUTO in join = ",self.attr)
                    k.getToken() # salta l'attributo
                else:    
                    #print("NON TROVATO ATTRIBUTO in join")
                    self.attr = None # serve?
                self.left = lnode  
                #self.right = node() # espressione dopo l'op. binario  OLD
                self.right = Exp() # espressione dopo l'op. binario   NEW
                #print('------ nodo IO =',self.name)
                #print('------ nodo SX =',self.left)
                #print('------ nodo DX =',self.right)
                #print('------ nodo SELF =',self)
    
        #print('------ nodo SELF PRIMA DI RETURN =',self)    
        return
    
        #pass  #era; serve?
  
    def toCode(self):
        '''This method converts the tree into a python code object'''
        code = self.toPython()
        return compile(code, '<relational_expression>', 'eval')

    def toPython(self):
        '''
        converts the RA expression into a Python code string;
        this will be converted using methods of Relation class
        '''
        
        #print("----------> ENTRATO IN toPython -------- name = ["+self.name+"]")
        #print("        --> ENTRATO IN toPython -------- kind = ", self.kind)
        if self.kind == BINARY:
            #- opcode = opdict[self.name][0] # codice intero dell'operazione (cfr. Scanner)
            opcode = self.code #2016
            func = fun_dict[opcode]       # nome della funzione Python da associare all'operatore 
            if self.attr != None:    
                attr = self.attr               # condizione del theta-join
                #print('Exp:-------> ATTR =',attr)
                spython = '%s.%s(%s,\"%s\")' % (self.left.toPython(), func, self.right.toPython(), attr)
                #print("-----------------> STRINGA PYTHON2A ="+spython)
                return spython
            else:
                # caso di op binario non theta-join:
                #print("        ---- caso di op binario non theta-join:")
                #print("             FUNC = "+func)
                leftexp  = self.left.toPython()
                rightexp = self.right.toPython()
                spython = '%s.%s(%s)' % (leftexp,func,rightexp)
                #print("-----------------> STRINGA PYTHON2B ="+spython) 
                #print("          LEFT  = "+leftexp)
                #print("          RIGHT = "+rightexp)
                #print("             spython =",spython)
                return spython
        elif self.kind == UNARY:
            attr = self.attr
            opcode = self.code #2016
            func = fun_dict[opcode]       # name of Python function to associate to operator 
            #print("      IN toPython-UNARY: FUNC =",func,"  OPCODE=",opcode,"  ATTR=",attr)
            if opcode == PROJECTION:      # projection
                #print("           ------------ PROJECTION")
                #attr = '\"%s\"' % attr.replace(' ', '').replace(',', '\",\"')
                attr = '[\"%s\"]' % attr.replace(' ', '').replace(',', '\",\"') #2016
            elif opcode == RENAME:        # rename
                #print("           ------------ RENAME: attr =",attr)
                #charrow = '→'             # carattere freccia di ridenominazione
                charrow = '->'             # carattere freccia di ridenominazione 
                attr = '{\"%s\"}' % attr.replace(',','\",\"').replace(charrow,'\":\"').replace(' ','')
                #print('ATTR modificati in RENAME =',attr)
            else:                         # selection
                #print("           ------------ SELECTION")
                attr = '\"%s\"' % attr
            spython = '%s.%s(%s)' % (self.child.toPython(), func, attr)
            utils.debug("-----------------> STRINGA PYTHON ="+spython)
            #print("-----------------> STRINGA PYTHON1 ="+spython) 
            return spython
        else: # nome di relazione
            utils.debug('   ---- NOME DI RELAZIONE in toPython: name = '+self.name)
            return self.name
        #pass  #???

    def printtree(self, level=0):
        '''returns a representation of the tree using indentation'''
        r = ''
        for i in range(level):
            r += '  '
        r += self.name
        if self.name in b_operators:
            r += self.left.printtree(level + 1)
            r += self.right.printtree(level + 1)
        elif self.name in u_operators:
            r += '\t%s\n' % self.attr
            r += self.child.printtree(level + 1)
        return '\n' + r
    
    def __eq__(self, other):
        if not (isinstance(other, node) and self.name == other.name and self.kind == other.kind):
            return False

        if self.kind == UNARY:
            if other.prop != self.attr:
                return False
            return self.child == other.child
        if self.kind == BINARY:
            return self.left == other.left and self.right == other.right
        return True

    def __str__(self):
        if (self.kind == RELATION):
            return self.name
        elif (self.kind == UNARY):
            return self.name + " " + self.attr + " (" + self.child.__str__() + ")"
        elif (self.kind == BINARY):
            if self.left.kind == RELATION:
                le = self.left.__str__()
            else:
                le = "(" + self.left.__str__() + ")"
            if self.right.kind == RELATION:
                re = self.right.__str__()
            else:
                re = "(" + self.right.__str__() + ")"

            return (le + self.name + re)

# static methods:

def parse(expr):
    '''
    parsing di un'espressione dell'algebra relazione
    e sua conversione in una stringa python eseguibile dalla funzione 'eval'
    '''
    #print('------------ Exp:parse: prima di t = ... ')
    t = Exp(expr)  # espressione in formato albero
    #print('++++++++++++ Exp:parse: dopo di t = ... ')
    #print("EXP-ALBERO DA CONVERTIRE IN PYTHON =",t)
    #utils.debug("EXP-ALBERO DA CONVERTIRE IN PYTHON ="+str(t))
    return t.toPython()

#-----------------------------------------

if __name__ == "__main__":
    #import rtypes
    #from Scanner import *
    #import parser
       
    #print("FUNDICT =",fun_dict[SUBTRACTION])
    
    #s = ' T ← R ⨝ S'
    #s = ' R ⨝ S ⨝ T'
    s = ' R join S join T'
    print("stringa =",s)
    exp = Exp(s)
    print("espressione AR =",exp)
    #print("EXP-ALBERO DA CONVERTIRE IN PYTHON =",exp)
    #utils.debug("EXP-ALBERO DA CONVERTIRE IN PYTHON ="+str(exp))
    #epy = parse(s)
    epy = exp.toPython()
    print("espressione Python =",epy)
    #pass

