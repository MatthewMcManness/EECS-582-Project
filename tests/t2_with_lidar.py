"""
Program Name: Counter Test With Lidar
Description: Tests functionality of EInkDisplay, Lidar, and Counter classes

Programmer(s): Magaly Camacho
Creation Date: 03/04/2025
Revisions: 
    - 03/04/2025 Initial Version (Magaly Camacho)

Preconditions: 
    - Components (button, light curtain, e-ink display, lidar) must be connected to and detected by the Raspberry Pi
Postconditions: 
    - None
Side Effects: 
    - The ballot count will be increased when the distance detected by the lidar is less than 20cm
    - When the button is pressed the count will be reset to 0
    - The E-ink display will update to reflect changes in the ballot count
Invariants: 
    - The ballot count will never be negative
Faults:
    - None known
"""

import time
from src import Counter

counter = Counter(debug=True) # initialize counter

try:
    counter.run()

# if error occurs, print message
except Exception as e:
    print(f"Error: {e}")