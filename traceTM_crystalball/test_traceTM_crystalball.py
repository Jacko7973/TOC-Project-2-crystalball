#!/usr/bin/env python3

# test_traceTM_crystalball.py
# Theory of Computing Project 2

import csv

from TM_utils_crystalball import TuringMachine, TuringMachineResult, TM_Status, load_TM, init_TM, trace_TM


### Constants

TESTS = (
    ("aplus.csv", "aaaaa", TM_Status.ACCEPTED),
    ("aplus.csv", "aaaab", TM_Status.REJECTED),
    ("aplus.csv", "aaaaaaaaaaaaaaaaaa", TM_Status.ACCEPTED),
    ("aplus.csv", "baa", TM_Status.REJECTED),
    ("aplus.csv", "a", TM_Status.ACCEPTED),
    ("aplus.csv", "aaacaa", TM_Status.REJECTED),

    ("equal_01s_DTM.csv", "01", TM_Status.ACCEPTED),
    ("equal_01s_DTM.csv", "1010", TM_Status.ACCEPTED),
    ("equal_01s_DTM.csv", "10101", TM_Status.REJECTED),
    ("equal_01s_DTM.csv", "11111111110000000000", TM_Status.ACCEPTED),

    ("equal_01s.csv", "01", TM_Status.ACCEPTED),
    ("equal_01s.csv", "1010", TM_Status.ACCEPTED),
    ("equal_01s.csv", "10101", TM_Status.REJECTED),
    ("equal_01s.csv", "11111111110000000000", TM_Status.ACCEPTED),
)

HEADERS = ("Machine Name", "Input String", "Result", "Max Depth", "# Transitions", "Average Nondeterminism", "Comments")


def test_individual(testcase:tuple) -> tuple:

    path, string, expected = testcase

    tm = load_TM(path)
    start_state = init_TM(tm, string)
    result = trace_TM(start_state, verbose=False)

    assert result.status == expected

    return result



def test_all(output_filename:str):

    if not output_filename.endswith(".csv"):
        output_filename = output_filename + ".csv"

    records = []
    for i, testcase in enumerate(TESTS, 1):
        try:
            result = test_individual(testcase)
            record = (testcase[0], testcase[1], result.status.value, result.depth, result.transitions, round(result.avg_nondeterminism, 3), "")
            records.append(record)
        except AssertionError:
            print(f"[INFO] Test Failed... (test={i})")
            return
        
    with open(output_filename, "w") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(HEADERS)
        for record in records:
            writer.writerow(record)
    
    print("[INFO] Status... success")
    print(f"[INFO] Output written to {output_filename}")


if __name__ == "__main__":
    test_all("results.csv")
