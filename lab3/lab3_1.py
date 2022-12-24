import sys
import numpy as np
from lab3_2 import *

TRANSIOTION_DELIMETER = ','
LEFT_INITITAL_STATE = '_'
RIGHT_FINAL_STATE = '_'

def get_atomic_rules(grammar):
    rules = list(map(lambda x: x.split(" -> "), grammar))
    rules = list(map(lambda x: [x[0], x[1].split(" | ")], rules))

    atomic_rules = []
    for rule in rules:
        for option in rule[1]:
            atomic_rules.append([rule[0], option])

    return np.array(atomic_rules)

def build_rule_array(atomic_rules, is_left_grammar):
    rules = list(map(lambda x: list(x), atomic_rules[:,1]))
    if is_left_grammar:
        for i, rule in enumerate(rules):
            if len(rule) == 1:
                rule.insert(0, LEFT_INITITAL_STATE)
            rule.append(atomic_rules[:,0][i])
    else:
        for i, rule in enumerate(rules):
            if len(rule) == 1:
                rule.append(RIGHT_FINAL_STATE)
            rule.insert(0, atomic_rules[:,0][i])

    return rules

def get_signals(NDFA, is_left_grammar):
    signals = np.zeros((1, NDFA.shape[1]), dtype=NDFA.dtype)

    if is_left_grammar:
        signals[0][-1] = 'F'
    else:
        for j in range(1, len(NDFA[0])):
            if RIGHT_FINAL_STATE in NDFA[0][j]:
                signals[0,j] = 'F'

    return signals

def build_NDFA(rules, is_left_grammar):    
    NDFA = np.zeros((1,1), dtype='<U25')     

    if is_left_grammar:
        states_queue = [LEFT_INITITAL_STATE]
    else:
        states_queue = [rules[0][0]]

    processed_states = []
    processed_inputs = []

    while len(states_queue) != 0:
        state = states_queue.pop(0)
        if state not in processed_states:
            NDFA = np.hstack((NDFA, np.zeros((NDFA.shape[0], 1), dtype=NDFA.dtype)))
            NDFA[0, -1] = state
            processed_states.append(state)
            for rule in rules:
                if rule[0] == state:
                    if rule[1] not in processed_inputs:
                        NDFA = np.vstack((NDFA, np.zeros((1, NDFA.shape[1]), dtype=NDFA.dtype)))
                        NDFA[-1, 0] = rule[1]
                        processed_inputs.append(rule[1])
                    row = np.where(NDFA[:,0] == rule[1])[0][0]
                    col = np.where(NDFA[0] == rule[0])[0][0]
                    if NDFA[row, col] == '':
                        NDFA[row, col] = rule[2]
                    else:
                        NDFA[row, col] = NDFA[row, col] + TRANSIOTION_DELIMETER + rule[2]

                    if (rule[2] not in states_queue) and (rule[2] not in processed_states):
                        states_queue.append(rule[2])

    signals = get_signals(NDFA, is_left_grammar)
    NDFA = np.vstack((signals, NDFA))

    return NDFA


def left_grammar_to_DFA(input):
    INITITAL_STATE = '_'
    atomic_rules = get_atomic_rules(input)
    rules = build_rule_array(atomic_rules, True)
    NDFA = build_NDFA(rules, True)

    return NDFA_to_DFA(NDFA)
   

def right_grammar_to_DFA(input):
    FINAL_STATE = '_'
    atomic_rules = get_atomic_rules(input)
    rules = build_rule_array(atomic_rules, False)
    NDFA = build_NDFA(rules, False)

    return NDFA_to_DFA(NDFA)

if __name__ == "__main__":
    expected_arg_count = 4
    if len(sys.argv) != expected_arg_count:
        print('usage: python lab3_1.py "grammar_type" "input_file" "output_file"')
        print('where "grammar_type" is either "left" or "right"')
        print("example: python lab3_1.py left left-side-grammar.txt output.csv")
        sys.exit()

    grammar_type = sys.argv[1]
    if grammar_type != "left" and grammar_type != "right":
        print('unknown transformation type')
        print('"grammar_type" is either "left" or "right"')
        sys.exit()

    with open(sys.argv[2]) as file:
        input = file.read().splitlines()

    if grammar_type == 'left':
        output = left_grammar_to_DFA(input)
    else:
        output = right_grammar_to_DFA(input)

    np.savetxt(sys.argv[3], output, delimiter=';', fmt='%s')