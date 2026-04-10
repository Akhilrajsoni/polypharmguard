import os
import platform

# Set Tesseract path BEFORE importing pytesseract
if platform.system() == 'Windows':
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(tesseract_path):
        os.environ['PATH'] = tesseract_path.replace('\\tesseract.exe', '\\') + os.pathsep + os.environ.get('PATH', '')

import pytesseract
import cv2
import numpy as np
from PIL import Image

class PrescriptionOCR:
    """OCR module to extract text from prescription images"""
    
    def __init__(self, tesseract_path=None):
        """
        Initialize OCR
        
        Args:
            tesseract_path: Path to tesseract executable (for Windows)
        """
        # Auto-detect Tesseract on Windows if path not provided
        if tesseract_path is None and platform.system() == 'Windows':
            common_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            ]
            for path in common_paths:
                if os.path.exists(path):
                    tesseract_path = path
                    break
        
        if tesseract_path:
            pytesseract.pytesseract.pytesseract_cmd = tesseract_path
        
        self.confidence_threshold = 30
    
    def preprocess_image(self, image_path):
        """Preprocess image for better OCR accuracy"""
        # Read image
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(binary, h=10)
        
        # Apply morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        processed = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
        
        return processed
    
    def extract_text(self, image_path, preprocess=True):
        """Extract text from prescription image"""
        if preprocess:
            processed_image = self.preprocess_image(image_path)
            text = pytesseract.image_to_string(processed_image)
        else:
            text = pytesseract.image_to_string(image_path)
        
        return text
    
    def extract_text_with_confidence(self, image_path, preprocess=True):
        """Extract text with confidence scores"""
        if preprocess:
            processed_image = self.preprocess_image(image_path)
            pil_image = Image.fromarray(processed_image)
        else:
            pil_image = Image.open(image_path)
        
        data = pytesseract.image_to_data(pil_image, output_type=pytesseract.Output.DICT)
        
        text_results = []
        for i, conf in enumerate(data['conf']):
            if int(conf) > self.confidence_threshold:
                text_results.append({
                    'text': data['text'][i],
                    'confidence': float(conf),
                    'level': data['level'][i]
                })
        
        return text_results
    
    def extract_lines(self, image_path, preprocess=True):
        """Extract text organized by lines"""
        if preprocess:
            processed_image = self.preprocess_image(image_path)
            pil_image = Image.fromarray(processed_image)
        else:
            pil_image = Image.open(image_path)
        
        data = pytesseract.image_to_data(pil_image, output_type=pytesseract.Output.DICT)
        
        lines = {}
        for i, line_num in enumerate(data['line_num']):
            if int(data['conf'][i]) > self.confidence_threshold:
                if line_num not in lines:
                    lines[line_num] = []
                lines[line_num].append({
                    'text': data['text'][i],
                    'confidence': float(data['conf'][i])
                })
        
        extracted_lines = []
        for line_num in sorted(lines.keys()):
            line_text = ' '.join([item['text'] for item in lines[line_num]])
            avg_confidence = np.mean([item['confidence'] for item in lines[line_num]])
            extracted_lines.append({
                'text': line_text.strip(),
                'confidence': avg_confidence
            })
        
        return extracted_lines


def main():
    """Test OCR functionality"""
    ocr = PrescriptionOCR()
    
    # Example usage (create a test image if needed)
    print("OCR Module Ready")
    print("Usage: ocr.extract_text('prescription_image.jpg')")


if __name__ == "__main__":
    main()
