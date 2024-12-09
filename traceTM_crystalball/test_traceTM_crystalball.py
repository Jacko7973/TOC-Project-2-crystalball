#!/usr/bin/env python3

# test_traceTM_crystalball.py
# Theory of Computing Project 2

import csv

from TM_utils_crystalball import TuringMachine, TuringMachineResult, TM_Status, load_TM, init_TM, trace_TM


### Constants

TESTS = (
    ("data_aplus_crystalball.csv", "aaaaa", TM_Status.ACCEPTED),
    ("data_aplus_crystalball.csv", "aaaab", TM_Status.REJECTED),
    ("data_aplus_crystalball.csv", "aaaaaaaaaaaaaaaaaa", TM_Status.ACCEPTED),
    ("data_aplus_crystalball.csv", "baa", TM_Status.REJECTED),
    ("data_aplus_crystalball.csv", "a", TM_Status.ACCEPTED),
    ("data_aplus_crystalball.csv", "aaacaa", TM_Status.REJECTED),

    ("data_equal_01s_DTM_crystalball.csv", "01", TM_Status.ACCEPTED),
    ("data_equal_01s_DTM_crystalball.csv", "1010", TM_Status.ACCEPTED),
    ("data_equal_01s_DTM_crystalball.csv", "10101", TM_Status.REJECTED),
    ("data_equal_01s_DTM_crystalball.csv", "11111111110000000000", TM_Status.ACCEPTED),

    ("data_equal_01s_crystalball.csv", "01", TM_Status.ACCEPTED),
    ("data_equal_01s_crystalball.csv", "1010", TM_Status.ACCEPTED),
    ("data_equal_01s_crystalball.csv", "10101", TM_Status.REJECTED),
    ("data_equal_01s_crystalball.csv", "11111111110000000000", TM_Status.ACCEPTED),

    ("data_loop_crystalball.csv", "", TM_Status.TIMEDOUT),
    ("data_loop_crystalball.csv", "a", TM_Status.TIMEDOUT),
    ("data_loop_crystalball.csv", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", TM_Status.TIMEDOUT),
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
    test_all("output_results_crystalball.csv")

