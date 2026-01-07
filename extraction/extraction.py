import re
from typing import Optional
from models.book_metadata import BookMetadata
from extraction.patterns import ExtractionPatterns

class InformationExtractor:
    "Extracts structured information from OCR text"
    
    def __init__(self, logger):
        self.logger = logger
        self.patterns = ExtractionPatterns()
        
    def extract(self, text: str) -> BookMetadata:
        "Extract all book metadata from text"
        self.logger.info("Startin information extraction")
        self.logger.debug("Input text preview", preview=text[:200] + "..." if len(text) > 200 else text)
        metadata = BookMetadata(raw_text=text)
        
        try:
            # Extract ISBN
            metadata.isbn_13 = self._extract_isbn_13(text)
            metadata.isbn_10 = self._extract_isbn_10(text)
            
            # Extract other fields
            metadata.publication_year = self._extract_year(text)
            metadata.pages = self._extract_pages(text)
            metadata.price = self._extract_price(text)
            metadata.edition = self._extract_edition(text)
            metadata.language = self._extract_language(text)
            
            # Extratc text-based fields
            metadata.title = self._extract_title(text)
            metadata.author = self._extract_author(text)
            metadata.language = self._extract_language(text)
            
            self.logger.info("Information extraction completed")
            self.logger.debug("Extracted fields", 
                            fields={k: v for k, v in metadata.to_dict().items() 
                                   if k != 'raw_text' and v is not None})
            
            return metadata
            
        except Exception as e:
            self.logger.error("Information extraction failed", error=e)
            raise
    
    def _extract_isbn_13(self, text: str) -> Optional[str]:
        match = re.search(self.patterns.ISBN_13_PATTERN, text, re.IGNORECASE)
        if match:
            isbn = self.patterns.clean_isbn(match.group(1))
            self.logger.debug(f"Found ISBN-13: {isbn}")
            return isbn
        return None
    
    def _extract_isbn_10(self, text: str) -> Optional[str]:
        match = re.search(self.patterns.ISBN_10_PATTERN, text, re.IGNORECASE)
        if match:
            isbn = self.patterns.clean_isbn(match.group(1))
            if not isbn.startswith('97'):
                self.logger.debug(f"Found ISBN-10: {isbn}")
                return isbn
        return None
    
    def _extract_year(self, text: str) -> Optional[str]:
        matches = re.findall(self.patterns.YEAR_PATTERN, text)
        if matches:
            year = matches[0]
            self.logger.debug(f"Found year: {year}")
            return year
        return None
    
    def _extract_pages(self, text: str) -> Optional[str]:
        match = re.search(self.patterns.PAGES_PATTERN, text, re.IGNORECASE)
        if match:
            pages = match.group(1)
            self.logger.debug(f"Found pages: {pages}")
            return pages
        return None
    
    def _extract_price(self, text: str) -> Optional[str]:
        match = re.search(self.patterns.PRICE_PATTERN, text)
        if match:
            price = match.group(0)
            self.logger.debug(f"Found price: {price}")
            return price
        return None
    
    def _extract_edition(self, text: str) -> Optional[str]:
        match = re.search(self.patterns.EDITION_PATTERN, text, re.IGNORECASE)
        if match:
            edition = match.group(1)
            self.logger.debug(f"Found edition: {edition}")
            return edition
        return None
    
    def _extract_language(self, text: str) -> Optional[str]:
        match = re.search(self.patterns.LANGUAGE_PATTERN, text, re.IGNORECASE)
        if match:
            language = match.group(1)
            self.logger.debug(f"Found language: {language}")
            return language
        return None
    
    def _extract_title(self, text: str) -> Optional[str]:
        lines = [line.strip() for line in text.split('\\n') if line.strip()]
        if lines:
            for line in lines[:3]:
                if len(line) > 5 and any(c.isupper() for c in line):
                    self.logger.debug(f"Extracted title: {line}")
                    return line
        return None
    
    def _extract_author(self, text: str) -> Optional[str]:
        for pattern in self.patterns.AUTHOR_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                author = match.group(1).strip()
                self.logger.debug(f"Found author: {author}")
                return author
        return None
    
    def _extract_publisher(self, text: str) -> Optional[str]:
        for pattern in self.patterns.PUBLISHER_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                publisher = match.group(1).strip()
                self.logger.debug(f"Found publisher: {publisher}")
                return publisher
        return None