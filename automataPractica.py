from lista_ligada import LSL
import itertools as it

archivo = open("Texto.txt")

errores = []

contador = 0

pileLlave = []

typevar = -1
contador = 0
af_pr = {
    'S': {'b': 'B', 'l': 'L', 'i': 'I', 'c': 'C', 'd': 'D', 'f': 'F1', 'w': 'W'},
    'W': {'h': 'H'},
    'B': {'o': 'O1', 'l': 'L'},
    'O1': {'o': 'O2', 'n': 'N1', 'r': 'RE', 'u': 'U'},
    'L': {'o': 'O1', 'e': 'E1E2'},
    'O2': {'l': 'L'},
    'U': {'b': 'B'},
    'N1': {'t': 'T', 'g': 'G'},
    'R': {},
    'E1E2': {'a': 'AE'},
    'T': {},
    'G': {},
    'N2': {},
    'I': {'n': 'N1', 'f': 'F2', 'l': 'L'},
    'C': {'h': 'H'},
    'F1': {'o': 'O1'},
    'F2': {},
    'H': {'a': 'AE', 'i': 'I'},
    'D': {'o': 'O1'},
    'E': {},
    'AE': {'n': 'N2E', 'r': 'RE'},
    'N2E': {},
    'RE': {},
}
af_pr_acc = {'R', 'E1E2', 'T', 'G', 'N2', 'F2', 'N2E', 'RE'}

af_sep = {
    'SE0': {',': 'SE1', ';': 'SE1'},
    'SE1': {}
}
af_sep_acc = {'SE1'}

af_op = {
    'OP0': {'+': 'OP1', '-': 'OP2', '=': 'OP3', '!': 'OP5', '<': 'OP6', '>': 'OP7', '&': 'OP8', '^': 'OP9',
            '|': 'OP10',
            '~': 'OP11', '/': 'OP3', '%': 'OP3'},
    'OP1': {'+': 'OP14', '=': 'OP14'},
    'OP2': {'-': 'OP14', '=': 'OP14'},
    'OP3': {'=': 'OP14'},
    'OP5': {'=': 'OP14'},
    'OP6': {'=': 'OP14', '<': 'OP3'},
    'OP7': {'=': 'OP14', '>': 'OP16'},
    'OP8': {'=': 'OP14', '&': 'OP14'},
    'OP9': {'=': 'OP14', '^': 'OP14'},
    'OP10': {'=': 'OP14', '|': 'OP14'},
    'OP11': {},
    'OP14': {},
    'OP16': {'=': 'OP14', '>': 'OP3'},
}
af_op_acc = {'OP1', 'OP2', 'OP3', 'OP6', 'OP7', 'OP8', 'OP9', 'OP10', 'OP11', 'OP14', 'OP16'}

af_bool = {
    'BO0': {'t': 'BO1', 'f': 'BO5'},
    'BO1': {'r': 'BO2'},
    'BO2': {'u': 'BO3'},
    'BO3': {'e': 'BO4'},
    'BO4': {},
    'BO5': {'a': 'BO6'},
    'BO6': {'l': 'BO7'},
    'BO7': {'s': 'BO4'}
}
af_bool_acc = {'BO4'}


def accepts(transitions, initial, accepting, s):
    state = initial
    for c in s:
        state = transitions[state][c] if c in transitions[state].keys() else None
        if state is None:
            break
    return state in accepting


def accepts_id(s):
    state = 'ID0'
    accepting = {'ID1'}
    for c in s:
        transitions = {
            'ID0': {c.isalpha(): 'ID1', c == '$': 'ID1', c == '_': 'ID1'},
            'ID1': {c.isalpha(): 'ID1', c == '$': 'ID1', c == '_': 'ID1', c.isnumeric(): 'ID1'}
        }
        if True in transitions[state].keys():
            state = transitions[state][True]
        else:
            state = transitions[state][c] if c in transitions[state].keys() else None
            if state is None:
                break
        transitions.clear()
    return state in accepting


