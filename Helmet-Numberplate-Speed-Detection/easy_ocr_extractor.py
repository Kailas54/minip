import easyocr
import numpy as np
import cv2

# Initialize reader once to keep it fast
# Use English since license plates usually use English characters
reader = easyocr.Reader(['en'], gpu=True)

def extract_plate(image):
    """
    Takes a cropped image of a license plate (numpy array)
    and returns the highest confidence text string.
    """
    if image is None or image.size == 0:
        return ""
        
    # EasyOCR expects a numpy array
    results = reader.readtext(image)
    
    if not results:
        return ""
        
    # results is a list of tuples: (bbox, text, prob)
    # Sort by probability or just return the highest probability one
    # Or join all detected texts if it's split into multiple words
    detected_texts = [res[1] for res in results if res[2] > 0.2] # simple threshold
    
    return " ".join(detected_texts).strip()
