"""
Program Name: Lightt Curtain Simulation
Description: simulates the light curtain and ballot being dropped into dropbox by pressing the space bar on the keyboard

Programmer(s): Ashley Aldave
Creation Date: 03/01/2025
Revisions: 
    - 02/15/2025 Initial Version (Ashley Aldave)

Preconditions: 
    - Components (button, light curtain, e-ink display, keyboard) must be connected to and detected by the Raspberry Pi
Postconditions: 
    - None
Side Effects: 
    - The ballot count will be updated when space bar is pressed on keyboard
    - The ballot count will be reset to 0 when the button is pressed
    - The E-ink display will update to reflect changes in the ballot count
Invariants: 
    - The ballot count will never be negative
"""
    
import time
import threading
import keyboard  # Requires 'pip install keyboard'
import logging

class LightCurtainSimulator:
    def __init__(self, counter):
        """
        Initializes the keyboard-based light curtain simulator.

        Parameters:
            counter (Counter): The counter instance to update.
        """
        self.counter = counter
        self.running = True

    def start(self):
        """Starts a background thread that listens for spacebar presses to simulate ballot entries."""
        def listen_for_space():
            logging.info("Press SPACE to simulate a ballot entry.")
            while self.running:
                keyboard.wait("space")  # Wait until spacebar is pressed
                self.counter._incAndUpdate()
                time.sleep(0.5)  # Prevent rapid multiple triggers
        
        thread = threading.Thread(target=listen_for_space, daemon=True) # Create a separate thread to listen for keyboard input so it doesn’t block the main program
        
        thread.start() # Start the background thread

    def stop(self):
        """Stops the simulation thread."""
        self.running = False  # This will stop the while loop inside listen_for_space()
        