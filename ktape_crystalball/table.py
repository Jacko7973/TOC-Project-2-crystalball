#!/usr/bin/env python3

import csv
from ktape_crystalball import *

TESTS = (
    ("flip.csv", ["aa_"], ["bb_"]),
    ("flip.csv", ["aabb_"], ["bbaa_"]),
    ("flip.csv", ["bb_"], ["aa_"]),
    ("flip.csv", ["bbaa_"], ["aabb_"]),

    ("right.csv", ["aa_", "____"], ["aa_", "$aa_"]),
    ("right.csv", ["aabb_", "______"], ["aabb_", "$aabb_"]),
    ("right.csv", ["bb_", "____"], ["bb_", "$bb_"]),
    ("right.csv", ["bbaa_", "______"], ["bbaa_", "$bbaa_"]),

    ("multiple1.csv", ["aa_", "___", "____"], ["aa_", "bb_", "$aa_"]),
    ("multiple1.csv", ["aabb_", "_____", "______"], ["aabb_", "bbaa_", "$aabb_"]),
    ("multiple1.csv", ["bb_", "___", "____"], ["bb_", "aa_", "$bb_"]),
    ("multiple1.csv", ["bbaa_", "_____", "______"], ["bbaa_", "aabb_", "$bbaa_"]),
)

HEADERS = ("Machine Name", "Tapes", "Input String", "Result", "Final State", "Transitions")

def run_test(testcase:tuple) -> tuple:
    machine_file, input_strings, output_strings = testcase

    tapes = [list(input_strings[i]) for i in range(0, len(input_strings))]
    
    termination_flag = int(sys.argv[len(sys.argv) - 1]) if len(sys.argv) > 3 else None

    name, tape, states, sigma, gamma, start, accept, reject, transitions = process_csv(machine_file)

    index = [0] * tape
    
    current, num_transitions = process_transitions(tape, transitions, start, accept, index, tapes, verbose=False)

    result = [''.join(sublist) for sublist in tapes]
    
    assert output_strings == result

    return (name, tape, input_strings, result, current, num_transitions)

def run_all(output_filename:str):
    if not output_filename.endswith(".csv"):
        output_filename = output_filename + ".csv"

    records = []
    for i, testcase in enumerate(TESTS, 1):
        result = run_test(testcase)
        if result:
            record = (result[0], ', '.join(testcase[1]), result[1], ', '.join(result[3]), result[4], result[5])
            records.append(record)

    with open(output_filename, "w") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(HEADERS)
        for record in records:
            writer.writerow(record)

    print("[INFO] Status... success")
    print(f"[INFO] Output written to {output_filename}")

    
if __name__ == "__main__":
    run_all("results.csv")
