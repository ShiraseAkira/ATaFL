from lexer import *

lexemes = [
    {'type': 'keyword', 'regex': 'prog +', 'descr': 'prog'},
    {'type': 'keyword', 'regex': 'id *', 'descr': 'id'},
    {'type': 'keyword', 'regex': 'begin +', 'descr': 'begin'},
    {'type': 'keyword', 'regex': 'end *', 'descr': 'end'},
    {'type': 'keyword', 'regex': 'var +', 'descr': 'var'},
    {'type': 'keyword', 'regex': 'int *', 'descr': 'int'},
    {'type': 'keyword', 'regex': 'float *', 'descr': 'float'},
    {'type': 'keyword', 'regex': 'bool *', 'descr': 'bool'},
    {'type': 'keyword', 'regex': 'string *', 'descr': 'string'},
    {'type': 'keyword', 'regex': 'read *', 'descr': 'read'},
    {'type': 'keyword', 'regex': 'write *', 'descr': 'write'},
    {'type': 'keyword', 'regex': 'num *', 'descr': 'num'},
    {'type': 'two_char_separator', 'regex': ':= *', 'descr': ':='},
    {'type': 'separator', 'regex': ': *', 'descr': ':'},
    {'type': 'separator', 'regex': '; *', 'descr': ';'},
    {'type': 'separator', 'regex': ', *', 'descr': ','},
    {'type': 'separator', 'regex': '\( *', 'descr': '('},
    {'type': 'separator', 'regex': '\) *', 'descr': ')'},
    {'type': 'space_separator', 'regex': ' +', 'descr': 'space(s)'},
    {'type': 'operators', 'regex': '\+ *', 'descr': '+'},
    {'type': 'operators', 'regex': '\* *', 'descr': '*'},
    {'type': 'operators', 'regex': '- *', 'descr': '-|(|id|num'},
    {'type': 'EOF', 'regex': '', 'descr': 'EOF'}
]

        # lex = {'token_id': self.lex_num,
        #        'lexem': self.input_single_line[self.position : self.position + lex_len],
        #        'lexem_id': lexemId,
        #        'line_num': position[0],
        #        'position': position[1]}

def raiseException(lexer, expected_lex_id, lex):
    position = '(' + str(lex['line_num'] + 1) + ', ' + str(lex['position']) + ')'
    raise Exception('Expected "' + lexemes[expected_lex_id]['descr'] + '", but got "' + lexemes[lex['lexem_id']]['descr'] +\
    '" instead at (line, position) == ' + position)

def raiseException2(lexer, expected_lex_id, lex):
    expected = []
    for id in expected_lex_id:
        expected.append(lexemes[id]['descr'])
    position = '(' + str(lex['line_num'] + 1) + ', ' + str(lex['position']) + ')'
    raise Exception('Expected "' + '|'.join(expected) + '", but got "' + lex['lexem'] +\
    '" instead at (line, position) == ' + position)

def prog(lexer):
    expected_lex_id = 0
    lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)

def id(lexer, lex={}):
    expected_lex_id = 1
    if not lex:
        lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)

def begin(lexer):
    expected_lex_id = 2
    lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)

def end(lexer, lex={}):
    expected_lex_id = 3
    if not lex:
        lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)

def eof(lexer):
    expected_lex_id = 22
    lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)

def var(lexer):
    expected_lex_id = 4
    lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)

def colon(lexer, lex={}):
    expected_lex_id = 13
    if not lex:
        lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)

def semicolon(lexer, lex={}):
    expected_lex_id = 14
    if not lex:
        lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)

def next_id_in_idlist(lexer, lex):
    expected_lex_id = 15
    if not lex:
        lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)

    id(lexer)
    return idlistplus(lexer)

def idlistplus(lexer):
    expected_lex_id = 15
    lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        return lex
    return next_id_in_idlist(lexer, lex)

def idlist(lexer):
    id(lexer)
    return idlistplus(lexer)    

def idtype(lexer):
    expected_lex_id = [5, 6, 7, 8]
    lex = lexer.getNextLex()
    if lex['lexem_id'] not in expected_lex_id:
        raiseException2(lexer, expected_lex_id, lex)

def varblock(lexer):
    var(lexer)
    lex = idlist(lexer)
    colon(lexer, lex)
    idtype(lexer)
    semicolon(lexer)


def left_paren(lexer):
    expected_lex_id = 16
    lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)
        
