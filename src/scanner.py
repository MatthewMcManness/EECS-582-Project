"""
Program Name: Scanner Class
Description: Scanner Class that identifies an IMb barcode in an image and gets a representative string

Programmer(s): Magaly Camacho
Creation Date: 04/09/2025
Revisions: 
    - 04/09/2025 Initial Version (Magaly Camacho)
    - 04/12/2025 Changed bar classification to be based on adjacent bars (Magaly Camacho) 
    
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
    - Potentially too slow to be effective
"""

import cv2, os
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
        # find shortest bar and get its index
        shortest_bar = min(bars, key=lambda b: b[3]) 
        shortest_bar_i = bars.index(shortest_bar)
        classifications = [" " if i != shortest_bar_i else "T" for i in range(len(bars))]

        # get representative string
        cls._classifyBars(bars, classifications, shortest_bar_i)
        return ("").join(classifications)

    @classmethod
    def _classifyBars(cls, bars:list, classifications:list[str], shortest_bar_i:int):
        """Classifies bar at index i as either a tracker, ascending, descending, or full bar. Recursively calls itself for the adjacent bars"""
        for direction in [-1, 1]:
            # reset to shortest bar as the previously classified bar
            i = shortest_bar_i + direction
            _, y_top_p, _, h_p = bars[shortest_bar_i]
            y_bottom_p = y_top_p + h_p
            type_p = "T"

            while 0 <= i < len(bars):
                _, y_top_i, _, h_i = bars[i]
                y_bottom_i = y_top_i + h_i

                top_offset = abs(y_top_i - y_top_p)
                bottom_offset = abs(y_bottom_i - y_bottom_p)

                type_i = cls._classifyBar(top_offset, bottom_offset, type_p, h_p)
                classifications[i] = type_i
                
                # make current bar i the previously classified bar for the next i
                y_top_p, y_bottom_p, h_p, type_p = y_top_i, y_bottom_i, h_i, type_i
                i += direction
    
    @classmethod
    def _classifyBar(cls, top_offset, bottom_offset, bar_p_type, bar_p_height):
        """Classifies a bar (i) based on its height difference with bar p, which has been previously classified"""
        # calculate height threshold based on height and type of bar_p (already classified) 
        height_thresh = cls._calculateHeightThresh(bar_p_type, bar_p_height)

        # if bars are close within threshold difference in height they are the same type
        if top_offset <= height_thresh and bottom_offset <= height_thresh:
            return bar_p_type
        
        # compare to tracker bar
        if bar_p_type == "T":
            if top_offset >= height_thresh and bottom_offset >= height_thresh:
                return "F"
            elif top_offset >= height_thresh:
                return "A"
            else:
                return "D"

        # compare to full bar 
        elif bar_p_type == "F":
            if top_offset >= height_thresh and bottom_offset >= height_thresh:
                return "T"
            elif top_offset >= height_thresh:
                return "D"
            else:
                return "A"
        
        # compare to ascending bar
        elif bar_p_type == "A":
            if top_offset >= height_thresh and bottom_offset >= height_thresh:
                return "D"
            elif top_offset >= height_thresh:
                return "T"
            else:
                return "F"
            
        # compare to descending bar
        elif bar_p_type == "D":
            if top_offset >= height_thresh and bottom_offset >= height_thresh:
                return "A"
            elif top_offset >= height_thresh:
                return "F"
            else:
                return "T"

    @staticmethod
    def _calculateHeightThresh(bar_type, bar_height):
        """Calculates height threshold based on a bar's height and type"""
        # adjust height to be that of tracker
        if bar_type == "F":
            bar_height /= 3.0
        elif bar_type in ["A", "D"]:
            bar_height /= 2.0
        
        # return threshold
        return bar_height / 1.8

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
        image_name = image_path.split(os.sep)[-1]
        out_path = image_path.replace(image_name, f"{os.sep}out{os.sep}{image_name}")
        cv2.imwrite(out_path, image)