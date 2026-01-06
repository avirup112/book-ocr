import logging 
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

class BookOcrLogger:
    
    def __init__(self, name: str= "BookOCR", log_dir: str="logs"):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create Logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        #Prevent duplicate handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
            
        # Create formatters
        detailed_formatter = logging.Formatter(
            fmt='%(asctime)s | %(name)s |%(levelname)8s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # File Handler - detailed logs
        log_file = self.log / f"simple_formatter = logging.Formatter(fmt='%(asctime)s | %(levelname)8s | %(message)s',datefmt='%H:%M:%S')"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # Console handler - simpler logs
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info(f"Logger initialized. Logs saved to: {log_file}")
        
    def debug(self, msg: str, **kwargs):
        "Log debug message with optional context"
        extra_info = f" | Context: {json.dumps(kwargs)}" if kwargs else ""
        self.logger.debug(f"{msg}{extra_info}")
    
    def info(self, msg: str, **kwargs):
        "Log info message with optional context"
        extra_info = f" | {json.dumps(kwargs)}" if kwargs else ""
        self.logger.info(f"{msg}{extra_info}")
    
    def warning(self, msg: str, **kwargs):
        "Log warning message with optional context"
        extra_info = f" | {json.dumps(kwargs)}" if kwargs else ""
        self.logger.warning(f"{msg}{extra_info}")
    
    def error(self, msg: str, error: Optional[Exception] = None, **kwargs):
        "Log error message with exception details"
        extra_info = f" | {json.dumps(kwargs)}" if kwargs else ""
        if error:
            self.logger.error(f"{msg}{extra_info}", exc_info=True)
        else:
            self.logger.error(f"{msg}{extra_info}")
    
    def critical(self, msg: str, error: Optional[Exception] = None, **kwargs):
        "Log critical message"
        extra_info = f" | {json.dumps(kwargs)}" if kwargs else ""
        if error:
            self.logger.critical(f"{msg}{extra_info}", exc_info=True)
        else:
            self.logger.critical(f"{msg}{extra_info}")
    
    def log_extraction_result(self, book_data: Dict[str, Any], image_path: str):
        "Special method to log extraction results"
        self.info("=" * 80)
        self.info(f"Extraction completed for: {image_path}")
        self.info(f"Fields extracted: {list(book_data.keys())}")
        for field, value in book_data.items():
            if value:
                self.info(f"  {field}: {value}")
        self.info("=" * 80)