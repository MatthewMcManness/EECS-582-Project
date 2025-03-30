"""
Program Name: Counter Class
Description: Counter class that keeps track of how many ballots have entered the drop box.
    Count can be reset by pressing the button inside the box.

Programmer(s): Magaly Camacho, Mariam Oraby, Ashley Aldave
Creation Date: 02/15/2025
Revisions: 
    - 02/15/2025 Initial Version (Magaly Camacho)
    - 02/16/2025 Implemented the _ballotCheck function (Mariam Oraby)
    - 03/01/2025 Changed GPIO library to gpiozero and refactored code to match, integrated E-Ink class
    - 03/04/2025 Added Lidar, implemented a run method, added placeholder methods to turn light on and to take a picture (Magaly Camacho)
    - 03/15/2025 implemented turn light on function (Ashley Aldave)
    - 03/16/2025 implemented take picture function (Mariam Oraby)
    - 03/16/2025 implemented turn light off function (Ashley Aldave)
    - 03/30/2025 Removed light curtain and light pins and comments, as they're not used (Magaly Camacho)
    
Preconditions: 
    - Components (button, e-ink display) must be connected to and detected by the Raspberry Pi
Postconditions: 
    - None
Side Effects: 
    - The ballot count will be updated when a ballot enters the drop box
    - The ballot count will be reset to 0 when the button is pressed
    - The E-ink display will update to reflect changes in the ballot count
Invariants: 
    - The ballot count will never be negative
Faults:
    - Camera code still needs to be tested
"""

import time
from gpiozero import Button, LED
from src.eink import EInkDisplay 
from src.lidar import Lidar
import picamera

class Counter:
    """Counter class that keeps track of the number of envelopes that enter the drop box"""
    MIN_DROP_DISTANCE = 20 # in cm

    def __init__(self, debug:bool=False):
        """
        Initializes counter to 0 and saves pins for components (button, e-ink display)
        
        Parameters: 
            debug (bool): print debug messages if True, don't print otherwise
        """
        if debug: print(f"Initializing Counter") # print debug statement if applicable
        self.count = 0 # initialize envelope count to 0
        self.debug = debug # save debug setting

        # button setup 
        self.button = Button(27) # receive button output from pin GPIO 27
        self.button.when_pressed = self._resetAndUpdate # reset count and update 

        # Get LiDAR and E-Ink Display
        self.lidar = Lidar(debug, self.MIN_DROP_DISTANCE)
        self.eink = EInkDisplay()

    def cleanup(self):
        """Clear E-Ink Display and make it go to sleep, and release other resources"""
        self.eink.clear_sleep()
        self.button.close()
        self.lidar.cleanup()

    def run(self):
        """Start counter"""
        if self.debug: print(f"Now Running\n\nCount (Initial): {self.count}") # print debug statement if applicable
        
        # continuously check if an envelope entered the box, if so...
        try:
            while True:
                if self._envelopeEntered():
                    self._incAndUpdate() # increase count and update E-Ink Display
                    self._take_picture() # take picture of envelope

        # catch keyboard interrupt
        except KeyboardInterrupt as e:
            print("\nCtrl + C: exiting...")

        # catch other errors
        except Exception as e:
            print(f"\nError: {e}")

        # release resources
        finally:
            self.cleanup()

    def _envelopeEntered(self) -> bool:
        """Check lidar measurement distance to see if an envelope has entered the box"""
        distance = self.lidar.getDistance()
        return distance < self.MIN_DROP_DISTANCE

    def _incAndUpdate(self):
        """Increase count and update E-Ink Display"""
        self.count += 1
        if self.debug: print(f"Count: {self.count}") # print debug statement if applicable
        self.eink.update_display(self.count)

    def _resetAndUpdate(self):
        """Reset count and update E-Ink Display"""
        self.count = 0
        self.eink.update_display(self.count)
        if self.debug: print(f"Count (reset): {self.count}") # print debug statement if applicable

    def _take_picture(self):
        """Takes a picture with the Raspberry Pi camera and saves it to a file"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")  # create a timestamp for the file name
        file_name = f"/home/pi/envelope_images/envelope_{timestamp}.jpg"  # specify file path
    
        try:
            # Initialize the camera
            with picamera.PICamera() as camera:
                camera.resolution = (1024, 768)  # set the resolution (you can adjust this)
                time.sleep(0.25)  # give the camera a couple of seconds to adjust to the lighting
                camera.capture(file_name)  # capture the image and save it to file
                if self.debug:
                    print(f"Picture taken and saved as {file_name}")  # debug statement
        except Exception as e:
            print(f"Error taking picture: {e}")  # catch errors, such as camera issues
