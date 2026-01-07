from dataclasses import dataclass, asdict
from typing import Optional ,Dict, Any

@dataclass
class BookMetadata:
    "Data class for book metadata"
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    isbn_10: Optional[str] = None
    isbn_13: Optional[str] = None
    publication_year: Optional[str] = None
    edition: Optional[str] = None
    pages: Optional[str] = None
    language: Optional[str] = None
    price: Optional[str] = None
    genre: Optional[str] = None
    raw_text: Optional[str] = None
    confidence: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        "Convert to dictionary, excluding None values."
        return {k: v for k, v in asdict(self).items() if v is not None}
    
    def __str__(self) -> str:
        "String representation"
        items = [f"{k}: {v}" for k, v in self.to_dict().items() if k != 'raw_text']
        return "\\n".join(items)