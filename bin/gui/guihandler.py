# File: guihandler.py
# Date: 20 gen 16
# Note: module that manages gui events

import sys
import os
import pickle
import socket

from PyQt4 import QtCore, QtGui
#from PyQt5 import QtCore, QtGui, QtWidgets

version = 'undefined'

from . import maingui, utils, Table  

NPORT = 2468
MSGLEN = 10000 #4056  # lunghezza massima dei messaggi (ATTENZIONE A QUELLO IN MultiServer)

class relForm(QtGui.QMainWindow):  #per PyQt4
#class relForm(QtWidgets.QMainWindow):    #per PyQt5

    def __init__(self, ui):
        QtGui.QMainWindow.__init__(self)  #per PyQt4
        #QtWidgets.QMainWindow.__init__(self)  #per PyQt5
        self.About = None
        self.relations = {}  # dizionario delle relazioni
        self.selectedRelation = None
        self.ui = ui
        self.filename = 'prova.csv' # current program name
        self.dbpath = '.'  # path of the root directory of databases
        self.dbname = ''   # current database name
        self.settings = QtCore.QSettings()
        self.lineNumber = 0  # numero della linea corrente in esecuzione
        self.lineText = ''   # testo della linea corrente in esecuzione
        #self.version = "RAEE - v. 0.42 - 7 ott 15"
        
        # connessione al server
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect(('localhost', NPORT))
        # lettura del messaggio di benvenuto
        data = self.clientsocket.recv(MSGLEN)
        data = data.decode('utf-8')
        #print('[<]',data)
        #print('[-] Connected to server!')
        print('[-] Connected to:',data)

        # esecuzione programma di configurazione NON QUI
        #self.execute('initRAEE.ra')
        #print('ESEGUITO PROG INITRAEE.RA')
              
    #--------------- parte nuova [lc] ------------------------

    # shows an error message
    def errorMessage(self,errmsg):
        msg = str(self.lineNumber)+': '+self.lineText    
        self.ui.messaggioErrore.setText(msg)
        self.boxMessage('Error',errmsg)
        return

    # visualizzazione messaggio su un box:
    #   header : intestazione del box
    #   msg    : messaggio da visualizzare
    def boxMessage(self,header,msg):
        QtGui.QMessageBox.information(None,header,msg)
        return

    # controlla la condizione cond; se non e' verificata segnala errore
    # e termina l'applicazione
    # return: True se la condizione e' soddisfatta
    def assertMessage(self,cond,msg):
        if not cond:
             self.errorMessage(msg)
             # sys.exit(-1)  # troppo 'forte'
             return False
        return True    

    # manda l'istruzione al server e riceve la stringa risultato;
    # questa istruzione costituisce l'unico punto di comunicazione con il server
    # ritorna la terna (cod,msg,data) dove:
    #   cod:  codice numerico dell'esito (>=0 se ok; <0 se errore)
    #   msg:  messaggio di esito
    #   data: pacchetto dati (messaggio dell'errore o risultato diviso in linee)
    # (cod:msg) costituiscono l'header, contenuto nella prima riga
    # data e' il pacchetto dati formato da piu' linee 8l'ultima e' <END>
    def sendToServer(self,query):
        #print('guihandler: in sendToServer: QUERY: ',query) #ERR in conversione
        msg = utils.conv(query)  # conversione dei caratteri operatori in stringhe
        print('[>]',msg)
        msg = msg.encode('utf-8')
        self.clientsocket.send(msg[:])
        #print('guihandler: in sendToServer: mandato MSG: ',msg)
        pack = self.clientsocket.recv(MSGLEN)  # intero pacchetto ricevuto
        pack = pack.decode('utf-8')
        print('[<]',pack)  # FA PERDERE SYNC CON SERVER ?
        lenheader = pack.index('\n') # fine della prima riga
        header = pack[:lenheader]
        #print('HEADER = ['+header+']')
        a = header.split(':')  # suddivisione header
        cod = int(a[0])
        msg = a[1]
        data = pack[lenheader+1:]
        #print('in sendToServer: ricevuto COD =',cod)   #,' DATA =',data)
        #print('[<]',cod)   #,' DATA =',data)
        #return data
        return (cod,msg,data)

    # esegue l'intero programma memorizzato nel file fname oppure
    # presente nella finestra di edit (se fname=='')
    def execute(self, fname=''):
        if fname != '':
            try:
                #fp = open(path)
                #prog = fp.read()
                f = open(fname,"rb") 
                prog = pickle.load(f)
                #print("guihandler:programma letto dal file ",fname,"= [",prog,"]")
                f.close()
            except Exception as e:
                utils.debug('File not found: '+fname)  
                #raise Exception('Error in opening configuration file \''+fname+'\'')
                print('Program not found: '+fname)  
                return
        else:
            prog = self.ui.SorgenteProgramma.toPlainText()

        #print("@ in guihandler.execute: sto per eseguire programma: ",prog)
        # split program into lines
        NL = chr(10)
        a = prog.split(NL)
        #utils.debug('in guihandler.execute: istruzioni = '+str(a))
     
        # execution of every expression,
        # skiping empty lines (begining with #)
        for i in range(len(a)):
            exp = a[i]
            self.lineNumber = i+1
            self.lineText = a[i]
            k = exp.find('#')
            if k >= 0:
                exp = exp[:k]
            exp = exp.strip()
            # 'end' command ends program
            if exp == 'end':
                break
            ris = self.executeExpression(exp)
            if ris<0: break

    # esegue l'espressione exp: alcuni comandi vengono gestiti localmente dalla GUI;
    # altri (assegnazioni, ...) vengono inviati al motore dell'elaborazione
    #
    # return:
    #   0 : esecuzione corretta
    #  -1 : comando errato
    #
    def executeExpression(self, exp):
        '''
        examples:
            dbpath db/azienda
            dbpath .
            debug on/off
            load REPARTO
            load *
            idtab ← expAR
        '''

        #utils.debug("guihandler:esecuzione espressione: "+exp)
        #print("guihandler:esecuzione espressione: "+exp) #ERR in codifica unicode
                       
        if exp == '':
            return 0

        a = exp.split() # splits exp into words

        if a[0] == 'debug':
            if not self.assertMessage(len(a)>1,'missing on/off'): return -1
            m = True if a[1]=='on' else False
            utils.setDebug(m)
                  
        elif a[0] == 'dbpath':
            #- """ quando veniva gestito nel client
            #- if not self.assertMessage(len(a)>1,'missing path'): return -1
            #- # RIM? if not self.assertMessage(os.path.exists(a[1]),'path \''+a[1]+'\' doesn\'t exists'): return -1
            #- self.dbpath = a[1]
            #- utils.debug('impostato DBPATH ='+self.dbpath)
            #- """
            if not self.assertMessage(len(a)>1,'missing path'): return -1
            self.dbpath = a[1] # memorizzazione locale
            #cod, msg, data = self.sendToServer(exp) #8gen16
            cod, msg, data = self.sendToServer("set "+exp) #13gen16
            if cod < 0:
                self.errorMessage(msg)
                return -1

        # set current database   
        elif a[0] == 'dbname':
            if not self.assertMessage(len(a)>1,'missing database name'): return -1
            self.dbname = a[1]
            #cod, msg, data = self.sendToServer("dbpath "+self.dbpath+self.dbname)
            cod, msg, data = self.sendToServer("set "+exp) #13gen16
            if cod < 0:
                self.errorMessage(msg)
                return -1
                 
        elif a[0] == 'get': # GET tabname
            cod, msg, data = self.sendToServer(exp) #31gen15
            if cod < 0:
                self.errorMessage(msg)
                return -1
            #print('guihandler: DATA in GET: ',data)
            """ -5gen16
            a = data.split('\n')
            s = ''
            for k in range(1,len(a)):  #MIGLIORARE
                #print('A[',k,']=',a[k])
                s += (a[k]+'\n')
            """
            s = data
            #print('TABELLA CSV:')
            #print(s)
            self.refreshTable(s)

        elif a[0] == 'send': # invia una tabella al server ... (per test)
            tab = "set REPARTO table\n"
            tab += "Sigla,Descrizione,Telefono,Responsabile\n"
            #tab = "def REPARTO values\n"
            
            tab += "A,NEWamministrazione,1000,AF01\n"
            tab += "P,NEWproduzione,2000,BA01\n"
            tab += "M,NEWmagazzino,3000,RG02\n"
            tab += "<END>"
              
            cod, msg, data = self.sendToServer(tab) 
            if cod < 0:
                self.errorMessage(msg)
                return -1
            print('guihandler: COD =',cod)
            print('guihandler: MSG =',msg)
            print('guihandler: DATA =',data)
                   
        elif a[0] == 'load':
            #print('comando LOAD in guihandler')
            #print("in guihandler: EXP =",exp)
            cod, msg, data = self.sendToServer(exp) #8gen16
            if cod < 0:
                self.errorMessage(msg)
                return -1
        
        elif a[0] == 'save':
            fn = self.dbpath+a[1]+'.csv'  # file name
            utils.debug('esecuzione comando SAVE: nomefile ='+fn)
            self.saveRelation(fn)
            assign = False # nulla da visualizzare
            toshow = False
           
        # visualizzazione del contenuto di una tabella 
        elif a[0] == 'show':
            tn = a[1]  # table name
            if not tn in self.relations:
                utils.debug('ERRORE: non trovata relazione '+tn)  
                errmsg = 'table \''+tn+'\' not found'
                self.errorMessage(errmsg)
                return -1
            utils.debug('esecuzione comando SHOW: nometabella = '+tn)
            result = eval(tn, self.relations)
            self.showRelation(result)
           
        # assegnazione nella forma "T ← ExprAR"
        # nella sendToServer viene convertita in formato per l'engine
        elif (exp.find('←') >= 0):
            errcode, errmsg, data = self.sendToServer(exp) 
            #print('guihandler: ERR in ASSIGN: ',errcode)  
            #print('guihandler: MSG in ASSIGN: ',errmsg)     # fa perdere SYNC... ?
            if errcode < 0:
                self.errorMessage(errmsg)
                return -1

            name = errmsg
            #result = self.sendToServer('get '+name)
            code, msg, data = self.sendToServer('get '+name) 
            #print('guihandler: RESULT ASSIGN: ',data)  # fa perdere SYNC...
            s = data
            #print('TABELLA CSV:')
            #print(s)
            self.refreshTable(s)
           
        # caso di comando errato
        else:
            self.errorMessage('Not a command : \''+exp+'\'')
            return -1
        
        return 0 # comando eseguito correttamente
   
    # visualizza la tabella codificata nelle stringa s
    # (serve per aggiornare i risultati ottenuti dall'engine)
    # struttura della stringa s, suddivisa in linee separate da EOL:
    #   nometabella
    #   lista attributi
    #   riga1
    #   riga2
    #   ...
    def refreshTable(self,s):
        # visualizzazione in forma tabellare della stringa s
        tab = Table.Table() # tabella vuota
        tab.decode_csv(s)
        tname = tab.relname
        self.relations[tname] = tab         # aggiunge relazione al dizionario
        self.updateRelations()                  # aggiorna la lista
        self.selectedRelation = tab
        #self.showRelation(self.selectedRelation) # visualizza la tabella

    # fine parte nuova lc =======================================
    
    # creazione di un nuovo file vuoto (sovrascrivendo il vecchio)
    def newFile(self):
        utils.debug('------------ in newFile ----------------')
        fname = "unamed.ra"
        self.ui.SorgenteProgramma.setPlainText("# File: ...\n# Date: ...\n# Note:...")  # testo di edit
        
        # setta il nome del file correntemente in edit 
        #self.setFileName(fname)  # questa forse non serve
        self.filename = fname
        self.ui.label_FileName.setText(fname)    # scrive nomefile di edit
        return

    # caricamento programma da file .ra
    def loadFile(self,fname=None):
        utils.debug('------- in loadFile -------- fname ='+str(fname))
        # Asking for file to load
        if fname == None:
            fname = QtGui.QFileDialog.getOpenFileName(self, QtGui.QApplication.translate(
                "Form", "Carica File"), "", QtGui.QApplication.translate("Form", "Programmi (*.ra);;Text Files (*.txt);;All Files (*)"))

        if not self.assertMessage(os.path.isfile(fname),'file \''+fname+'\' not found'): return -1
        
        f = open(fname,"rb") 
        prog = pickle.load(f)
        #print("programma letto =",prog)
        #print("guihandler2: PATH =",os.getcwd())
        #print("guihandler2: FNAME =",fname)
        f.close()

        # estrazione nome file dal percorso
        a = fname.split('/')        # split the full path
        name = a[len(a)-1].lower()  # takes only the lowercase filename
        self.ui.SorgenteProgramma.setPlainText(prog)    # scrive prog sulla finestra di edit
        
        # setta il nome del file correntemente in edit
        self.filename = fname
        self.ui.label_FileName.setText(name)    # scrive nomefile di edit
        return

    # salvataggio programma
    def saveFile(self):
        prog = self.ui.SorgenteProgramma.toPlainText()
        fname = self.filename 
        utils.debug('------- in saveFile -------- fname ='+fname)
        utils.debug('------- in saveFile -------- prog  ='+prog)  
        f = open(fname,"wb")
        pickle.dump(prog,f) 
        f.close()
        return

    # salvataggio programma
    def saveFileAs(self):
        utils.debug('------- in saveFileAs --------')           
        prog = self.ui.SorgenteProgramma.toPlainText()
        #print("programma da salvare = ",prog);
        fname = QtGui.QFileDialog.getSaveFileName(self, QtGui.QApplication.translate(
            "Form", "Salva File"), "", QtGui.QApplication.translate("Form", "Programmi (*.ra)"))
        if (len(fname) == 0):  # Returns if no file was selected
            return
        f = open(fname,"wb")
        pickle.dump(prog,f) 
        f.close()
        return
   
    #=========================================== fine parte nuova

    # carica una relazione da un file csv e le assegna il nome indicato (controllare che sia ok)
    # se non e' precisato il nome della relazione viene assegnata al nome del file;
    # parametri:
    #   - path e' il percorso completo del file da caricare (es. db\azienda\REPARTO.csv)
    #     se path==None viene richiesta la selezione di un file
    #   - name e' il nome che viene assegnato alla tabella in memoria
    #     se name==None viene assunto il nome del file csv (senza percorso ed estensione)
    # return: -1 if error in loading csv file
    #
    def loadRelation(self, path=None, name=None):
        '''
        Loads a relation from a csv file.
        Without parameters it will ask the user which relation to load,
        otherwise it will load filename, giving it name.
        It shouldn't be called giving filename but not giving name.
        '''
        
        # select file name to load
        if path == None:
            path = QtGui.QFileDialog.getOpenFileName(self,
                       QtGui.QApplication.translate("Form","Load Relation"), "",
                       QtGui.QApplication.translate("Form","Relations (*.csv);;Text Files (*.txt);;All Files (*)"))

        utils.debug('in guihandler.loadRelation: path='+path)

        if name == None:
            # rebuild table name
            f = path.split('/')           # Split the full path
            name = f[len(f) - 1].upper()  # Takes uppercase filename
      
        if len(name) == 0:
            return 0

        if (name.endswith(".CSV")):       # removes the extension
            name = name[:-4]

        #print("in guihandler.loadRelation : PATH =",path)  #percorso completo
        #print("in guihandler.loadRelation : NAME =",name)  #nome della tabella

        cod, msg, data = self.sendToServer('load '+path+' '+name)
        if cod < 0:
            self.errorMessage(msg)
            return -1
        #print('guihandler: RIS in LOAD: ',ris)
        cod, msg, tab = self.sendToServer('get '+name) 
        #print('guihandler: TAB in LOAD: ',tab)   # fa perdere SYNC...
        
        #assegnazione del nome alla relazione letta: [lc]
        #self.relations[name].relname = name #... migliorare;  serve??? [-28dic15]
        #self.updateRelations()
        self.refreshTable(tab)

    def showRelation(self, rel):
        '''Shows the selected relation into the table'''
        self.ui.table.clear()

        if rel == None:  # No relation to show
            self.ui.table.setColumnCount(1)
            self.ui.table.headerItem().setText(0, "Empty relation")
            return
        self.ui.table.setColumnCount(len(rel.header.attributes))

        # Set content
        for i in rel.content:
            item = QtGui.QTreeWidgetItem()
            for j in range(len(i)):
                item.setText(j, i[j])
            self.ui.table.addTopLevelItem(item)
            #print("    # item =",item)

        # Sets columns
        for i in range(len(rel.header.attributes)):
            self.ui.table.headerItem().setText(i, rel.header.attributes[i])
            self.ui.table.resizeColumnToContents(i)  # Must be done in order to avoid  too small columns

        # Setta nome relazione nell'intestazione [lc]
        self.ui.label_RelationName.setText(rel.relname)    # scrive nomefile di edit

    def printRelation(self, item):
        self.selectedRelation = self.relations[item.text()]
        self.showRelation(self.selectedRelation)

    def showAttributes(self, item):
        '''Shows the attributes of the selected relation'''
        rel = item.text()
        self.ui.lstAttributes.clear()
        for j in self.relations[rel].header.attributes:
            self.ui.lstAttributes.addItem(j)

    def updateRelations(self):
        self.ui.lstRelations.clear()
        for i in self.relations:
            if i != "__builtins__":
                self.ui.lstRelations.addItem(i)

    def saveRelation(self, fname=None):
        ''' salvataggio su disco del contenuto di una relazione:
        se il nome del file non e' precisato (filename==None) viene
        attivata una finestra per la scelta del nome del file su cui salvare
        '''
        if fname == None:
            fname = QtGui.QFileDialog.getSaveFileName(self, QtGui.QApplication.translate(
                "Form", "Save Relation"), "", QtGui.QApplication.translate("Form", "Relations (*.csv)"))
                       
        if (len(fname) == 0):  # Returns if no file was selected
            return
        self.selectedRelation.save(fname)
        return

    def unloadRelation(self):
        for i in self.ui.lstRelations.selectedItems():
            del self.relations[i.text()]
        self.updateRelations()

    def editRelation(self): # DA COMPLETARE
        #from . import creator
        for i in self.ui.lstRelations.selectedItems():
            rel = self.relations[i.text()]
            print('Edit della relazione: [DA COMPLETARE!!!]\n',rel)
        #self.updateRelations()

    def newRelation(self): # attualmente (8dic14) non viene richiamata
        return  # tagliata la funzione originale
    
    def closeEvent(self, event):
        self.save_settings()
        event.accept()

    def save_settings(self):
        # self.settings.setValue("width",)
        pass

    def restore_settings(self):
        # self.settings.value('session_name','default').toString()
        pass

    def showAbout(self):
        global version
        self.boxMessage('About',version)
        pass
             
    def addProduct(self):
        #self.addSymbolInQuery("⨉")
        self.addSymbolInQuery("⨯")

    def addDifference(self):
        self.addSymbolInQuery("∸")

    def addUnion(self):
        self.addSymbolInQuery("∪")

    def addIntersection(self):
        self.addSymbolInQuery("∩")

    def addDivision(self):
        self.addSymbolInQuery("÷")

    def addOLeft(self):
        self.addSymbolInQuery("⟕")

    def addJoin(self):
        #self.addSymbolInQuery(u'\u2a1d')
        self.addSymbolInQuery("⨝")

    def addORight(self):
        self.addSymbolInQuery("⟖")

    def addOuter(self):
        self.addSymbolInQuery("⟗")

    def addProjection(self):
        self.addSymbolInQuery("π")

    def addSelection(self):
        self.addSymbolInQuery("σ")

    def addRename(self):
        self.addSymbolInQuery("ρ")

    def addArrow(self):
        self.addSymbolInQuery("→")
        
    def addAssign(self):
        self.addSymbolInQuery("←")

    def addLessEqual(self):
        self.addSymbolInQuery("≤")

    def addGreaterEqual(self):
        self.addSymbolInQuery("≥")

    def addNotEqual(self):
        self.addSymbolInQuery("≠")

    def addAnd(self):
        self.addSymbolInQuery("∧")
        
    def addOr(self):
        self.addSymbolInQuery("∨")
        
    def addNot(self):
        self.addSymbolInQuery("¬")

    # copia di simboli delimitatori di un attributo
    def addAttr(self):
        self.addSymbolInQuery("⦇⦈")

    # per prova
    def addSimboliDiProva(self):
        self.addSymbolInQuery("⦇⦈←σπρᑌᑎ−≤≥≠ ᐅᐊ ᗆᗉ ×**+-÷ᐱᐯ¬→")
        
    def addSymbolInQuery(self, symbol):
        #self.ui.txtQuery.insert(symbol)  #originale
        #self.ui.txtQuery.setFocus()      #originale
        
        # lc 26set14
        #self.ui.SorgenteProgramma.setPlainText(symbol)    # setta tutto il testo
        #self.ui.SorgenteProgramma.appendPlainText(symbol) # appende su nuova linea
        self.ui.SorgenteProgramma.insertPlainText(symbol)
        self.ui.SorgenteProgramma.setFocus()
   
        
if __name__ == "__main__":

    import sip  # needed on windows (rimesso il 17dic14 per convertire in exe)
    from PyQt4 import QtGui
    #from PyQt5 import QtGui
    #from gui import maingui, guihandler #per prova
    import maingui #, guihandler #per prova

    #guihandler.version = version

    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('None')
    app.setApplicationName('RAEE')
        
    ui = maingui.Ui_MainWindow()
    #Form = guihandler.relForm(ui)
    Form = relForm(ui)

    #Form.setFont(QtGui.QFont("Dejavu Sans Bold"))  #orig
    Form.setFont(QtGui.QFont("Arial")) # a cosa serve?

    ui.setupUi(Form)
    Form.restore_settings()

    Form.execute('RAEE.ra') # programma di configurazione
    #print('eseguito file RAEE.ra')

    Form.show()
    sys.exit(app.exec_())

      
     
        
