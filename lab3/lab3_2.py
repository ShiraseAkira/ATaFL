import sys
import numpy as np

def get_eclosure_dict(empty_transitions):
    eclosure_dict = {}

    for state in empty_transitions:
        eclosure_dict[state[0]] = [state[0]]
        if len(state[1]) != 0:
            for transition in state[1].split(','):
                if transition not in eclosure_dict[state[0]]:
                    eclosure_dict[state[0]].append(transition)

    is_eclosure_buld = False
    while not is_eclosure_buld:
        is_eclosure_buld = True
        for key in eclosure_dict:
            for state in eclosure_dict[key]:
                for transition in eclosure_dict[state]:
                    if transition not in eclosure_dict[key]:
                        eclosure_dict[key].append(transition)
                        is_eclosure_buld = False

    for key in eclosure_dict:
        eclosure_dict[key].sort()

    return eclosure_dict

def build_DFA(ndfa_no_empty_symbols, eclosure_dict):
    dfa = np.zeros((ndfa_no_empty_symbols.shape[0] - 1, 1), dtype=ndfa_no_empty_symbols.dtype)
    for i, line in enumerate(ndfa_no_empty_symbols[1:]):
        dfa[i] = line[0]

    ndfa_state_signal_map = ndfa_no_empty_symbols[1::-1,1:]
    ndfa_original_states = ndfa_no_empty_symbols[1,1:]
    input_chars = ndfa_no_empty_symbols.T[0,2:]

    ndfa_no_indicies = ndfa_no_empty_symbols[2:,1:]
    initial_ndfa_state = ndfa_original_states[0]
    initial_dfa_state = eclosure_dict[initial_ndfa_state]

    states_to_process = [initial_dfa_state]
    states_done = []
    while len(states_to_process) != 0:
        dfa_state = states_to_process.pop(0)
        if dfa_state not in states_done:
            states_done.append(dfa_state)
            new_col = np.zeros((dfa.shape[0], 1), dtype=dfa.dtype)

            new_col[0, 0] = ''.join(dfa_state)
            for char_idx in range(len(input_chars)):
                new_state = []
                for original_state in dfa_state:
                    original_state_idx = np.where(ndfa_original_states == original_state)[0][0]
                    original_transitions = ndfa_no_indicies[char_idx, original_state_idx]
                    if len(original_transitions) != 0:
                        new_state.extend(original_transitions.split(','))
                
                if len(new_state) != 0:
                    state_with_eclosures = []
                    for target in new_state:
                        for state in eclosure_dict[target]:
                            if state not in state_with_eclosures:
                                state_with_eclosures.append(state)
                    state_with_eclosures.sort()
                    states_to_process.append(state_with_eclosures)
                    new_col[char_idx + 1, 0] = ''.join(state_with_eclosures)

            dfa = np.hstack((dfa, new_col))

    state_labels = {}
    for i in range(len(states_done)):
        state_labels[''.join(states_done[i])] = 'S' + str(i)

    for i in range(len(dfa)):
        for j in range(1, len(dfa[0])):
            if len(dfa[i, j]) != 0 :
                dfa[i, j] = state_labels[dfa[i, j]]

    signals = np.zeros((1, dfa.shape[1]), dtype=dfa.dtype)
    for i in range(len(states_done)):
        signal = ''
        for elem in states_done[i]:
            idx = np.where(ndfa_state_signal_map[0] == elem)[0][0]
            signal = signal + ndfa_state_signal_map[1, idx]
        signals[0,i + 1] = signal
    
    dfa = np.vstack((signals, dfa))
    
    return state_labels, dfa

def NDFA_to_DFA(ndfa, empty_char='e', print_state_labels=True):
    empty_char_row_idx_arr = np.where(ndfa[:,0] == empty_char)[0]
    if len(empty_char_row_idx_arr) == 0 :
        empty_char_transitions_row = np.zeros(ndfa[1,1:].shape, dtype=ndfa.dtype)
        empty_transitions = np.vstack((ndfa[1,1:], empty_char_transitions_row)).T
    else:
        empty_char_transitions_row = np.where(ndfa[:,0] == empty_char)[0][0]
        empty_transitions = np.vstack((ndfa[1,1:], ndfa[empty_char_transitions_row,1:])).T
        ndfa = np.delete(ndfa, empty_char_transitions_row, axis=0)
    eclosure_dict = get_eclosure_dict(empty_transitions)

    state_labels, dfa = build_DFA(ndfa, eclosure_dict)

    if print_state_labels:
        for key in state_labels:
            print(state_labels[key], ' = ', key)

    return dfa


if __name__ == "__main__":
    expected_arg_count = 3
    if len(sys.argv) != expected_arg_count:
        print('usage: python lab3_2.py "input_file" "output_file"')
        print("example: python lab3_2.py input.csv output.csv")
        sys.exit()

    input = np.genfromtxt(sys.argv[1], delimiter=';', dtype='<U25')

    output = NDFA_to_DFA(input)

    np.savetxt(sys.argv[2], output, delimiter=';', fmt='%s')