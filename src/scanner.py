"""
Program Name: Scanner Class
Description: Scanner Class that identifies an IMb barcode in an image and gets a representative string

Programmer(s): Magaly Camacho
Creation Date: 04/09/2025
Revisions: 
    - 02/15/2025 Initial Version (Magaly Camacho)
    
Preconditions: 
    - The provided image path must lead to an existing image which must be a png
Postconditions: 
    - None
Side Effects: 
    - None
Invariants: 
    - The image at the provided path will not be modified
Faults:
    - Currently, it can only identify barcodes in images where the barcode is the only thing present
    - Doesn't account for an image not having a barcode or not being able to find one
    - Assumes there's an image at the given image path
    - Height threshold needs to be adjusted
    - Classification process may need to be adjusted to start from the shortest bar, then classify each bar based on the two adjacent bars (to account for distortion)
    - Potentially too slow to be effective
"""

import cv2
from cv2.typing import MatLike
from typing import Union

class IMBScanner:
    @classmethod
    def getBarcodeString(cls, image_path:str):
        """Get the representative string for a barcode in an image"""
        image = cls._loadAdjustImage(image_path) # load and adjust image
        bars = cls._lookForBars(image) # look for bars in the image
        #print([bar for bar in bars[0:7]]) 
        cls._drawBars(bars, image_path) # draw outlines of bars on a copy of the image
        barcode_string = cls._getReprString(bars) # classify bars to get barcode string
        return barcode_string

    @staticmethod
    def _loadAdjustImage(image_path:str) -> tuple[MatLike, MatLike]:
        """Load and adjust the image at the given image path"""
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) # load image
        blurred = cv2.GaussianBlur(image, (5, 5), 0) # blur slightly to reduce noise

        # convert to black and white, invert colors so bars are white on a black background
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) 

        return thresh 

    """def _getIMbLocation():
        pass

    def _cropImage():
        pass"""

    @classmethod
    def _getReprString(cls, bars:list) -> list[str]:
        """Returns a representative string for the barcode"""
        # find shortest bar and calculate its center and the height threshold
        shortest_bar = min(bars, key=lambda b: b[3]) 
        tracker_height = shortest_bar[3] 
        tracker_center = shortest_bar[1] + tracker_height // 2 
        height_thresh = tracker_height / 1.8 

        #print(f"shortest: {shortest_bar}")
        #print(f"tracker center: {tracker_center}")
        #print(f"thres: {height_thresh}")

        # classify bars based on tracker center and height threshold
        classifications = [cls._classifyBar(y, h, tracker_center, height_thresh) for (x, y, w, h) in bars]
        
        return ("").join(classifications)
    
    @staticmethod
    def _classifyBar(y_top, height, tracker_center, height_thresh):
        """Classifies a bar as either a tracker, ascending, descending, or full bar"""
        # calculate offsets from the tracker's center
        top_offset = tracker_center - y_top
        bottom_offset = y_top + height - tracker_center
        #print(f"bar: top({top_offset}), bottom({bottom_offset})")

        # classify based on offsets and a height thresh
        if top_offset > height_thresh and bottom_offset > height_thresh:
            return "F"
        elif top_offset > height_thresh:
            return "A"
        elif bottom_offset > height_thresh:
            return "D"
        else:
            return "T"

    @staticmethod
    def _lookForBars(image: MatLike) -> Union[list, list[tuple[int, int, int, int]]]:
        """Looks for bars (contours) in the given image"""
        # find contours (bar shapes), only get outermost shapes and compress the contour points
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        bars = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c) # get location and size
            bars.append((x, y, w, h)) # save bar

        bars.sort(key=lambda b: b[0]) # sort left to right
        
        return bars

    @staticmethod
    def _drawBars(bars:list, image_path:str):
        """Draws a rectangle around each bar in the given bars on the given image (for testing purposes)"""
        image = cv2.imread(image_path) # load the image

        # draw a rectangle around each bar
        for (x, y, w, h) in bars:
            y_bottom = y + h

            cv2.rectangle(image, (x, y), (x + w, y_bottom), (0, 255, 0), 1)

        # save the new image 
        image_name = image_path.split("\\")[-1]
        out_path = image_path.replace(image_name, f"\\out\\{image_name}")
        cv2.imwrite(out_path, image)