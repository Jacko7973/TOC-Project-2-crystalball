# TM_utils_crystalball.py
# Theory of Computing Project 2

from enum import Enum
import csv
from collections import namedtuple, deque, defaultdict

### Enums

class TM_Status(Enum):
    UNKNOWN = "Unknown"
    ACCEPTED = "Accpeted"
    REJECTED = "Rejected"
    TIMEDOUT = "Timed Out"


### Type Declarations

TuringMachine = namedtuple("TuringMachine", ["name", "q", "sigma", "gamma", "q0", "qacc", "qrej", "delta"])
TuringMachineTransition = namedtuple("TuringMachineTransition", ["curr_state", "curr_char", "next_state", "write_char", "tape_direction"])
TuringMachineStep = namedtuple("TuringMachineStep", ["tm", "tape_left", "state", "tape_right", "depth"])
TuringMachineResult = namedtuple("TuringMachineResult", ["status", "depth", "transitions", "avg_nondeterminism"])


### Functions

def load_TM(path:str) -> TuringMachine:
    # Load the turing machine from a CSV file
    try:
        with open(path, "r") as f:
            reader = csv.reader(f, delimiter=",")
            name = next(reader)[0]
            q = frozenset(next(reader))
            sigma = frozenset(next(reader))
            gamma = frozenset(next(reader))
            q0 = next(reader)[0]
            qacc = next(reader)[0]
            qrej = next(reader)[0]

            delta = []
            for transition in reader:
                delta.append(TuringMachineTransition(*transition))

            # Create the TuringMachine object
            return TuringMachine(
                name=name,
                q=q,
                sigma=sigma,
                gamma=gamma,
                q0=q0,
                qacc=qacc,
                qrej=qrej,
                delta=frozenset(delta)
            )

    except FileNotFoundError:
        raise ValueError(f"[ERR] Unable to open file {path}")
    except (StopIteration, IndexError):
        raise ValueError(f"[ERR] Improperly formatted Turing Machine CSV: {path}")


def perform_transition(step:TuringMachineStep) -> list[TuringMachineStep]:
    # Single iteration of a transition on a turing machine
    outputs = []
    current_tape_char = step.tape_right[0] if len(step.tape_right) else "_"

    for transition in step.tm.delta:
        if transition.curr_state != step.state or transition.curr_char != current_tape_char: continue

        write_char = transition.write_char
        new_tape_left = step.tape_left
        new_tape_right = step.tape_right

        # Update the tapes based on the transition instructions
        if transition.tape_direction == "R":
            new_tape_left = new_tape_left + write_char
            new_tape_right = new_tape_right[1:] if len(new_tape_right) else ""
        elif transition.tape_direction == "L":
            new_tape_right = (new_tape_left[-1] if len(new_tape_left) else "") + write_char + (new_tape_right[1:] if len(new_tape_right) else "")
            new_tape_left = new_tape_left[:-1] if len(new_tape_left) else ""

        new_step = TuringMachineStep(step.tm, new_tape_left, transition.next_state, new_tape_right, step.depth + 1)
        outputs.append(new_step)

    # If a transition doesnt exist, transition to reject state
    if not outputs:
        outputs.append(TuringMachineStep(step.tm, step.tape_left, step.tm.qrej, step.tape_right, step.depth + 1))

    return outputs


def step_to_tuple(step:TuringMachineStep) -> tuple:
    # Format a step into a readable tuple
    return (step.tape_left, step.state, step.tape_right)


def init_TM(tm:TuringMachine, input:str) -> TuringMachineStep:
    # Setup turing machine on input string to begin simulating
    return TuringMachineStep(tm, "_", tm.q0, input + "_", 1)


def trace_TM(step:TuringMachineStep, depth_cap:int=1000, verbose:bool=True) -> TuringMachineResult:
    # Trace the steps of an NTM
    dq = deque([(step, None)])
    seen = {}
    options_counts = []
    max_depth = 0
    transitions = 0

    status = TM_Status.UNKNOWN

    while dq and status != TM_Status.ACCEPTED:

        s, prev = dq.popleft()

        # Don't processes repeat steps
        if s in seen:
            continue
        seen[s] = prev

        transitions += 1
        max_depth = max(max_depth, s.depth)
        if s.depth >= depth_cap:
            continue

        # Exit search if accept state found
        if s.state == s.tm.qacc:
            status = TM_Status.ACCEPTED
            break

        if s.state == s.tm.qrej:
            continue

        new_steps = perform_transition(s)
        options_counts.append(len(new_steps))

        for st in new_steps:
            dq.append((st, s))


    verbose and print(f"Maximum search tree depth: {max_depth}")
    verbose and print(f"Total transitions simulated: {transitions}")
    verbose and print()

    if status == TM_Status.ACCEPTED:
        # String accepted by turing machine
        trace = []
        prev_state = s
        while prev_state:
            trace.insert(0, prev_state)
            prev_state = seen[prev_state]

        verbose and print(f"String accepted in {s.depth} steps.")
        verbose and print("Configuration trace...")
        for st in trace:
            verbose and print(f"\t{step_to_tuple(st)}")

    else:
        if s.state == s.tm.qrej:
            # String rejected by turing machine
            status = TM_Status.REJECTED
            verbose and print(f"String rejected in {transitions} transitions.")
        else:
            # Simulation reached maximum depth
            status = TM_Status.TIMEDOUT
            verbose and print(f"Execution stopped after {transitions} transitions.")

    # Return the information about the search
    return TuringMachineResult(
        status=status,
        depth=max_depth,
        transitions=transitions,
        avg_nondeterminism=sum(options_counts) / len(options_counts)
        )


