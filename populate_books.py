#!/usr/bin/env python3
"""
Script to populate the database with books from Open Library API
"""

import logging
import sys
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import init_database, db_manager
from openlibrary_client import OpenLibraryClient
from models import Book

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BookPopulator:
    def __init__(self):
        self.client = OpenLibraryClient()
        
    def save_book_to_db(self, session: Session, book_data: Dict) -> bool:
        """Save a single book to the database"""
        try:
            # Check if book already exists (by title and author)
            existing_book = session.query(Book).filter(
                Book.title == book_data['title'],
                Book.author == book_data['author']
            ).first()
            
            if existing_book:
                logger.info(f"Book already exists: {book_data['title']} by {book_data['author']}")
                return False
            
            # Create new book
            book = Book(**book_data)
            session.add(book)
            session.commit()
            
            logger.info(f"Successfully added: {book_data['title']} by {book_data['author']}")
            return True
            
        except IntegrityError as e:
            session.rollback()
            logger.warning(f"Integrity error for book '{book_data['title']}': {e}")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving book '{book_data['title']}': {e}")
            return False
    
    def fetch_and_save_books(self, target_count: int = 50) -> int:
        """Fetch books from Open Library and save to database"""
        logger.info(f"Starting to fetch {target_count} books from Open Library")
        
        # Get database session
        session = db_manager.get_session()
        if not session:
            logger.error("Failed to get database session")
            return 0
        
        try:
            # Get diverse collection of books
            raw_books = self.client.get_diverse_book_collection(target_count)
            
            if not raw_books:
                logger.error("No books found from Open Library")
                return 0
            
            saved_count = 0
            total_books = len(raw_books)
            
            logger.info(f"Processing {total_books} books...")
            
            for i, raw_book in enumerate(raw_books):
                logger.info(f"Processing book {i+1}/{total_books}: {raw_book.get('title', 'Unknown')}")
                
                # Format book data
                formatted_book = self.client.format_book_data(raw_book)
                
                # Try to get work details for description
                work_key = raw_book.get('key')
                if work_key:
                    work_details = self.client.get_work_details(work_key)
                    if work_details:
                        formatted_book = self.client.format_book_data(raw_book, work_details)
                
                # Save to database
                if self.save_book_to_db(session, formatted_book):
                    saved_count += 1
                
                # Stop if we've reached our target
                if saved_count >= target_count:
                    break
            
            logger.info(f"Successfully saved {saved_count} books to the database")
            return saved_count
            
        except Exception as e:
            logger.error(f"Error during book fetching process: {e}")
            return 0
        finally:
            session.close()
    
    def get_database_stats(self):
        """Get current database statistics"""
        session = db_manager.get_session()
        if not session:
            logger.error("Failed to get database session")
            return
        
        try:
            total_books = session.query(Book).count()
            recent_books = session.query(Book).order_by(Book.created_at.desc()).limit(5).all()
            
            logger.info(f"Database Stats:")
            logger.info(f"  Total books: {total_books}")
            logger.info(f"  Recent additions:")
            
            for book in recent_books:
                logger.info(f"    - {book.title} by {book.author} ({book.first_publish_year})")
            
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
        finally:
            session.close()

def main():
    """Main function to populate the database"""
    logger.info("Starting book database population")
    
    # Initialize database
    logger.info("Initializing database...")
    if not init_database():
        logger.error("Failed to initialize database. Please check your database configuration.")
        sys.exit(1)
    
    # Create populator and fetch books
    populator = BookPopulator()
    
    # Get current stats
    populator.get_database_stats()
    
    # Fetch and save books
    target_count = 50
    saved_count = populator.fetch_and_save_books(target_count)
    
    if saved_count > 0:
        logger.info(f"Successfully populated database with {saved_count} books!")
        
        # Show final stats
        populator.get_database_stats()
    else:
        logger.error("No books were added to the database")
        sys.exit(1)

if __name__ == "__main__":
    main() 