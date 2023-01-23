import sys
import numpy as np
from lab2 import *
from lab3_2 import *
from lab4 import *

if __name__ == "__main__":
    expected_arg_count = 3
    if len(sys.argv) != expected_arg_count:
        print('usage: python all_in_one.py "input_file" "output_file"')
        print("example: python all_in_one.py regex.txt output.csv")
        sys.exit()

    with open(sys.argv[1], 'r') as file:
        regex = file.read()

    automata = regex_to_NDFA(regex)
    automata = NDFA_to_DFA(automata, print_state_labels=False)
    automata = moore_minimize(automata)


    np.savetxt(sys.argv[2], automata, delimiter=';', fmt='%s')