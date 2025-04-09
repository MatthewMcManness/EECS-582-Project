"""
Program Name: Scanner Tests
Description: Runs tests to check correctness of IMBScanner class

Programmer(s): Magaly Camacho
Creation Date: 04/09/2025
Revisions: 
    - 02/15/2025 Initial Version (Magaly Camacho)
    
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
import os

if __name__ == "__main__":
    print("Running tests...")

    # get path to barcodes and their info
    wd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    barcodes_dir = os.path.join(wd, "tests\\barcodes\\")
    barcode_strings_path = os.path.join(barcodes_dir, "barcodes.txt") # has correct strings and the flags to tests

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
                image_name = f"t{barcode_n}_{combo}.png"
                image_path = barcodes_dir + image_name
                scanned_string = IMBScanner.getBarcodeString(image_path)

                # update stats
                count_total += 1
                if scanned_string == actual_string:
                    count_correct += 1

                # print comparison if test failed
                else:
                    print(f"\t{actual_string}", end="\n\t")
                    [print(" ", end="") if char == actual_string[i] else print(actual_string[i], end="") for i, char in enumerate(scanned_string)]
                    print(".")
            
            barcode_n += 1 # move on to next barcode

        print(f"Done. {count_correct}/{count_total} passed") # print tests stats