def right_paren(lexer, lex={}):
    expected_lex_id = 17
    if not lex:
        lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)

def read_statement(lexer, lex={}):
    expected_lex_id = 9
    if not lex:
        lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)

    left_paren(lexer)
    lex = idlist(lexer)
    right_paren(lexer, lex)
    semicolon(lexer)

def write_statement(lexer, lex={}):
    expected_lex_id = 10
    if not lex:
        lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)

    left_paren(lexer)
    lex = idlist(lexer)
    right_paren(lexer, lex)
    semicolon(lexer)


def assign_operator(lexer):
    expected_lex_id = 12
    lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)

def num(lexer, lex={}):
    expected_lex_id = 11
    if not lex:
        lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)

def assign_statement(lexer, lex={}):
    id(lexer, lex)
    assign_operator(lexer)
    lex = sum_st(lexer)
    semicolon(lexer, lex)


def sum_st(lexer, lex={}):
    lex = product(lexer)
    return sum_st_plus(lexer, lex)

def sum_st_plus(lexer, lex={}):
    expected_lex_id = 19
    if not lex:
        lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        return lex
    return next_term_in_sum(lexer)

def next_term_in_sum(lexer):
    lex = sum_st(lexer)
    return sum_st_plus(lexer, lex)


def factor(lexer, lex={}):
    expected_lex_id = [21, 16, 11, 1]
    if not lex:
        lex = lexer.getNextLex()
    if lex['lexem_id'] not in expected_lex_id:
        raiseException2(lexer, expected_lex_id, lex)
    if lex['lexem_id'] == 21:
        factor(lexer)
    elif lex['lexem_id'] == 16:
        lex = sum_st(lexer)
        right_paren(lexer, lex)
    elif lex['lexem_id'] == 11:
        num(lexer, lex)
    elif lex['lexem_id'] == 1:
        id(lexer, lex)

def product_plus(lexer, lex={}):
    expected_lex_id = 20
    if not lex:
        lex = lexer.getNextLex()
    if lex['lexem_id'] != expected_lex_id:
        return lex
    return next_factor_in_product(lexer)


def next_factor_in_product(lexer, lex={}):
    expected_lex_id = [21, 16, 11, 1]
    if not lex:
        lex = lexer.getNextLex()
    if lex['lexem_id'] not in expected_lex_id:
        raiseException2(lexer, expected_lex_id, lex)

    factor(lexer, lex)
    return product_plus(lexer)

 
def product(lexer, lex={}):
    factor(lexer, lex)
    return product_plus(lexer)

def statement(lexer, lex={}):
    if not lex:
        lex = lexer.getNextLex()
    expected_lex_id = [9, 10, 1]
    if lex['lexem_id'] not in expected_lex_id:
        raiseException2(lexer, expected_lex_id, lex)
    if lex['lexem_id'] == 9:
        read_statement(lexer, lex)
    elif lex['lexem_id'] == 10:
        write_statement(lexer, lex)
    elif lex['lexem_id'] == 1:
        assign_statement(lexer, lex)


def next_statement_in_statement_list(lexer, lex):
    expected_lex_id = [9, 10, 1]
    if not lex:
        lex = lexer.getNextLex()
    if lex['lexem_id'] not in expected_lex_id:
        raiseException(lexer, expected_lex_id, lex)

    statement(lexer, lex)
    return list_statement_plus(lexer)

def list_statement_plus(lexer):
    expected_lex_id = [9, 10, 1]
    lex = lexer.getNextLex()
    if lex['lexem_id'] not in expected_lex_id:
        return lex
    return next_statement_in_statement_list(lexer, lex)

def list_statement(lexer):
    statement(lexer)
    return list_statement_plus(lexer)    


def program(lexer):
    prog(lexer)
    id(lexer)
    varblock(lexer)
    begin(lexer)
    lex = list_statement(lexer)
    end(lexer, lex)
    eof(lexer)

if __name__ == "__main__":
    expected_arg_count = 2
    if len(sys.argv) != expected_arg_count:
        print('usage: python recursive_descent.py "input_file"')
        print("example: python recursive_descent.py input.txt")
        sys.exit()

    with open(sys.argv[1], 'r') as file:
        input_file = file.read().lower()

    lexer = Lexer(input_file, lexemes)

    try:
        program(lexer)
        print('All file processed, content belongs to grammar')
    except Exception as e:
        print(e)
