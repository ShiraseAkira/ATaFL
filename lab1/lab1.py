import sys
import numpy as np

def mealy_to_moore(mealy):
    original_states = mealy[0, 1:]
    signals = mealy[1:, 0]
    transitions = mealy[1:, 1:]

    states = {state: ("s"+str(i)+"/"+state).split('/')  \
        for i, state in enumerate(np.unique(mealy[1:, 1:]))}
    moore = np.empty([len(signals) + 2, len(states)+1], dtype='<U25')
    for i, v in enumerate(states.values()):
        moore[0][i+1] = v[2]
        moore[1][i+1] = v[0]
        original_state = v[1]
        original_state_column = list(original_states).index(original_state)
        original_transitions = transitions[:,original_state_column]
        for j in range(len(original_transitions)):
            moore[2+j][i+1] = states[original_transitions[j]][0]

    for i in range(len(signals)):
        moore[2+i][0] = signals[i]

    return moore

def moore_to_mealy(moore):
    state_output = moore[:2,1:].T
    state_map = {s[1]: s[1] + '/' + s[0] for s in state_output}
    mealy = moore[1:,:].astype('<U25')
    for i in range(1, len(mealy)):
        for j in range(1, len(mealy[1])):
            mealy[i][j] = state_map[mealy[i][j]]
    return mealy


expected_arg_count = 4
if len(sys.argv) != expected_arg_count:
    print('usage: python lab1.py "transform_type" "input_file" "output_file"')
    print('where "transform_type" is either "mealy-to-moore" or "moore-to-mealy"')
    print("example: python lab1.py mealy-to-moore input.csv output.csv")
    sys.exit()

transform_type = sys.argv[1]
if transform_type != "mealy-to-moore" and transform_type != "moore-to-mealy":
    print('unknown transformation type')
    print('"transform_type" is either "mealy-to-moore" or "moore-to-mealy"')
    sys.exit()

input = np.genfromtxt(sys.argv[2], delimiter=';', dtype=str)

if transform_type == 'mealy-to-moore':
    output = mealy_to_moore(input)
else:
    output = moore_to_mealy(input)

np.savetxt(sys.argv[3], output, delimiter=';', fmt='%s')