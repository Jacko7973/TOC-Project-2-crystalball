#!/usr/bin/env python3

# traceTM_crystalball.py
# Theory of Computing Project 2

import argparse
import sys

from TM_utils_crystalball import TuringMachine, TuringMachineStep, TuringMachineResult, load_TM, perform_transition, init_TM, trace_TM


def main():
    parser = argparse.ArgumentParser(
                    prog='traceTM_crystalball',
                    description='Trace the execution of a Nondeterministic Turing Machine',
                )
    parser.add_argument("file", help="File name of CSV Turing Machine")
    parser.add_argument("string", help="Input string to Turing Machine")
    parser.add_argument("--max-depth", type=int, default=1000, required=False, help="Maximum search tree depth (default=1000)")

    # Parse command line arguments
    args = parser.parse_args(sys.argv[1:])

    # Set up and display information about machine
    tm = load_TM(args.file)
    print(f"Machine name: '{tm.name}'")
    print(f"Input string: '{args.string}'")
    print(f"{' Running ':=^40}")

    # Run the simulation in verbose mode
    start_step = init_TM(tm, args.string)
    trace_TM(start_step, args.max_depth)


if __name__ == "__main__":
    main()
