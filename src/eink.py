"""
Program Name: E-Ink Display Class
Description: Class that updates the e-ink display to reflect change in ballot count.

Programmer(s): Ashley Aldave, Manvir Kaur, Magaly Camacho, Mariam Oraby
Creation Date: 02/15/2025
Revisions: 
    - 02/15/2025 Initial Version (Ashley and Manvir)
    - 02/16/2025 Adding Prologue Comments
    - 02/24/2025 Fixing code (Ashley and Manvir)
    - 03/01/2025 Renamed file, refactored code to better fit the rest of the codebase, comments (Magaly and Mariam)

Preconditions: 
    - E-ink display must be working, as well as connected to and detected by the Raspberry Pi
Postconditions: 
    - None
Side Effects: 
    - The E-ink display will update to reflect changes in the ballot count
Invariants: 
    - The ballot count displayed will never be negative
Faults:
    - None known
"""

import os, atexit
from waveshare_epd import epd2in13_V4 # E-Ink Display 2.13in V4
from PIL import Image, ImageDraw, ImageFont

class EInkDisplay:
    def __init__(self, count:int=0):
        """Start e-ink"""
        # Save font for text
        font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "misc/Font.ttc") # get font path
        self.font = ImageFont.truetype(font_path, 24) # font size 24

        self.current_count = count # initialize current count
        self._start_e_ink() # turn e-ink on

    def clear_sleep(self):
        """Clear E-Ink Display and make it go to sleep"""
        self.epd.init()
        self.epd.Clear(0xFF)
        self.epd.sleep()
        epd2in13_V4.epdconfig.module_exit(cleanup=True)

    def update_display(self, count:int):
        """
        Update display to show the given count

        Parameters:
            count (int): the count to display
        """
        # Don't change display if the given count is the same as the currently displayed one
        if self.current_count == count:
            return
        self.current_count = count # save the new count
        self._set_display() # update display

    def _display_setup(self):
        """Set up the display with the count label"""
        self.image = Image.new('1', (self.epd.height, self.epd.width), 255)  #  # create base image (255=white background)
        self.draw = ImageDraw.Draw(self.image) # 
        self.draw.text((10, 30), "Envelope Count:", font=self.font, fill=0) # write the label
        self.epd.displayPartBaseImage(self.epd.getbuffer(self.image)) # display the label
    
    def _set_display(self):
        """Sets display to current count"""
        self.draw.rectangle((10, 60, 220, 105), fill = 255) # cover old count
        self.draw.text((10, 60), f"{self.current_count}", font=self.font, fill=0) # write the count
        self.epd.displayPartial(self.epd.getbuffer(self.image)) # show the updated count

    def _start_e_ink(self, ):
        """Initialize e-ink display with the given count"""
        self.epd = epd2in13_V4.EPD() # E-Ink Display 2.13in V4
        self.epd.init_fast() # fast init
        self._display_setup() # display count label
        self._set_display() # display count 
