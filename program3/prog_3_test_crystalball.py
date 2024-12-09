#!/usr/bin/env python3

import csv
import re
import unittest
from prog_3_crystalball import TwoStackTM

def parse_transitions(csv_filename):
    # Read the CSV file and parse transitions
    transitions_list = []

    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Combine all columns in the row
            full_row = ''.join(row)

            # Use regex to parse the transitions
            transition_pattern = r"\('(.*?)'\s*,\s*'(.*?)'\s*,\s*'(.*?)'\)\s*:\s*\('(.*?)'\s*,\s*'(.*?)'\s*,\s*'(.*?)'\)"

            # Find all transitions
            transitions = re.findall(transition_pattern, full_row)

            # Create transition dictionary
            transition_dict = {}
            for trans in transitions:
                key = (trans[0], trans[1], trans[2])
                value = (trans[3], trans[4], trans[5])
                transition_dict[key] = value

            # Extract states and alphabet
            states = set()
            alphabet = set()

            for trans in transitions:
                states.update([trans[0], trans[3], trans[1], trans[2], trans[4], trans[5]])
                alphabet.update([trans[1], trans[2], trans[4], trans[5]])

            # Remove 'E' (epsilon) from alphabet if present
            alphabet.discard('E')

            # Remove 'q_accept' and 'q_reject' from states if present
            states.discard('q_accept')
            states.discard('q_reject')

            # Add the parsed transitions to the list
            transitions_list.append({
                'transitions': transition_dict,
                'states': sorted(list(states)),
                'alphabet': sorted(list(alphabet))
            })

    return transitions_list

class TestTwoStackTM(unittest.TestCase):
    def setUp(self):
        # Define hardcoded transitions
        self.transitions = {('q0', 'a', 'E'): ('q1', 'E', 'a'),('q0', 'b', 'E'): ('q_reject', 'E', 'E'),('q1', 'b', 'a'): ('q_reject', 'E', 'E'),('q1', 'E', 'a'): ('q_accept', 'E', 'E'), ('q1', 'a', 'a'): ('q1', 'E', 'a')}
        # Initialize TwoStackTM instance
        self.tm = TwoStackTM(
            name="Two-Stack TM",
            states=['q0', 'q1', 'q2', 'q_accept', 'q_reject'],
            alphabet=['a', 'b', 'E'],
            start_state='q0',
            accept_state='q_accept',
            reject_state='q_reject',
            transitions=self.transitions
        )

    def test_valid_input(self):
        input_string = "aabb"
        result = self.tm.run(input_string)
        f.write(f"{self.tm.name},{input_string},{result},{self.tm.step},{self.tm.step},1\n")
        self.assertEqual(result, 'q_reject')

    def test_invalid_input(self):
        input_string = "ab"
        result = self.tm.run(input_string)
        f.write(f"{self.tm.name},{input_string},{result},{self.tm.step},{self.tm.step},1\n")
        self.assertEqual(result, 'q_reject')

    def test_empty_input(self):
        input_string = ""
        result = self.tm.run(input_string)
        f.write(f"{self.tm.name},{input_string},{result},{self.tm.step},{self.tm.step},1\n")
        self.assertEqual(result, 'q_reject')

    def test_reject_start_with_b(self):
        input_string = "bba"
        result = self.tm.run(input_string)
        self.assertEqual(result, 'q_reject')
        f.write(f"{self.tm.name},{input_string},{result},{self.tm.step},{self.tm.step},1\n")
    
    def test_valid_input(self):
        input_string = "aaa"
        result = self.tm.run(input_string)
        f.write(f"{self.tm.name},{input_string},{result},{self.tm.step},{self.tm.step},1\n")
        self.assertEqual(result, 'q_accept')

    def test_invalid_input(self):
        input_string = "a"
        result = self.tm.run(input_string)
        f.write(f"{self.tm.name},{input_string},{result},{self.tm.step},{self.tm.step},1\n")
        self.assertEqual(result, 'q_accept')

    def test_empty_input(self):
        input_string = "aaa"
        result = self.tm.run(input_string)
        f.write(f"{self.tm.name},{input_string},{result},{self.tm.step},{self.tm.step},1\n")
        self.assertEqual(result, 'q_accept')

    def test_reject_start_with_b(self):
        input_string = "aaaaaa"
        result = self.tm.run(input_string)
        f.write(f"{self.tm.name},{input_string},{result},{self.tm.step},{self.tm.step},1\n")
        self.assertEqual(result, 'q_accept')

