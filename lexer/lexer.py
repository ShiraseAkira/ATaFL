import sys
import numpy as np
from .lab2 import *
from .lab3_2 import *
from .lab4 import *

# lexemes = [
#     {'type': 'keyword', 'regex': '(prog +)|(id *)|(begin +)|(end)|(var +)|(int *)|(float *)|(bool *)|(string *)|(read *)|(write *)|(num *)'},
#     {'type': 'two_char_separator', 'regex': ':= *'},
#     {'type': 'separator', 'regex': '(: *)|(; *)|(, *)|(\( *)|(\) *)'},
#     {'type': 'space_separator', 'regex': ' +'},
#     {'type': 'operators', 'regex': '(\+ *)|(\* *)|(- *)'}
# ]






lexemes = [
    {'type': 'keyword', 'regex': 'prog +'},
    {'type': 'keyword', 'regex': 'id *'},
    {'type': 'keyword', 'regex': 'begin +'},
    {'type': 'keyword', 'regex': 'end *'},
    {'type': 'keyword', 'regex': 'var +'},
    {'type': 'keyword', 'regex': 'int *'},
    {'type': 'keyword', 'regex': 'float *'},
    {'type': 'keyword', 'regex': 'bool *'},
    {'type': 'keyword', 'regex': 'string *'},
    {'type': 'keyword', 'regex': 'read *'},
    {'type': 'keyword', 'regex': 'write *'},
    {'type': 'keyword', 'regex': 'num *'},
    {'type': 'two_char_separator', 'regex': ':= *'},
    {'type': 'separator', 'regex': ': *'},
    {'type': 'separator', 'regex': '; *'},
    {'type': 'separator', 'regex': ', *'},
    {'type': 'separator', 'regex': '\( *'},
    {'type': 'separator', 'regex': '\) *'},
    {'type': 'space_separator', 'regex': ' +'},
    {'type': 'operators', 'regex': '\+ *'},
    {'type': 'operators', 'regex': '\* *'},
    {'type': 'operators', 'regex': '- *'}
]

class Lexer:
    def __init__(self, input_text, lexemes) -> None:
        self.input_text = input_text
        self.input_single_line = input_text.replace("\n", " ")
        self.position = 0
        self.lexemes = lexemes

        for i in range(len(self.lexemes)):
            automata = regex_to_NDFA(self.lexemes[i]['regex'])
            automata = NDFA_to_DFA(automata, print_state_labels=False)
            automata = moore_minimize(automata)
            self.lexemes[i]['automata'] = automata

        self.lex_num = 0

    def getPosition(self):
        passed_string = self.input_text[:self.position]
        line = passed_string.count('\n')
        last_line_start = passed_string.rfind('\n')
        if last_line_start == -1:
            last_line_start = 0
        position = self.position - last_line_start
        return (line, position)
        
    def isDone(self):
        return self.position >= len(self.input_single_line)

    def findLex(self, automata):
        def getTransition():
            state_idx = np.where(states == current_state)[0][0]
            state_transitions = transitions_t[state_idx]
            transition_idx = np.where(input_alphabet == string_to_look[characters_processed])[0][0]
            transition = state_transitions[transition_idx]
            return transition

        string_to_look = self.input_single_line[self.position:]
        signals = automata[0][1:]

        automata_w_o_signals = automata[1:]
        states = automata_w_o_signals[0][1:]

        automata_w_o_signals_states = automata_w_o_signals[1:]
        automata_wo_sig_st_t = automata_w_o_signals_states.T
        input_alphabet = automata_wo_sig_st_t[0]

        transitions_t = automata_wo_sig_st_t[1:]

        current_state = states[0]
        characters_processed = 0

        while characters_processed < len(string_to_look) and (string_to_look[characters_processed] in input_alphabet) and getTransition() != '':
            current_state = getTransition()
            characters_processed += 1

        state_idx = np.where(states == current_state)[0][0]
        isFound = signals[state_idx] == 'F'

        return isFound, characters_processed

    def getNextLex(self):
        isFound = False
        lexemId = 0
        while lexemId < len(self.lexemes):
            isFound, lex_len = self.findLex(self.lexemes[lexemId]['automata'])
            if isFound:
                break
            lexemId += 1

        position = self.getPosition()

        if not isFound:
            raise Exception('Unknown token at (line, position) == ' + str(position))

        lex = {'token_id': self.lex_num,
               'lexem': self.input_single_line[self.position : self.position + lex_len],
               'lexem_id': lexemId,
               'line_num': position[0],
               'position': position[1]}

        self.position += lex_len
        self.lex_num += 1
        return lex

if __name__ == "__main__":
    expected_arg_count = 2
    if len(sys.argv) != expected_arg_count:
        print('usage: python lexer.py "input_file"')
        print("example: python lexer.py input.txt")
        sys.exit()

    with open(sys.argv[1], 'r') as file:
        input_file = file.read().lower()

    lexer = Lexer(input_file, lexemes)

    while not lexer.isDone():
        lex = lexer.getNextLex()
        print(lex)
