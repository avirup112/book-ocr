import re 

class ExtractionPatterns:
    """Regex patterns for extracting book information"""
    
    ## ISBN Patterns
    ISBN_10_PATTERN = r'ISBN(?:-10)?[:\\s]*(\\d{1,5}[-\\s]?\\d{1,7}[-\\s]?\\d{1,7}[-\\s]?[\\dX])'
    ISBN_13_PATTERN = r'ISBN(?:-13)?[:\\s]*(97[89][-\\s]?\\d{1,5}[-\\s]?\\d{1,7}[-\\s]?\\d{1,7}[-\\s]?\\d)'
    
    # Publication patterns
    YEAR_PATTERN = r'\\b(19\\d{2}|20[0-2]\\d)\\b'
    PAGES_PATTERN = r'(\\d+)\\s*(?:pages|pp\\.?|p\\.?)'
    EDITION_PATTERN = r'(\\d+(?:st|nd|rd|th)\\s+edition)'
    
    # Price and language
    PRICE_PATTERN = r'[\\$£€₹]\\s*\\d+\\.?\\d*'
    LANGUAGE_PATTERN = r'(?:language|lang)[:\\s]+([a-z]+)'
    
    # Author patterns
    AUTHOR_PATTERNS = [
        r'(?:by|author|written by)[:\\s]+([A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*)',
        r'([A-Z][a-z]+\\s+[A-Z][a-z]+)(?:\\s*\\n|\\s*$)'
    ]
    
    # Publisher patterns
    PUBLISHER_PATTERNS = [
        r'(?:published by|publisher)[:\\s]+([A-Z][A-Za-z\\s&]+)',
        r'([A-Z][a-z]+\\s+(?:Press|Publications|Publishers|Books))'
    ]
    
    @staticmethod
    def clean_isbn(isbn_string: str) -> str:
        "Remove hyphens and spaces from ISBN"
        return re.sub(r'[-\\s]', '', isbn_string)