from abc import ABC, abstractmethod
import numpy as np 


class BaseOCREngine(ABC):
    "Abstract base class for OCR engines."
    
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        
    @abstractmethod
    def extract_text(self, image: np.ndarray) -> str:
        "Extract text from preprocessed image"
        pass
    
    @abstractmethod
    def get_confidence(self) -> float:
        "Get confidence score of last extraction"
        pass