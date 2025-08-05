#!/usr/bin/env python3
"""
Test script to verify database connection and display sample data
"""

import logging
from database import init_database, db_manager
from models import Book

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    """Test database connection and display sample data"""
    logger.info("Testing database connection...")
    
    # Initialize database
    if not init_database():
        logger.error("❌ Failed to connect to database")
        logger.error("Please check your .env file and database configuration")
        return False
    
    logger.info("✅ Database connection successful!")
    
    # Get session and test queries
    session = db_manager.get_session()
    if not session:
        logger.error("❌ Failed to create database session")
        return False
    
    try:
        # Get total book count
        total_books = session.query(Book).count()
        logger.info(f"📚 Total books in database: {total_books}")
        
        if total_books == 0:
            logger.info("💡 No books found. Run 'python populate_books.py' to add some books!")
            return True
        
        # Show some sample books
        logger.info("\n📖 Sample books:")
        sample_books = session.query(Book).limit(5).all()
        
        for i, book in enumerate(sample_books, 1):
            logger.info(f"  {i}. {book.title}")
            logger.info(f"     Author: {book.author}")
            logger.info(f"     Year: {book.first_publish_year}")
            logger.info(f"     Subjects: {book.subjects[:100] if book.subjects else 'N/A'}...")
            logger.info("")
        
        # Show books by publication year
        recent_books = session.query(Book).filter(
            Book.first_publish_year.isnot(None)
        ).order_by(Book.first_publish_year.desc()).limit(3).all()
        
        if recent_books:
            logger.info("🕐 Most recent publications:")
            for book in recent_books:
                logger.info(f"  - {book.title} ({book.first_publish_year}) by {book.author}")
        
        logger.info("\n✅ Database test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during database test: {e}")
        return False
    finally:
        session.close()

def main():
    """Main function"""
    logger.info("=" * 50)
    logger.info("LitWise Books - Database Connection Test")
    logger.info("=" * 50)
    
    success = test_connection()
    
    if success:
        logger.info("\n🎉 Everything looks good! Your database is ready to use.")
    else:
        logger.info("\n🔧 Please fix the issues above and try again.")
        
        logger.info("\nTroubleshooting tips:")
        logger.info("1. Check your .env file exists and has correct database credentials")
        logger.info("2. Ensure your database server is running and accessible")
        logger.info("3. Verify the database name exists on your server")
        logger.info("4. Test your connection with a MySQL client first")

if __name__ == "__main__":
    main() 