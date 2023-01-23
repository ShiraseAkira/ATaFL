import sys
import numpy as np

special_regex_chars = ['(', ')', '|', '+', '*', '\\']
empty_transition = '@'

def get_input_dict(reg):
    input_chars = []
    next_char = ''
    for char in reg:
        if char in special_regex_chars:
            if next_char == '':
                if char == '\\':
                    next_char = char
                continue 
        if char == '\n':
            char = '\\n'
        if char not in input_chars:
            input_chars.append(char)
        next_char = ''
    input_chars.append(empty_transition)
    input_chars = np.asarray(input_chars, dtype='<U1024')
    return input_chars

def get_trivial_automata(char, input_chars):
    state_names = np.zeros(3, dtype=input_chars.dtype)
    state_names[1] = str(get_trivial_automata.counter) + "_s0"
    state_names[2] = str(get_trivial_automata.counter) + "_s1"

    transitions = np.zeros((2, input_chars.shape[0]), dtype=input_chars.dtype)
    char_idx = np.where(input_chars == char)[0][0]
    transitions[0][char_idx] = state_names[2]
    
    states_signals = np.vstack((input_chars, transitions))
    automata = np.vstack((state_names, states_signals.T))
    get_trivial_automata.counter += 1
    return automata

def add_final_state(automata):
    signals = np.zeros(automata.shape[1], dtype=automata.dtype)
    signals[-1] = 'F'
    return np.vstack((signals, automata))

def join_partial_automatas(partial_automatas):
    if len(partial_automatas) == 0:
        empty = np.zeros((2,2), dtype='<U1024')
        empty[-1][-1] = 's0'
        return empty
    if len(partial_automatas) == 1:
        return add_final_state(partial_automatas[0])
    automata = partial_automatas[0]
    signals = automata.T[0]
    empty_transition_idx = np.where(signals == empty_transition)[0][0]

    for i in range(1, len(partial_automatas)):
        next_automata = partial_automatas[i]
        next_automata_no_signals_transposed = next_automata.T[1:]
        next_automata_initial_state = next_automata_no_signals_transposed[0][0]

        if automata[empty_transition_idx][-1] == '':
            automata[empty_transition_idx][-1] = next_automata_initial_state
        else:
            automata[empty_transition_idx][-1] = automata[empty_transition_idx][-1] + ',' + next_automata_initial_state

        automata = np.vstack((automata.T,next_automata_no_signals_transposed)).T

    automata = add_final_state(automata)
    return automata

def closure_automata(automata):
    inputs = automata.T[0]
    empty_transition_idx = np.where(inputs == empty_transition)[0][0]

    new_initial_state_name = 'ic' + str(closure_automata.counter)
    new_initial_state = np.zeros(automata.shape[0], dtype=automata.dtype)
    new_initial_state[0] = new_initial_state_name
    old_initial_state_name = automata[0, 1]
    new_initial_state[empty_transition_idx] = old_initial_state_name

    new_final_state_name = 'fc' + str(closure_automata.counter)
    new_final_state = np.zeros(automata.shape[0], dtype=automata.dtype)
    new_final_state[0] = new_final_state_name
    new_initial_state[empty_transition_idx] = new_initial_state[empty_transition_idx] + ',' + new_final_state_name

    automata[empty_transition_idx][-1] = automata[empty_transition_idx][-1] + ',' + new_final_state_name


    result_automata = np.vstack((inputs, new_initial_state, automata.T[1:], new_final_state))

    closure_automata.counter += 1
    return result_automata.T

def patch_automata(automata, char):
    initial_state_name = automata[0, 1]

    inputs = automata.T[0]
    empty_transition_idx = np.where(inputs == empty_transition)[0][0]

    if automata[empty_transition_idx][-1] == '':
        automata[empty_transition_idx][-1] = initial_state_name
    else:
        automata[empty_transition_idx][-1] = automata[empty_transition_idx][-1] + ',' + initial_state_name
    
    if char == '*':
        automata = closure_automata(automata)

    return automata