def check_type_variable():
    global tokenstuple
    if len(tokenstuple) > 1:
        state = 'TV1'
        for i in range(2):
            transitions = {
                'TV1': {
                    tokenstuple[i][0] == 'tipo' and tokenstuple[i][1] != 'if' and tokenstuple[i][1] != 'else': 'TV4',
                    tokenstuple[i][0] == 'variable': 'TV3',
                    tokenstuple[i][0] != 'tipo' and tokenstuple[i][0] != 'variable': 'TV3'},
                'TV2': {
                    tokenstuple[i][0] == 'tipo' and tokenstuple[i][1] != 'if' and tokenstuple[i][1] != 'else': 'TV2',
                    tokenstuple[i][0] == 'variable': 'TV2',
                    tokenstuple[i][0] != 'tipo' and tokenstuple[i][0] != 'variable': 'TV2'},
                'TV3': {
                    tokenstuple[i][0] == 'tipo' and tokenstuple[i][1] != 'if' and tokenstuple[i][1] != 'else': 'TV3',
                    tokenstuple[i][0] == 'variable': 'TV3',
                    tokenstuple[i][0] != 'tipo' and tokenstuple[i][0] != 'variable': 'TV3'},
                'TV4': {
                    tokenstuple[i][0] == 'tipo' and tokenstuple[i][1] != 'if' and tokenstuple[i][1] != 'else': 'TV1',
                    tokenstuple[i][0] == 'variable': 'TV2',
                    tokenstuple[i][0] != 'tipo' and tokenstuple[i][0] != 'variable': 'TV1'}
            }
            if True in transitions[state].keys():
                state = transitions[state][True]
            else:
                state = transitions[state][c] if c in transitions[state].keys() else None
                if state is None:
                    break
            transitions.clear()
        if state == 'TV2':
            return 1
        elif state == 'TV3':
            return 0
        else:
            return 0
    return -1


def accepts_const(s):
    state = 'C0'
    accepting = {'C2', 'C3', 'C7', 'C13', 'C14', 'C15'}
    for c in s:
        transitions = {
            'C0': {c.isnumeric(): 'C2', '.': 'C8', '+': 'C1', '-': 'C1', '"': 'C12', "'": 'C11'},
            'C1': {c.isnumeric(): 'C2', '.': 'C8'},
            'C2': {c.isnumeric(): 'C2', '.': 'C3'},
            'C3': {c.isnumeric(): 'C3'},
            'C6': {c.isnumeric(): 'C7'},
            'C7': {c.isnumeric(): 'C7'},
            'C8': {c.isnumeric(): 'C3'},
            'C11': {c.isnumeric(): 'C14', '.': 'C14', '+': 'C14', '-': 'C14', "'": 'C15', c.isalpha(): 'C14',
                    not c.isalnum() and c != "'": 'C14'},
            'C12': {c.isnumeric(): 'C12', '.': 'C12', '+': 'C12', '-': 'C12', '"': 'C13', c.isalpha(): 'C12',
                    not c.isalnum() and c != '"': 'C12'},
            'C13': {},
            'C14': {"'": 'C15'},
            'C15': {}
        }
        if True in transitions[state].keys():
            state = transitions[state][True]
        else:
            state = transitions[state][c] if c in transitions[state].keys() else None
            if state is None:
                break
        transitions.clear()
    return state in accepting


def add_token(wl):
    global tokenstuple
    global af_pr
    global af_op
    w = ''.join(wl)
    if accepts(af_pr, 'S', af_pr_acc, w):
        tokenstuple.append(('tipo', w))
    elif accepts(af_op, 'OP0', af_op_acc, w):
        tokenstuple.append(('operador', w))
    elif accepts(af_sep, 'SE0', af_sep_acc, w):
        tokenstuple.append(('separador', w))
    elif accepts(af_bool, 'BO0', af_bool_acc, w):
        tokenstuple.append(('boolean', w))
    elif accepts_const(w):
        tokenstuple.append(('constante', w))
    elif accepts_id(w):
        tokenstuple.append(('variable', w))


