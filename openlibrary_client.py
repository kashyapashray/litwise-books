import requests
import time
import json
import logging
from typing import List, Dict, Optional
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenLibraryClient:
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'LitWise-Books/1.0 (https://github.com/yourusername/litwise-books)'
        })
    
    def search_books(self, query: str, limit: int = 50) -> List[Dict]:
        """Search for books using Open Library search API"""
        params = {
            'q': query,
            'limit': limit,
            'fields': 'key,title,author_name,first_publish_year,isbn,subject,cover_i,publisher,number_of_pages_median'
        }
        
        try:
            logger.info(f"Searching for books with query: {query}")
            response = self.session.get(
                self.config.OPENLIBRARY_SEARCH_URL,
                params=params,
                timeout=self.config.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            books = data.get('docs', [])
            logger.info(f"Found {len(books)} books")
            
            # Add delay to be respectful to the API
            time.sleep(self.config.REQUEST_DELAY)
            
            return books
            
        except requests.RequestException as e:
            logger.error(f"Error searching books: {e}")
            return []
    
    def get_work_details(self, work_key: str) -> Optional[Dict]:
        """Get detailed information about a book work"""
        if not work_key.startswith('/works/'):
            work_key = f"/works/{work_key}"
        
        url = f"{self.config.OPENLIBRARY_BASE_URL}{work_key}.json"
        
        try:
            logger.info(f"Fetching work details for: {work_key}")
            response = self.session.get(url, timeout=self.config.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            # Add delay to be respectful to the API
            time.sleep(self.config.REQUEST_DELAY)
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Error fetching work details for {work_key}: {e}")
            return None
    
    def get_edition_details(self, edition_key: str) -> Optional[Dict]:
        """Get detailed information about a book edition"""
        if not edition_key.startswith('/books/'):
            edition_key = f"/books/{edition_key}"
        
        url = f"{self.config.OPENLIBRARY_BASE_URL}{edition_key}.json"
        
        try:
            logger.info(f"Fetching edition details for: {edition_key}")
            response = self.session.get(url, timeout=self.config.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            # Add delay to be respectful to the API
            time.sleep(self.config.REQUEST_DELAY)
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Error fetching edition details for {edition_key}: {e}")
            return None
    
    def search_popular_books(self, subject: str = "fiction", limit: int = 50) -> List[Dict]:
        """Search for popular books by subject"""
        return self.search_books(f"subject:{subject}", limit)
    
    def get_diverse_book_collection(self, limit: int = 50) -> List[Dict]:
        """Get a diverse collection of books from different genres"""
        subjects = [
            "fiction", "science fiction", "mystery", "romance", "fantasy",
            "biography", "history", "science", "philosophy", "psychology",
            "business", "self-help", "cooking", "travel", "poetry"
        ]
        
        books_per_subject = max(1, limit // len(subjects))
        all_books = []
        
        for subject in subjects:
            if len(all_books) >= limit:
                break
                
            books = self.search_popular_books(subject, books_per_subject)
            all_books.extend(books)
            
            logger.info(f"Collected {len(books)} books from {subject} category")
        
        # Return only the requested number of books
        return all_books[:limit]
    
    def format_book_data(self, book_data: Dict, work_details: Optional[Dict] = None) -> Dict:
        """Format book data into a standardized structure"""
        # Extract basic information
        title = book_data.get('title', 'Unknown Title')
        authors = book_data.get('author_name', [])
        author = ', '.join(authors) if authors else 'Unknown Author'
        
        # Get publication year
        first_publish_year = book_data.get('first_publish_year')
        
        # Get ISBNs
        isbns = book_data.get('isbn', [])
        isbn = isbns[0] if isbns else None
        isbn13 = None
        if isbns:
            for isbn_val in isbns:
                if len(isbn_val) == 13:
                    isbn13 = isbn_val
                    break
        
        # Get subjects
        subjects = book_data.get('subject', [])
        subjects_str = ', '.join(subjects[:10]) if subjects else None  # Limit to first 10 subjects
        
        # Get cover image
        cover_id = book_data.get('cover_i')
        cover_image_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg" if cover_id else None
        
        # Get publisher
        publishers = book_data.get('publisher', [])
        publisher = publishers[0] if publishers else None
        
        # Get page count
        number_of_pages = book_data.get('number_of_pages_median')
        
        # Get work key for future reference
        work_key = book_data.get('key')
        
        # Extract description from work details if available
        description = None
        if work_details and 'description' in work_details:
            desc = work_details['description']
            if isinstance(desc, dict) and 'value' in desc:
                description = desc['value']
            elif isinstance(desc, str):
                description = desc
        
        return {
            'title': title,
            'author': author,
            'isbn': isbn,
            'isbn13': isbn13,
            'first_publish_year': first_publish_year,
            'publisher': publisher,
            'number_of_pages': number_of_pages,
            'openlibrary_key': work_key,
            'work_key': work_key,
            'description': description,
            'subjects': subjects_str,
            'cover_image_url': cover_image_url,
            'language': 'en'  # Default to English
        } 