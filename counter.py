"""
Program Name: Counter Class
Description: Counter class that keeps track of how many ballots have entered the drop box.
    Count can be reset by pressing the button inside the box.

Programmer(s): Magaly Camacho, Mariam Oraby
Creation Date: 02/15/2025
Revisions: 
    - 02/15/2025 Initial Version (Magaly Camacho)
    - 02/16/2025 Implemented the _ballotCheck function (Mariam Oraby)
    - 03/01/2025 Changed GPIO library to gpiozero and refactored code to match, integrated E-Ink class

Preconditions: 
    - Components (button, light curtain, e-ink display) must be connected to and detected by the Raspberry Pi
Postconditions: 
    - None
Side Effects: 
    - The ballot count will be updated when a ballot enters the drop box
    - The ballot count will be reset to 0 when the button is pressed
    - The E-ink display will update to reflect changes in the ballot count
Invariants: 
    - The ballot count will never be negative
Faults:
    - Light curtain code still needs to be tested on hardware
"""

import time, atexit
from gpiozero import Button
from eink import EInkDisplay 

class Counter:
    """Counter class that keeps track of the number of envelopes that enter the drop box"""
    def __init__(self, debug:bool=False):
        """
        Initializes counter to 0 and saves pins for components (button, light curtain, e-ink display)
        
        Parameters: 
            debug (bool): print debug messages if True, don't print otherwise
        """
        self.count = 0 # initialize envelope count to 0
        if debug: print(f"Count (Initial): {self.count}") # print debug statement if applicable
        self.debug = debug # save debug setting

        # button setup 
        self.button = Button(27) # receive button output from pin GPIO 27
        self.button.when_pressed = self._resetAndUpdate # reset count and update 

        # light curtain setup
        self.light_curtain = Button(22) # connected to GPIO22
        self.light_curtain.when_pressed = self._incAndUpdate

        # start E-Ink Display
        self.eink = EInkDisplay()

    def cleanup(self):
        """Clear E-Ink Display and make it go to sleep, and release GPIO resources"""
        self.eink.clear_sleep()
        self.button.close()
        self.light_curtain.close()

    def _incAndUpdate(self):
        """Increase count and update E-Ink Display"""
        self.count += 1
        self.eink.update_display(self.count)
        if self.debug: print(f"Count: {self.count}") # print debug statement if applicable

    def _resetAndUpdate(self):
        """Reset count and update E-Ink Display"""
        self.count = 0
        self.eink.update_display(self.count)
        if self.debug: print(f"Count (reset): {self.count}") # print debug statement if applicable