def token_to_LSL():
    global tokenstuple
    lsl = LSL()
    for i in tokenstuple:
        lsl.anadir_al_final(i[0], i[1])
    lsl_string = ""
    node = lsl.primero
    while node is not None:
        lsl_string += "["
        lsl_string += str(node.clase)
        lsl_string += ", "
        lsl_string += str(node.dato)
        lsl_string += "]"
        if node.liga is not None:
            lsl_string += " => "
        node = node.liga
    return lsl_string


def empty_list(lt):
    if lt:
        add_token(lt)
        lt.clear()


def isDelimiter(ch):
    if ch == ' ' or ch == '+' or ch == '-' or ch == '*' or \
            ch == '/' or ch == ',' or ch == ';' or ch == '>' or \
            ch == '<' or ch == '=' or ch == '(' or ch == ')' or \
            ch == '[' or ch == ']' or ch == '{' or ch == '}':
        return True
    return False


def isOperator(ch):
    return accepts(af_op, 'OP0', af_op_acc, ch)


def validIdentifier(ch):
    return accepts_id(ch)


def isKeyword(kw):
    if kw == "if" or kw == "else" or \
            kw == "while" or kw == "do" or \
            kw == "break" or \
            kw == "continue" or kw == "int" \
            or kw == "double" or kw == "float" \
            or kw == "return" or kw == "char" \
            or kw == "case" or kw == "boolean" \
            or kw == "sizeof" or kw == "long" \
            or kw == "short" or kw == "typedef" \
            or kw == "switch" or kw == "unsigned" \
            or kw == "void" or kw == "static" \
            or kw == "struct" or kw == "goto" \
            or kw == "true" or kw == "false":
        return True
    return False


def isBoolean(kw):
    if kw == "true" or kw == "false":
        return True
    return False


def isInteger(ch):
    if len(ch) == 0:
        return False
    for i in range(len(ch)):
        if ch[i].isdigit() == False or (ch == '-' and i > 0):
            return False
    return True


def isRealNumber(ch):
    hasDecimal = False
    if len(ch):
        return False
    for i in range(len(ch)):
        if not ch[i].isdigit() or (ch == '-' and i > 0):
            return False
        if ch[i] == '.':
            hasDecimal = True
    return hasDecimal


def parse(ch, lsl):
    assert isinstance(lsl, LSL)
    left = 0
    right = 0
    length = len(ch);
    while right < length - 1 and left <= right:
        if not isDelimiter(ch[right]):
            right += 1
        if isDelimiter(ch[right]) and left == right:
            if lsl.ultimo is not None and isOperator(ch[right]) and isOperator(lsl.ultimo.dato):
                lsl.ultimo.dato += ch[right]
            elif isOperator(ch[right]):
                lsl.anadir('operador', ch[right])
            elif ch[right] == ';':
                lsl.anadir('separador', ch[right])
            elif ch[right] == '(' or ch[right] == '{' or ch[right] == '}' or ch[right] == ')':
                lsl.anadir('delimitador', ch[right])
            right += 1
            left = right
        elif isDelimiter(ch[right]) and left != right \
                or (right == length and left != right):
            subStr = ch[left:right]
            if isBoolean(subStr):
                lsl.anadir('booleano', subStr)
            elif isKeyword(subStr):
                if subStr == 'while' or subStr == 'if' or subStr == 'for' or subStr == 'else':
                    lsl.anadir('palabra reservada', subStr)
                else:
                    lsl.anadir('tipo', subStr)
            elif isInteger(subStr):
                lsl.anadir('constante', subStr)
            elif isRealNumber(subStr):
                lsl.anadir('constante', subStr)
            elif validIdentifier(subStr) \
                    and not isDelimiter(ch[right - 1]):
                lsl.anadir('variable', subStr)
            left = right


