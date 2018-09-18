# File: Engine.py
# Date: 20 gen 16
# Note: motore che esegue le istruzioni dell'AR e gestisce la memoria
#       istruzioni:
#                   load tabname 
#                   set tabname expAR

from . import Exp, Relation, utils, Server 
import os

class Engine(Server.Server):
      
    def __init__(self):
        self.servername = 'Engine ver. 20 gen 16'
        self.relations = {}  # dizionario delle relazioni in memoria
        self.dbpath = '' 
        self.dbname = '' 
        #Server.__init__(self)  #ok con: from Server import *
        Server.Server.__init__(self)  
        #self.loadCatalog() # crea e carica il catalogo (basidati e loro tabelle)
        
    def dump(self):
        print('LISTA RELAZIONI DELL\'ENGINE:')
        for r in self.relations:
            print('-->',r)

    def loadCatalog(self):
        name = 'CATALOG'                                    # catalog relation name
        rel = Relation.Relation(name)                       # empty relation
        rel.header = Relation.Header(('Database','Table'))  # catalog schema
        rel.content = set()
        #print('Engine:------> in loadCatalog')      
        try:
            for c in os.listdir(self.dbpath): # nomi delle cartelle delle basidati
                #print('Engine: DB =',c)
                dbname = self.dbpath  #nome della cartella contenente i file .csv
                #print('Engine:DBNAME =',dbname)
                for f in os.listdir(dbname+'\\'+c): # nomi dei file delle tabelle .csv
                    #print('    F =',f)
                    tn = f[:-4] # per eliminare estensione '.csv'
                    utils.debug('NOME FILE TABELLA ='+tn)
                    rel.content.add((c,tn))
            self.relations[name] = rel
            #self.relations[name].relname = name #... migliorare FATTO SOPRA
        except Exception as e:
            print('ERRORE in Engine.loadCatalog:',str(e))
                               
    def loadRelation(self,relname):
        path = self.dbpath+'/'+self.dbname+'/'+relname+'.csv'
        #print('In Engine: LOADRELATION path=',path,'  name=',relname)
        result = Relation.Relation()   # empty relation
        ris = result.load(relname,path)
        if ris[0]<0:
            return -1
        self.relations[relname] = result
        self.relations[relname].relname = relname #... migliorare
        return 0
                
    # override di ServerMulti.execute
    # elabora la query e ritorna il risultato
    def execute(self,query):
        #print('CHIAMATA Engine.execute!!!!!!!!!!!!!!')
        s = self.execInstruction(query)
        #print('RISPOSTA dell\'Engine:',s)
        print('[<]',s)
        if s[len(s)-1] != '\n' : s += '\n'
        return s+'<END>\n' # teminatore (per Java)
       
    # ritorna il risultato (senza la <END> finale)           
    def execInstruction(self,exp):
        #print('istruzione da eseguire nell\'engine:',exp)
        a = exp.split() # splits exp into words
        
        #print('    #### exp =',exp)
        #for i in range(len(a)):
        #    print('    ####',a[i])
            
        if len(a) == 0:
            return '-1: no instruction'
       
        # impostazione del percorso della cartella dei database 
        #- elif a[0] == 'dbpath': 
        #-    self.dbpath = a[1]
        #-    return '0:'+'dbpath \"'+a[1]+'\" setted'
             
        elif a[0] == 'load': # formato: load relname [path]
            path = a[1]
            if len(a) < 2:
                return '-1:No relation to load.'
            relname = a[1]
            #print('In Engine: LOAD path=',path,'  name=',relname)
            if relname == 'CATALOG':
                self.loadCatalog() # crea e carica il catalogo (basidati e loro tabelle)
            elif relname == '*':
                # carica tutte le relazioni del db corrente
                ext  = '.csv'
                path = self.dbpath+'/'+self.dbname
                #print('PATH ='+self.dbpath+'/'+self.dbname)
                if not os.path.exists(path):
                    return '-44:path \"'+path+'\" doesn\'t exists'
                for f in os.listdir(self.dbpath+'/'+self.dbname):
                    #print('NOME FILE ='+f)
                    if f.endswith(ext):
                        tn = f[:-4]
                        utils.debug('NOME FILE TABELLA ='+tn)
                        #print('     NOME FILE TABELLA ='+tn)
                        self.loadRelation(tn)
            else:
                self.loadRelation(relname)
                
            return '0:'+relname 

        # richiesta dell'invio di una relazione 
        elif a[0] == 'get': # formato: get relname
            name = a[1]
            #print('In Engine: GET: name=',name)
            if name in self.relations:
                result = self.relations[name] 
                #print('RISULTATO in Engine GET =\n',result)
                return '0:'+name+'\n'+result.csv()
            else:
                return '-404:'+'Relation \"'+name+'\" not found'
            
        # Sintassi:
        # 1) SET DBPATH Percorso
        # 2) SET DBNAME NomeDB
        # 3) SET NomeTabella Espressione
        # 4) SET NomeTabella TABLE Schema [Tuple] <END>
        # 5) SET NomeTabella VALUES Tuple         <END>
        #
        elif a[0] == 'set': # formato: set relname expAR
            #print('In Engine: ASSIGN:',exp)
            #print('a[1].UPPER =',a[1].upper())

            if len(a)<2:
                return '-1:'+'incomplete instruction \"set\"'
            
            if a[1].upper() == 'DBNAME':
                #print('Engine:trovato DBNAME =',a[2])
                self.dbname = a[2]
                return '0:'+'dbname \"'+a[2]+'\" setted'
            
            elif a[1].upper() == 'DBPATH':
                #print('Engine:trovato DBPATH =',a[2])
                self.dbpath = a[2]
                #return "0:DBNAME"
                return '0:'+'dbpath \"'+a[2]+'\" setted'

            elif (a[2].upper() == 'TABLE') or (a[2].upper() == 'VALUES'):
                tname = a[1]
                oper = a[2] # operazione: VALUES o TABLE
                lines = exp.split('\n')
                #tab = tname+'\n' # testo in linee contenente la tabella csv
                tab = ''
                for i in range(1,len(lines)-1):  # -1 per il <END> finale
                    #print('LINEA ',i,'=',lines[i])
                    tab += lines[i]+"\n"
                if oper == 'table':
                    #print('Engine: operazione TABLE')
                    tab = tname+'\n'+tab # aggiunta 1^ linea con nome tabella
                    result = Relation.Relation(tab)
                    self.relations[tname] = result         # aggiunge relazione al dizionario
                    self.relations[tname].relname = tname  # assegnazione del nome alla tabella                  
                elif oper == 'values':
                    #print('Engine: TAB VALUES passato =['+tab+']')
                    self.relations[tname].replace(tab)
                    #print('Engine: operazione VALUES')
                else:
                    return '-1: unricognized operation \"'+oper+'\"'
                return '0:'+tname
            
            else:
                #---- caso di assegnazione con espressione ----
                tname = a[1]  # nome tabella assegnanda
                pos   = exp.find(tname)
                exp   = exp[pos+len(a[1]):].strip() # parte destra dell'assegnazione
                #print("TROVATA ASSEGNAZIONE ALLA RELAZIONE:")
                #print("          TNAME =",tname)
                #print("          EXP   =",exp)
                #if not Types.is_valid_relation_name(tname):
                if not Exp.is_valid_relation_name(tname):
                    errmsg = "Wrong name \'"+tname+"\' for destination relation." 
                    return "-1:"+errmsg 
              
                # valutazione dell'espressione
                #
                # conversione dell'espressione sostituendo i token uni-carattere (es. ≤)
                # con una coppia di caratteri interpretabili dalla funzione eval di Python
                #print("--------- prima di queryc")
                queryc = Exp.changeOperators(exp)  # cambia = in == (x Python)
                #print("+++++++++ dopo di queryc")

                utils.debug("in Engine.executeExpression : query ="+exp)
                #expr = parser.parse(queryc)            # conversione exp in codice Python
                #print('---- prima di parse ---- queryc =',queryc)
                expr = Exp.parse(queryc)   #utils.         # conversione exp in codice Python
                #expr = parse(queryc)            # conversione exp in codice Python
                utils.debug(queryc+" --> "+expr)       # debug
                #print('---- prima di eval: EXPR =',expr)
                try:
                    result = eval(expr,self.relations)     # valutazione espressione
                except Exception as e:
                    errmsg = str(e)
                    return '-10:'+errmsg
                #print('++++ dopo di eval +++++')
                self.relations[tname] = result         # aggiunge relazione al dizionario
                self.relations[tname].relname = tname  # assegnazione del nome alla tabella
                #print('RISULTATO in Engine ASSIGN: =\n',result)
                #return 'ok\n'+result.csv()   #30dic15
                return '0:'+tname
       
        # richiesta del client di chiusura della connessione 
        elif a[0] == 'close': 
            print('CHIUSA LA CONNESSIONE IN Engine')
            return '0:'+'Connection closed'
        else:
            print('Istruzione errata in Engine')
            return '-2:'+'Error in expression \''+exp+'\''+' in Engine'

#-------------------------------------
if __name__ == "__main__":
    eng = Engine()
    eng.active(2468)
      
              
       

