"""
Program Name: Scanner Tests
Description: Runs tests to check correctness of IMBScanner class

Programmer(s): Magaly Camacho
Creation Date: 04/09/2025
Revisions: 
    - 04/09/2025 Initial Version (Magaly Camacho)
    - 04/13/2025 Changed comparison string to be based on actual string and added args parser (Magaly Camacho)
    
Preconditions: 
    - Barcode images must be located in the tests/barcodes/ directory
Postconditions: 
    - None
Side Effects: 
    - None
Invariants: 
    - The barcode images will not be modified
Faults:
    - None known
"""

from src.scanner import IMBScanner
import os, argparse

def run():
    # parser set up
    parser = argparse.ArgumentParser(description="Test 3: Scanner")
    parser.add_argument("-c", "--clean", help="remove all output files before running test", action="store_true")
    parser.add_argument("-co", "--cleanonly", help="remove all output files, don't run tests", action="store_true")
    parser.add_argument("-f", "--flags", type=str, help="which combo flags to not execute")

    # parse args
    args = parser.parse_args()
    if args.flags is None:
        args.flags = "all"
    else:
        args.flags = args.flags.split()

    # get path to barcodes and their info
    wd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    barcodes_dir = os.path.join(wd, f"tests{os.sep}barcodes{os.sep}")
    out_dir = os.path.join(barcodes_dir, "out")
    barcode_strings_path = os.path.join(barcodes_dir, "barcodes.txt") # has correct strings and the flags to tests

    # clean
    if args.clean or args.cleanonly:
        print("Deleting output files")
        for filename in os.listdir(out_dir):
            if filename != ".gitkeep":
                os.remove(os.path.join(out_dir, filename))

    # clean only
    if args.cleanonly:
        return

    # run tests
    print("Running tests...")

    with open(barcode_strings_path) as file:
        # helpers
        barcode_n = 1
        count_correct = 0
        count_total = 0

        # iterate through barcode info in barcodes.txt
        for line in file:
            barcode_info = line.strip().split()
            actual_string = barcode_info[0] # get actual string for barcode
            flag_combos = barcode_info[1:] 

            # test each barcode combo
            for combo in flag_combos:
                if not combo in args.flags and args.flags != "all":
                    continue

                image_name = f"t{barcode_n}_{combo}.png"
                image_path = barcodes_dir + image_name
                scanned_string = IMBScanner.getBarcodeString(image_path)

                # update stats
                count_total += 1
                if scanned_string == actual_string:
                    count_correct += 1

                # print comparison if test failed
                else:
                    print(f"\tTest t{barcode_n}_{combo} failed")
                    print(f"\t\t{actual_string}", end="\n\t\t")
                    [print(" ", end="") if char == scanned_string[i] else print(scanned_string[i], end="") for i, char in enumerate(actual_string)]
                    print(".")
            
            barcode_n += 1 # move on to next barcode

        print(f"Done. {count_correct}/{count_total} passed") # print tests stats

if __name__ == "__main__":
    run()