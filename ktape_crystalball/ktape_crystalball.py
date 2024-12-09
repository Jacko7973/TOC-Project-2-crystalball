#!/bin/env python3

import csv
import sys

# load the TM by parsing the machine file
def process_csv(filename):
    # Local variables for the data
    name = None
    tape = 1
    states = None
    sigma = None
    gamma = None
    start = None
    accept = None
    reject = None
    transitions = []

    with open(filename, 'r') as csvfile:
        automata = csv.reader(csvfile)
    
        first = next(automata)
        name = first[0]
        if len(first) == 2:
            tape = int(first[1])
        
        states = next(automata)
        sigma = next(automata)
        gamma = next(automata)
        start = next(automata)[0]
        accept = next(automata)[0]
        reject = next(automata)[0]

        for transition in automata:
            transitions.append(transition)
    
    return name, tape, states, sigma, gamma, start, accept, reject, transitions

# process the transitions (check for state and old characters)
def process_transitions(tape, transitions, start, accept, index, tapes, verbose=True):
    old = [] # list of old characters
    new = [] # list of new characters
    moves = [] # list of moves
    current = start
    num_transitions = 0
    step = 1

    verbose and print("Step 0:")
    verbose and print(f"Tape 1: {' ' + ''.join(tapes[0])}")
    for index_tape in range(1, tape):
        verbose and print(f"Tape {index_tape + 1}: {' ' + ''.join(tapes[index_tape])}")

    i = 0
    while i < len(transitions) and current != accept:
        transition = transitions[i]
        
        state = transition[0]
        new_state = transition[tape + 1]
            
        for char in range(1, tape + 1):
            old.append(transition[char])
        
        for char in range(2 + tape, 2 + 2 * tape):
            new.append(transition[char])

        for move in range(2 + 2 * tape, 2 + 3 * tape):
            moves.append(transition[move])

        # check if moving the head is valid
        if bool_move(state, current, old, tapes, index, accept):
            num_transitions += 1
            current = new_state

            # replace old characters with new characters
            replace_characters(old, new, tapes, index)
            # move the head (either left, right, or stay)
            move_tape(moves, index)
    
            verbose and print()
            verbose and print(f"Step {step}:")

            for index_tape in range(0, tape):
                head_index = index[index_tape]
                tape_string = ''.join(tapes[index_tape])
                
                verbose and print(f"Tape {index_tape + 1}: {tape_string[:head_index] + ' ' + tape_string[head_index:]}")

            i = 0
            step += 1
        else:
            i += 1

        old = [] # reset the list of old characters
        new = [] # reset the list of new characters
        moves = [] # reset the list of moves

    return current, num_transitions


def bool_move(state, current, old, tapes, index, accept):
    if current != state:
        return False

    if current == accept:
        return False

    for i, char in enumerate(old):
        if char == '*':
            continue
        elif char != tapes[i][index[i]]:
            return False
        else:
            continue

    return True
          

def replace_characters(old, new, tapes, index):
    for i, old_char in enumerate(old):
        if old_char == tapes[i][index[i]] or old_char == '*':
            if new[i] == '*':
                continue
            else:
                tapes[i][index[i]] = new[i]


def move_tape(moves, index):
    for i, move in enumerate(moves):
        if move == 'S':
            continue
        elif move == 'L':
            index[i] -= 1
        elif move == 'R':
            index[i] += 1
            

def main():
    if len(sys.argv) < 3:
        print("Usage: python ktape_turing.py <machine_file> <input_string> [<termination_flag>]")
        sys.exit(1)

    machine_file = sys.argv[1]
    tapes = [list(sys.argv[i]) for i in range(2, len(sys.argv) - 1)]
    
    termination_flag = int(sys.argv[len(sys.argv) - 1]) if len(sys.argv) > 3 else None

    # process the machine file
    name, tape, states, sigma, gamma, start, accept, reject, transitions = process_csv(machine_file)

    print(f"Machine name: {name}")
    input_strings = []
    
    for i in range(0, tape):
        input_string = ''.join(tapes[i])
        input_strings.append(input_string)
        
    print(f"Input string: {input_strings}")
    print()

    index = [0] * tape

    # process the transitions
    current, num_transitions = process_transitions(tape, transitions, start, accept, index, tapes)

    output_strings = []
    for i in range(0, tape):
        output_string = ''.join(tapes[i])
        output_strings.append(output_string)

    return (name, tape, input_strings, output_strings, current, num_transitions)
    
    
if __name__ == "__main__":
    main()
