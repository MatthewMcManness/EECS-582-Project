"""
Program Name: Main
Description: Main entry point for the project

Programmer(s): Magaly Camacho
Creation Date: 04/24/2025
Revisions: 
    - 04/24/2025 Initial Version (Magaly Camacho)
    - 04/27/2025 Turned debug off (Magaly Camacho)
    
Preconditions: 
    - Components (button, e-ink display, cameras, lidar) must be connected to and detected by the Raspberry Pi
Postconditions: 
    - None
Side Effects: 
    - The ballot count will be updated when a ballot enters the drop box
    - The ballot count will be reset to 0 when the button is pressed
    - The E-ink display will update to reflect changes in the ballot count
    - The cameras will take pictures of the envelopes
Invariants: 
    - The ballot count will never be negative
Faults:
    - None
"""

from src.counter import Counter

if __name__ == "__main__":
    counter = Counter()
    counter.run()
