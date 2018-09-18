# File: Relation.py
# Date: 20 gen 16
# Note: adattamento del file relation.py di Relational
#       This module provides a classes to represent relations and to perform
#       relational operations on them.

from . import Exp, Types

import csv

class Relation (object):

    '''This objects defines a relation (as a group of consistent tuples) and operations
    A relation can be represented using a table
    Calling an operation and providing a non relation parameter when it is expected will
    result in a None value'''
    __hash__ = None
    
    # crea una relazione a partire da un testo csv organizzato in linee
    # secondo il seguente formato (argomento text):
    # oppure, se text != None, in base ad un testo secondo il seguente formato csv in linee:
    #
    #   TabName
    #   Attr1, Attr2, ..., Attrn
    #   v11,   v12,   ..., v1n
    #   ...
    #   vm1,   vmn,   ..., vmn
    #
    # Se text==None viene generata una relazione vuota di nome 'unnamed';
    # se text contiene una sola linea (nome tabella) viene generata una r. di nome indicato;
    # se text contiene 2 linee viene definito anche lo schema della rel. (seconda linea);
    # se text contiene >2 linee, dalla terza sono riportati i dati dell'estensione
    #
    def __init__(self, text=None):    
        '''
        Creates a relation.
        Empty relations are used in internal operations.
        '''
        #print('Relation: TEXT =',text)
        self._readonly = False
        if text != None:
            lines = text.split('\n')
            nl = len(lines)
            if nl>0: name = lines[0]
        else:
            nl = 0
            name = 'unnamed'
        self.relname = name  # relation name #lc
        self.header = Header([])
        self.content = set()

        # definizione dello schema e dell'estensione
        if nl>1:
             a = lines[1].split(',')
             self.header = Header(tuple(a))  # array dei nomi degli attributi
             if nl>2:
                 for i in range(2,nl-1):  # Iterating rows
                     a = lines[i].split(',')
                     self.content.add(tuple(a)) # USARE insert per evitare ripetizioni
                 
    def _make_writable(self):
        '''If this relation is marked as readonly, this
        method will copy the content to make it writable too'''

        if self._readonly:
            self.content = set(self.content)
            self._readonly = False
            
    # name : nome interno da assegnare alla tabella
    # path : perscorso completo del file da leggere
    def load(self, name, path):
        '''
        Loads the relation name from the file specified by path.
        The file will be handled like a comma separated as described in RFC4180.
        '''
        self.relname = name  # relation name #lc

        """
        if (len(path) == 0) and (len(name)==0):  # Empty relation
            self.content = set()
            self.header = Header([])
            return
        """
        
        # Opening file
        #utils.debug("in Relation.__init__ : PATH = "+path)
        #utils.debug("in Relation.__init__ : NAME = "+name)
        #fp = open(path)    # migliorato sotto
        try:
            fp = open(path)
        except Exception as e:
            #print('ERRORE IN APERTURA FILE')
            #raise Exception('Error in opening file \''+path+'\'')
            return(-1,'Error in opening file \''+path+'\'')
                                    
        reader = csv.reader(fp)  # Creating a csv reader
        self.header = Header(next(reader))  # read 1st line
        self.content = set()
              
        for i in reader.__iter__():  # Iterating rows
            self.content.add(tuple(i)) # USARE insert per evitare ripetizioni

        # Closing file
        fp.close()
        return(0,'ok')


    def save(self, filename):
        '''
        Saves the relation in a file. By default will save using the csv
        format as defined in RFC4180, but setting comma_separated to False,
        it will use the old format with space separated values.
        '''

        fp = open(filename, 'w')  # opening file
        writer = csv.writer(fp)   # creating csv writer

        # It wants an iterable containing iterables
        head = (self.header.attributes,)
        writer.writerows(head)

        # Writing content, already in the correct format
        writer.writerows(self.content)
        fp.close()  # Closing file

    def _rearrange_(self, other):
        '''If two relations share the same attributes in a different order, this method
        will use projection to make them have the same attributes' order.
        It is not exactely related to relational algebra. Just a method used
        internally.
        Will return None if they don't share the same attributes'''
        if (self.__class__ != other.__class__):
            return None
        if self.header.sharedAttributes(other.header) == len(self.header.attributes) == len(other.header.attributes):
            return other.projection(list(self.header.attributes))
        return  None

    def _autocast(self, string):
        '''Depending on the regexp matched by the string,
        it will perform automatic casting'''
        tmpstring = Types.Rstring(string)
        if len(tmpstring) > 0 and tmpstring.isInt():
            return int(tmpstring)
        elif len(tmpstring) > 0 and tmpstring.isFloat():
            return float(tmpstring)
        elif len(tmpstring) > 0 and tmpstring.isDate():
            return Types.rdate(tmpstring)
        else:
            return tmpstring

    def selection(self, expr):
        '''Selection, expr must be a valid boolean expression, can contain field names,
        constant, math operations and boolean ones.'''
        attributes = {}
        newt = Relation()
        newt.header = Header(list(self.header.attributes))
        for i in self.content:
            # Fills the attributes dictionary with the values of the tuple
            for j in range(len(self.header.attributes)):
                attributes[self.header.attributes[j]] = self._autocast(i[j])

            try:
                #print('in Relation.selection expr = ',expr)
                #print('in Relation.selection attr = ',attributes)
                if eval(expr, attributes):
                    newt.content.add(i)
                    #print('+ ',i)
                #else:
                    #print('- ',i)
            except Exception as e:
                raise Exception("Failed to evaluate %s\n%s" % (expr, e.__str__()))
        return newt

    def product(self, other):
        '''Cartesian product, attributes must be different to avoid collisions
        Doing this operation on relations with colliding attributes will
        cause an exception.
        It is possible to use rename on attributes and then use the product'''

        if (self.__class__ != other.__class__)or(self.header.sharedAttributes(other.header) != 0):
            raise Exception('Unable to perform product on relations with colliding attributes')
        newt = Relation()
        newt.header = Header(self.header.attributes + other.header.attributes)

        for i in self.content:
            for j in other.content:
                newt.content.add(i + j)
        return newt

    def projection(self, * attributes):
        '''Projection operator, takes many parameters, for each field to use.
        Can also use a single parameter with a list.
        Will delete duplicate items
        If an empty list or no parameters are provided, returns None'''
        # Parameters are supplied in a list, instead with multiple parameters
        if isinstance(attributes[0], list):
            attributes = attributes[0]

        # Avoiding duplicated attributes
        attributes1 = []
        for i in attributes:
            if i not in attributes1:
                attributes1.append(i)
        attributes = attributes1

        ids = self.header.getAttributesId(attributes)
        #print('Relation: ATTRS =',attributes,'  ids =',ids)
        if len(ids) == 0 or len(ids) != len(attributes):
            raise Exception('Invalid attributes for projection')
        newt = Relation()
        # Create the header
        h = []
        for i in ids:
            h.append(self.header.attributes[i])
        newt.header = Header(h)

        # Create the body
        for i in self.content:
            row = []
            for j in ids:
                row.append(i[j])
            newt.contenuti.add(tuple(row))
        return newt

    def rename(self, params):
        '''Operation rename. Takes a dictionary
        Will replace the itmem with its content.
        For example if you want to rename a to b, provide {"a":"b"}
        '''
        result = []

        newt = Relation()
        newt.header = Header(list(self.header.attributes))

        for old, new in params.items():
            if (newt.header.rename(old, new)) == False:
                raise Exception('Unable to find attribute: %s' % old)

        newt.content = self.content
        newt._readonly = True
        return newt

    def intersection(self, other):
        '''Intersection operation. The result will contain items present in both
        operands.
        Will return an empty one if there are no common items.
        Will return None if headers are different.
        It is possible to use projection and rename to make headers match.'''
        other = self._rearrange_(other)  # Rearranges attributes' order
        if (self.__class__ != other.__class__)or(self.header != other.header):
            raise Exception(
                'Unable to perform intersection on relations with different attributes')
        newt = Relation()
        newt.header = Header(list(self.header.attributes))

        newt.content = self.content.Intersectionection(other.content)
        return newt

    def difference(self, other):
        '''Difference operation. The result will contain items present in first
        operand but not in second one.
        Will return an empty one if the second is a superset of first.
        Will return None if headers are different.
        It is possible to use projection and rename to make headers match.'''
        other = self._rearrange_(other)  # Rearranges attributes' order
        if (self.__class__ != other.__class__)or(self.header != other.header):
            raise Exception(
                'Unable to perform difference on relations with different attributes')
        newt = Relation()
        newt.header = Header(list(self.header.attributes))

        newt.content = self.content.difference(other.content)
        return newt

    def division(self, other):
        '''Division operator
        The division is a binary operation that is written as R ÷ S. The
        result consists of the restrictions of tuples in R to the
        attribute names unique to R, i.e., in the header of R but not in the
        header of S, for which it holds that all their combinations with tuples
        in S are present in R.
        '''

        # d_headers are the headers from self that aren't also headers in other
        d_headers = list(set(self.header.attributes) - set(other.header.attributes))
        t = self.projection(d_headers).product(other)
        return self.projection(d_headers).difference(t.difference(self).projection(d_headers))

    def union(self, other):
        '''Union operation. The result will contain items present in first
        and second operands.
        Will return an empty one if both are empty.
        Will not insert tuplicated items.
        Will return None if headers are different.
        It is possible to use projection and rename to make headers match.'''
        other = self._rearrange_(other)  # Rearranges attributes' order
        if (self.__class__ != other.__class__)or(self.header != other.header):
            raise Exception('Unable to perform union on relations with different attributes')
        newt = Relation()
        newt.header = Header(list(self.header.attributes))

        newt.content = self.content.union(other.content)
        return newt

    def join(self, other, cond=None):    
        '''Natural join, joins on shared attributes (one or more). If there are no
        shared attributes, it will behave as cartesian product.
        se la condizione cond e' diversa da None viene eseguito un theta-join,
        altrimenti un join naturale
        '''

        # soluzione provvisoria: il theta join viene eseguito mediante un prodotto cartesiano
        # seguito da una selezione (migliorare l'efficienza)
        if cond != None:
            return self.product(other).selection(cond)

        # List of attributes in common between the relations
        shared = list(set(self.header.attributes)
                      .intersection(set(other.header.attributes)))

        newt = Relation()  # Creates the new relation

        # Adding to the headers all the fields, done like that because order is needed
        newt.header = Header(list(self.header.attributes))
        for i in other.header.attributes:
            if i not in shared:
                newt.header.attributes.append(i)

        # Shared ids of self
        sid = self.header.getAttributesId(shared)
        # Shared ids of the other relation
        oid = other.header.getAttributesId(shared)

        # Non shared ids of the other relation
        noid = []
        for i in range(len(other.header.attributes)):
            if i not in oid:
                noid.append(i)

        for i in self.content:
            for j in other.content:
                match = True
                for k in range(len(sid)):
                    match = match and (i[sid[k]] == j[oid[k]])

                if match:
                    item = list(i)
                    for l in noid:
                        item.append(j[l])

                    newt.content.add(tuple(item))

        return newt

   
    def outer(self, other):
        '''Does a left and a right outer join and returns their union.'''
        a = self.outer_right(other)
        b = self.outer_left(other)
        return a.union(b)


    def outer_right(self, other):
        '''Outer right join. Considers self as left and param as right. If the
        tuple has no corrispondence, empy attributes are filled with a "---"
        string. This is due to the fact that empty string or a space would cause
        problems when saving the relation.
        Just like natural join, it works considering shared attributes.'''
        return other.outer_left(self)


    #def outer_left(self, other, swap=False):  #orig
    def outer_left(self, other, swap_bho=False):  #lc
        '''Outer left join. Considers self as left and param as right. If the
        tuple has no corrispondence, empty attributes are filled with a "---"
        string. This is due to the fact that empty string or a space would cause
        problems when saving the relation.
        Just like natural join, it works considering shared attributes.'''

        shared = []
        for i in self.header.attributes:
            if i in other.header.attributes:
                shared.append(i)

        newt = Relation()  # Creates the new relation

        # Adds all the attributes of the 1st relation
        newt.header = Header(list(self.header.attributes))

        # Adds all the attributes of the 2nd, when non shared
        for i in other.header.attributes:
            if i not in shared:
                newt.header.attributes.append(i)
        # Shared ids of self
        sid = self.header.getAttributesId(shared)
        # Shared ids of the other relation
        oid = other.header.getAttributesId(shared)

        # Non shared ids of the other relation
        noid = []
        for i in range(len(other.header.attributes)):
            if i not in oid:
                noid.append(i)

        for i in self.content:
            # Tuple partecipated to the join?
            added = False
            for j in other.content:
                match = True
                for k in range(len(sid)):
                    match = match and (i[sid[k]] == j[oid[k]])

                if match:
                    item = list(i)
                    for l in noid:
                        item.append(j[l])

                    newt.content.add(tuple(item))
                    added = True
                    
            # If it didn't partecipate, adds it
            if not added:
                item = list(i)
                for l in range(len(noid)):
                    #item.append("---")
                    item.append(NULL)
                newt.content.add(tuple(item))

        return newt

    #-------------------- join esterni con condizione [+lc] -----------------------

    # left outer theta-join join esterno sinistro con condizione
    # if swap==True tuples of other are placed at the left side
    # and the tuples of selft are pleced at the right side
    # (to manage outer right join)
    def left_theta_join(self, other, cond, swap=False):
        #print("--------> relation.left_theta_join 1")
        attributes = {}
        newt = Relation()  # empty relation
        #print("--------> relation.left_theta_join 2")
        if not swap:
            newt.header = Header(self.header.attributes + other.header.attributes)
        else:    
            newt.header = Header(other.header.attributes + self.header.attributes)

        for i in self.content: # loop on self tuples
            added = False
            for j in other.content:  # loop on other's' tuples
                row = i+j if not swap else j+i    
                # Fills the attributes dictionary with the values of the tuple
                for j in range(len(newt.header.attributes)):
                    attributes[newt.header.attributes[j]] = newt._autocast(row[j])

                try:
                    if eval(cond, attributes):
                        newt.content.add(row)
                        added = True
                    
                except Exception as e:
                    raise Exception("Failed to evaluate %s\n%s" % (cond, e.__str__()))

            # If it didn't partecipate, adds it
            if not added:
                #newt.content.add(i)  #provvisorio ok
                t1 = list(i)
                t2 = []
                for l in range(len(other.header.attributes)):
                    t2.append(NULL)
                row = t1+t2 if not swap else t2+t1    
                newt.content.add(tuple(row))
                
        return newt
 
    def right_theta_join(self, other, cond):
        return other.left_theta_join(self,cond,True)

    # full outer theta join
    def full_theta_join(self, other, cond):
        a = self.left_theta_join(other,cond)  
        b = self.right_theta_join(other,cond)
        return a.union(b)

    #-----------------------------------------------------------------------------
  
    def __eq__(self, other):
        '''Returns true if the relations are the same, ignoring order of items.
        This operation is rather heavy, since it requires sorting and comparing.'''
        other = self._rearrange_(
            other)  # Rearranges attributes' order so can compare tuples directly

        if (self.__class__ != other.__class__)or(self.header != other.header):
            return False  # Both parameters must be a relation

        if set(self.header.attributes) != set(other.header.attributes):
            return False

        # comparing content
        return self.content == other.content

    def __str__(self):
        '''Returns a string representation of the relation, can be printed with
        monospaced fonts'''
        m_len = []  # Maximum lenght string
        for f in self.header.attributes:
            m_len.append(len(f))

        for f in self.content:
            col = 0
            for i in f:
                if len(i) > m_len[col]:
                    m_len[col] = len(i)
                col += 1

        res = ""
        for f in range(len(self.header.attributes)):
            res += "%s" % (self.header.attributes[f].ljust(2 + m_len[f]))

        for r in self.content:
            col = 0
            res += "\n"
            for i in r:
                res += "%s" % (i.ljust(2 + m_len[col]))
                col += 1

        return res

    # conversione relazione in formato csv
    def csv(self):  #lc
        '''
        Convert relation in a csv format:
        tabname
        attr1,attr2,attr3
        v11,v12,v13
        v21,v22,v23
        '''
        res = self.relname+"\n"
        for a in self.header.attributes:
            res += a+","
        res = res[:len(res)-1] # elimina , finale
        res += '\n'   
                    
        for r in self.content:
            for i in r:
                res += i+','
            res = res[:len(res)-1] # elimina , finale 
            res += '\n'    
        return res

    # sostituisce tutta l'estensione della relazione con i valori
    # contenuti nelle righe di text (in formato csv) [lc]
    def replace(self, text):
        #print('Relation:replace:\n TEXT=[',text,']')
        lines = text.split('\n')
        nl = len(lines)-1    # l'ultima riga e' vuota; perche'?
        self.content = set() # svuotamento
        for i in range(nl):  # Iterating rows
            a = lines[i].split(',')
            #print('Relation: A =',a)
            self.content.add(tuple(a)) # USARE insert per evitare ripetizioni
        return nl

    def update(self, expr, dic):
        '''Update, expr must be a valid boolean expression, can contain field names,
        constant, math operations and boolean ones.
        This operation will change the relation itself instead of generating a new one,
        updating all the tuples that make expr true.
        Dic must be a dictionary that has the form field name:value.
        Every kind of value will be converted into a string.
        Returns the number of affected rows.'''
        self._make_writable()
        affected = 0
        attributes = {}
        keys = list(dic.keys())  # List of headers to modify
        f_ids = self.header.getAttributesId(
            keys)  # List of indexes corresponding to keys

        # new_content=[] #New content of the relation
        for i in self.content:
            for j in range(len(self.header.attributes)):
                attributes[self.header.attributes[j]] = self._autocast(i[j])

            if eval(expr, attributes):  # If expr is true, changing the tuple
                affected += 1
                new_tuple = list(i)
                # Deleting the tuple, instead of changing it, so other
                # relations can still point to the same list without
                # being affected.
                self.content.remove(i)
                for k in range(len(keys)):
                    new_tuple[f_ids[k]] = str(dic[keys[k]])
                self.content.add(tuple(new_tuple))
        return affected

    def insert(self, values):
        '''Inserts a tuple in the relation.
        This function will not insert duplicate tuples.
        All the values will be converted in string.
        Will return the number of inserted rows.'''

        # Returns if tuple doesn't fit the number of attributes
        if len(self.header.attributes) != len(values):
            return 0

        self._make_writable()

        # Creating list containing only strings
        t = []
        for i in values:
            t.append(str(i))

        prevlen = len(self.content)
        self.content.add(tuple(t))
        return len(self.content) - prevlen

    def delete(self, expr):
        '''Delete, expr must be a valid boolean expression, can contain field names,
        constant, math operations and boolean ones.
        This operation will change the relation itself instead of generating a new one,
        deleting all the tuples that make expr true.
        Returns the number of affected rows.'''
        self._make_writable()
        attributes = {}
        affected = len(self.content)
        new_content = set()  # New content of the relation
        for i in self.content:
            for j in range(len(self.header.attributes)):
                attributes[self.header.attributes[j]] = self._autocast(i[j])

            if not eval(expr, attributes):
                affected -= 1
                new_content.add(i)
        self.content = new_content
        return affected

   
#=========================================================================

class Header (object):

    '''This class defines the header of a relation.
    It is used within relations to know if requested operations are accepted'''

    # Since relations are mutable we explicitly block hashing them
    __hash__ = None

    def __init__(self, attributes):
        '''Accepts a list with attributes' names. Names MUST be unique'''
        self.attributes = attributes

        for i in attributes:
            #if not is_valid_relation_name(i):
            #if not Rstring(i).is_valid_relation_name():
            if not Exp.is_valid_relation_name(i):
                raise Exception('"%s" is not a valid attribute name' % i)

    def __repr__(self):
        return "header(%s)" % (self.attributes.__repr__())

    def rename(self, old, new):
        '''Renames a field. Doesn't check if it is a duplicate.
        Returns True if the field was renamed, False otherwise'''

        if not Exp.is_valid_relation_name(new):
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
        '''Returns a list with numeric index corresponding to field's name'''
        res = []
        for i in param:
            for j in range(len(self.attributes)):
                if i == self.attributes[j]:
                    res.append(j)
        return res

if __name__ == "__main__":
    #import utils
    #from Types  import *  # per provare in locale 
    r = Relation('dipendente.csv')
    print('R=',r)
    r.delete('Cognome>\'G\'')
    print('R=',r)
    
    