def variableEscrita(palabra):
    estado = 'S'
    bandera = 0
    bandera2 = 0

    pile = []

    if len(palabra) == 1:
        estado = "¬"
        return estado

    palabra = palabra.rstrip()

    for i in range(len(palabra)):
        if estado == 'S':
            if palabra[i] == "i" and palabra[i + 1] == "f":
                estado = "X"
                bandera = 1
            elif palabra[i] == "w" and palabra[i + 1] == "h" and palabra[i + 2] == "i" and palabra[i + 3] == "l" and \
                    palabra[i + 4] == "e":
                estado = 'Z3'
                bandera = 2
            elif palabra[i] == "e" and palabra[i + 1] == "l" and palabra[i + 2] == "s" and palabra[i + 3] == "e":
                estado = "Z2"
            elif palabra[i].isalpha() or palabra[i] == "_" or palabra[i] == "$":
                estado = 'A'
            elif palabra[i] == " ":
                estado = 'S'
            elif palabra[i] == "{":
                pileLlave.append("{")
                estado = "¬"
            elif palabra[i] == ";":
                estado = "ERROR12"
            elif palabra[i] == "}":
                if pileLlave == []:
                    estado = "ERROR13"
                    return estado
                else:
                    pileLlave.pop()
                    estado = '¬'


            else:
                estado = 'ERROR1'
                return estado

        elif estado == 'A':
            if palabra[i].isalpha() or palabra[i] == "_" or palabra[i] == "$":
                estado = 'A'
            elif palabra[i].isdigit():
                estado = 'A'
            elif palabra[i] == " ":
                estado = 'B'
            elif palabra[i] == ",":
                estado = 'C'
            elif palabra[i] == "=":
                estado = 'D'
            elif palabra[i] == "+" or palabra[i] == "-" or palabra[i] == "*" or palabra[i] == "/":
                estado = 'P'
            elif palabra[i] == ";":
                estado = 'ERROR4'
            elif palabra[i] == ";":
                estado = '¬'
            else:
                estado = 'ERROR2'
                return estado

        elif estado == "B":
            if palabra[i] == " ":
                estado = "B"
            elif palabra[i] == ",":
                estado = 'C'
            elif palabra[i] == "=":
                estado = 'D'
            elif palabra[i] == "+" or palabra[i] == "-" or palabra[i] == "*" or palabra[i] == "/":
                estado = 'P'
            elif palabra[i] == ";":
                estado = "ERROR4"
            elif palabra[i] == ";":
                estado = "¬"
            elif palabra[i].isalpha() or palabra[i] == "_" or palabra[i] == "$":
                estado = "ERROR3"
            else:
                estado = "ERROR4"
                return estado

        elif estado == "C":
            if palabra[i].isalpha() or palabra[i] == "_" or palabra[i] == "$":
                estado = "A"
            elif palabra[i] == " ":
                estado = "C"
            else:
                estado = "ERROR2"
                return estado

        elif estado == "D":
            if palabra[i] == " ":
                estado = "D"
            elif palabra[i] == '"':
                estado = "E"
            elif palabra[i].isalpha() or palabra[i] == "_" or palabra[i] == "$":
                estado = "H"
            elif palabra[i].isdigit():
                estado = "J"
            elif palabra[i] == "(":
                pile.append("(")
                estado = "D"
            elif palabra[i] == "'":
                estado = "R"
            else:
                estado = "ERROR4"
                return estado

        elif estado == "E":
            if palabra[i] == '"':
                estado = "F"
            else:
                estado = "E"


        elif estado == "F":
            if palabra[i] == ";":
                estado = "¬"
            elif palabra[i] == ",":
                estado = "C"
            elif palabra[i] == " ":
                estado = "I"
            elif palabra[i] == "+" or palabra[i] == "-" or palabra[i] == "*" or palabra[i] == "/":
                estado = "G"
            elif palabra[i] == "=" or palabra[i] == "!":
                estado = "M"
            elif palabra[i] == "<" or palabra[i] == ">":
                estado = "O"
            elif palabra[i] == "&" or palabra[i] == "|":
                estado = "K"
            elif palabra[i] == ")" and bandera > 0 and len(pile) == 1:
                pile.pop()
                estado = "Z"

            else:
                estado = "ERROR5"
                return estado

        elif estado == "G":
            if palabra[i] == ' ':
                estado = "G"
            elif palabra[i] == '"':
                estado = "E"
            elif palabra[i].isalpha() or palabra[i] == "_" or palabra[i] == "$":
                estado = "H"
            elif palabra[i].isdigit():
                estado = "J"
            elif palabra[i] == "(":
                pile.append("(")
                estado = "G"
            elif palabra[i] == "'":
                estado = "R"
            else:
                estado = "ERROR6"
                return estado

        elif estado == "H":
            if palabra[i].isalpha() or palabra[i] == "_" or palabra[i] == "$":
                estado = "H"
            elif palabra[i].isdigit():
                estado = "H"
            elif palabra[i] == ' ':
                estado = "I"
            elif palabra[i] == "+" or palabra[i] == "-" or palabra[i] == "*" or palabra[i] == "/":
                estado = "G"
            elif palabra[i] == ",":
                estado = "S"
            elif palabra[i] == "=":
                estado = "M"
            elif palabra[i] == "=" or palabra[i] == "!":
                estado = "M"
            elif palabra[i] == "<" or palabra[i] == ">":
                estado = "O"
            elif palabra[i] == "&" or palabra[i] == "|":
                estado = "K"
            elif palabra[i] == ";":
                estado = "¬"

            elif palabra[i] == ")" and bandera > 0 and len(pile) == 1:
                bandera2 = 1
                pile.pop()
                estado = "Z"

            elif palabra[i] == ")":
                if pile == []:
                    estado = "ERROR13"
                    return estado

                else:
                    pile.pop()
                    estado = "H"
            else:
                estado = "ERROR7"
                return estado

        elif estado == "I":
            if palabra[i] == ' ':
                estado = "I"
            elif palabra[i] == "+" or palabra[i] == "-" or palabra[i] == "*" or palabra[i] == "/":
                estado = "G"
            elif palabra[i] == ",":
                estado = "S"
            elif palabra[i] == "&" or palabra[i] == "|":
                estado = "K"
            elif palabra[i] == "=" or palabra[i] == "!":
                estado = "M"
            elif palabra[i] == "!":
                estado = "M"
            elif palabra[i] == "<" or palabra[i] == ">":
                estado = "O"
            elif palabra[i] == ";":
                estado = "¬"
            elif palabra[i] == ")" and bandera > 0 and len(pile) == 1:
                pile.pop()
                estado = "Z"
            elif palabra[i] == ")":
                if pile == []:
                    estado = "ERROR13"
                    return estado
                else:
                    pile.pop()
                    estado = "I"
            else:
                estado = "ERROR2"
                return estado

        elif estado == "J":
            if palabra[i].isdigit():
                estado = "J"
            elif palabra[i] == ' ':
                estado = "I"
            elif palabra[i] == "+" or palabra[i] == "-" or palabra[i] == "*" or palabra[i] == "/":
                estado = "G"
            elif palabra[i] == ",":
                estado = "S"
            elif palabra[i] == "=" or palabra[i] == "!":
                estado = "M"
            elif palabra[i] == "<" or palabra[i] == ">":
                estado = "O"
            elif palabra[i] == "&" or palabra[i] == "|":
                estado = "K"
            elif palabra[i] == ";":
                estado = "¬"
            elif palabra[i] == ")" and bandera > 0 and len(pile) == 1:
                pile.pop()
                estado = "Z"
            elif palabra[i] == ")":
                if pile == []:
                    estado = "ERROR13"
                    return estado
                else:
                    pile.pop()
                    estado = "J"
            else:
                estado = "ERROR2"
                return estado

        elif estado == "K":
            if palabra[i] == palabra[i - 1]:
                estado = "L"
            elif palabra[i] == "=":
                estado = "D"

            else:
                estado = "ERROR8"
                return estado

        elif estado == "L":
            if palabra[i] == " ":
                estado = "D"
            elif palabra[i].isdigit():
                estado = "D"
            elif palabra[i].isalpha() or palabra[i] == "_" or palabra[i] == "$":
                estado = "D"
            elif palabra[i] == '"':
                estado = "E"
            elif palabra[i] == "(":
                pile.append("(")
                estado = "L"
            elif palabra[i] == "'":
                estado = "R"
            else:
                estado = "ERROR4"
                return estado

        elif estado == "M":
            if palabra[i] == "=":
                estado = "D"

            else:
                estado = "ERROR9"
                return estado


        elif estado == "O":
            if palabra[i] == "=":
                estado = "D"
            elif palabra[i].isalpha() or palabra[i] == "_" or palabra[i] == "$":
                estado = "H"
            elif palabra[i].isdigit():
                estado = "J"
            elif palabra[i] == " ":
                estado = "D"
            elif palabra[i] == '"':
                estado = "E"
            elif palabra[i] == "(":
                pile.append("(")
                estado = "O"
            else:
                estado = "ERROR4"
                return estado

        elif estado == "P":
            if palabra[i] == "=":
                estado = "D"
            elif palabra[i] == palabra[i - 1]:
                if palabra[i] == "+" or palabra[i] == "-":
                    estado = "Q"
            else:
                estado = "ERROR4"
                return estado

        elif estado == "Q":
            if palabra[i] == ";":
                estado = "¬"
            elif palabra[i] == " ":
                estado = "Q"

            else:
                estado = "ERROR10"
                return estado

        elif estado == "R":
            if palabra[i] == "'":
                estado = "U"
            else:
                estado = "T"

        elif estado == "T":
            if palabra[i] == "'":
                estado = "U"
            elif palabra[i] == ";":
                estado = "E"
                return estado
            else:
                estado = "ERROR11"
                return estado

        elif estado == "U":
            if palabra[i] == ";":
                estado = "¬"
            elif palabra[i] == ",":
                estado = "C"
            elif palabra[i] == " ":
                estado = "I"
            elif palabra[i] == "+" or palabra[i] == "-" or palabra[i] == "*" or palabra[i] == "/":
                estado = "G"
            elif palabra[i] == "=" or palabra[i] == "!":
                estado = "M"
            elif palabra[i] == "<" or palabra[i] == ">":
                estado = "O"
            elif palabra[i] == "&" or palabra[i] == "|":
                estado = "K"

            else:
                estado = "ERROR5"
                return estado

        elif estado == "X":
            if palabra[i] == "f":
                estado = "X"
            elif palabra[i] == " ":
                estado = "X"
            elif palabra[i] == "(":
                pile.append("(")
                estado = "D"
            else:
                estado = "ERROR14"
                return estado

        elif estado == "Z":

            if palabra[i] == " ":
                estado = "Z"
            elif palabra[i] == "{":
                pileLlave.append("{")
                estado = "¬"
            else:
                estado = "ERROR4"
                return estado

        elif estado == "Z2":

            if palabra[i] == "l":
                estado = "Z2"
            elif palabra[i] == "s":
                estado = "Z2"
            elif palabra[i] == "e":
                estado = "Z2"
            elif palabra[i] == " ":
                estado = "Z2"
            elif palabra[i] == "{":
                pileLlave.append("{")
                estado = "¬"
            else:
                estado = "ERROR14"
                return estado

        elif estado == "Z3":
            if palabra[i] == "h":
                estado = "Z3"
            elif palabra[i] == "i":
                estado = "Z3"
            elif palabra[i] == "l":
                estado = "Z3"
            elif palabra[i] == "e":
                estado = "Z3"
            elif palabra[i] == " ":
                estado = "Z3"
            elif palabra[i] == "(":
                pile.append("(")
                estado = "D"
            else:
                estado = "ERROR14"
                return estado



        elif estado == "¬":
            if palabra[i] == " ":
                estado = "¬"
            elif palabra[i] == "e" and palabra[i + 1] == "l" and palabra[i + 2] == "s" and palabra[i + 3] == "e":
                estado = "Z2"
            elif palabra[i] == "}":
                if pileLlave == []:
                    estado = "ERROR13"
                    return estado
                else:
                    pileLlave.pop()
                    estado = '¬'
            else:
                estado = "ERROR1"
                return estado

    if pile != []:
        estado = "ERROR13"

    return estado


