import numpy as np
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False

from ocr.base_engine import BaseOCREngine

class EasyOCREngine(BaseOCREngine):
    "EasyOCR implementation"
    
    def __init__(self, logger, config):
        super().__init__(logger, config)
        
        if not EASYOCR_AVAILABLE:
            raise ImportError("EasyOCR not available. Install: pip install easyocr")
        
        self.logger.info("Initializing EasyOCR reader...")
        self.reader = easyocr.Reader(config.OCR_LANGUAGES, gpu=False)
        self.logger.info("EasyOCR reader initialized")
        self.last_confidence = 0.0
    
    def extract_text(self, image: np.ndarray) -> str:
        "Extract text using EasyOCR"
        self.logger.info("Starting EasyOCR extraction")
        
        try:
            results = self.reader.readtext(image)
            
            if results:
                text = " ".join([result[1] for result in results])
                self.last_confidence = np.mean([result[2] for result in results])
            else:
                text = ""
                self.last_confidence = 0.0
            
            self.logger.info("EasyOCR completed", 
                           text_length=len(text),
                           confidence=f"{self.last_confidence:.2f}")
            
            return text.strip()
            
        except Exception as e:
            self.logger.error("EasyOCR extraction failed", error=e)
            raise
    
    def get_confidence(self) -> float:
        return self.last_confidence