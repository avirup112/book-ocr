import cv2
import numpy as np
from pathlib import Path
from typing import Optional

class ImagePreprocessor:
    "Handles image preprocessing for better OCR results"
    
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
    
    def preprocess(self, image_path: str, save_processed: bool = False) -> np.ndarray:
        "Apply preprocessing pipeline to image"
        self.logger.info(f"Preprocessing image: {image_path}")
        
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            self.logger.debug("Original image loaded", 
                            shape=img.shape, 
                            dtype=str(img.dtype))
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.logger.debug("Converted to grayscale")
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(
                gray, None, 
                self.config.DENOISE_STRENGTH, 7, 21
            )
            self.logger.debug("Applied denoising")
            
            # Adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                denoised, 255, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY,
                self.config.ADAPTIVE_THRESHOLD_BLOCK_SIZE,
                self.config.ADAPTIVE_THRESHOLD_C
            )
            self.logger.debug("Applied adaptive thresholding")
            
            # Deskew if needed
            processed = self._deskew(thresh)
            
            # Save processed image if requested
            if save_processed:
                self._save_processed_image(processed, image_path)
            
            self.logger.info("Image preprocessing completed successfully")
            return processed
            
        except Exception as e:
            self.logger.error("Image preprocessing failed", error=e, 
                            image_path=image_path)
            raise
    
    def _deskew(self, image: np.ndarray) -> np.ndarray:
        "Correct image skew"
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        if abs(angle) > 0.5:
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(
                image, M, (w, h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE
            )
            self.logger.debug(f"Deskewed image by {angle:.2f} degrees")
            return rotated
        
        return image
    
    def _save_processed_image(self, image: np.ndarray, original_path: str):
        "Save preprocessed image"
        try:
            output_path = self.config.PROCESSED_DIR / Path(original_path).name
            cv2.imwrite(str(output_path), image)
            self.logger.debug(f"Saved processed image to: {output_path}")
        except Exception as e:
            self.logger.warning(f"Could not save processed image", error=e)
