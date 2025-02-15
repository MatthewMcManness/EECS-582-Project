"""
Program Name: Counter Class
Description: Counter class that keeps track of how many ballots have entered the drop box.
    Count can be reset by pressing the button inside the box.

Programmer(s): Magaly Camacho
Creation Date: 02/15/2025
Revisions: 
    - 02/15/2025 Initial Version (Magaly Camacho)

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
    - None known
"""

class Counter:
    """
    Counter class that keeps track of the number of ballots that enter the drop box
    """
    def __init__(self, button_pin, light_curtain_pin, e_ink_display_pin):
        """
        Initializes counter to 0 and saves pins for components (button, light curtain, e-ink display)
        
        Parameters:
            button_pin: the pin the button is connected to 
            light_curtain_pin: the pin the light curtain is connected to
            e_ink_display_pin: the pin the e_ink_display is connected to
        """
        ballot_count = 0 # initialize ballot count to 0

        # pins
        button_pin = button_pin
        light_curtain_pin = light_curtain_pin
        e_ink_display_pin = e_ink_display_pin

    def run(self):
        """Continuously checks if the button has been pressed and if a ballot has entered the drop box"""
        while True:
            self._buttonCheck()
            self._ballotCheck()

    def _ballotCheck(self):
        """Increases counter if a ballot enters the box"""
        pass

    def _buttonCheck(self):
        """Resets counter if the button is pressed"""
        if self._isButtonPressed():
            self._resetCounter()

    def _isButtonPressed(self):
        """
        Checks if the button is pressed
        
        Returns:  
            bool: if the button is pressed (True) or not (False)
        """
        return self.button_pin.read_digital() == 1

    def _incCounter(self, amount:int=1):
        """
        Increases the count by a specified amount (defaults to 1)
        
        Parameters:
            amount (int): the amount to increase the ballot count by (defaults to 1)
        """
        self.ballot_count += amount

    def _resetCounter(self):
        """Resets ballot count to 0"""
        self.ballot_count = 0

    def _updateDisplay(self):
        """Updates E-ink display to show the current ballot count"""
        pass