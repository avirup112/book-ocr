import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from config import Config
from utils import BookOcrLogger
from models import BookMetadata
from preprocessing import ImagePreprocessor
from extraction import InformationExtractor, ExtractionPatterns
from ocr import BaseOCREngine, TeseseractEngine

__all__ = [
    'Config',
    'BookOCRLogger',
    'BookMetadata',
    'ImagePreprocessor',
    'InformationExtractor',
    'ExtractionPatterns',
    'BaseOCREngine',
    'TesseractEngine',
]

try:
    from ocr import EasyOCREngine
    __all__.append('EasyOCREngine')
except ImportError:
    pass


class BookOCR:
    """Main class orchestrating the entire OCR pipeline"""
    
    def __init__(self, config: Config = None):
        # Use default config if none provided
        self.config = config or Config()
        self.config.create_directories()
        
        # Initialize logger
        self.logger = BookOcrLogger("BookOCR", str(self.config.LOG_DIR))
        self.logger.info("Initializing Book OCR System")
        
        # Initialize components
        self.preprocessor = ImagePreprocessor(self.logger, self.config)
        
        # Initialize OCR engine based on config
        if self.config.OCR_ENGINE == "easyocr":
            self.ocr_engine = EasyOCREngine(self.logger, self.config)
        else:
            self.ocr_engine = TeseseractEngine(self.logger, self.config)
        
        self.extractor = InformationExtractor(self.logger)
        
        self.logger.info("Book OCR System initialized successfully")
    
    def process_image(self, image_path: str, save_processed: bool = False) -> BookMetadata:
        """Process a single book image and extract metadata"""
        self.logger.info("=" * 80)
        self.logger.info(f"Processing book image: {image_path}")
        self.logger.info("=" * 80)
        
        try:
            # Step 1: Preprocess
            self.logger.info("Step 1/3: Preprocessing image")
            processed_image = self.preprocessor.preprocess(image_path, save_processed)
            
            # Step 2: OCR
            self.logger.info("Step 2/3: Performing OCR")
            text = self.ocr_engine.extract_text(processed_image)
            
            # Step 3: Extract information
            self.logger.info("Step 3/3: Extracting information")
            metadata = self.extractor.extract(text)
            metadata.confidence = self.ocr_engine.get_confidence()
            
            # Log results
            self.logger.log_extraction_result(metadata.to_dict(), image_path)
            
            return metadata
            
        except Exception as e:
            self.logger.critical("Failed to process image", error=e, 
                               image_path=image_path)
            raise
    
    def process_batch(self, image_paths: List[str], 
                     output_file: Optional[str] = None,
                     save_processed: bool = False) -> List[BookMetadata]:
        """Process multiple book images"""
        self.logger.info(f"Starting batch processing of {len(image_paths)} images")
        
        results = []
        for idx, image_path in enumerate(image_paths, 1):
            self.logger.info(f"Processing image {idx}/{len(image_paths)}")
            try:
                metadata = self.process_image(image_path, save_processed)
                results.append(metadata)
            except Exception as e:
                self.logger.error(f"Failed to process {image_path}", error=e)
                results.append(None)
        
        # Save results if output file specified
        if output_file:
            self._save_results(results, output_file)
        
        successful = sum(1 for r in results if r is not None)
        self.logger.info(f"Batch processing completed. Successful: {successful}/{len(image_paths)}")
        return results
    
    def find_all_images(self) -> List[Path]:
        """Find all image files in the input directory"""
        # Supported image extensions
        extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif']
        
        image_files = []
        for ext in extensions:
            image_files.extend(self.config.INPUT_DIR.glob(ext))
            # Also check uppercase
            image_files.extend(self.config.INPUT_DIR.glob(ext.upper()))
        
        # Sort by filename
        image_files = sorted(image_files)
        
        self.logger.info(f"Found {len(image_files)} images in {self.config.INPUT_DIR}")
        return image_files
    
    def process_all_images(self, save_processed: bool = False) -> List[BookMetadata]:
        """Process all images in the input directory"""
        image_files = self.find_all_images()
        
        if not image_files:
            self.logger.warning("No images found in input directory")
            print(f"⚠️  No images found in: {self.config.INPUT_DIR}")
            print(f"   Please place your images (img48.jpg - img62.jpg) in this folder.")
            return []
        
        # Convert Path objects to strings
        image_paths = [str(img) for img in image_files]
        
        # Generate output filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"batch_results_{timestamp}.json"
        
        # Process batch
        results = self.process_batch(image_paths, output_file, save_processed)
        
        return results
    
    def _save_results(self, results: List[BookMetadata], output_file: str):
        """Save extraction results to JSON file"""
        try:
            output_path = self.config.OUTPUT_DIR / output_file
            
            data = [r.to_dict() if r else None for r in results]
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Results saved to: {output_path}")
            print(f"\n✅ Results saved to: {output_path}")
            
        except Exception as e:
            self.logger.error("Failed to save results", error=e, 
                            output_file=output_file)
    
    def print_summary(self, results: List[BookMetadata]):
        """Print a summary of processed images"""
        successful = [r for r in results if r is not None]
        failed = len(results) - len(successful)
        
        print("\n" + "=" * 80)
        print("PROCESSING SUMMARY")
        print("=" * 80)
        print(f"Total Images: {len(results)}")
        print(f"✅ Successful: {len(successful)}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {len(successful)/len(results)*100:.1f}%")
        print("=" * 80)
        
        if successful:
            print("\n📚 EXTRACTED BOOKS:")
            print("-" * 80)
            for idx, result in enumerate(successful, 1):
                print(f"\n{idx}. Book Information:")
                if result.title:
                    print(f"   Title: {result.title}")
                if result.author:
                    print(f"   Author: {result.author}")
                if result.isbn_13:
                    print(f"   ISBN-13: {result.isbn_13}")
                elif result.isbn_10:
                    print(f"   ISBN-10: {result.isbn_10}")
                if result.publisher:
                    print(f"   Publisher: {result.publisher}")
                if result.publication_year:
                    print(f"   Year: {result.publication_year}")
                if result.confidence:
                    print(f"   Confidence: {result.confidence:.1%}")


