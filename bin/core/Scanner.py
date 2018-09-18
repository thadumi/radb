# File: Scanner.py
# Date: 16 gen 16
# Note: lexycal analyzer for relational algebra expressions

NULLTOKEN = -1   # token 'nullo'

class Token:
      
    def __init__(self, t, s):
        self.type = t
        self.name = s

    def __str__(self):
        return "(" + str(self.type) + "," + str(self.name) + ")"


from sre_parse import Pattern, SubPattern, parse
from sre_compile import compile as sre_compile
from sre_constants import BRANCH, SUBPATTERN

class Scanner(object):

    def __init__(self, rules, flags=0):
        pattern = Pattern()
        pattern.flags = flags
        pattern.groups = len(rules) + 1

        self.rules = [name for name, _ in rules]
        self._scanner = sre_compile(SubPattern(pattern, [
            (BRANCH, (None, [SubPattern(pattern, [
                (SUBPATTERN, (group, parse(regex, flags, pattern))),
            ]) for group, (_, regex) in enumerate(rules, 1)]))
        ])).scanner
        self.at = [] # array dei token
        self.idx = 0 # indice su at del token corrente

    def scan(self, string, skip=False):
        sc = self._scanner(string)

        match = None
        for match in iter(sc.search if skip else sc.match, None):
            yield self.rules[match.lastindex - 1], match

        """
        if not skip and not match or match.end() < len(string):
            raise EOFError(match.end())
        """

    # imposta la stringa da analizzare
    def setString(self,s):
        self.at = []
        self.idx = 0
        #print('settata stringa in scanner--------->',s)
        for token, match in self.scan(s):
            #print('KTOK =',token,match.group())
            if token != 'SPACES':
                t = Token(token,match.group())
                #print('Scanner:TOK =',t)
                self.at.append(t)
        self.at.append(Token(NULLTOKEN,'null_token'))  # per chiudere
        #print('TOKENS =',at)

    # token corrente
    def curToken(self):
        return self.at[self.idx]

    # token prossimo
    def nextToken(self):
        if (self.idx+1) < len(self.at):
            return self.at[self.idx+1]
        else:
            return Token(NULLTOKEN,'null_token')

    # avanza al prossimo token e lo ritorna
    def getToken(self):
        if (self.idx+1) < len(self.at):
            self.idx += 1

#---- main ----
if __name__ == "__main__":
    #main()
    #s = '123 S     := 45.621  .89  join 67  <= lato76 \'Belluno76\' 45.2+7  x56 4.12'
    #s = 'T := R [Sigla1234 <=123] join [Sigla=\'BL\' and Abitanti<123456] S ljoin REPARTO minus x'
    s = 'selection [Reparto=\'P\']DIPENDENTE'
    #for token, match in scanner.scan(s):
    #    print((token, match.group()))

    regole = ([
               ('SPACES', r'\s+'),
               ('ADD', r'\+'),
               ('AND', r'and'),
               ('ORD', r'or'),
               ('NOT', r'not'),
               ('NOTEQUAL', r'!='),
               ('EQUAL', r'='),
               ('LESS', r'<'),
               ('GREATER', r'>'),
               ('LESSEQUAL', r'<='),
               ('GREATEREQUAL', r'>='),
               ('ASSIGN', r':='), #serve ancora? [17gen16]
               ('JOIN', r'join'),
               #('LEFTSQUARE', r'\['),
               #('RIGHTSQUARE', r'\]'),
               ('num', '[-+]?[0-9]*\.?[0-9]+'),  # non riconsce 67. SISTEMARE
               ('ident', r'[a-zA-Z][a-zA-Z0-9]*'),
               ('string', r'\'[a-zA-Z0-9]+\''),
               #('oprel', r'[=<>]+'),
               ('paren_open', r'\('),
               ('paren_close', r'\)'),
               #('ATTRIB', r'\[[\w,.=<>\']*\]'),
               ('ATTRIB', r'\[[a-zA-Z0-9()<>=!+\-\*/\', ]*\]'), #   [espressione]
               (NULLTOKEN, r'null_token')
             ])

    sc = Scanner(regole)
    sc.setString(s)
    #sc.setString('123!=34')
    i = 0
    while sc.curToken().type != NULLTOKEN:
        print('TOKEN =',sc.curToken())
        sc.getToken()
        i += 1
        if i==30:
            break
    print('finito')



