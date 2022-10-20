import sys
import numpy as np

def get_reachability_list(transitions, states):
    states_size = states.shape[0]
    state_is_reachable = np.full((states_size,), False) # Тут будем отслеживать, достижимо ли состояние
    state_is_reachable[0] = True # Считаем начальное состояние[состояние в первой колонке] всегда достижимым

    states_queue_to_check = [states[0]]
    while len(states_queue_to_check) != 0:
        state = states_queue_to_check.pop(0) # Берем верхний стэйт
        state_idx = np.where(states == state)
        for i in range(0, len(transitions)): # Проходим по его переходам, проверяя наши ли мы новые достижимые состояния
            new_state = transitions[i][state_idx]
            new_state_idx = np.where(states == new_state)
            if state_is_reachable[new_state_idx] == False: # Нашли новое достижимое состояние
                state_is_reachable[new_state_idx] = True
                states_queue_to_check.append(new_state)
    
    return state_is_reachable

def get_equivalent_classes(classes, states, transitions):
    state_transitions_dict = dict(zip(states, transitions.T))

    repeat = True
    while repeat:
        repeat = False

        state_transitions_in_equivalents = {}
        for state, state_transitions in state_transitions_dict.items():
            state_transition_in_equivalents = []
            for transition in state_transitions:
                for i, class_states in enumerate(classes.values()):
                    if transition in class_states:
                        state_transition_in_equivalents.append(str(i))
            state_transitions_in_equivalents[state] = "".join(state_transition_in_equivalents)

        new_classes = {}
        for i, value in enumerate(classes.values()):
            for state in value:
                new_class_name = str(i) + state_transitions_in_equivalents[state]
                if new_class_name in new_classes:
                    new_classes[new_class_name].append(state)
                else:
                    new_classes[new_class_name] = [state]

        if len(new_classes) != len(classes):
            classes = new_classes
            repeat = True

    return new_classes.values()


def mealy_minimize(mealy):
    original_states = mealy[0, 1:]
    transitions_with_outputs = mealy[1:, 1:]

    # Разделяем переходы с сигналами
    transitions = np.empty(transitions_with_outputs.shape, dtype='<U25') 
    signals = np.empty(transitions_with_outputs.shape, dtype='<U25')
    for i in range(0, len(transitions_with_outputs)):
        for j in range(0, len(transitions_with_outputs[0])):
            cell_content = transitions_with_outputs[i][j].split('/')
            transitions[i][j] = cell_content[0]
            signals[i][j] = cell_content[1]

    is_state_reachable = get_reachability_list(transitions, original_states)

    # выкидываем недостижимые состояния
    states = original_states[is_state_reachable]
    transitions = transitions.T
    transitions = transitions[is_state_reachable].T
    s = signals.T
    signals = s[is_state_reachable].T

    # Начальное разбиение на классы эквивалентности
    signals_str = list(map(lambda x: "".join(x), signals.T))
    classes = {}
    for i in range(len(signals_str)):
        if signals_str[i] in classes:
            classes[signals_str[i]].append(states[i])
        else:
            classes[signals_str[i]] = [states[i]]

    equivalent_classes = get_equivalent_classes(classes, states, transitions)

    unique_states = []
    new_states_replacement_dict = {}
    for i, equvalent_class in enumerate(equivalent_classes):
        unique_states.append(equvalent_class[0])
        for state in equvalent_class:
            new_states_replacement_dict[state] = 's' + str(i)

    is_state_left = np.full(states.shape, False)
    for state in unique_states:
        is_state_left[np.where(states == state)] = True

    # выкидываем упраздненные состояния
    states = states[is_state_left]
    transitions = transitions.T
    transitions = transitions[is_state_left].T
    s = signals.T
    signals = s[is_state_left].T

    # заменяем переходы в таблице на эквивалентные и добавляем обратно сигналы
    for i in range(len(transitions)):
        for j in range(len(states)):
            transitions[i][j] = new_states_replacement_dict[transitions[i][j]] + '/' + signals[i][j]
    # переименовываем состояния
    for i in range(len(states)):
        states[i] = new_states_replacement_dict[states[i]]

    # Соединяем состояния (строка индексов) с переходами/сигналами
    states_transitions = np.vstack((states,transitions))

    # Добавляем обратно колонку входных символов
    automata = np.vstack((mealy[:, 0], states_transitions.T)).T
    return automata


def moore_minimize(moore):
    original_states = moore[1, 1:]
    transitions = moore[2:, 1:]
    signals = moore[0, 1:]

    is_state_reachable = get_reachability_list(transitions, original_states)

    # выкидываем недостижимые состояния
    states = original_states[is_state_reachable]
    transitions = transitions.T
    transitions = transitions[is_state_reachable].T
    signals = signals[is_state_reachable]

    # Начальное разбиение на классы эквивалентности
    # signals_str = list(map(lambda x: "".join(x), signals.T))
    classes = {}
    for i in range(len(signals)):
        if signals[i] in classes:
            classes[signals[i]].append(states[i])
        else:
            classes[signals[i]] = [states[i]]

    equivalent_classes = get_equivalent_classes(classes, states, transitions)

    unique_states = []
    new_states_replacement_dict = {}
    for i, equvalent_class in enumerate(equivalent_classes):
        unique_states.append(equvalent_class[0])
        for state in equvalent_class:
            new_states_replacement_dict[state] = 's' + str(i)

    is_state_left = np.full(states.shape, False)
    for state in unique_states:
        is_state_left[np.where(states == state)] = True

    # выкидываем упраздненные состояния
    states = states[is_state_left]
    transitions = transitions.T
    transitions = transitions[is_state_left].T
    signals = signals[is_state_left]

    # заменяем переходы в таблице на эквивалентные
    for i in range(len(transitions)):
        for j in range(len(states)):
            transitions[i][j] = new_states_replacement_dict[transitions[i][j]]
    # переименовываем состояния
    for i in range(len(states)):
        states[i] = new_states_replacement_dict[states[i]]

    # Соединяем сигналы, состояния и переходы
    states_transitions = np.vstack((signals,states,transitions))

    # Добавляем обратно колонку входных символов
    automata = np.vstack((moore[:, 0], states_transitions.T)).T

    return automata


expected_arg_count = 4
if len(sys.argv) != expected_arg_count:
    print('usage: python lab1.py "automata_type" "input_file" "output_file"')
    print('where "automata_type" is either "mealy" or "moore"')
    print("example: python lab1.py mealy input.csv output.csv")
    sys.exit()

automata_type = sys.argv[1]
if automata_type != "mealy" and automata_type != "moore":
    print('unknown transformation type')
    print('"automata_type" is either "mealy" or "moore"')
    sys.exit()

input = np.genfromtxt(sys.argv[2], delimiter=';', dtype='<U25')

if automata_type == 'mealy':
    output = mealy_minimize(input)
else:
    output = moore_minimize(input)

np.savetxt(sys.argv[3], output, delimiter=';', fmt='%s')