for linea in archivo:
    contador = contador + 1

    est = variableEscrita(linea)
    symbols = {'+', '-', '~', '*', '/', '%', '<', '>', '=', '!', '&', '^'}
    tokenstuple = []
    l1 = []
    for c, nextc in it.zip_longest(linea, linea[1:], fillvalue=None):
        if c.isspace():
            empty_list(l1)
        elif c == ',' or c == ";":
            empty_list(l1)
            l1.append(c)
            add_token(l1)
            l1.clear()
        elif c in symbols:
            if len(l1) > 0 and l1[0] not in symbols:
                empty_list(l1)
            if nextc in symbols:
                l1.append(c)
            else:
                l1.append(c)
                add_token(l1)
                l1.clear()
        else:
            l1.append(c)
    if l1:
        add_token(l1)
    l1.clear()
    typevar = check_type_variable()
    if typevar == 1:
        linea = linea.split()
        linea1 = linea[1:]
        est = variableEscrita(''.join(str(x) for x in linea1))
    elif typevar == 0:
        est = variableEscrita(linea)

    if est == "ERROR1":
        fallo = "Linea " + str(contador) + ":El nombre de la variable empieza con un carácter invalido"
        errores.append(fallo)
    elif est == "ERROR2":
        fallo = "Linea " + str(contador) + ":Uso de signos prohibidos en el nombramiento de la variable"
        errores.append(fallo)
    elif est == "ERROR3":
        fallo = "Linea " + str(contador) + ":Uso de espacios en el nombramiento de la variable"
        errores.append(fallo)
    elif est == "ERROR4":
        fallo = "Linea " + str(contador) + ":Uso de signos prohibidos o falta de un elemento"
        errores.append(fallo)
    elif est == "E":
        fallo = "Linea " + str(contador) + ":Comillas sin cerrar"
        errores.append(fallo)
    elif est == "ERROR5":
        fallo = "Linea " + str(contador) + ":Uso de signos prohibidos despues del cierre de comillas"
        errores.append(fallo)
    elif est == "ERROR6":
        fallo = "Linea " + str(contador) + ":Uso de signos prohibidos despues de un operador aritmetico"
        errores.append(fallo)
    elif est == "ERROR7":
        fallo = "Linea " + str(contador) + ":Uso indebido de comillas"
        errores.append(fallo)
    elif est == "ERROR8":
        fallo = "Linea " + str(contador) + ":Uso de signos que no son el respectivo operador logico"
        errores.append(fallo)
    elif est == "ERROR9":
        fallo = "Linea " + str(contador) + ":Uso de signos que no son el respecto '=' "
        errores.append(fallo)
    elif est == "ERROR10":
        fallo = "Linea " + str(
            contador) + ":Signos invalidos despues de los operadores de incremento o decremento '++' / '--' "
        errores.append(fallo)
    elif est == "ERROR11":
        fallo = "Linea " + str(contador) + ":Cantidad de caracteres mayor de la permitida"
        errores.append(fallo)
    elif est == "ERROR12":
        fallo = "Linea " + str(contador) + ":Linea vacia"
        errores.append(fallo)
    elif est == "ERROR13":
        fallo = "Linea " + str(contador) + ":Linea desbalanceada"
        errores.append(fallo)
    elif est == "ERROR14":
        fallo = "Linea " + str(contador) + ":Uso de palabra reservada if"
        errores.append(fallo)
    elif est != "¬":
        fallo = "Linea " + str(contador) + ":Falta el operador de cierre ';'"
        errores.append(fallo)

if pileLlave != []:
    fallo = "Lista desbalanceada / Falta de '{' o '}' "
    errores.append(fallo)

for i in range(len(errores)):
    print(errores[i])

if len(errores) == 0:
    lsl = LSL()
    lsl_string = ''
    archivo.seek(0, 0)
    for linea in archivo:
        parse(linea, lsl)
    node = lsl.primero
    while node is not None:
        lsl_string += "[ "
        lsl_string += str(node.clase)
        lsl_string += " , "
        lsl_string += str(node.dato)
        lsl_string += " ]"
        if node.liga is not None:
            lsl_string += " => "
        node = node.liga

    print(lsl_string)