if __name__ == '__main__':
    with open("output_program_3_crystalball.csv", "w") as f:
        unittest.main()

'''
def test_two_stack_tm(csv_filename):
    # Parse transitions from CSV
    transitions_list = parse_transitions(csv_filename)

    # Define accepted and rejected inputs for testing
    accepted_inputs = [
        ["1111111", "11", "1211", "1122", "12211"],
        ["a", "aa", "aaa", "abab", "ab"],
        ["babab", "aaab", "b", "bbb", "ab"],
        ["a", "aaaa", "aaa", "aa", "aaaaaaaaa"]
    ]

    rejected_inputs = [
        ["1", "2", "", "21", "12"],
        ["b", "bababa", "bb", "baa", "bbb"],
        ["a", "", "aaaa", "aaaaaaaa", "aaaaaaaaaaaaaaa"],
        ["ababa", "aaaab", "b", "baa", ""]
    ]

    transition = [{('q0', '1', 'E'): ('q1', 'E', '1'),('q1', 'E', '1'): ('q_reject', 'E', 'E'),('q1', '1', '1'): ('q_accept', 'E', 'E'),('q0', '2', 'E'): ('q0', 'E', 'E'), ('q1', '2', '1'):('q1', 'E', '1'), ('q0', 'E', 'E'):('q_reject', 'E','E')},
            {('q0', 'a', 'E'): ('q_accept', 'E', 'E'),('q0', 'b', 'E'):('q_reject', 'E', 'E')},
            {('q0', 'b', 'E'): ('q_accept', 'E', 'E'),('q0', 'b', 'a'): ('q_accept', 'E', 'E'),('q0', 'a', 'a'): ('q0', 'E', 'a'),('q0', 'a', 'E'): ('q0', 'E', 'a')},
            {('q0', 'a', 'E'): ('q1', 'E', 'a'),('q0', 'b', 'E'): ('q_reject', 'E', 'E'),('q1', 'b', 'a'): ('q_reject', 'E', 'E'),('q1', 'E', 'a'): ('q_accept', 'E', 'E'), ('q1', 'a', 'a'): ('q1', 'E', 'a')}]

    names = [".*1+.*1+", "a^.*", ".*b.*", "a+"]
    state = [{'q0','q1','q_reject','q_accept'},{'q0','q_accept','q_reject'},{'q0','q1','q_reject','q_accept'},{'q0','q1','q_reject','q_accept'}] 
    alphabets = [{'1','2','E'},{'a','b','E'},{'b','a','E'},{'a','b','E'}]
    # Test each set of transitions
    for i, trans_set in enumerate(transition, 1):
        print(f"\n--- Transition Set {i} ---")
        tm = TwoStackTM(
            name=names[i-1],
            states=state[i-1],
            alphabet=alphabets[i-1],
            start_state='q0',
            accept_state='q_accept',
            reject_state='q_reject',
            transitions=transition[i-1]
            )
        
        tm = TwoStackTM(
            name=f"Two-Stack TM Test Set {i}",
            states=set(trans_set['states'] + ['q0', 'q_accept', 'q_reject']),
            alphabet=set(trans_set['alphabet'] + ['E']),
            start_state='q0',
            accept_state='q_accept',
            reject_state='q_reject',
            transitions=trans_set['transitions']
        )
        # Test accepted inputs
        for input_string in accepted_inputs[i - 1]:
            result = tm.run(input_string)
            print(f"Input: {input_string} -> Expected: q_accept, Actual: {result}, "
                  f"Result: {'PASSED' if result == 'q_accept' else 'FAILED'}")

        # Test rejected inputs
        for input_string in rejected_inputs[i - 1]:
            result = tm.run(input_string)
            print(f"Input: {input_string} -> Expected: q_reject, Actual: {result}, "
                  f"Result: {'PASSED' if result == 'q_reject' else 'FAILED'}")

if __name__ == "__main__":
    test_two_stack_tm('transitions.csv')
'''
