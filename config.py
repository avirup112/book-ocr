import os 
from pathlib import Path

class Config:
    # Base directories
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    INPUT_DIR = DATA_DIR / "input"
    OUTPUT_DIR = DATA_DIR/ "output"
    PROCESSED_DIR = DATA_DIR/ "processed"
    LOG_DIR = BASE_DIR/ "logs"
    
    # Ocr settings
    OCR_ENGINE = "easyocr" # just jeta lagbe tokhon change kore dibi either tesseract or easyocr
    OCR_LANGUAGES = ["en"]
    
    # Image processing settings 
    DENOISE_STRENGTH = 10 
    ADAPTIVE_THRESHOLD_BLOCK_SIZE = 11
    ADAPTIVE_THRESHOLD_C = 2
    
    # logging settings 
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)8s | %(funcName)s:%(lineno)d | %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # Extraction Settings
    MIN_CONFIDENCE = 0.5
    
    @classmethod
    def create_directories(cls):
        "Create all necessary directories"
        for directory in [cls.DATA_DIR, cls.INPUT_DIR, cls.OUTPUT_DIR, 
                         cls.PROCESSED_DIR, cls.LOG_DIR]:
            directory.mkdir(parents=True, exist_ok=True)