import cv2
import numpy as np

def extract_plate_text(plate_image):
    """
    Extract text from license plate using EasyOCR.
    Returns the detected text or None if nothing readable.
    """
    try:
        import easyocr
        
        # Preprocess image for better OCR
        gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY, 11, 2)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh, None, 30, 7, 21)
        
        # Initialize EasyOCR reader (cache it for speed)
        if not hasattr(extract_plate_text, 'reader'):
            extract_plate_text.reader = easyocr.Reader(['en'], gpu=True, verbose=False)
        
        # Read text
        results = extract_plate_text.reader.readtext(denoised)
        
        if results:
            # Filter by confidence and combine text
            texts = []
            for res in results:
                bbox, text, confidence = res
                if confidence > 0.4:  # Only use high-confidence detections
                    texts.append(text)
            
            if texts:
                combined_text = ' '.join(texts).strip()
                
                # Clean up the text - keep only alphanumeric and common characters
                cleaned = ''.join(c if c.isalnum() or c in ' -' else '' for c in combined_text)
                cleaned = ' '.join(cleaned.split())  # Remove extra spaces
                
                # Return if we got meaningful text (at least 4 chars for plates)
                if len(cleaned) >= 4:
                    return cleaned.upper()
    
    except Exception as e:
        print(f"EasyOCR error: {e}")
    
    # Fallback: Try simple contour analysis
    try:
        gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        char_contours = [c for c in contours if cv2.contourArea(c) > 50]
        
        if len(char_contours) >= 3:
            return f"PLATE-{len(char_contours)}CH"
    except:
        pass
    
    return None

def detect_and_extract_plate(vehicle_crop):
    """
    Detect license plate in vehicle crop and extract text.
    Returns: (plate_found, plate_text, plate_image)
    """
    if vehicle_crop is None or vehicle_crop.size == 0:
        return False, "", None
    
    # Convert to HSV for better plate detection
    hsv = cv2.cvtColor(vehicle_crop, cv2.COLOR_BGR2HSV)
    
    # Define range of blue colors (common for Indian plates)
    # Also check for white/yellow plates
    plate_masks = []
    
    # Blue plates
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    plate_masks.append(mask_blue)
    
    # White plates
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 20, 255])
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    plate_masks.append(mask_white)
    
    # Yellow plates
    lower_yellow = np.array([20, 50, 150])
    upper_yellow = np.array([35, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    plate_masks.append(mask_yellow)
    
    # Combine masks
    combined_mask = cv2.bitwise_or(plate_masks[0], plate_masks[1])
    combined_mask = cv2.bitwise_or(combined_mask, plate_masks[2])
    
    # Morphological operations to clean up noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Look for rectangular plate-shaped contours
    best_plate = None
    best_score = 0
    
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        
        # Check if it's a quadrilateral (4 sides)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            area = cv2.contourArea(contour)
            
            # Plate should have reasonable size and aspect ratio
            if 1000 < area < 50000:  # Adjust based on your video resolution
                aspect_ratio = float(w) / h
                if 1.5 < aspect_ratio < 5.0:  # Plates are wider than tall
                    score = area * aspect_ratio  # Prefer larger, well-proportioned plates
                    if score > best_score:
                        best_score = score
                        best_plate = (x, y, w, h)
    
    if best_plate:
        x, y, w, h = best_plate
        plate_roi = vehicle_crop[y:y+h, x:x+w]
        
        # Try to extract text
        plate_text = extract_plate_text(plate_roi)
        
        if plate_text:
            return True, plate_text, plate_roi
        else:
            # Found plate but couldn't read text
            return True, "UNREADABLE", plate_roi
    
    return False, "", None
