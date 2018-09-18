# File: Table.py
# Date: 5 gen 16
# Note: versione ridotta della classe Relation;
#       serve solo per memorizzare i dati della relazione;
#       non permette operazioni

import csv

class Table:
   
    __hash__ = None
    
    # crea una relazione vuota
    def __init__(self):
        self._readonly = False
        self.relname = 'unnamed'  # relation name #lc
        self.header = Header([])
        self.content = set()

    def csv(self):  
        '''
        Convert relation in a csv format:
        tabname;
        attr1,attr2,attr3;
        v11,v12,v13;
        v21,v22,v23;
        '''

        res = self.relname+"\n"
        for a in self.header.attributes:
            res += a+","
        res = res[:len(res)-1] # elimina ,
        res += ';\n'    
                    
        for r in self.content:
            for i in r:
                res += i+','
            res = res[:len(res)-1] # elimina ,    
            res += '\n'      
        return res

    # converte una stringa csv in tabella
    def decode_csv(self,s):  #lc
        '''
        Convert relation in a csv format:
        tabname;
        attr1,attr2,attr3;
        v11,v12,v13;
        v21,v22,v23;
        '''

        a = s.split('\n')
        self.relname = a[0]                    # table name
        self.header = Header(a[1].split(','))  # attributes  
        self.content = set()
              
        for i in range(2,len(a)-1): # -1 per l'<END> finale
            if a[i] == '<END>': break
            self.content.add(tuple(a[i].split(',')))

   
#=========================================================================

class Header (object):

    '''This class defines the header of a relation.
    It is used within relations to know if requested operations are accepted'''

    # Since relations are mutable we explicitly block hashing them
    __hash__ = None

    def __init__(self, attributes):
        '''Accepts a list with attributes' names. Names MUST be unique'''
        self.attributes = attributes

        """ RIM [-1.1.16]
        for i in attributes:
            #if not is_valid_relation_name(i):
            #if not Rstring(i).is_valid_relation_name():
            if not is_valid_relation_name(i):
                raise Exception('"%s" is not a valid attribute name' % i)
        """
        
    """
    def __repr__(self):
        return "header(%s)" % (self.attributes.__repr__())

    def rename(self, old, new):
        #'''Renames a field. Doesn't check if it is a duplicate.
        #Returns True if the field was renamed, False otherwise'''

        if not is_valid_relation_name(new):
            raise Exception('%s is not a valid attribute name' % new)

        try:
            id_ = self.attributes.index(old)
            self.attributes[id_] = new
        except:
            return False
        return True

    def sharedAttributes(self, other):
        '''Returns how many attributes this header has in common with a given one'''
        return len(set(self.attributes).intersection(set(other.attributes)))

    def __str__(self):
        '''Returns String representation of the field's list'''
        return self.attributes.__str__()

    def __eq__(self, other):
        return self.attributes == other.attributes

    def __ne__(self, other):
        return self.attributes != other.attributes

    def getAttributesId(self, param):
        #'''Returns a list with numeric index corresponding to field's name'''
        res = []
        for i in param:
            for j in range(len(self.attributes)):
                if i == self.attributes[j]:
                    res.append(j)
        return res
    """


"""
if __name__ == "__main__":
    #import utils
    from Types  import *  # per provare in locale 
    r = Relation('dipendente.csv')
    print('R=',r)
    r.delete('Cognome>\'G\'')
    print('R=',r)
"""    
    
