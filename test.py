"""
Program Name: Counter Test
Description: Tests functionality of EInkDisplay and Counter classes

Programmer(s): Magaly Camacho, Mariam Oraby
Creation Date: 03/01/2025
Revisions: 
    - 03/01/2025 Initial Version (Magaly Camacho, Mariam Oraby)

Preconditions: 
    - Components (button, light curtain, e-ink display) must be connected to and detected by the Raspberry Pi
Postconditions: 
    - None
Side Effects: 
    - The ballot count will be increased every 3 seconds, unless the button is pressed in which case the count will be reset to 0
    - The E-ink display will update to reflect changes in the ballot count
Invariants: 
    - The ballot count will never be negative
Faults:
    - None known
"""

import time, atexit
from counter import Counter

if __name__ == "__main__":
    try:
        counter = Counter(debug=True) # initialize counter

        while True:
            counter._incAndUpdate() # increase count and update display
            time.sleep(3) # wait 3 seconds

            # stop when ballot count reaches 5
            if counter.count == 2:
                print("Stopping")
                break

    # if error occurs, print it and stop e-ink
    except Exception as e:
        print(f"Error: {e}") 

    # release resources
    finally:
        counter.cleanup()