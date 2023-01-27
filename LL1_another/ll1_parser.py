import sys

terminals = ["E","E'","T","T'","F"]

non_terminals = ["3","8","a","b","-","(",")","+","*","$"]

axiom = 'E'

rules = [
    {'id': 0, 'left': "E", 'right': ["T","E'"]},
    {'id': 1, 'left': "E'", 'right': ["+","T","E'"]},
    {'id': 2, 'left': "E'", 'right': []},
    {'id': 3, 'left': "T", 'right': ["F","T'"]},
    {'id': 4, 'left': "T'", 'right': ["*","F","T'"]},
    {'id': 5, 'left': "T'", 'right': []},
    {'id': 6, 'left': "F", 'right': ["-","F"]},
    {'id': 7, 'left': "F", 'right': ["(","E",")"]},
    {'id': 8, 'left': "F", 'right': ["a"]},
    {'id': 9, 'left': "F", 'right': ["b"]},
    {'id': 10, 'left': "F", 'right': ["3"]},
    {'id': 11, 'left': "F", 'right': ["8"]}
]

table = [
    # 3, 8, a, b, -, (, ), +, *, $
    [ 0, 0, 0, 0, 0, 0,-1,-1,-1,-1], # E
    [-1,-1,-1,-1,-1,-1, 2, 1,-1, 2], # E'
    [ 3, 3, 3, 3, 3, 3,-1,-1,-1,-1], # T
    [-1,-1,-1,-1,-1,-1, 5, 5, 4, 5], # T'
    [10,11, 8, 9, 6, 7,-1,-1,-1,-1], # F
]

def parse(input_path):
    
    with open(input_path, 'r') as i:
        input_string = i.readline()
    input_string += '$'
    input_position = 0

    for i in range(len(input_string)):
        if input_string[i] not in non_terminals:
            raise Exception('Unknown character "' + input_string[i] +\
                '" at position ' + str(i))

    stack = [axiom, '$']

    while len(stack) > 0:
        if input_position >= len(input_string):
            break
        # if input_position == 28:
        #     print(input_string[input_position], stack)
        head = stack.pop(0)
        # print(head)

        if head == input_string[input_position]:
            input_position += 1
            continue
        try:
            row = terminals.index(head)
        except:
            raise Exception('Expected "' + head + \
                '" but "' + input_string[input_position] + '" given at position ' + \
                str(input_position))

        col = non_terminals.index(input_string[input_position])

        id_rule = table[row][col]
        # print(id_rule, ':', rules[id_rule]['left'], \
        #     '->', ' '.join(rules[id_rule]['right']))
            
        if id_rule == -1:
            # print(head, input_string[input_position], stack)
            raise Exception('Unexpected character "' + input_string[input_position] +\
                '" at position ' + str(input_position))

        stack = rules[id_rule]['right'] + stack

    if len(stack) != 0 or len(input_string) != input_position:
        raise Exception('Expected "' + stack[0] + '" but string ended')

if __name__ == "__main__":
    expected_arg_count = 2
    if len(sys.argv) != expected_arg_count:
        print('usage: python ll1_parser.py "input_file"')
        print("example: python ll1_parser.py input.txt")
        sys.exit()

    try:
        parse(sys.argv[1])
        print('Whole file processed, content belongs to grammar')
    except Exception as e:
        print(e)