def make_parallel_automatas(automata1, automata2):
    inputs = automata1.T[0]
    empty_transition_idx = np.where(inputs == empty_transition)[0][0]

    new_initial_state_name = 'i' + str(make_parallel_automatas.counter)
    new_initial_state = np.zeros(automata1.shape[0], dtype=automata1.dtype)
    new_initial_state[0] = new_initial_state_name
    new_final_state_name = 'f' + str(make_parallel_automatas.counter)
    new_final_state = np.zeros(automata1.shape[0], dtype=automata1.dtype)
    new_final_state[0] = new_final_state_name

    new_initial_state[empty_transition_idx] = automata1[0][1] + ',' + automata2[0][1]

    for automata in [automata1, automata2]:
        if automata[empty_transition_idx][-1] == '':
            automata[empty_transition_idx][-1] = new_final_state_name
        else:
            automata[empty_transition_idx][-1] = automata[empty_transition_idx][-1] + ',' + new_final_state_name

    automata1_no_inputs = automata1.T[1:]
    automata2_no_inputs = automata2.T[1:]

    result_automata = np.vstack((inputs, new_initial_state, automata1_no_inputs, automata2_no_inputs, new_final_state))

    make_parallel_automatas.counter += 1
    return result_automata.T

def regex_to_NDFA(reg, input_chars = []):
    if len(input_chars) == 0:
        input_chars = get_input_dict(reg)

    regex_position = 0
    partial_automatas = []
    parallel_next = False
    got_second_to_parallel = False
    while regex_position < len(reg):
        if reg[regex_position] == '+' or reg[regex_position] == '*':
            automata = partial_automatas.pop()
            automata = patch_automata(automata, reg[regex_position])
            partial_automatas.append(automata)
            regex_position += 1
            continue

        if parallel_next and got_second_to_parallel:
            automata2 = partial_automatas.pop()
            automata1 = partial_automatas.pop()
            automata = make_parallel_automatas(automata1, automata2)
            partial_automatas.append(automata)
            parallel_next = False
            got_second_to_parallel = False

        if reg[regex_position] == '(':
            depth = 1
            position = regex_position + 1
            while depth != 0 and position < len(reg):
                if reg[position] == '\\':
                    position += 2
                    continue

                if reg[position] ==  '(':
                    depth += 1
                
                if reg[position] ==  ')':
                    depth -= 1

                position += 1

            automata = regex_to_NDFA(reg[regex_position + 1:position - 1], input_chars)[1:]
            if parallel_next:
                # automata1 = partial_automatas.pop()
                # automata = make_parallel_automatas(automata1, automata)
                # parallel_next = False
                got_second_to_parallel = True
            partial_automatas.append(automata)
            regex_position = position
            continue
        
        if reg[regex_position] == '|':
            parallel_next = True
            regex_position += 1
            continue

        if reg[regex_position] == '\\':
            regex_position += 1

        if reg[regex_position] == '\n':
            automata = get_trivial_automata('\\n', input_chars)
        else:
            automata = get_trivial_automata(reg[regex_position], input_chars)
        if parallel_next:
            # automata1 = partial_automatas.pop()
            # automata = make_parallel_automatas(automata1, automata)
            # parallel_next = False
            got_second_to_parallel = True
        partial_automatas.append(automata)
        regex_position += 1

    if parallel_next and got_second_to_parallel:
        automata2 = partial_automatas.pop()
        automata1 = partial_automatas.pop()
        automata = make_parallel_automatas(automata1, automata2)
        partial_automatas.append(automata)
        parallel_next = False
        got_second_to_parallel = False

    NDFA = join_partial_automatas(partial_automatas)
    return NDFA


get_trivial_automata.counter = 0
make_parallel_automatas.counter = 0
closure_automata.counter = 0

if __name__ == "__main__":
    expected_arg_count = 3
    if len(sys.argv) != expected_arg_count:
        print('usage: python lab4.py "input_file" "output_file"')
        print("example: python lab3_2.py regex.txt output.csv")
        sys.exit()

    with open(sys.argv[1], 'r') as file:
        regex = file.read()

    output = regex_to_NDFA(regex)


    np.savetxt(sys.argv[2], output, delimiter=';', fmt='%s')