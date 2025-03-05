"""
Program Name: Lidar Class
Description: Class that serves as an interface to Garmin LiDAR Lite v3 sensor

Programmer(s): Magaly Camacho
Creation Date: 03/04/2025
Revisions: 
    - 03/04/2025 Initial Version (Magaly Camacho)

Preconditions: 
    - smbus2 must be installed, LiDAR must be connected to and recognized by the Raspberry Pi
Postconditions: 
    - None
Side Effects: 
    - Writes distance data to registers
Invariants: 
    - None
Faults:
    - None known
"""

from smbus2 import SMBus
import time

class Lidar:
    I2C_ADDR = 0x62             # default I2C address

    ACQ_COMMAND_REG = 0x00      # device command
    FULL_DELAY_HIGH_REG = 0x0f  # distance measurement high byte
    FULL_DELAY_LOW_REG = 0x10   # distance measurement low byte

    NO_CORRECTION = 0x03        # take distance measurement without receiver bias correction
    WITH_CORRECTION = 0x04      # take distance measurement with receiver bias correction

    def __init__(self, debug:bool=False, max_debug_dist:int=0):
        """
        Initialize lidar to use the given bus and apply receiver bias correction
        
        Parameters:
            bus (int): the bus to write to, defaults to bus 1
            debug (bool): print debug information if True, doesn't print otherwise
            max_debug_dist (int): only print distance debug if distance measured is greater than max_debug_dist (in cm)
        """
        self.bus = SMBus(1) # initialize I2C bus
        self.debug = debug
        self.max_debug_dist = max_debug_dist
        self._write(self.ACQ_COMMAND_REG, self.WITH_CORRECTION) # perform receiver bias correction 

    def getDistance(self):
        """
        Returns the distance read by the LiDAR in cm

        Returns:
            int: the measured distance (in cm), None if the LiDAR was unable to get a reading
        """
        try:
            # write distance data
            self._write(self.ACQ_COMMAND_REG, self.NO_CORRECTION)

            # get distance data 
            dist_high_byte = self._read(self.FULL_DELAY_HIGH_REG)
            dist_low_byte = self._read(self.FULL_DELAY_LOW_REG)
            distance = ((dist_high_byte << 8) + dist_low_byte)

            if self.debug and distance <= self.max_debug_dist: print(f"Lidar distance: {distance} cm")
            return distance
            
        except Exception as e:
            if self.debug: print(f"\nError getting Lidar distance: {e}")
            return 

    def cleanup(self):
        """Closes the I2C connection"""
        self.bus.close()

    def _read(self, reg):
        """Write the value at the given register"""
        return self.bus.read_byte_data(self.I2C_ADDR, reg)

    def _write(self, reg, value):
        """Write the given value to the given register"""
        self.bus.write_byte_data(self.I2C_ADDR, reg, value)
        time.sleep(0.03)