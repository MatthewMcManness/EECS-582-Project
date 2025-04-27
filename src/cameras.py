"""
Program Name: Cameras Class
Description: Class that serves as an interface to the Raspberry Pi cameras 

Programmer(s): Magaly Camacho, Ashley Aldave, Manvir Kaur
Creation Date: 02/15/2025
Revisions: 
    - 04/27/2025 Initial Version (Magaly Camacho, Manvir Kaur)
    
Preconditions: 
    - Cameras must be connected to and detected by the Raspberry Pi
Postconditions: 
    - None
Side Effects: 
    - Cameras will take and save pictures
Invariants: 
    - None
Faults:
    - None
"""

import time, os, asyncio
from picamera2 import Picamera2, Preview
from libcamera import Transform

class Cameras:
    def __init__(self, debug:bool):
        """Configure cameras and give them time to adjust to exposure and focus"""
        self.debug = debug
        self.camera_names = ["bottom", "top"]
        cameras = []

        # configure and start cameras
        for i in range(2):
            cameras.append(Picamera2(camera_num=i))
            config = cameras[i].create_still_configuration(
                main={"size": (4608, 2592)}, 
                transform=Transform(), 
                controls={"AfMode":2, "AfRange":1} # enable autofocus mode, look for nearby objects
            )
            cameras[i].configure(config)
            
            if debug:
                cameras[i].start_preview(Preview.QTGL)
            
            cameras[i].start()

        # give cameras time to adjust
        time.sleep(2)
        self.cameras = cameras

        if debug:
            print("Cameras ready")

    def take_pictures(self):
        """Take pictures and save them"""
        timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")

        for i, name in enumerate(self.camera_names):
            self.cameras[i].capture_file(f"images/{timestamp}_{name}.jpg")
    
    def stop(self):
        """Stop cameras"""
        for camera in self.cameras:
            if camera.started:
                camera.stop()