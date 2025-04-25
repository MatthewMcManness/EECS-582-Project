import time
from picamera2 import Picamera2, Preview
import os
from libcamera import Transform

def _take_picture():
    """Takes a picture with the Raspberry Pi camera and saves it to a file"""
    timestamp = time.strftime("%Y%m%d-%H%M%S")  # create a timestamp for the file name
    file_name = f"envelope_{timestamp}.jpg"  # specify file path
    
    try:
        # Initialize the camera
        #with picamera.PiCamera() as camera:
            #camera.resolution = (1024, 768)  # set the resolution (you can adjust this)
            #time.sleep(0.25)  # give the camera a couple of seconds to adjust to the lighting
            #camera.capture(file_name)  # capture the image and save it to file
            #if self.debug:
            #print(f"Picture taken and saved as {file_name}")  # debug statement

        picam2 = Picamera2()
        config = picam2.create_still_configuration(main={"size":(4096,4096)}, transform=Transform())
        picam2. configure(config)
        preview_config = picam2.create_preview_configuration(main={"size":(4096, 4096)})
        picam2.configure(preview_config)
        picam2.start_preview(Preview.QTGL)
        picam2.start()
        time.sleep(0.25)
        picam2.capture_file(file_name)
        print(f"Picture taken and saved as {file_name}")

    except Exception as e:
        print(f"Error taking picture: {e}")  # catch errors, such as camera issues


_take_picture()
