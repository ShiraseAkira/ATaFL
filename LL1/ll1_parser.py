import sys
# from lexer import *

# lexemes = [
#     {'type': 'operand', 'regex': 'id'},
#     {'type': 'operand', 'regex': 'a'},
#     {'type': 'operand', 'regex': 'b'},
#     {'type': 'operand', 'regex': '8'},
#     {'type': 'operand', 'regex': '3'},
#     {'type': 'operator', 'regex': '-'},
#     {'type': 'operator', 'regex': '\+'},
#     {'type': 'operator', 'regex': '\*'}
# ]

def read_table_file(file_path):
    keys = ['character', 'guide_set', 'move', 'error', 'pointer', 'stack', 'end']
    with open(file_path, 'r') as file:
        table = file.read().splitlines()

    for i in range(len(table)):
        table[i] = table[i].split(';')
        table[i][1] = table[i][1].split(',')
        table[i][4] = int(table[i][4]) - 1

        for j in [2,3,5,6]:
            if table[i][j] == 'False':
                table[i][j] = False
            else: 
                table[i][j] = True

        table[i] = dict(zip(keys, table[i]))
    return table

# def raise_error(table_row, lex):
#     raise Exception('Expected ' + str(table_row['guide_set']) + ', but "' + lex['lexem'] +\
#     '" given instead at (position) == ' + str(lex['position']))

def raise_error(table_row, input_string, string_position):
    raise Exception('Expected ' + str(table_row['guide_set']) + ', but "' + input_string[string_position] +\
    '" given instead at (position) == ' + str(string_position))

def parse(table, input_path):
    with open(input_path, 'r') as i:
        input_string = i.readline()
    
    string_position = 0
    table_row = 0
    stack = []

    while True:
        if table[table_row]['stack']:
            stack.append(table_row + 1)

        if input_string[string_position] in table[table_row]['guide_set']:

            # print('found')
            # print('character: ', input_string[string_position], ' ; stack: ', stack, ' ; table_row: ', table_row)
            # print('row: ', table[table_row])
            # print()
            if table[table_row]['move']:
                string_position += 1

            if string_position >= len(input_string):
                break

            if table[table_row]['pointer'] >= 0:
                table_row = table[table_row]['pointer']
            elif len(stack) > 0:
                table_row = stack.pop()
            else:
                raise Exception('Invalid string')
        else:
            # print('NOT found')
            # print('character: ', input_string[string_position], ' ; stack: ', stack, ' ; table_row: ', table_row)
            # print('row: ', table[table_row])
            # print()

            if table[table_row]['error']:
                raise_error(table[table_row], input_string, string_position)
            else:
                table_row += 1
                continue

    while len(stack) > 0:
        table_row = stack.pop()
        if '$' not in table[table_row]['guide_set']:
            raise Exception('Invalid string')






if __name__ == "__main__":
    expected_arg_count = 3
    if len(sys.argv) != expected_arg_count:
        print('usage: python ll1_parser.py "ll1_table_file" "input_file"')
        print("example: python ll1_parser.py ll1_table.csv input.txt")
        sys.exit()

    table = read_table_file(sys.argv[1])

    parse(table, sys.argv[2])
    try:
        print('Whole file processed, content belongs to grammar')
    except Exception as e:
        print(e)
        