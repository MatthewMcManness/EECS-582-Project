import time
from picamera2 import Picamera2, Preview
from libcamera import Transform
import os

def take_pictures():
        """Take simultaneous pictures on camera 0 and camera 1."""
        # prepare timestamped filenames
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file0 = f"envelope_cam0_{timestamp}.jpg"
        file1 = f"envelope_cam1_{timestamp}.jpg"
        
    try:
        # initialize both cameras by number
        cam0 = Picamera2(camera_num=0)
        cam1 = Picamera2(camera_num=1)

        # configure each for high-res stills
        config0 = cam0.create_still_configuration(main={"size": (4608, 2592)}, transform=Transform(), controls={"AfMode": 2})
        config1 = cam1.create_still_configuration(main={"size": (4608, 2592)}, transform=Transform(), controls={"AfMode": 2})
        cam0.configure(config0)
        cam1.configure(config1)

        # (Optional) start previews if you want a live feed window
        #cam0.start_preview(Preview.QTGL)
        #cam1.start_preview(Preview.QTGL)

        # start both cameras
        cam0.start()
        cam1.start()

        # give them time to adjust exposure/focus
        time.sleep(2)

        # capture both frames
        cam0.capture_file(file0)
        # add delay here if needed depending on camera angles and gravity
        cam1.capture_file(file1)
        print(f"Captured {file0} and {file1}")

        # clean up
        cam0.stop()
        cam1.stop()
        #cam0.stop_preview()
        #cam1.stop_preview()

if __name__ == "__main__":
    take_pictures()
