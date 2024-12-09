#!/usr/bin/env python3

class TwoStackTM:
    def __init__(self, name, states, alphabet, start_state, accept_state, reject_state, transitions):
        #constructor function
        self.name = name
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.transitions = transitions
        self.state = start_state
        self.stack1 = []
        self.stack2 = []
        self.step = 0

    def print_state(self):
        print(f"Step {self.step}: State {self.state}")
        print(f"Stack1: {' '.join(reversed(self.stack1))}")
        print(f"Stack2: {' '.join(reversed(self.stack2))}")

    def run(self, input_string):
        # Initialize stacks with input string
        self.stack1 = list(input_string[::-1])  # Push input string onto stack1
        self.stack2 = []
        print(f"Machine: {self.name}")
        print(f"Input: {input_string}")
        self.print_state()
        #loops through until state is not the accpet or reject state
        while self.state not in {self.accept_state, self.reject_state}:
            # Read current symbols or `None` if stack is empty
            # self.step = 1
            top1 = self.stack1.pop() if self.stack1 else 'E'
            top2 = self.stack2.pop() if self.stack2 else 'E'
            # Get transition rule
            key = (self.state, top1, top2)
            if key not in self.transitions:
                print(key)
                self.state = self.reject_state
                break
            #apply transitions
            new_state, new_top1, new_top2 = self.transitions[key]
            self.state = new_state
            # update stacks
            if new_top1 != 'E': self.stack1.append(new_top1)
            if new_top2 != 'E': self.stack2.append(new_top2)
            self.step += 1
            self.print_state()
        print(f"Final State: {self.state}")
        print("Accepted" if self.state == self.accept_state else "Rejected")
        return self.state

def main():
    #list of transitions
    transitions = {
        #('q0', '1', 'E'): ('q1', 'E', '1'),('q1', 'E', '1'): ('q_reject', 'E', 'E'),('q1', '1', '1'): ('q_accept', 'E', 'E'),('q0', '2', 'E'): ('q0', 'E', 'E'), ('q1', '2', '1'):('q1', 'E', '1')
        #('q0', 'a', 'E'): ('q1', 'E', 'a'),('q0', 'b', 'E'): ('q_reject', 'E', 'E'),('q1', 'b', 'a'): ('q_reject', 'E', 'E'),('q1', 'E', 'a'): ('q_accept', 'E', 'E'), ('q1', 'a', 'a'): ('q1', 'E', 'a')
        ('q0', 'a', 'E'): ('q_accept', 'E', 'E'),('q0', 'b', 'E'):('q_reject', 'E', 'E')
    }
    #set class attributes
    tm = TwoStackTM(
        name="Two-Stack TM",
        states={'q0', 'q_accept', 'q_reject'},
        alphabet={'a', 'E', 'b'},
        start_state='q0',
        accept_state='q_accept',
        reject_state='q_reject',
        transitions=transitions
    )
    tm.run("b")

if __name__ == "__main__":
    main()
