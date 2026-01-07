"""
OCR engine implementations
"""

from .base_engine import BaseOCREngine
from .tesseract_engine import TeseseractEngine

__all__ = ['BaseOCREngine', 'TesseractEngine']

# Conditionally import EasyOCR if available
try:
    from .easyocr_engine import EasyOCREngine
    __all__.append('EasyOCREngine')
except ImportError:
    pass