def main():
    """Main entry point"""
    print("\n" + "=" * 80)
    print("📚 BOOK OCR INFORMATION EXTRACTOR")
    print("=" * 80)
    
    # Initialize system
    config = Config()
    book_ocr = BookOCR(config)
    
    print(f"\n📂 Input Directory: {config.INPUT_DIR}")
    print(f"📂 Output Directory: {config.OUTPUT_DIR}")
    print(f"🔧 OCR Engine: {config.OCR_ENGINE}")
    
    # Choose processing mode
    print("\n" + "-" * 80)
    print("PROCESSING MODE:")
    print("-" * 80)
    
    # MODE 1: Process all images automatically
    print("\n🚀 Processing all images in input folder...")
    results = book_ocr.process_all_images(save_processed=True)
    
    if results:
        book_ocr.print_summary(results)
        print("\n✅ Processing complete! Check the output folder for detailed results.")
    else:
        print("\n⚠️  No images to process or all processing failed.")
    
    # MODE 2: Process specific images (alternative)
    # Uncomment below to process specific images only
    """
    print("\n🚀 Processing specific images...")
    image_list = [
        str(config.INPUT_DIR / "img48.jpg"),
        str(config.INPUT_DIR / "img49.jpg"),
        str(config.INPUT_DIR / "img50.jpg"),
        str(config.INPUT_DIR / "img51.jpg"),
        str(config.INPUT_DIR / "img52.jpg"),
        str(config.INPUT_DIR / "img53.jpg"),
        str(config.INPUT_DIR / "img54.jpg"),
        str(config.INPUT_DIR / "img55.jpg"),
        str(config.INPUT_DIR / "img56.jpg"),
        str(config.INPUT_DIR / "img57.jpg"),
        str(config.INPUT_DIR / "img58.jpg"),
        str(config.INPUT_DIR / "img59.jpg"),
        str(config.INPUT_DIR / "img60.jpg"),
        str(config.INPUT_DIR / "img61.jpg"),
        str(config.INPUT_DIR / "img62.jpg"),
    ]
    
    results = book_ocr.process_batch(
        image_list, 
        output_file="extracted_data.json",
        save_processed=True
    )
    
    if results:
        book_ocr.print_summary(results)
    """
    
    # MODE 3: Process single image (alternative)
    # Uncomment below to process just one image
    """
    try:
        image_path = str(config.INPUT_DIR / "img48.jpg")
        print(f"\n🚀 Processing single image: {image_path}")
        
        metadata = book_ocr.process_image(image_path, save_processed=True)
        
        print("\n" + "=" * 80)
        print("EXTRACTED METADATA:")
        print("=" * 80)
        print(metadata)
        print("=" * 80)
        
    except FileNotFoundError:
        print(f"❌ Image not found. Please place images in: {config.INPUT_DIR}")
    except Exception as e:
        print(f"❌ Error: {e}")
    """


if __name__ == "__main__":
    main()