"""
Program Name: Scanner Class
Description: Scanner Class that identifies an IMb barcode in an image and gets a representative string

Programmer(s): Magaly Camacho
Creation Date: 04/09/2025
Revisions: 
    - 04/09/2025 Initial Version (Magaly Camacho)
    - 04/12/2025 Changed bar classification to be based on adjacent bars (Magaly Camacho) 
    - 04/13/2025 Scanner can now find the IMb in an image that includes more than just the IMb (Magaly Camacho)
    
Preconditions: 
    - The provided image path must lead to an existing image which must be a png
Postconditions: 
    - None
Side Effects: 
    - None
Invariants: 
    - The image at the provided path will not be modified
Faults:
    - Doesn't account for an image not having a barcode or not being able to find one
    - Assumes there's an image at the given image path
    - Potentially too slow to be effective
    - Doesn't account for orientation
"""

import cv2, os
from cv2.typing import MatLike
from typing import Union

class IMBScanner:
    PAD = 5 # padding for when cropping image
    HEIGHT_RATIO = 1.8 # height ratio for height threshfold for classifying bars
    NUM_BARS = 65 # number of bars in an IMb 

    @staticmethod
    def getBarcodeString(image_path:str):
        """Get the representative string for a barcode in an image"""
        thresh = IMBScanner._loadAdjustImage(image_path) 
        candidate_regions = IMBScanner._getCandidateIMbRegions(thresh, image_path)

        bars_info = IMBScanner._analyzeCandidateIMbRegions(thresh, candidate_regions) 

        if bars_info is None:
            return " "*IMBScanner.NUM_BARS
        
        bars, x_offset, y_offset = bars_info
        
        IMBScanner._drawBars(bars, image_path, x_offset, y_offset) # draw outlines of bars on a copy of the image, for debugging
        barcode_string = IMBScanner._getReprString(bars)

        return barcode_string

    @staticmethod
    def _loadAdjustImage(image_path:str) -> tuple[MatLike, MatLike]:
        """Load and adjust the image at the given image path"""
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) # load image
        blurred = cv2.GaussianBlur(image, (5, 5), 0) # blur slightly to reduce noise

        # convert to black and white, invert colors so bars are white on a black background
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) 

        return thresh

    @staticmethod
    def _getCandidateIMbRegions(thresh:MatLike, image_path:str) -> MatLike:
        """Identifies the area in the image where the barcode is and then crops the image"""
        # connect barcode bars
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 6))
        connected = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        IMBScanner.saveImage(image_path, connected, "connected")

        # find contours of candidate regions based on connected bars
        regions, _ = cv2.findContours(connected, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # return roi after analyzing candidate regions
        return regions

    @staticmethod
    def _analyzeCandidateIMbRegions(image, regions):
        """Check each candidate region to see if it has enough bars to be an IMb"""
        for region in regions:
            x, y, w, h = cv2.boundingRect(region)
            
            if w >= 3 * h: # *** orientation fix ?
                y_top = y - IMBScanner.PAD
                y_bottom = y + h + IMBScanner.PAD
                x_left = x - IMBScanner.PAD
                x_right = x + w + IMBScanner.PAD

                image_cropped = image[y_top:y_bottom, x_left:x_right]

                bars = IMBScanner._getBars(image_cropped)
                if len(bars) == IMBScanner.NUM_BARS: # might need to be more lenient
                    return bars, x, y
                
        return None
                
    @staticmethod
    def _getReprString(bars:list) -> list[str]:
        """Returns a representative string for the barcode"""
        # find shortest bar and get its index
        shortest_bar = min(bars, key=lambda b: b[3]) 
        shortest_bar_i = bars.index(shortest_bar)
        classifications = [" " if i != shortest_bar_i else "T" for i in range(len(bars))]

        # get representative string
        IMBScanner._classifyBars(bars, classifications, shortest_bar_i)
        return ("").join(classifications)

    @staticmethod
    def _classifyBars(bars:list, classifications:list[str], shortest_bar_i:int):
        """Classifies bar at index i as either a tracker, ascending, descending, or full bar. Recursively calls itself for the adjacent bars"""
        for direction in [-1, 1]:
            # reset to shortest bar as the previously classified bar
            i = shortest_bar_i + direction
            _, y_top_p, _, h_p = bars[shortest_bar_i]
            y_bottom_p = y_top_p + h_p
            type_p = "T"

            while 0 <= i < len(bars):
                # get bar i info 
                _, y_top_i, _, h_i = bars[i]
                y_bottom_i = y_top_i + h_i

                # calculate height offsets between bar i and bar p
                top_offset = abs(y_top_i - y_top_p)
                bottom_offset = abs(y_bottom_i - y_bottom_p)

                # classify bar i based on bar p
                type_i = IMBScanner._classifyBar(top_offset, bottom_offset, type_p, h_p)
                classifications[i] = type_i
                
                # make current bar i the previously classified bar p for the next bar i
                y_top_p, y_bottom_p, h_p, type_p = y_top_i, y_bottom_i, h_i, type_i
                i += direction
    
    @staticmethod
    def _classifyBar(top_offset, bottom_offset, bar_p_type, bar_p_height):
        """Classifies a bar (i) based on its height difference with bar p, which has been previously classified"""
        # calculate height threshold based on height and type of bar_p (already classified) 
        height_thresh = IMBScanner._calculateHeightThresh(bar_p_type, bar_p_height)

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
        
        # return height threshold
        return bar_height / IMBScanner.HEIGHT_RATIO

    @staticmethod
    def _getBars(image: MatLike) -> Union[list, list[tuple[int, int, int, int]]]:
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
    def _drawBars(bars:list, image_path:str, x_offset, y_offset):
        """Draws a rectangle around each bar in the given bars on the given image (for testing purposes)"""
        image = cv2.imread(image_path) # load the image

        # draw a rectangle around each bar
        for x, y, w, h in bars:
            x += x_offset - IMBScanner.PAD
            y += y_offset - IMBScanner.PAD
            y_bottom = y + h

            cv2.rectangle(image, (x, y), (x + w, y_bottom), (0, 255, 0), 1)

        # save the new image 
        image_name = image_path.split(os.sep)[-1]
        out_path = image_path.replace(image_name, f"{os.sep}out{os.sep}{image_name}")
        cv2.imwrite(out_path, image)

    @staticmethod
    def saveImage(image_path, image, tag=""):
        image_name = image_path.split(os.sep)[-1]
        out_path = image_path.replace(image_name, f"{os.sep}out{os.sep}{tag}_{image_name}")
        cv2.imwrite(out_path, image)