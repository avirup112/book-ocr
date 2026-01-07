import numpy as np 
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

from ocr.base_engine import BaseOCREngine

class TeseseractEngine(BaseOCREngine):
    "Tesseract OCR implementation"
    
    def __init__(self, logger, config):
        super().__init__(logger, config)
        
        if not TESSERACT_AVAILABLE:
            raise ImportError("Tesseract not available. Install: pip install pytesseract")
        
        self.logger.info("Initialized Tesseract OCR engine")
        self.last_confidence = 0.0
    
    def extract_text(self, image: np.ndarray) -> str:
        "Extract text using Tesseract"
        self.logger.info("Starting Tesseract OCR extraction")
        
        try:
            # Extract text
            text = pytesseract.image_to_string(image)
            
            # Get confidence
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in data['conf'] if conf != '-1']
            self.last_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            self.logger.info("Tesseract OCR completed", text_length=len(text),confidence=f"{self.last_confidence:.2f}")
            return text.strip()
            
        except Exception as e:
            self.logger.error("Tesseract extraction failed", error=e)
            raise
        
    def get_confidence(self) -> float:
        return self.last_confidence / 100.0  # Normalize to 0-1